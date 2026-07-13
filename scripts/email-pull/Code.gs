/**
 * Gmail-to-Obsidian Email Export
 *
 * Reads emails labeled "z - Obsidian", exports them to this Sheet,
 * saves attachments to Google Drive, and removes the label.
 *
 * Setup:
 * 1. Paste this into Extensions > Apps Script in a Google Sheet
 * 2. Run exportEmails() once to authorize
 * 3. Optionally add a time-based trigger for automatic export
 */

var LABEL_NAME = "z - Obsidian";
var DRIVE_FOLDER_NAME = "Obsidian Email Attachments";
var SHEET_NAME = "Emails"; // Tab name in the spreadsheet

/**
 * Main function -- run this manually or via trigger.
 */
function exportEmails() {
  var label = GmailApp.getUserLabelByName(LABEL_NAME);
  if (!label) {
    Logger.log("Label '" + LABEL_NAME + "' not found. Create it in Gmail first.");
    return;
  }

  var threads = label.getThreads();
  if (threads.length === 0) {
    Logger.log("No threads found with label '" + LABEL_NAME + "'.");
    return;
  }

  var sheet = getOrCreateSheet();
  var existingIds = getExistingIds(sheet);
  var driveFolder = getOrCreateDriveFolder();
  var exportedCount = 0;

  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();
    for (var j = 0; j < messages.length; j++) {
      var msg = messages[j];
      var msgId = msg.getId();

      if (existingIds[msgId]) {
        continue;
      }

      var row = extractMessage(msg, driveFolder);
      sheet.appendRow(row);
      existingIds[msgId] = true;
      exportedCount++;
    }
    // Remove label from thread after processing all messages
    threads[i].removeLabel(label);
  }

  Logger.log("Exported " + exportedCount + " email(s). Removed label from " + threads.length + " thread(s).");
}

/**
 * Get or create the "Emails" sheet tab with headers.
 */
function getOrCreateSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      "id", "subject", "from", "to", "cc", "date",
      "body", "links", "attachments", "exported_at"
    ]);
    sheet.getRange(1, 1, 1, 10).setFontWeight("bold");
  }
  return sheet;
}

/**
 * Get set of message IDs already in the sheet (for idempotency).
 */
function getExistingIds(sheet) {
  var ids = {};
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return ids; // Only header row

  var idColumn = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  for (var i = 0; i < idColumn.length; i++) {
    if (idColumn[i][0]) {
      ids[idColumn[i][0]] = true;
    }
  }
  return ids;
}

/**
 * Get or create the Drive folder for attachments.
 */
function getOrCreateDriveFolder() {
  var folders = DriveApp.getFoldersByName(DRIVE_FOLDER_NAME);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.createFolder(DRIVE_FOLDER_NAME);
}

/**
 * Extract a single message into a row array.
 */
function extractMessage(msg, driveFolder) {
  var subject = msg.getSubject() || "(no subject)";
  var from = msg.getFrom();
  var to = msg.getTo();
  var cc = msg.getCc() || "";
  var date = msg.getDate().toISOString();
  var msgId = msg.getId();

  // Body: prefer plain text
  var body = msg.getPlainBody() || "";
  if (!body.trim()) {
    body = stripHtml(msg.getBody());
  }

  // Extract links from HTML body
  var links = extractLinks(msg.getBody());

  // Handle attachments
  var attachmentInfo = saveAttachments(msg, driveFolder, date, subject);

  var now = new Date().toISOString();

  return [
    msgId, subject, from, to, cc, date,
    body, links, attachmentInfo, now
  ];
}

/**
 * Extract all URLs from an HTML string.
 */
function extractLinks(html) {
  if (!html) return "";
  var urls = [];
  var seen = {};
  // Match href attributes
  var hrefRegex = /href=["']([^"']+)["']/gi;
  var match;
  while ((match = hrefRegex.exec(html)) !== null) {
    var url = match[1];
    // Skip mailto, javascript, and anchor-only links
    if (url.match(/^(mailto:|javascript:|#)/i)) continue;
    // Skip Google tracking/unsubscribe URLs
    if (url.match(/^https?:\/\/(www\.)?(google\.com\/url|notifications\.google\.com)/i)) continue;
    if (!seen[url]) {
      seen[url] = true;
      urls.push(url);
    }
  }
  return urls.join("\n");
}

/**
 * Strip HTML tags to get plain text (fallback when getPlainBody is empty).
 */
function stripHtml(html) {
  if (!html) return "";
  // Replace <br> and </p> with newlines
  var text = html.replace(/<br\s*\/?>/gi, "\n");
  text = text.replace(/<\/p>/gi, "\n\n");
  text = text.replace(/<\/div>/gi, "\n");
  // Remove all remaining tags
  text = text.replace(/<[^>]+>/g, "");
  // Decode HTML entities
  text = text.replace(/&amp;/g, "&");
  text = text.replace(/&lt;/g, "<");
  text = text.replace(/&gt;/g, ">");
  text = text.replace(/&quot;/g, '"');
  text = text.replace(/&#39;/g, "'");
  text = text.replace(/&nbsp;/g, " ");
  // Collapse excessive whitespace
  text = text.replace(/\n{3,}/g, "\n\n");
  return text.trim();
}

/**
 * Save message attachments to Drive and return info string.
 * Returns newline-separated "filename|driveUrl" pairs.
 */
function saveAttachments(msg, parentFolder, dateStr, subject) {
  var attachments = msg.getAttachments();
  if (!attachments || attachments.length === 0) return "";

  // Create a subfolder: YYYY-MM-DD-subject-slug
  var datePrefix = dateStr.substring(0, 10); // "2026-04-07"
  var slug = subject.toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s]+/g, "-")
    .substring(0, 40)
    .replace(/-$/, "");
  var folderName = datePrefix + "-" + (slug || "email");

  // Reuse existing subfolder if it exists
  var subFolders = parentFolder.getFoldersByName(folderName);
  var folder = subFolders.hasNext() ? subFolders.next() : parentFolder.createFolder(folderName);

  var infoParts = [];
  for (var i = 0; i < attachments.length; i++) {
    var att = attachments[i];
    var fileName = att.getName();
    // Skip inline images (typically tracking pixels or signatures)
    if (att.isGoogleType()) continue;
    if (att.getSize() === 0) continue;

    var file = folder.createFile(att);
    var url = file.getUrl();
    infoParts.push(fileName + "|" + url);
  }

  return infoParts.join("\n");
}

/**
 * Utility: manually clear all data (keep headers). Use for testing.
 */
function clearSheet() {
  var sheet = getOrCreateSheet();
  var lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    sheet.deleteRows(2, lastRow - 1);
  }
  Logger.log("Sheet cleared.");
}

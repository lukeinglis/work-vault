---
title: Home
tags: [dashboard]
---

# Work Vault

**[[Todo]]** | **[[Initiatives Board]]** | **[[Commands]]** | **[[Automation]]**

---

## This Week

```dataview
LIST WITHOUT ID "[[" + file.path + "|" + title + "]]"
FROM "02-Weekly"
WHERE !contains(file.path, "_summaries")
SORT file.name DESC
LIMIT 1
```

## Components

```dataview
TABLE WITHOUT ID "[[" + file.path + "|" + title + "]]" AS "Component", status AS "Status", updated AS "Last Updated"
FROM "01-Components"
WHERE file.name = "_overview"
SORT title ASC
```

## Initiatives

```dataviewjs
const overviews = dv.pages('"01-Components"').where(p => p.file.name === "_overview").sort(p => p.title);
for (const ov of overviews) {
  dv.header(4, ov.title);
  const component = ov.initiative;
  const initiatives = dv.pages('"01-Components"')
    .where(p => p.tags && p.tags.includes("initiative") && p.file.name !== "_overview" && p.initiative === component)
    .sort(p => p.status);
  if (initiatives.length > 0) {
    dv.table(["Initiative", "Status"], initiatives.map(p => ["[[" + p.file.path + "|" + p.title + "]]", p.status]));
  } else {
    dv.paragraph("_No initiatives_");
  }
}
```

## Recent Meetings

```dataview
TABLE WITHOUT ID file.link AS "Meeting", date AS "Date"
FROM "03-Meetings"
WHERE contains(tags, "meeting") AND !contains(file.path, "_transcripts")
SORT date DESC
LIMIT 8
```

## Inbox Queue

```dataviewjs
const intake = dv.pages('"04-Inbox/intake"').length;
const total = dv.pages('"04-Inbox"').length;
dv.paragraph(`**${intake}** items awaiting triage | **${total}** total inbox items | [[04-Inbox/intake|Open Intake →]]`);
```

## Weekly Summaries

```dataview
TABLE WITHOUT ID file.link AS "Summary"
FROM "02-Weekly/_summaries"
SORT file.name DESC
LIMIT 5
```

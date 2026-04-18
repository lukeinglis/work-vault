Run deep competitive/adjacent landscape research for one or all initiatives. Produces comprehensive, source-rich briefs with links to papers, repos, blog posts, and announcements. Includes bidirectional Jira alignment analysis. These briefs should be a go-to reference for up-to-date knowledge on each domain.

**Usage:** `/research` (redhat-ai default) or `/research all` or `/research its` or `/research fine-tuning` or `/research ai-innovation` or `/research redhat-ai`

**Depth:** `/research --depth quick` or `/research --depth standard` (default) or `/research --depth deep`

## Depth Levels

| Level | Time | Search Queries | Deep Dives | Jira Integration | Output |
|-------|------|---------------|------------|------------------|--------|
| `quick` | 1-5 min | 5-8 per domain | Skip | Skip | Executive summary + recent developments only |
| `standard` | 5-10 min | 10-15 per domain | 3-5 follow-ups | Active features/epics, light mapping | Full brief |
| `deep` | 20-30 min | 15-20 per domain | 5-10, cross-referenced | Full Jira scan, detailed alignment + gap analysis | Comprehensive brief with strategic recommendations |

## Initiatives and Research Scope

### Inference-Time Scaling (`its`)
- **File:** `01-Components/inference-time-scaling/research/competitive-landscape.md`
- **Domain:** inference-time scaling, test-time scaling, test-time compute, reasoning strategies, search/planning at inference
- **IMPORTANT SCOPE NOTE:** ITS is about ALGORITHMS AND TECHNIQUES for scaling compute at inference time -- NOT general inference serving infrastructure. Do NOT include vLLM engine updates, SGLang benchmarks, llm-d architecture, NVIDIA Dynamo, Gateway API, Kubernetes inference infra, or hardware specs. Those belong in the `redhat-ai` domain. ITS covers what happens ABOVE the serving layer: how to make models reason better by spending more compute strategically.
- **Research areas:**
  - Academic papers on test-time compute scaling laws, search strategies, verification, reward models
  - Reasoning model releases -- ONLY as they relate to controllable thinking budgets, reasoning effort levels, and adaptive compute (not general model benchmarks)
  - ITS algorithms and frameworks: Best-of-N, self-consistency, MCTS for LLMs, process reward models, hierarchical voting, particle filtering
  - Adaptive compute allocation: per-query budget estimation, elastic scaling, token budget control
  - Novel decoding strategies specifically for reasoning: speculative decoding for reasoning models, latent reasoning, interleaved thinking
  - How cloud providers expose test-time compute controls (thinking effort parameters, reasoning budgets)
  - its-hub SDK competitive positioning: what alternatives exist for ITS-as-a-platform-service
  - RL for reasoning: GRPO, RLVR, reward-guided generation (as it intersects with ITS sampling)
- **NOT in scope (covered by redhat-ai):** inference engine performance, distributed inference architecture, model serving platforms, inference hardware, inference cost per token, Kubernetes inference networking
- **Key question:** What's advancing in test-time compute ALGORITHMS AND TECHNIQUES that Red Hat should know about, respond to, or build on?
- **Jira:** RHAISTRAT, component: Inference-Time Scaling

### Fine-Tuning (`fine-tuning`)
- **File:** `01-Components/fine-tuning/research/competitive-landscape.md`
- **Domain:** fine-tuning platforms, synthetic data generation, post-training techniques, alignment
- **Research areas:**
  - SDG platforms and offerings (Gretel, Tonic, NVIDIA NeMo Curator, Argilla, Scale AI, Snorkel)
  - Fine-tuning platforms and services (Anyscale, Modal, Together, Fireworks, Lambda, OpenPipe)
  - Post-training techniques (DPO, GRPO, KTO, RLHF variants, constitutional AI, distillation, merging)
  - Open source training frameworks (Axolotl, LLaMA-Factory, TRL, OpenRLHF, torchtune)
  - Data quality and curation research (filtering, decontamination, curriculum learning)
  - Enterprise fine-tuning trends (on-prem vs cloud, compliance, cost structures)
- **Key question:** What's the competitive landscape for enterprise fine-tuning and SDG, and where do SDG-Hub and Training-Hub fit?
- **Jira:** RHAISTRAT, component: Fine-Tuning

### AI Innovation (`ai-innovation`)
- **File:** `01-Components/ai-innovation/research/competitive-landscape.md`
- **Domain:** new AI tools (especially open source), Claude Code ecosystem, agent frameworks, AI developer tooling
- **Research areas:**
  - Claude Code: new features, skills, MCP servers, SDK updates, community extensions
  - Open source AI tools gaining traction (agent frameworks, coding assistants, research tools)
  - MCP ecosystem: new servers, integrations, community projects
  - AI-powered developer tools (Cursor, Windsurf, Cody, Aider, Continue, etc.)
  - Open source agent frameworks (LangGraph, CrewAI, AutoGen, Smolagents, OpenHands)
  - Research tools and knowledge management (NotebookLM, Elicit, Semantic Scholar tools)
  - Notable GitHub repos, Product Hunt launches, Hacker News trending projects
- **Key question:** What new tools or capabilities should the team know about or adopt?
- **Jira:** RHAISTRAT, component: AI Innovation

### Red Hat AI (`redhat-ai`) -- DEFAULT
- **File:** `01-Components/ai-innovation/research/competitive-landscape-red-hat-ai.md`
- **Domain:** Red Hat AI product portfolio, enterprise AI platform competition, industry trends affecting Red Hat AI
- **Research areas:**
  - Red Hat AI current offerings (Red Hat OpenShift AI, RHOAI components, InstructLab, Podman AI Lab, Neural Magic/vLLM)
  - Direct competitors (NVIDIA AI Enterprise, IBM watsonx, Google Vertex AI, AWS SageMaker, Azure AI, Databricks/Mosaic, Anyscale/Ray)
  - Enterprise AI platform trends (on-prem vs hybrid vs cloud, Kubernetes-native AI, MLOps maturity)
  - Open source AI ecosystem health (vLLM adoption, InstructLab community, KServe/ModelMesh)
  - Industry analyst coverage (Gartner, Forrester, IDC on AI platforms)
  - Partner ecosystem (IBM integration, NVIDIA partnership, cloud provider relationships)
  - Regulatory and compliance trends affecting enterprise AI adoption
  - Customer and community sentiment (reviews, case studies, adoption signals)
- **Key question:** How is Red Hat AI positioned in the enterprise AI platform market, what are competitors doing, and what industry trends should we be tracking?
- **Jira:** RHAISTRAT, all components

## Execution Philosophy

**Depth over speed.** At `standard` and `deep` levels, each initiative's research should take real time for thorough agent work. This is not a quick scan. The goal is to produce a reference document comprehensive enough that you can rely on it as your primary source for what's happening in each domain. Do not cut corners to save time. Follow threads. Read the actual papers and blog posts, not just titles. Cross-reference claims across sources.

At `quick` level, prioritize recency and signal. Get the headlines, skip the deep dives.

## Steps

1. **Determine scope and depth:**
   - Parse the argument to determine which initiative(s) to research
   - No arg = run `redhat-ai` only at `standard` depth
   - `all` = launch all four parallel agents
   - Parse `--depth` flag (default: `standard`)
   - Single initiative name = run just that one

2. **For each initiative, launch a dedicated research agent** with the initiative's scope, research areas, key question, and depth level from above. The agent should:

   a. **Read the existing research brief** to understand what's already captured, when it was last updated, and what the current state of knowledge is. This determines what's "new" vs. already known.

   b. **Pull active Jira work (standard and deep only).** Query RHAISTRAT for active Features and Epics matching the initiative's component. This becomes the baseline for alignment analysis. Use the Jira MCP tools.

   c. **Conduct phased web research, scaled to depth level.**

      **Phase 1 -- Broad landscape scan:**
      - `quick`: 5-8 search queries across highest-priority research areas
      - `standard`: 10-15 search queries across all research areas
      - `deep`: 15-20 search queries with varied formulations per area
      - Search academic sources (arxiv, semantic scholar, Google Scholar)
      - Search industry sources (company blogs, release announcements, product launches)
      - Search community sources (Reddit r/MachineLearning, r/LocalLLaMA, Hacker News, Twitter/X)
      - Search GitHub for trending repos, new releases, star counts

      **Phase 2 -- Deep dives on significant findings (standard + deep only):**
      - `standard`: 3-5 follow-up fetches on the most significant findings
      - `deep`: 5-10 follow-up fetches with cross-referencing
      - For each significant finding, fetch the primary source
      - Read actual paper abstracts and key findings, not just titles
      - Read actual blog posts and release notes for specifics
      - Check GitHub repos for activity, star counts, contributor momentum
      - Cross-reference claims: if one source says X, verify with another (`deep` only)

      **Phase 3 -- Strategic alignment analysis (standard + deep only):**

      Two directions:

      **a. Active work vs. landscape ("What we're building"):**
      - For each active Jira Feature/Epic, identify related competitive developments
      - Flag where competitors are ahead, behind, or taking a different approach
      - Note where our in-flight work addresses a real competitive gap

      **b. Landscape vs. active work ("What we're NOT building"):**
      - Identify significant industry developments with NO corresponding Jira work
      - Flag emerging areas gaining traction that are absent from the roadmap
      - Categorize gaps: intentional omission vs. potential blind spot vs. emerging opportunity
      - This section is the strategic early warning system

      Focus on developments since the brief's last update date (or the last 2-3 months if no prior update). When doing a first-time build, cover the full landscape comprehensively.

   d. **Synthesize findings into a comprehensive brief.** The research brief should be structured as:

      ```markdown
      ---
      title: "Competitive Landscape: [Initiative Name]"
      initiative: [initiative-tag]
      type: research
      created: YYYY-MM-DD
      updated: YYYY-MM-DD
      ---

      # Competitive Landscape: [Initiative Name]

      > Last updated: YYYY-MM-DD | Next scheduled: YYYY-MM-DD

      ## Executive Summary
      5-8 bullet overview of the current landscape state and what's changed recently. This should be readable in 60 seconds and give a PM enough context to speak intelligently about the space.

      ## Key Players and Projects
      Organized by category with sub-sections. For each entry:
      - What it is and who's behind it
      - Current status and maturity
      - Key differentiators
      - Links (repo, docs, product page)

      ## Recent Developments
      Reverse chronological. Each entry dated, linked to source, with analysis of significance.
      Format: `**YYYY-MM-DD** - [Title/event](link) - Why it matters. What it means for the space.`
      Include enough entries to cover the last 2-3 months comprehensively.

      ## Papers and Research
      Notable academic work. For each:
      - Title, authors, date, [arxiv/paper link]
      - One-paragraph summary of contribution and key findings
      - Why it matters for practitioners (not just theoretical interest)

      ## Open Source Projects to Watch
      Repos gaining momentum. For each:
      - Name, link, star count, recent commit activity
      - What it does and why it's notable
      - Adoption signals (who's using it, integrations, community size)

      ## Roadmap Alignment

      ### Active Work vs. Landscape
      For each active Jira Feature/Epic, how it maps to competitive developments:
      - Where we're ahead, behind, or taking a different approach
      - Where our in-flight work addresses a real competitive gap

      ### Industry Gaps -- Areas NOT on the Roadmap
      Significant industry developments with no corresponding active Jira work:

      | Area | Signal Strength | Category | Notes |
      |------|----------------|----------|-------|
      | ... | High/Med/Low | Blind spot / Intentional omission / Emerging opportunity | ... |

      This is the strategic early warning section. Review with engineering leads.

      ## Relevance to Red Hat
      Detailed competitive positioning analysis:
      - Where Red Hat's offerings sit relative to the landscape
      - Competitive threats to watch
      - Opportunities to pursue or gaps to fill
      - Trends that could shift our positioning

      ## Open Questions / Worth Tracking
      Things that aren't clear yet but could matter. Emerging trends to monitor.
      Include specific things to search for in the next research cycle.
      ```

   e. **Return the completed brief content and a research summary** (8-12 bullets) of key findings. Flag anything urgent or directly actionable.

3. **After all agents complete:**
   - Write each brief to its file
   - Present a consolidated summary across all initiatives to the user
   - Call out cross-cutting themes (e.g., a trend that affects multiple initiatives)
   - Highlight the "NOT building" gaps as priority items for review
   - Flag anything that warrants immediate attention or a deeper dive

## Research Quality Standards

- **Primary sources over summaries.** Link to the paper, not the blog post about the paper. Link to the GitHub repo, not the tweet about the repo.
- **Date everything.** Every development, paper, and release gets a date. "Recently" is meaningless in 6 months.
- **Include links.** Every claim should link to its source. Papers get arxiv links. Projects get GitHub links. Announcements get blog post links.
- **Be specific.** "Gretel launched synthetic tabular data v2 with differential privacy support" not "Gretel is doing interesting work."
- **Distinguish signal from noise.** Not every arxiv paper matters. Focus on things with real traction: citations, GitHub stars, adoption, benchmark results, production deployments.
- **Note what's unverified.** If something comes from a single source or seems speculative, say so.
- **Capture competitive positioning.** Don't just list what exists. Analyze where Red Hat's offerings sit relative to the landscape.

Run deep competitive/adjacent landscape research for one or all of your components. Produces comprehensive, source-rich briefs.

**Usage:** `/research` (all components) or `/research <component-name>`

## Steps

1. **Determine scope** -- which component(s) to research
   - Reads `01-Components/` to discover available components
   - If a specific component is named, research only that one

2. **For each component, launch a research agent** that:
   - Reads the existing `research/` folder for prior briefs
   - Conducts exhaustive web research in 3 phases:
     1. **Landscape scan** -- key players, products, open source projects
     2. **Recent developments** -- last 90 days of news, releases, papers
     3. **Deep dives** -- specific areas identified in phase 1-2

3. **Synthesize findings** into a comprehensive brief:
   - Executive summary (3-5 bullet TL;DR)
   - Key players and their positioning
   - Recent developments (dated, with sources)
   - Relevant papers and technical reports
   - Open source projects and their maturity
   - Implications for your product/initiative
   - Competitive positioning analysis

4. **Save brief** to `01-Components/<component>/research/YYYY-MM-DD-landscape-brief.md`

5. **Return summary** of all completed research

## Research Principles
- Prioritize depth over breadth
- Always include primary sources (not just summaries)
- Date all findings -- research decays fast
- Flag anything that directly impacts current initiatives

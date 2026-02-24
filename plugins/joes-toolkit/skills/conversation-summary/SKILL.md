---
name: conversation-summary
description: Transform long conversations into granular phase analyses and narrative synthesis. Use when a user provides conversation files (ChatGPT exports, interview transcripts, message logs, Slack exports, meeting notes) and asks to summarize, analyze, or extract insights. Triggers include requests to summarize conversations, analyze chats, process ChatGPT exports, summarize a directory of conversation files, or extract insights from long transcripts. Handles conversations too large for a single context window by chunking, parallel analysis, and narrative synthesis.
---

# Conversation Summary

Transform long conversations into structured granular analyses and a cohesive narrative synthesis. Designed for conversations too large for a single context window.

## Workflow

### Phase 1: Preparation

1. **Assess the input.** Read the file to determine format and size.
2. **Chunk the conversation** into segments of ~60-80K chars each. Split at natural boundaries (time gaps, topic shifts, message breaks). Never split mid-message.
3. **Save chunks** to `chunks/chunk_1.txt` through `chunks/chunk_N.txt`.
4. **Determine chunk count** from total size. Aim for 5-10 chunks. Fewer than 5 loses granularity; more than 10 creates too many analysis files.

For ChatGPT JSON exports, parse the JSON to extract messages first, then chunk the plain text. If the conversation has clear date/topic breaks, prefer those as chunk boundaries.

### Phase 2: Parallel Granular Analysis

Spawn **one sonnet agent per chunk** using `run_in_background: true`. Each agent reads one chunk and produces a standardized analysis.

See [references/analysis-template.md](references/analysis-template.md) for the full agent prompt template and section customization guide.

Key points:
- Each analysis uses an **8-section format**: Timeline & Context, Key Events, Exact Words, Advice Given vs Acted On, Physical/Setup Details, Participant Observations, Emotional Arc, Open Threads
- Sections are adaptable — see [references/conversation-types.md](references/conversation-types.md) for type-specific modifications
- The previous chunk's last 2 lines provide continuity context for the next chunk's agent
- **Exact quotes are non-negotiable** — 10-20 per chunk minimum

### Phase 3: Collect and Verify

1. Wait for all agents to complete (use `TaskOutput` with `block: true`).
2. Write each analysis to `chunks/chunk_{N}_analysis.md`.
3. Verify all files exist with `Glob`.

### Phase 4: Narrative Synthesis

Spawn **one opus agent** with access to all analysis files. It reads every analysis and produces a cohesive narrative synthesis.

See [references/synthesis-template.md](references/synthesis-template.md) for the full synthesis prompt and guidelines.

Key points:
- Structure emerges from content — don't force a template
- Weave in exact quotes from the analyses
- Literary quality — engaging narrative, not a clinical report
- Aim for 5,000-8,000 words depending on source length
- Every claim traceable to a specific analysis

## File Structure

```
{working-directory}/
├── chunks/
│   ├── chunk_1.txt
│   ├── chunk_1_analysis.md
│   ├── chunk_2.txt
│   ├── chunk_2_analysis.md
│   ├── ...
│   ├── chunk_N.txt
│   └── chunk_N_analysis.md
└── synthesis.md
```

## Key Principles

1. **Exact quotes are non-negotiable.** The participant's own words reveal more than any paraphrase.
2. **Granularity before synthesis.** The per-chunk analyses are the foundation. The synthesis is built on them, not instead of them.
3. **Parallel execution is essential.** Each chunk analysis is independent — always run them concurrently.
4. **Adapt the template, don't force it.** Drop irrelevant sections, add domain-specific ones.
5. **The synthesis should be literary.** Not a report — a narrative.
6. **Opus for synthesis, sonnet for analysis.** Detail extraction = sonnet. Creative narrative construction = opus.

## Examples

```
# Basic usage
/conversation-summary ~/exports/chatgpt-export.json

# Specify chunk count
/conversation-summary ~/interviews/transcript.md --chunks 6

# Skip to synthesis if analyses already exist
/conversation-summary ~/project/chunks/ --synthesis-only
```

## Notes

- Chunk boundaries must respect message boundaries — never split mid-message
- Total processing time scales with chunk count (parallel) + synthesis (sequential): expect 3-8 minutes for a typical long conversation
- For batch processing a directory of conversations, process each file independently using the same workflow

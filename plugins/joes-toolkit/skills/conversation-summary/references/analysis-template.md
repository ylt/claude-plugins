# Chunk Analysis Prompt Template

Use this template when spawning per-chunk analysis agents.

## Agent Prompt

```
You are analyzing chunk {N} of {TOTAL} from a long conversation. Your job is to produce a deeply granular analysis — not a summary. Extract specifics: exact quotes, precise observations, concrete details.

Context: {BRIEF_DESCRIPTION_OF_CONVERSATION}

{If N > 1: "The previous chunk ended with: {LAST_2_LINES_OF_PREVIOUS_CHUNK}"}

Read the chunk file at: {CHUNK_PATH}

Produce your analysis in this exact 8-section format:

## Timeline & Context
When does this chunk sit in the overall story? What's the state of affairs at the start? What period does it cover?

## Key Events (chronological, detailed)
Number each event. Include specific details — what exactly happened, what was said, what changed. Don't summarize; narrate with precision. Include behavioral observations, decisions made, and turning points.

## Exact Words (selected quotes)
Pull 10-20 of the most revealing, emotional, or important verbatim quotes. Use blockquotes. Choose quotes that capture voice, reveal character, show emotion, or mark turning points. Include typos/informal spelling as-is.

## Advice/Guidance Given vs Acted On
If the conversation involves any advice, recommendations, or suggestions: what was recommended, what was actually done, and where did the participants diverge from guidance? Note when someone pushed back and why.

## Physical/Setup Details
Any concrete details about the environment, equipment, tools, systems, locations, or logistics mentioned. These ground the analysis in specifics.

## Participant Observations
Specific behavioral notes for each participant. What patterns emerge? What personality traits are visible? How do they interact differently with different people/topics?

## Emotional Arc
Map the emotional journey through this chunk. What's the emotional state at entry, how does it shift, what triggers the shifts? Use evidence from tone, word choice, and explicit statements.

## Open Threads
What questions are unresolved at the end of this chunk? What's been set up but not yet paid off? What will the next chunk likely need to address?

Write the analysis to: {OUTPUT_PATH}
```

## Section Customization

The 8 sections above are defaults. Adapt to fit the conversation type:

| Conversation Type | Replace Section | With |
|---|---|---|
| Technical discussions | Physical/Setup Details | Technical Details & Architecture |
| Interviews | Advice Given vs Acted On | Questions Asked & Responses |
| Debates/Arguments | (add new section) | Arguments & Counterarguments |
| Meeting minutes | Open Threads | Action Items & Follow-ups |
| Support tickets | Emotional Arc | Resolution Progress |

## Critical Guidance

- **Exact Words is non-negotiable.** Without verbatim quotes the analysis becomes generic. 10-20 quotes minimum per chunk.
- **Narrate, don't summarize.** Key Events should read like a detailed account, not bullet-point highlights.
- **Preserve voice.** Include typos, informal spelling, slang as-is. These reveal character.
- **Track divergence.** When advice is given but not followed, that's always significant. Note *why* they diverged.

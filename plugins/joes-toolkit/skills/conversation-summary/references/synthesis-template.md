# Narrative Synthesis Prompt Template

Use this template when spawning the synthesis agent after all chunk analyses are complete.

## Agent Prompt

```
You have {N} granular analyses of a long conversation. Read all of them, then write a narrative synthesis that tells the complete story.

Analysis files:
{LIST_ALL_ANALYSIS_FILE_PATHS}

Write to: {SYNTHESIS_PATH}

Guidelines:
- Structure the synthesis into clear sections that emerge from the content (don't force a template — let the material dictate the structure)
- Common sections that work well:
  - The Full Arc (complete narrative from start to finish)
  - The Cast (character portraits of key participants)
  - Phase Transitions (major turning points)
  - The Emotional Journey
  - Recurring Threads (patterns that repeat across the conversation)
  - What Worked and What Didn't
  - Where Things Stand (current state at conversation's end)
- Weave in exact quotes from the analyses — they're the life of the document
- Include specific details (equipment, timestamps, behavioral patterns) naturally in the prose
- Preserve literary quality — this should read as engaging long-form narrative, not a clinical report
- Aim for roughly 5,000-8,000 words depending on source length
- Every claim should be traceable to a specific analysis
```

## Key Principles

- **Literary, not clinical.** The synthesis is a narrative, not a report. The reader should feel the emotional journey and meet participants as characters.
- **Quotes are the life of the document.** Weave exact quotes from the analyses into the prose. Without them, the synthesis loses its power.
- **Let structure emerge.** Don't force sections. If the conversation has a strong technical thread, create a section for it. If there's no clear "cast," skip character portraits.
- **Details ground the narrative.** Equipment, timestamps, locations, specific behavioral patterns — these make the synthesis feel real rather than abstract.
- **Traceable claims.** Every assertion should be supportable by evidence in the granular analyses.

## Model Routing

Use **opus** for synthesis. The chunk analyses are detail extraction (sonnet handles well). The synthesis requires creative narrative construction and cross-chunk pattern recognition — opus is better here.

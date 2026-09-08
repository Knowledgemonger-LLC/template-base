---
name: Handoff
description: Turn-ending messages stand alone for a reader who has not read the code
keep-coding-instructions: true
---

These rules govern messages that end a turn. Reasoning and mid-turn narration stay
terse and technical, and nothing explained there counts as already explained.

The reader knows the domain and the goal, and has never read this code. Explain
this codebase. Do not explain general programming concepts.

In every turn-ending message:

- State what is now true in the first line, then the detail, then what is not done.
- Describe changes as behavior, not as code. "Malformed uploads now fail loudly
  instead of truncating," not "refactored the validator."

When asking a question, include what forced the decision, the options with their
consequences, your recommendation and the reasoning behind it, and what you will
assume if the user defers. Never present options without a recommendation. Ask the
fewest questions that unblock the work, at the point the answer is needed.

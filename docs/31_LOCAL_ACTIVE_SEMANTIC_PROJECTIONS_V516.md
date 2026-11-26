# Active local semantic projections (V5.16)

Manager's V5.16 writer materializes a **derived** active dictionary inside each
local Kristal without overwriting canonical artifacts. It obtains the exact
active registry, graph, crosswalk, and dictionary catalog from the Authoring
Kit's existing `.kristal/v11/authoring.json` profile.

The profile is the local operator's authoring selection. Other v11 revisions
remain preserved as historical candidate artifacts. No consumer may silently
select the newest revision or interpret multiple older crosswalk targets as
simultaneously active. The projection is a convenience read model, not a
replacement for the v11 Authoring Kit validation or canonical commitment.

Output lives in `derived/semantic/v516/active-<digest>.json` with an atomic
pointer at `derived/semantic/active-resolution.json`. Multiple lexical
surfaces are retained with explicit layer priorities and provenance. Existing
accepted exactMatch records remain source-recorded only; alternative candidate
QIDs remain candidates. Ambiguous language is never merged by surface form.

If future evidence warrants changing a graph, identity, or crosswalk, create a
fresh canonical v11 revision through the Kit's recoverable transaction journal
and explicitly select it. The derived V5.16 operation does not itself make a
new canonical semantic claim, build v9 state, qualify, or publish.

See Manager `docs/SEMANTIC_LOCAL_EVOLUTION_V516.md` for the one-shot command.

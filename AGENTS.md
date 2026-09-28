# 42 — Project Memory

This file is the compact working memory for any LLM or developer editing this site. Read it in full before making changes. Keep it short. Rewrite it in place when the project changes; never turn it into a changelog or diary.

## Intent
Build one enduring, extremely lean website for the same work under two public identities:
- epistemicoctahedron.com → “Epistemic Octahedron”
- thephilosophersstone.com → “The Philosopher’s Stone”

Both domains run the same code and content. The current hostname determines the displayed identity. A visitor stays on whichever domain they entered.

The site should feel like an object encountered directly, not a conventional informational website. The opening view is a black field with the octahedron centered on desktop and mobile. No permanent visible header or conventional navbar. Interaction, motion, and disclosure should stay subtle.

The full paper does not need to be embedded or uploaded as a PDF. The website may eventually express its material in a compact, web-native form on one main page without making the initial experience heavy.

## Editing protocol
1. Read this file fully before every task.
2. Read every implementation file that the change could affect in full before editing it. Do not patch from snippets alone.
3. Interpret a request in light of the project intent and existing behavior, not only its literal wording.
4. Before adding a mechanism, verify that an equivalent mechanism does not already exist.
5. Preserve unrelated behavior. Make the smallest coherent change that satisfies the underlying intent.
6. Prefer extending or simplifying an existing system over creating a parallel one.
7. Avoid dependencies, frameworks, build steps, abstractions, and files unless they earn their complexity.
8. Keep first-load work minimal. Long-form content must never block the opening octahedron.
9. After a meaningful change, update the Current State or Decisions below only if the compressed project memory would otherwise become inaccurate.
10. Never append historical notes. Replace stale statements. If this file starts becoming long, compress it.

## Context discipline
- This file is the authoritative compressed map of the project.
- Source code remains the ground truth for exact behavior.
- Stable long-form theory/content is not required reading for an unrelated UI or rendering change unless that change can affect how the content is structured, named, navigated, or interpreted.
- If implementation grows, keep a compact map here so an editor knows what must be inspected before changing a subsystem.
- Do not silently delete or redesign something because it seems irrelevant to the current request.

## Current State
- One implementation file: `index.html`.
- Black full-screen opening view with a centered white wireframe octahedron.
- Octahedron is generated from six mathematical vertices and twelve edges, with no 3D asset or dependency.
- Subtle idle rotation; pointer/touch drag rotates it directly; reduced-motion users get a static idle state.
- Hostname-sensitive identity is established in one place.
- No navigation or theory presentation has been chosen yet.

## Decisions / Invariants
- One codebase serves both domains.
- Domain identity changes presentation naming, not the underlying theory.
- No forced redirect between the two domains.
- No permanent visible header by default.
- Desktop and mobile are first-class targets.
- The opening experience must remain fast even when the site eventually contains substantial theory text.
- Keep the codebase compact enough that its active implementation can be reread rather than guessed at.
- The octahedron should remain geometrically generated and lightweight unless a later visual requirement clearly justifies more machinery.

## Implementation Map
- `index.html` — complete current site: shell, styling, domain identity, octahedron geometry/projection, idle motion, and pointer/touch input.

## Threshold for splitting files
Do not split code merely for organization. Split only when a section becomes large enough that keeping it together makes full inspection harder. When splitting, update this map with each file’s ownership and dependency boundaries.

# 42 — Project Memory

This file is the compact working memory for any LLM or developer editing this site. Read it in full before making changes. Keep it short. Rewrite it in place when the project changes; never turn it into a changelog or diary.

## Intent
Build one enduring, extremely lean website for the same work under two public identities:
- epistemicoctahedron.com → “Epistemic Octahedron”
- thephilosophersstone.com → “The Philosopher’s Stone”

Both domains run the same code and content. The current hostname determines the displayed identity. A visitor stays on whichever domain they entered.

The site should feel like an object encountered directly, not a conventional informational website. The opening view is a black field with the octahedron centered on desktop and mobile. No permanent visible header or conventional navbar. Interaction, motion, and disclosure should stay subtle. The visual language may develop toward a precise magic-circle/interface treatment rather than a conventional 3D-object presentation.

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
- Black full-screen opening view with a centered white wireframe octahedron, displayed at a larger responsive scale (about 160% of the earlier baseline).
- Geometry: six vertices, twelve outer edges, three internal axes; orthographic projection; no 3D asset or library.
- Default orientation is the exact symmetric face-on star view: yaw π/4, pitch asin(1/√3).
- Direct drag imparts angular momentum. Released motion decays freely, then the nearest of four anchors magnetically captures it with a lightly underdamped spring/overshoot: main, top, side, bottom. The side anchor keeps the main yaw (π/4) and flattens pitch to 0 to avoid the quadrant-looking orientation.
- There is no continuous idle rotation.
- Set-angle overlays fade in only as motion becomes slow and an anchor is approached. The outer circle and all current overlay content appear only at the main anchor.
- Main overlay: outer ring now sits slightly inside the projected vertex radius so it visibly intersects the octahedron; E/P/M/C/W/K labels sit close outside that ring. Each large initial extends radially outward into its concept name (Empathy, Practicality, Maturity, Collapse, Wisdom, Knowledge), with a deliberate gap before the smaller suffix letters, which gradually fade toward the word’s end. An inner inscribed ring; larger black-filled x/y/z marker circles anchored to exact axis/edge intersections (y: MC×KE, x: EP×KC, z: WK×EC). Their shared radius guides curved inscription text only; no visible ring line is drawn there. Three separator dots are independently placed 120° apart. Each of the three inscriptions now owns its own 120° invisible arc sector, centered on its x/y/z marker, so phrases cannot spill into one another. The shared text radius sits slightly inside the marker radius to clear the KE/KC/EC lines; the top accountability sector is directed left-to-right so it reads upright without a separate radial offset hack. The three curved inscription texts are intentionally smaller than the surrounding labels.
- Hostname-sensitive identity is established in one place. No conventional navigation or theory presentation has been chosen yet.

## Decisions / Invariants
- One codebase serves both domains; no forced redirect.
- Domain identity changes naming, not underlying theory.
- No permanent visible header by default.
- Desktop and mobile are first-class targets.
- Opening experience must stay fast as theory content grows.
- Keep active implementation compact enough to reread rather than guess at.
- Octahedron stays geometrically generated and lightweight unless a later visual requirement clearly earns more machinery.
- Projection remains orthographic unless intentionally revisited.
- Snap overlays are screen-space interface geometry derived from the current projected shape, not a second 3D object.
- Do not invent detailed top/side/bottom overlay content until it is intentionally designed.

## Implementation Map
- `index.html` — complete current site: shell, domain identity, octahedron geometry/projection, inertial drag + magnetic snapping, and set-angle overlay rendering.

## Threshold for splitting files
Do not split code merely for organization. Split only when keeping a section together makes full inspection harder. When splitting, update this map with each file’s ownership and dependency boundaries.

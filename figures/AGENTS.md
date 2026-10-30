# 42 / Figures — Project Memory

Read this file before editing anything under `figures/`. This directory is a figure-staging surface for the paper. Keep its behavior independent from the public `/42/` experience unless the user explicitly asks to synchronize a change back into the main site.

## Intent
Use `figures/` as a clean interactive source for paper figures. The user should be able to ask for a particular view, plot, overlay, label set, or camera treatment, and have that figure-specific state built here without cluttering the default page.

The default page is deliberately empty except for the structure itself: full white viewport, centered black wireframe octahedron, desktop and mobile. No visible title, toolbar, labels, plot, explanatory text, or conventional UI.

## Geometry and semantics
The model geometry is inherited from root `/42/`: six vertices, twelve outer edges, and three diametric axes, with no 3D asset or rendering library.

Canonical model coordinates:
- x = Purpose: +x Empathy / affected welfare, -x Practicality / real-world constraint.
- y = Accountability: +y Maturity / answerability, -y Collapse / insulation.
- z = Meaning: +z Wisdom / contextual interpretation, -z Knowledge / informational grounding.

Do not casually rename, swap, mirror, or reinterpret these coordinates. Figure work may hide labels, but the underlying coordinate meaning stays stable.

## Default rendering
- `index.html` is a standalone SVG renderer.
- White background, black structure.
- Orthographic projection only in the default state. There is no perspective divide.
- The structure is exactly centered in the viewport on desktop and mobile.
- The outer edges retain the subtle depth-opacity cue from `/42/`; internal axes are black but lighter.
- One-finger touch drag and desktop LMB/pointer drag rotate the structure directly.
- Released drag preserves momentum, then magnetically settles with the same spring/damping feel used by `/42/`.
- No idle rotation.
- No two-finger pan/zoom behavior here unless explicitly requested for figure work.

## Magnetic view grid
The figure surface has 20 authored snap anchors. Every band has four quarter-turn yaw variants:
- yaw = 45°, 135°, 225°, 315°
- top: pitch +90°
- upper diagonal: pitch +45°
- side: pitch 0°
- lower diagonal: pitch -45°
- bottom: pitch -90°

IDs are `top-0..3`, `upper-0..3`, `side-0..3`, `lower-0..3`, and `bottom-0..3`.

The initial view is `upper-0` (yaw 45°, pitch +45°). Do not add the root site's 35.264° face-on `main` anchor here unless the user asks for it.

## Figure-specific features
The default page must stay visually bare. Plotting, overlays, labels, annotations, alternate line treatments, explicit angle displays, and perspective rendering should appear only when the user asks for a figure that needs them.

`window.FIGURES` intentionally exposes the current geometry, snap list, orthographic projection identity, current angle state, direct angle setting, snap targeting, and an empty `figureLayer`. Use or extend that surface for requested figure work rather than adding permanent visible controls.

Do not pre-build speculative figure systems. Add only what a requested figure needs, keep it isolated under `figures/`, and preserve the bare default when that requested state is not active.

## Editing protocol
1. Read this file and the complete affected implementation file before editing.
2. Preserve the exact geometry and coordinate semantics unless the user's request is explicitly about changing them.
3. Prefer small additions to the existing SVG renderer over libraries, frameworks, build steps, or duplicated renderers.
4. Keep paper-figure experiments inside `figures/` unless the user explicitly asks to change root `/42/`.
5. Keep this file compressed and current. Rewrite stale statements instead of appending a changelog.

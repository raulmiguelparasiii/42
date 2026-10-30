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

## Default rendering and interaction
- `index.html` is a standalone SVG renderer.
- White background, black structure.
- Orthographic projection only in the default state. There is no perspective divide.
- The structure is exactly centered in the viewport on desktop and mobile.
- The outer edges retain the subtle depth-opacity cue from `/42/`; internal axes are black but lighter.
- Orientation is a full quaternion, not a yaw/pitch-only state.
- One-finger touch drag and desktop LMB/pointer drag use an object-relative virtual trackball. The point grabbed on the currently visible projection determines the rotation axis. This must preserve the physical grab expectation: in a top view, a left swipe from the visible lower half rolls the structure clockwise, while the same left swipe from the visible upper half rolls it counter-clockwise.
- Do not replace trackball drag with fixed screen-space `dx → yaw` / `dy → pitch`; that breaks orientation-relative grabbing once another face or edge is in front.
- Released trackball drag preserves 3D angular momentum, then magnetically settles to the nearest authored quaternion snap with the same lightly underdamped feel as `/42/`.
- Two-finger pinch scales the figure from 0.6× to 1.6× for inspection. If a two-finger gesture drops back to one finger, that remaining finger resumes trackball rotation from its current location without a jump.
- No idle rotation.

## Magnetic view grid
The figure surface has 28 authored snap anchors.

Top and bottom each have eight rotational snaps, one every 45° around the vertical axis:
- yaw = 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
- top: pitch +90°
- bottom: pitch -90°

The other three bands have four quarter-turn variants at yaw = 45°, 135°, 225°, 315°:
- upper diagonal: pitch +asin(1/√3) ≈ +35.26438968°
- side: pitch 0°
- lower diagonal: pitch -asin(1/√3) ≈ -35.26438968°

The ±35.26438968° diagonal is the exact symmetric face-on angle used by root `/42/`. Do not replace it with ±45°.

IDs are:
- `top-0..7`
- `upper-0..3`
- `side-0..3`
- `lower-0..3`
- `bottom-0..7`

The initial view is `upper-0`: yaw 45°, pitch +asin(1/√3) ≈ +35.26438968°.

## Figure-specific features
The default page must stay visually bare. Plotting, overlays, labels, annotations, alternate line treatments, explicit angle displays, and perspective rendering should appear only when the user asks for a figure that needs them.

`window.FIGURES` exposes the current geometry, snap list, orthographic projection identity, exact root `/42/` main pitch, full quaternion orientation, approximate legacy yaw/pitch readout, direct angle/orientation setting, scale control, snap targeting, and an empty `figureLayer`. Use or extend that surface for requested figure work rather than adding permanent visible controls.

Do not pre-build speculative figure systems. Add only what a requested figure needs, keep it isolated under `figures/`, and preserve the bare default when that requested state is not active.

## Editing protocol
1. Read this file and the complete affected implementation file before editing.
2. Preserve the exact geometry and coordinate semantics unless the user's request is explicitly about changing them.
3. Preserve the object-relative trackball interaction unless the user's request is explicitly about changing it.
4. Prefer small additions to the existing SVG renderer over libraries, frameworks, build steps, or duplicated renderers.
5. Keep paper-figure experiments inside `figures/` unless the user explicitly asks to change root `/42/`.
6. Keep this file compressed and current. Rewrite stale statements instead of appending a changelog.

# 42 / Figures — Project Memory

Read this file before editing anything under `figures/`. This directory is a paper-figure staging surface. Keep it independent from public `/42/` behavior unless the user explicitly asks to synchronize a change back.

## Geometry and semantics
The structure is the same octahedron as root `/42/`: six signed vertices, twelve shell edges, three signed relations, and null at the origin.

Canonical coordinates:
- x = Purpose: -x Practicality, +x Empathy.
- y = Accountability: -y Insulation, +y Answerability.
- z = Meaning: -z Knowledge, +z Wisdom.
- null = Absence.
- the octahedral surface = Stance.

Do not rename, swap, mirror, or reinterpret these coordinates without an explicit request.

## Camera, rotation, and snaps
- Default rendering is orthographic on a white background.
- Orientation is a full quaternion.
- One-finger touch and desktop LMB use object-relative virtual-trackball rotation. Preserve the physical grab invariant: in top view, a left swipe from the visible lower half rolls clockwise; the same left swipe from the visible upper half rolls counter-clockwise.
- Two-finger touch remains a rotation gesture. The centroid steers the same trackball while pinch distance may also scale the figure from 0.6× to 1.6×. Never turn two-finger touch into zoom-only behavior.
- Released motion preserves 3D momentum and then magnetically captures the nearest authored quaternion snap.
- There are 28 snaps. Top and bottom each have yaw 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°. Upper/side/lower use yaw 45°, 135°, 225°, 315°. Upper/lower pitch is exactly ±asin(1/√3) ≈ ±35.26438968°, matching root `/42/`, never ±45°.

## Figure controls
The below-figure control surface is intentional and may grow as figure needs grow.

Relations:
- Purpose, Accountability, and Meaning each have a master line visibility toggle.
- Each relation independently switches between black and gray.
- Global `All black` and `All gray` controls set all three relation colors together.
- Relation labels use their full names only: Purpose, Accountability, Meaning. They can be off/on, dragged, pinned in screen space, and reset.

Signed poles:
- Practicality = `P` / `Practicality`
- Empathy = `E` / `Empathy`
- Insulation = `Ins` / `Insulation`
- Answerability = `Ans` / `Answerability`
- Knowledge = `K` / `Knowledge`
- Wisdom = `W` / `Wisdom`
- Absence = `∅` / `Absence`

Each signed pole has its own half-relation visibility and point marker. Its label cycles off → short → full. A relation master visibility toggle still governs its two signed halves as a group.

Labels:
- Labels start beside their anchor.
- Dragging a visible label pins it to that screen-space position and must suppress figure rotation for that gesture.
- A pinned label gets a thin gray leader line back to its moving anchor.
- Every draggable label has an independent Reset action that returns it to its default beside-anchor position.
- Keep label hit areas generous enough for touch without making ordinary figure rotation hard to start elsewhere.

Stance:
- Stance is an opaque solid shell.
- When enabled, hidden/back shell edges are suppressed rather than drawn through the fill.
- Interior signed-relation segments and the origin marker are hidden behind the opaque shell.
- Visible shell edges may remain as the black boundary.

## API and editing protocol
`window.FIGURES` exposes geometry, snaps, state, snap targeting, relation color control, label reset, and the empty `figureLayer`. Extend this surface when a requested figure needs programmatic control.

Before editing:
1. Read this file and the complete affected implementation file.
2. Preserve unrelated behavior and the full quaternion trackball.
3. Prefer extending the standalone SVG implementation over adding libraries or build steps.
4. Keep changes inside `figures/` unless explicitly asked otherwise.
5. Rewrite stale memory in place. Do not append a changelog.

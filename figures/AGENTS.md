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

## Opening composition and controls
- The mobile opening viewport is reserved for the centered octahedron and white space. Do not shrink, push, or reflow the octahedron to make room for controls.
- The octahedron keeps the original responsive scale, `min(67.2vw, 67.2vh)`, centered in a full `100dvh` stage.
- Figure controls live in a separate below-the-fold white sheet. Only a small sheet handle peeks into the bottom of the opening viewport. The handle supports ordinary vertical page scrolling and tapping it scrolls the control sheet into view.
- The blank opening stage does not act as a page-scroll gesture area on touch; use the sheet handle/control sheet to scroll on mobile.

## Camera, rotation, and momentum
- Orientation is a full quaternion.
- With Stance off, rendering is orthographic.
- With Stance on, rendering switches automatically to a perspective projection. Surface visibility uses camera-relative face tests, hidden shell edges are suppressed, and rear/occluded pole markers and labels disappear automatically while their toggle state is preserved.
- One-finger touch and desktop LMB use object-relative virtual-trackball rotation. Preserve the physical grab invariant: in top view, a left swipe from the visible lower half rolls clockwise; the same left swipe from the visible upper half rolls counter-clockwise.
- Two-finger touch follows the white Atlas's combined gesture: moving the finger-pair center steers the figure in screen yaw/pitch, twisting the pair rolls the figure around the viewing axis, and pinching simultaneously scales it from 0.6× to 1.6×. These motions use Figures' own quaternion math and share its angular momentum and magnetic snapping. When one finger remains, it resumes the native trackball without resetting momentum.
- Active drag is tracked at the window level so leaving the SVG does not abruptly kill the gesture.
- Released motion preserves angular momentum, decays naturally, and then the nearest authored magnetic snap captures it once motion is slow enough.
- Leaving the visible octahedron during an active drag does not kill the gesture; release behavior remains the same wherever the pointer/finger ends.
- There are 28 snaps. Top and bottom each have yaw 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°. Upper/side/lower use yaw 45°, 135°, 225°, 315°. Upper/lower pitch is exactly ±asin(1/√3) ≈ ±35.26438968°, matching root `/42/`, never ±45°.

## Figure controls and defaults
Default state:
- Stance/surface is ON.
- Purpose, Accountability, and Meaning relation lines remain enabled and black, but their text labels start OFF.
- Signed pole half-relations/points remain enabled. Signed pole labels start in short form: Practicality `P`, Empathy `E`, Insulation `Ins`, Answerability `Ans`, Knowledge `K`, Wisdom `W`.
- Absence point remains enabled in state but is naturally hidden by an opaque Stance surface; its label starts OFF. Short Absence is `∅`.

Relations:
- Purpose, Accountability, and Meaning each have a master line visibility toggle.
- Each relation independently switches between black and gray.
- Global `All black` and `All gray` controls set all three relation colors together.
- Relation labels cycle off → `purposive axis` → `purposive relation` → `x-axis` → off for Purpose; off → `accountability axis` → `accountability relation` → `y-axis` → off for Accountability; and off → `meaning axis` → `meaning relation` → `z-axis` → off for Meaning. Each label connects to a distinct noncentral point on its own signed relation rather than sharing the origin. They can be dragged, pinned in screen space, and reset. Relation rows wrap their long label controls onto a second row on mobile.

Signed poles:
- Practicality = `P` / `Practicality`
- Empathy = `E` / `Empathy`
- Insulation = `Ins` / `Insulation`
- Answerability = `Ans` / `Answerability`
- Knowledge = `K` / `Knowledge`
- Wisdom = `W` / `Wisdom`
- Absence = `∅` / `Absence`

Each signed pole has its own half-relation visibility and point marker. Its label cycles off → short → full. A relation master visibility toggle still governs its two signed halves as a group.

## Label interaction
- Labels start beside their anchor and are non-selectable on iPhone/iOS. Native text selection and touch callouts must not compete with label interaction on the figure stage. Label lettering and hit boxes remain visually the same size at every pinch scale: the text is enlarged to its former 1.6× zoomed-in size, and each label group counter-scales around its anchor as the figure zooms. The default placement uses each label's measured text box, current zoom, and projected pole/axis direction so even long names clear their target on all sides.
- The label text itself does not receive pointer events. A deliberately generous transparent hit rectangle surrounds it.
- Pressing a visible label enters an armed hold state. A visible outline/progress indicator fills over about 850 ms. Small finger movement is tolerated within a generous wiggle threshold so slight drift does not hand the gesture to octahedron rotation.
- Once the hold completes, dragging pins the label to that screen-space position. The label keeps the initial grab offset so it does not jump under the finger.
- Moving decisively beyond the wiggle threshold before the hold completes cancels label arming and hands the gesture to ordinary octahedron rotation. A second touch also cancels label arming/dragging and starts the combined two-finger gesture, whether that touch lands on a label or elsewhere on the stage.
- A pinned label gets a thin gray leader line back to its moving anchor; its endpoint is clipped to just outside the measured label rectangle, leaving a consistent text gap. Relation labels show the same short leader even before pinning so their noncentral axis targets are explicit. Lines disappear when the target falls inside the protected text area.
- Every draggable label has an independent Reset action that returns it to its default beside-anchor position.
- When Stance occludes a pole/anchor, the corresponding marker, label, and leader are hidden automatically. Pinned screen coordinates remain stored and reappear when the anchor becomes visible again.

## Stance
- Stance is an opaque solid shell.
- With Stance on, perspective projection is active.
- Only camera-facing shell faces render; rear shell edges are suppressed rather than drawn through the fill.
- Interior signed-relation segments and the origin/Absence marker are hidden behind the opaque shell.
- Visible shell edges remain as the black boundary.

## Figure state handoff
- The below-fold controls include a Figure state card with a Default view option, a selector for Figure 1 through Figure 24, a live read-only JSON preview, and a Copy current state button.
- Default view is selected on every fresh page load and preserves the native opening composition. Selecting Figure 1 loads the authored user-approved Figure 1 snapshot: exact bottom-1 quaternion, scale 1.3723686050883095, Stance off, Purpose/Meaning axis labels at pinned offsets, full P/E/K/W pole labels, and hidden accountability poles/absence. Selecting Default view or any unsaved figure (2–24) restores the native default composition. Figure numbers still label the exported live state; further edits are not automatically saved, and the user supplies new figure states for deliberate implementation. No local-storage persistence or automatic import is implied.
- The export uses the existing `window.FIGURES.getState()` payload and adds `format: "42-figures-state-v1"` and `figure: "Figure N"`. The payload covers the precise quaternion orientation, snap target, scale, relation visibility/color/label/pins, pole visibility/label/pins, and Stance. The state is an instantaneous configuration, excluding motion velocity. The readout updates several times per second but pauses when focused so selection/copy remains stable. The copy action reads the latest instantaneous state, supports Clipboard API with a selection fallback, and does not alter the figure.
- Preserve this handoff contract when adding permanent figures; it is meant to let the user supply canonical per-figure states, which can then be implemented deliberately in a later task.

## API and editing protocol
`window.FIGURES` exposes geometry, snaps, current projection mode, state, snap targeting, relation color control, label reset, Stance control, motion stop, and the empty `figureLayer`. Extend this surface when a requested figure needs programmatic control.

Before editing:
1. Read this file and the complete affected implementation file.
2. Preserve unrelated behavior and the full quaternion trackball.
3. Preserve the full-screen opening composition and below-fold sheet unless the user explicitly changes it.
4. Prefer extending the standalone SVG implementation over adding libraries or build steps.
5. Keep changes inside `figures/` unless explicitly asked otherwise.
6. Rewrite stale memory in place. Do not append a changelog.

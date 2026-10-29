from pathlib import Path


def once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, found {count}")
    return text.replace(old, new, 1)

path = Path('index.html')
s = path.read_text()

old_commit = r'''const commitReturnPortal = state => {
  if (
    portalPreviewMode || portalTransitioning || compositionMode !== 'atlas' ||
    !state || Number(state.distance) > PORTAL_PREVIEW_RADIUS
  ) return false;
  portalTransitioning = true;
  atlasPointerActive = false;
  atlasPortalState = state;
  syncBlackFromAtlas(state);
  compositionMode = 'black';
  const frame = portalPreviewFrame;
  if (frame) {
    frame.classList.remove('is-active');
    frame.classList.add('is-committing');
    frame.style.opacity = '0';
    frame.setAttribute('aria-hidden', 'true');
  }
  velocityYaw = 0;
  velocityPitch = 0;
  snapTarget = { ...snaps[0] };
  releasedAt = performance.now();
  restoreBlackPortalMatch(true);
  setTimeout(() => {
    frame?.classList.remove('is-committing');
    portalTransitioning = false;
  }, 300);
  return true;
};'''
new_commit = r'''const commitReturnPortal = state => {
  if (
    portalPreviewMode || portalTransitioning || compositionMode !== 'atlas' ||
    !state?.returnReady
  ) return false;
  portalTransitioning = true;
  atlasPointerActive = false;
  atlasPortalState = state;
  syncBlackFromAtlas(state);
  compositionMode = 'black';
  const frame = portalPreviewFrame;
  if (frame) {
    frame.classList.remove('is-active');
    frame.classList.add('is-committing');
    frame.style.opacity = '0';
    frame.setAttribute('aria-hidden', 'true');
  }
  velocityYaw = 0;
  velocityPitch = 0;
  snapTarget = { ...snaps[0] };
  releasedAt = performance.now();
  restoreBlackPortalMatch(true);
  setTimeout(() => {
    frame?.classList.remove('is-committing');
    portalTransitioning = false;
  }, 300);
  return true;
};'''
s = once(s, old_commit, new_commit, 'return commit')

old_atlas_preview = r'''  if (!portalPreviewFrame) return;
  const state = atlasPortalState;
  const distance = Number(state?.distance);
  const active = atlasPointerActive && Number.isFinite(distance);
  const amount = active ? portalAmount(distance) : 0;
  if (active && distance <= PORTAL_PREVIEW_RADIUS) {
    syncBlackFromAtlas(state);
  } else if (blackPortalMatch) {
    restoreBlackPortalMatch(false);
  }
  portalPreviewFrame.style.opacity = String(1 - PORTAL_MAX_OPACITY * amount);
};'''
new_atlas_preview = r'''  if (!portalPreviewFrame) return;
  const state = atlasPortalState;
  const rawAmount = Number(state?.returnAmount);
  const amount = Number.isFinite(rawAmount) ? clamp(rawAmount, 0, 1) : 0;
  if (amount > 0.001) {
    syncBlackFromAtlas(state);
  } else if (blackPortalMatch) {
    restoreBlackPortalMatch(false);
  }
  portalPreviewFrame.style.opacity = String(1 - PORTAL_MAX_OPACITY * amount);
};'''
s = once(s, old_atlas_preview, new_atlas_preview, 'atlas return preview')

old_state_msg = r'''  if (data.type === 'stone-atlas-state') {
    if (compositionMode !== 'atlas') return;
    atlasPortalState = data.state || null;
    atlasPointerActive = Boolean(data.pointerActive);
    return;
  }
  if (data.type === 'stone-atlas-release') {
    if (compositionMode !== 'atlas') return;
    atlasPointerActive = false;
    atlasPortalState = data.state || atlasPortalState;
    if (!commitReturnPortal(atlasPortalState)) {
      if (portalPreviewFrame) portalPreviewFrame.style.opacity = '1';
      restoreBlackPortalMatch(false);
    }
    return;
  }'''
new_state_msg = r'''  if (data.type === 'stone-atlas-state') {
    if (compositionMode !== 'atlas') return;
    atlasPortalState = data.state || null;
    atlasPointerActive = Boolean(data.pointerActive);
    if (atlasPortalState?.returnReady) commitReturnPortal(atlasPortalState);
    return;
  }
  if (data.type === 'stone-atlas-release') {
    if (compositionMode !== 'atlas') return;
    atlasPointerActive = false;
    atlasPortalState = data.state || atlasPortalState;
    return;
  }'''
s = once(s, old_state_msg, new_state_msg, 'atlas state/release messages')

old_snap = r'''      const snapOverlayOpacity = target => {
        if (explainer.active) return 0;'''
new_snap = r'''      const snapOverlayOpacity = target => {
        if (explainer.active || compositionMode === 'atlas' || portalTransitioning) return 0;'''
s = once(s, old_snap, new_snap, 'snap overlay suppression')

old_main = r'''        const mainOpacity = explainer.active
          ? 0
          : clamp(1 - mainDistance / 0.16, 0, 1) * motionFactor;'''
new_main = r'''        const mainOpacity = (explainer.active || compositionMode === 'atlas' || portalTransitioning)
          ? 0
          : clamp(1 - mainDistance / 0.16, 0, 1) * motionFactor;'''
s = once(s, old_main, new_main, 'main overlay suppression')

path.write_text(s)

agents = Path('AGENTS.md')
a = agents.read_text()
old_memory = '''- A hidden reciprocal composition doorway to the Philosopher’s Stone Atlas uses the exact vertically mirrored orientation yaw π/4, pitch −asin(1/√3); it is deliberately not a fifth magnetic snap. The browser stays on the current `/42/` page. The Atlas is lazily loaded as a second full-screen composition inside the page: inside a 4° angular window, the inactive composition is synchronized to the active Stone’s exact projected pose and crossfaded up to 52%, receding continuously as the user pulls away. Releasing inside the window commits the composition without navigation. The newly active Stone begins at the same on-screen pose, then moves to its native UI position and snaps to that composition’s normal resting orientation. The reverse doorway uses the same projected-pose handoff. An 8° outer window preloads the inactive composition invisibly.'''
new_memory = '''- A hidden black→white composition doorway to the Philosopher’s Stone Atlas uses the exact vertically mirrored orientation yaw π/4, pitch −asin(1/√3); it is deliberately not a fifth magnetic snap. The browser stays on the current `/42/` page. An 8° outer window lazily preloads the Atlas; inside the final 4°, its Stone is synchronized to the black Stone’s exact projected pose and crossfaded up to 52%. The seam uses a near-orthographic 1.15° perspective lens only for geometric continuity. Releasing inside the doorway commits without navigation; over about 0.9 s the Atlas Stone moves into its native layout/orientation while its camera continuously returns to the native 45° perspective, without blocking interaction. Returning to black no longer uses a fixed reciprocal doorway: a deliberate fast Atlas throw above the normal snap range arms a momentum-preserving capture. Native angular momentum continues to decay while a gentle attraction increasingly pulls the Stone toward the exact quaternion corresponding to the black main view yaw π/4, pitch +asin(1/√3). During the final 12° the bare black wireframe progressively appears and the Atlas lens flattens back toward the seam; touching again cancels the capture. Once the exact return view remains untouched for one second, the white composition yields to black and the Stone slides into `/42/`’s native framing before ordinary black overlays reappear.'''
a = once(a, old_memory, new_memory, 'AGENTS composition state')
agents.write_text(a)

print('Parent hybrid controller patch applied.')

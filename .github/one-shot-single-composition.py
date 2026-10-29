from pathlib import Path


def once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, found {count}")
    return text.replace(old, new, 1)


p = Path('index.html')
s = p.read_text()

old_css = """    #portal-preview {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
  display: block;
  opacity: 0;
  pointer-events: none;
  z-index: 20;
  background: #f8fafc;
  transition: opacity 80ms linear;
}
#portal-preview.is-committing {
  opacity: 1 !important;
  transition: opacity 220ms ease;
}
"""
new_css = """    #portal-preview {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
      opacity: 0;
      pointer-events: none;
      z-index: 20;
      background: #f8fafc;
      transition: opacity 80ms linear;
    }
    #portal-preview.is-active {
      pointer-events: auto;
    }
    #portal-preview.is-committing {
      transition: opacity 220ms ease;
    }
"""
s = once(s, old_css, new_css, 'portal composition CSS')

s = once(
    s,
    "const ATLAS_URL = 'https://raulmiguelparasiii.github.io/epistemic-octahedron/philosophers-stone-atlas/';\n",
    "const ATLAS_URL = 'https://raulmiguelparasiii.github.io/epistemic-octahedron/philosophers-stone-atlas/';\nconst ATLAS_ORIGIN = new URL(ATLAS_URL).origin;\n",
    'Atlas origin'
)

old_state = """const PORTAL_YAW = Math.PI / 4;
const PORTAL_PITCH = -MAIN_PITCH;
const PORTAL_PRELOAD_RADIUS = 8 * Math.PI / 180;
const PORTAL_PREVIEW_RADIUS = 4 * Math.PI / 180;
const PORTAL_MAX_OPACITY = 0.52;
let portalPreviewFrame = null;
let portalTransitioning = false;
let portalArrivalLocked = portalArrival;
let portalEntryHeld = portalPreviewMode || portalArrival;
"""
new_state = """const PORTAL_YAW = Math.PI / 4;
const PORTAL_PITCH = -MAIN_PITCH;
const PORTAL_PRELOAD_RADIUS = 8 * Math.PI / 180;
const PORTAL_PREVIEW_RADIUS = 4 * Math.PI / 180;
const PORTAL_MAX_OPACITY = 0.52;
let portalPreviewFrame = null;
let portalTransitioning = false;
let portalArrivalLocked = portalArrival;
let portalEntryHeld = portalPreviewMode || portalArrival;
let compositionMode = 'black';
let atlasReady = false;
let atlasPointerActive = false;
let atlasPortalState = null;
let blackPreviewActive = false;
let blackPortalMatch = null;
let atlasActivationTimer = 0;
"""
s = once(s, old_state, new_state, 'single composition state')

start = s.index("const portalAngularDistance = () => Math.hypot(")
end = s.index("      const updateFirstPrinciplesScrollHint = () => {", start)
old_portal = s[start:end]
new_portal = r"""const portalAngularDistance = () => Math.hypot(
  wrap(PORTAL_YAW - yaw),
  PORTAL_PITCH - pitch
);
const portalAmount = distance => smoothstep(
  clamp(1 - distance / PORTAL_PREVIEW_RADIUS, 0, 1)
);
const stoneShellRect = () => {
  const rect = stoneShell.getBoundingClientRect();
  return { left: rect.left, top: rect.top, width: rect.width, height: rect.height };
};
const postAtlasMessage = message => {
  if (!portalPreviewFrame?.contentWindow) return;
  portalPreviewFrame.contentWindow.postMessage(message, ATLAS_ORIGIN);
};
const ensurePortalPreview = () => {
  if (portalPreviewMode || portalPreviewFrame) return portalPreviewFrame;
  const frame = document.createElement('iframe');
  frame.id = 'portal-preview';
  frame.title = "The Philosopher's Stone Atlas";
  frame.tabIndex = -1;
  frame.setAttribute('aria-hidden', 'true');
  frame.src = ATLAS_URL + '?embedded=1';
  document.body.appendChild(frame);
  portalPreviewFrame = frame;
  return frame;
};
const captureBlackPortalMatch = () => {
  if (blackPortalMatch) return blackPortalMatch;
  const rect = stoneShellRect();
  blackPortalMatch = {
    style: stoneShell.getAttribute('style'),
    rect
  };
  return blackPortalMatch;
};
const setBlackPortalRect = rect => {
  if (!rect) return false;
  const left = Number(rect.left);
  const top = Number(rect.top);
  const width = Number(rect.width);
  const height = Number(rect.height);
  if (
    !Number.isFinite(left) || !Number.isFinite(top) ||
    !Number.isFinite(width) || !Number.isFinite(height) ||
    width <= 0 || height <= 0
  ) return false;
  captureBlackPortalMatch();
  stoneShell.style.position = 'fixed';
  stoneShell.style.left = left + 'px';
  stoneShell.style.top = top + 'px';
  stoneShell.style.width = width + 'px';
  stoneShell.style.height = height + 'px';
  stoneShell.style.aspectRatio = 'auto';
  stoneShell.style.margin = '0';
  stoneShell.style.transform = 'none';
  stoneShell.style.transition = 'none';
  return true;
};
const finishBlackPortalRestore = saved => {
  if (!saved) return;
  if (saved.style === null) stoneShell.removeAttribute('style');
  else stoneShell.setAttribute('style', saved.style);
  blackPortalMatch = null;
  applyMobileViewport();
};
const restoreBlackPortalMatch = (animate = false) => {
  const saved = blackPortalMatch;
  if (!saved) return;
  if (!animate) {
    finishBlackPortalRestore(saved);
    return;
  }
  const startRect = stoneShell.getBoundingClientRect();
  const endRect = saved.rect;
  const started = performance.now();
  const duration = 280;
  const step = now => {
    const raw = clamp((now - started) / duration, 0, 1);
    const t = smoothstep(raw);
    setBlackPortalRect({
      left: startRect.left + (endRect.left - startRect.left) * t,
      top: startRect.top + (endRect.top - startRect.top) * t,
      width: startRect.width + (endRect.width - startRect.width) * t,
      height: startRect.height + (endRect.height - startRect.height) * t
    });
    if (raw < 1) {
      requestAnimationFrame(step);
      return;
    }
    finishBlackPortalRestore(saved);
  };
  requestAnimationFrame(step);
};
const syncAtlasFromBlack = () => {
  if (!atlasReady) return;
  postAtlasMessage({
    type: 'stone-composition-sync-from-black',
    yaw,
    pitch,
    rect: stoneShellRect()
  });
};
const cancelBlackPortalPreview = () => {
  if (!blackPreviewActive) return;
  blackPreviewActive = false;
  postAtlasMessage({ type: 'stone-composition-cancel-black-preview' });
};
const syncBlackFromAtlas = state => {
  if (!state?.pose || !state?.metrics) return false;
  const nextYaw = Number(state.pose.yaw);
  const nextPitch = Number(state.pose.pitch);
  const centerX = Number(state.metrics.centerX);
  const centerY = Number(state.metrics.centerY);
  const unitScale = Number(state.metrics.unitScale);
  if (
    !Number.isFinite(nextYaw) || !Number.isFinite(nextPitch) ||
    !Number.isFinite(centerX) || !Number.isFinite(centerY) ||
    !Number.isFinite(unitScale) || unitScale <= 0
  ) return false;
  const shellSize = unitScale * 240 / 86;
  yaw = nextYaw;
  pitch = clamp(nextPitch, -PITCH_LIMIT, PITCH_LIMIT);
  velocityYaw = 0;
  velocityPitch = 0;
  snapTarget = null;
  return setBlackPortalRect({
    left: centerX - shellSize / 2,
    top: centerY - shellSize / 2,
    width: shellSize,
    height: shellSize
  });
};
const activateAtlasComposition = () => {
  const frame = ensurePortalPreview();
  if (!frame) return;
  clearTimeout(atlasActivationTimer);
  frame.classList.add('is-committing');
  frame.style.opacity = '1';
  frame.setAttribute('aria-hidden', 'false');
  if (atlasReady) {
    syncAtlasFromBlack();
    postAtlasMessage({ type: 'stone-composition-activate-atlas' });
  }
  atlasActivationTimer = setTimeout(() => {
    if (compositionMode !== 'atlas') return;
    frame.classList.add('is-active');
    frame.classList.remove('is-committing');
  }, 300);
};
const commitPortal = () => {
  if (
    portalPreviewMode || portalArrivalLocked || portalTransitioning ||
    explainer.active || compositionMode !== 'black' || !dragging ||
    portalAngularDistance() > PORTAL_PREVIEW_RADIUS
  ) return false;
  portalTransitioning = true;
  portalEntryHeld = false;
  compositionMode = 'atlas';
  velocityYaw = 0;
  velocityPitch = 0;
  snapTarget = null;
  blackPreviewActive = false;
  activateAtlasComposition();
  setTimeout(() => { portalTransitioning = false; }, 320);
  return true;
};
const commitReturnPortal = state => {
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
};
const updatePortalPreview = () => {
  if (portalPreviewMode || portalTransitioning) return;
  if (compositionMode === 'black') {
    const distance = portalAngularDistance();
    if (portalArrivalLocked) {
      if (distance > PORTAL_PREVIEW_RADIUS * 1.5) portalArrivalLocked = false;
      if (portalPreviewFrame) portalPreviewFrame.style.opacity = '0';
      return;
    }
    if (distance < PORTAL_PRELOAD_RADIUS) ensurePortalPreview();
    const active = dragging && !explainer.active;
    const amount = active ? portalAmount(distance) : 0;
    if (active && distance <= PORTAL_PREVIEW_RADIUS) {
      blackPreviewActive = true;
      syncAtlasFromBlack();
    } else {
      cancelBlackPortalPreview();
    }
    if (portalPreviewFrame) {
      portalPreviewFrame.style.opacity = atlasReady
        ? String(PORTAL_MAX_OPACITY * amount)
        : '0';
    }
    return;
  }

  if (!portalPreviewFrame) return;
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
};
window.addEventListener('message', event => {
  if (!portalPreviewFrame || event.source !== portalPreviewFrame.contentWindow) return;
  if (event.origin !== ATLAS_ORIGIN) return;
  const data = event.data || {};
  if (data.type === 'stone-atlas-ready') {
    atlasReady = true;
    if (compositionMode === 'atlas') activateAtlasComposition();
    else if (blackPreviewActive) syncAtlasFromBlack();
    return;
  }
  if (data.type === 'stone-atlas-state') {
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
  }
  if (data.type === 'stone-atlas-cancel') {
    atlasPointerActive = false;
    if (compositionMode === 'atlas' && portalPreviewFrame) {
      portalPreviewFrame.style.opacity = '1';
    }
    restoreBlackPortalMatch(false);
  }
});
"""
s = s[:start] + new_portal + s[end:]

s = once(
    s,
    """      const settlePhysics = (now, dt) => {
  if (dragging) return;
  if (portalEntryHeld && !explainer.active) {
""",
    """      const settlePhysics = (now, dt) => {
  if (compositionMode === 'atlas') return;
  if (dragging) return;
  if (portalEntryHeld && !explainer.active) {
""",
    'pause black physics while Atlas active'
)

s = once(
    s,
    """        settlePhysics(now, dt);
        draw();
        updatePortalPreview();
        requestAnimationFrame(frame);
""",
    """        updatePortalPreview();
        settlePhysics(now, dt);
        draw();
        requestAnimationFrame(frame);
""",
    'composition sync before draw'
)

# Keep pointer-release behavior but normalize the now-composition-based commit call.
s = once(
    s,
    """      const stopDrag = event => {
  if (!dragging) return;
  const portalCommitted = commitPortal();
        dragging = false;
""",
    """      const stopDrag = event => {
        if (!dragging) return;
        const portalCommitted = commitPortal();
        dragging = false;
""",
    'stop drag formatting'
)

p.write_text(s)

agents = Path('AGENTS.md')
a = agents.read_text()
old_portal_memory = "- A hidden reciprocal portal to the Philosopher’s Stone Atlas uses the exact vertically mirrored orientation yaw π/4, pitch −asin(1/√3); it is deliberately not a fifth magnetic snap. While the Stone is actively held within a 4° angular window, the atlas is lazily preloaded and crossfaded up to 52%, receding continuously as the user pulls away. Releasing inside that window commits a fast full-page transition. Portal previews cannot recursively open another portal, and a portal arrival holds the exact doorway orientation until the user begins dragging and stays return-locked until the Stone leaves the doorway zone. The atlas implements the same mechanism in reverse at its visually equivalent quaternion.\n"
new_portal_memory = "- A hidden reciprocal composition doorway to the Philosopher’s Stone Atlas uses the exact vertically mirrored orientation yaw π/4, pitch −asin(1/√3); it is deliberately not a fifth magnetic snap. The browser stays on the current `/42/` page. The Atlas is lazily loaded as a second full-screen composition inside the page: inside a 4° angular window, the inactive composition is synchronized to the active Stone’s exact projected pose and crossfaded up to 52%, receding continuously as the user pulls away. Releasing inside the window commits the composition without navigation. The newly active Stone begins at the same on-screen pose, then moves to its native UI position and snaps to that composition’s normal resting orientation. The reverse doorway uses the same projected-pose handoff. An 8° outer window preloads the inactive composition invisibly.\n"
a = once(a, old_portal_memory, new_portal_memory, 'AGENTS portal state')
old_nav = "- Hostname-sensitive identity is established in one place. There is still no conventional navbar; the only page-level navigation is the hidden reciprocal Stone portal to the Atlas.\n"
new_nav = "- Hostname-sensitive identity is established in one place. There is still no conventional navbar. The Atlas doorway is a visual composition switch inside the current page rather than page-level navigation.\n"
a = once(a, old_nav, new_nav, 'AGENTS navigation state')
agents.write_text(a)

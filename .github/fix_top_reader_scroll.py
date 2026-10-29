from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = """    #first-principles-panel {
      position: absolute;
      left: 50%;
      top: 81dvh;
      bottom: max(14px, env(safe-area-inset-bottom));"""
new = """    #first-principles-panel {
      position: fixed;
      left: 50%;
      top: 81dvh;
      bottom: max(14px, env(safe-area-inset-bottom));"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

old = """      overflow-y: auto;
      overscroll-behavior: contain;
      -webkit-overflow-scrolling: touch;
      touch-action: pan-y;"""
new = """      min-height: 0;
      overflow-y: scroll;
      overscroll-behavior-y: contain;
      -webkit-overflow-scrolling: touch;
      touch-action: pan-y;"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

p.write_text(s)

s = p.read_text()
assert '#first-principles-panel {\n      position: fixed;' in s
assert 'overflow-y: scroll;' in s
assert 'overscroll-behavior-y: contain;' in s

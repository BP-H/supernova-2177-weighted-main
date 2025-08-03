# pages/enter_metaverse.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import streamlit as st

def main(main_container=None) -> None:
    # play nice if another page already set config
    try:
        st.set_page_config(page_title="enter metaverse", layout="wide", initial_sidebar_state="collapsed")
    except Exception:
        pass

    st.markdown("### enter metaverse")
    st.caption("a multi-portal ride /// game-like exploration through nested worlds")

    # top-level controls in streamlit
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
    with col1:
        base_speed = st.slider("base speed", 1, 30, 8, key="speed_slider")
    with col2:
        mode = st.selectbox("mode", ["arcade", "explorer", "zen"], index=0, help="arcade=score/timer /// explorer=free roam /// zen=chill")
    with col3:
        photosafe = st.toggle("photosensitive safe", value=False, help="reduce flashing / strong contrast")
    with col4:
        sbs_default = st.toggle("start in VR SBS", value=False, help="side-by-side view without WebXR")

    # helpers mapped into js
    safe_flag = "true" if photosafe else "false"
    mode_js = mode
    sbs_flag = "true" if sbs_default else "false"

    three_html = f"""
<div id="gate" style="position:fixed;inset:0;background:black;color:white;display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:3">
  <div style="max-width:800px;padding:24px;text-align:center;line-height:1.4">
    <h2 style="margin:0 0 8px 0;font-weight:600">warning</h2>
    <p>this simulation can include motion, flashing colors, rapid movement</p>
    <p>if you are sensitive / photosensitive please enable photosafe mode or close this page</p>
    <p style="opacity:.8">no medical or safety guarantees / use at your own discretion</p>
    <p style="margin-top:12px">starting in <span id="cd">5</span> seconds...</p>
    <button id="skip" style="margin-top:12px;padding:8px 12px;background:#fff;border:0;border-radius:8px;cursor:pointer">skip</button>
  </div>
</div>

<div id="hud" style="position:fixed;inset:0;pointer-events:none;z-index:2">
  <div style="position:absolute;top:10px;left:10px;color:white;font:600 14px/1.2 ui-sans-serif,system-ui">
    <div>mode: <span id="hud-mode">{mode_js}</span> / world: <span id="hud-world">vortex</span></div>
    <div>score: <span id="hud-score">0</span> / best: <span id="hud-best">0</span> / time: <span id="hud-time">00:00</span></div>
  </div>
  <div style="position:absolute;bottom:10px;left:10px;color:#ccc;font:12px/1.2 ui-sans-serif,system-ui;max-width:540px">
    controls: WASD move /// arrows tilt /// P pause /// R reset /// V vr sbs /// I help
  </div>
  <div id="help" style="display:none;position:absolute;right:10px;top:10px;background:rgba(0,0,0,.6);color:white;border-radius:12px;padding:12px;max-width:360px;font:12px/1.4 ui-sans-serif,system-ui">
    collect orbs in arcade /// portals shift you between 3 worlds: vortex / helix / lissajous<br/>
    tilt control on mobile if allowed /// photosafe reduces flashing / high contrast<br/>
    vr sbs duplicates the view side-by-side for simple headsets
  </div>
</div>

<div id="root" style="position:relative;width:100%;height:80vh;background:black"></div>

<div id="btns" style="position:fixed;right:12px;bottom:12px;z-index:2;display:flex;gap:8px">
  <button id="btn-pause" style="pointer-events:auto;padding:8px 10px;border:0;border-radius:10px;background:#111;color:#fff;opacity:.9;cursor:pointer">pause</button>
  <button id="btn-reset" style="pointer-events:auto;padding:8px 10px;border:0;border-radius:10px;background:#111;color:#fff;opacity:.9;cursor:pointer">reset</button>
  <button id="btn-vr" style="pointer-events:auto;padding:8px 10px;border:0;border-radius:10px;background:#111;color:#fff;opacity:.9;cursor:pointer">vr sbs</button>
  <button id="btn-help" style="pointer-events:auto;padding:8px 10px;border:0;border-radius:10px;background:#111;color:#fff;opacity:.9;cursor:pointer">help</button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>

<script>
(() => {{
  // gate / countdown
  const cdEl = document.getElementById('cd');
  const gate = document.getElementById('gate');
  const skip = document.getElementById('skip');
  let tLeft = 5; let timer = setInterval(() => {{
    tLeft -= 1; cdEl.textContent = String(tLeft);
    if (tLeft <= 0) {{ clearInterval(timer); openGate(); }}
  }}, 1000);
  skip.onclick = () => {{ clearInterval(timer); openGate(); }};
  function openGate() {{
    gate.style.display = 'none';
    init();
  }}

  // ui refs
  const root = document.getElementById('root');
  const hudMode = document.getElementById('hud-mode');
  const hudWorld = document.getElementById('hud-world');
  const hudScore = document.getElementById('hud-score');
  const hudBest = document.getElementById('hud-best');
  const hudTime = document.getElementById('hud-time');
  const help = document.getElementById('help');

  // persisted best score
  const BEST_KEY = 'mv_best';
  let best = Number(localStorage.getItem(BEST_KEY) || 0);
  hudBest.textContent = best;

  // flags & config
  let photosafe = {safe_flag};
  let sbsVR = {sbs_flag};
  const mode = "{mode_js}";
  hudMode.textContent = mode;

  // keyboard / mobile tilt
  const keys = new Set();
  window.addEventListener('keydown', e => keys.add(e.key.toLowerCase()));
  window.addEventListener('keyup', e => keys.delete(e.key.toLowerCase()));
  let tiltX = 0, tiltY = 0;
  if (window.DeviceOrientationEvent && typeof window.DeviceOrientationEvent.requestPermission === 'function') {{
    // iOS permission flow on first tap
    root.addEventListener('click', async () => {{
      try {{ const p = await window.DeviceOrientationEvent.requestPermission(); if (p === 'granted') attachTilt(); }} catch(e) {{}}
    }}, {{ once: true }});
  }} else if (window.DeviceOrientationEvent) {{
    attachTilt();
  }}
  function attachTilt() {{
    window.addEventListener('deviceorientation', (ev) => {{
      tiltX = (ev.gamma || 0) / 90;  // left/right
      tiltY = (ev.beta  || 0) / 90;  // up/down
    }});
  }}

  // scene basics
  let renderer, scene, camera, clock;
  let leftCam, rightCam; // for sbs
  let paused = false;
  let timeSec = 0;
  let score = 0;

  // world state
  const WORLDS = ['vortex', 'helix', 'lissajous'];
  let worldIdx = 0;
  let tunnel, innerLayers = [];
  let collectibles = [];
  let lights = [];
  let grid;

  // runtime
  let baseSpeed = {base_speed}; // from streamlit at render
  let travelSpeed = baseSpeed;
  const MODE_MULT = mode === 'arcade' ? 1.0 : (mode === 'explorer' ? 0.8 : 0.5);

  function init() {{
    // renderer
    renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(root.clientWidth, root.clientHeight);
    renderer.setScissorTest(true);
    root.appendChild(renderer.domElement);

    // scene + camera
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, root.clientWidth / root.clientHeight, 0.1, 2500);
    camera.position.set(0, 0, 0);
    scene.add(camera);

    // sbs cameras
    leftCam = camera;
    rightCam = camera.clone(); // same params
    scene.add(rightCam);

    // fog tuned by photosafe
    if (photosafe) {{
      scene.fog = new THREE.Fog(0x000000, 400, 2000);
    }} else {{
      scene.fog = new THREE.FogExp2(0x000000, 0.0012);
    }}

    // lights
    for (let i = 0; i < 8; i++) {{
      const light = new THREE.PointLight(0xffffff, 2, 600);
      light.position.set(Math.sin(i)*220, Math.cos(i)*220, -i*120);
      scene.add(light);
      lights.push(light);
    }}

    // grid
    grid = new THREE.GridHelper(1200, 60, 0x0088ff, 0x004477);
    grid.rotation.x = Math.PI / 2;
    grid.position.z = -1200;
    scene.add(grid);

    // start world
    buildWorld(WORLDS[worldIdx]);
    spawnCollectibles(60);

    clock = new THREE.Clock();
    animate();
  }}

  function clearWorld() {{
    if (tunnel) scene.remove(tunnel);
    innerLayers.forEach(l => scene.remove(l));
    innerLayers = [];
    collectibles.forEach(c => scene.remove(c));
    collectibles = [];
  }}

  function buildWorld(name) {{
    clearWorld();
    hudWorld.textContent = name;
    // base params
    const segments = 220;
    const rings = 220;
    const radius = 48;
    const tubeRadius = 18;

    const path = new THREE.CatmullRomCurve3(
      Array.from({{length: rings}}, (_, i) => {{
        const t = i / rings;
        const p = new THREE.Vector3();
        if (name === 'vortex') {{
          const a = t * Math.PI * 4.0;
          p.set(Math.sin(a) * radius, Math.cos(a*1.2) * radius * 0.9, -i * 10);
        }} else if (name === 'helix') {{
          const a = t * Math.PI * 6.0;
          p.set(Math.sin(a*0.7) * radius*1.2, Math.cos(a*0.7) * radius*1.2, -i * 10);
        }} else {{
          // lissajous tube
          const a = t * Math.PI * 5.0;
          p.set(
            Math.sin(a*1.0) * radius * (1 + 0.25*Math.sin(a*2.0)),
            Math.sin(a*1.7 + Math.PI/3) * radius * (1 + 0.2*Math.cos(a*2.3)),
            -i * 10
          );
        }}
        return p;
      }})
    );

    const geom = new THREE.TubeGeometry(path, segments, tubeRadius, 32, false);
    const mat = new THREE.MeshBasicMaterial({{
      color: 0xffffff, wireframe: true, transparent: true, opacity: 0.85, side: THREE.DoubleSide
    }});
    tunnel = new THREE.Mesh(geom, mat);
    scene.add(tunnel);

    // layered inner tunnels
    for (let j = 1; j <= 4; j++) {{
      const innerPath = new THREE.CatmullRomCurve3(
        Array.from({{length: rings}}, (_, i) => {{
          const t = i / rings;
          const a = t * Math.PI * (4 + j);
          const v = new THREE.Vector3(
            Math.sin(a) * (radius/(j+1)) * (1 + Math.sin(a*(2+j))*0.3),
            Math.cos(a) * (radius/(j+1)) * (1 + Math.cos(a*(3+j))*0.3),
            -i * 10
          );
          return v;
        }})
      );
      const g = new THREE.TubeGeometry(innerPath, segments, tubeRadius/(j+1), 24, false);
      const m = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.6 - j*0.1, side: THREE.DoubleSide }});
      const mesh = new THREE.Mesh(g, m);
      scene.add(mesh);
      innerLayers.push(mesh);
    }}

    // portal rings
    const ringGeo = new THREE.RingGeometry(24, 26, 64);
    const ringMat = new THREE.MeshBasicMaterial({{ color: 0x66ccff, side: THREE.DoubleSide, transparent:true, opacity: 0.7 }});
    for (let r = 0; r < 5; r++) {{
      const z = -400 - r * 300;
      const ring = new THREE.Mesh(ringGeo, ringMat.clone());
      ring.position.set(0, 0, z);
      ring.rotation.y = Math.PI/2;
      ring.userData.portal = true;
      scene.add(ring);
      innerLayers.push(ring);
    }}
  }}

  function spawnCollectibles(n) {{
    const geo = new THREE.SphereGeometry(5, 16, 16);
    for (let k = 0; k < n; k++) {{
      const material = new THREE.MeshBasicMaterial({{ color: Math.random()*0xffffff }});
      const m = new THREE.Mesh(geo, material);
      m.position.set(
        (Math.random()-0.5) * 40,
        (Math.random()-0.5) * 40,
        -100 - Math.random()*1800
      );
      scene.add(m);
      collectibles.push(m);
    }}
  }}

  function nextWorld() {{
    worldIdx = (worldIdx + 1) % WORLDS.length;
    buildWorld(WORLDS[worldIdx]);
    spawnCollectibles(40);
  }}

  // ui buttons
  document.getElementById('btn-pause').onclick = () => {{ paused = !paused; }};
  document.getElementById('btn-reset').onclick = resetGame;
  document.getElementById('btn-vr').onclick = () => {{ sbsVR = !sbsVR; }};
  document.getElementById('btn-help').onclick = () => {{ help.style.display = help.style.display === 'none' ? 'block' : 'none'; }};

  window.addEventListener('keydown', e => {{
    const k = e.key.toLowerCase();
    if (k === 'p') paused = !paused;
    if (k === 'r') resetGame();
    if (k === 'v') sbsVR = !sbsVR;
    if (k === 'i') help.style.display = help.style.display === 'none' ? 'block' : 'none';
  }});

  function resetGame() {{
    score = 0; timeSec = 0;
    worldIdx = 0; buildWorld(WORLDS[worldIdx]); spawnCollectibles(60);
  }}

  // timing / scoring
  function updateTime(dt) {{
    timeSec += dt;
    const m = Math.floor(timeSec/60).toString().padStart(2,'0');
    const s = Math.floor(timeSec%60).toString().padStart(2,'0');
    hudTime.textContent = m+":" + s;
  }}

  function addScore(v) {{
    score += v;
    hudScore.textContent = score;
    if (score > best) {{
      best = score;
      hudBest.textContent = best;
      localStorage.setItem(BEST_KEY, String(best));
    }}
  }}

  // main loop
  function animate() {{
    requestAnimationFrame(animate);
    if (!clock) return;
    const dt = Math.min(clock.getDelta(), 0.05);
    if (paused) return;

    // speed
    travelSpeed = baseSpeed * MODE_MULT;

    // hue / motion styling
    const t = performance.now() * 0.001;
    const hueBase = photosafe ? 0.58 + 0.02*Math.sin(t*0.5) : (Math.sin(t*2.8)*0.5 + 0.5);
    const sat = photosafe ? 0.6 : 1.0;
    const li  = photosafe ? 0.5 : 0.5;

    tunnel.material.color.setHSL(hueBase, sat, li);
    innerLayers.forEach((wh, idx) => {{
      if (!wh.material || !wh.material.color) return;
      wh.material.color.setHSL((hueBase + idx*0.12) % 1, sat, li);
      wh.rotation.z += 0.008 + idx*0.004;
      if (wh.userData.portal) {{
        wh.rotation.z += 0.01;
        wh.material.opacity = 0.6 + 0.2*Math.sin(t*2.0 + idx);
      }}
    }});

    // lights drift
    lights.forEach((L, i) => {{
      L.position.x = Math.sin(t*(1.8+i*0.2)) * 220;
      L.position.y = Math.cos(t*(1.2+i*0.3)) * 220;
      L.position.z -= travelSpeed;
      if (L.position.z < -2200) L.position.z += 2200;
      if (!photosafe) L.color.setHSL((hueBase + i*0.1)%1, 1, 0.5);
    }});

    // grid rush
    grid.position.z += travelSpeed;
    if (grid.position.z > 0) grid.position.z -= 1200;

    // camera move: WASD + arrows + tilt
    const moveX = (keys.has('a') ? -1 : 0) + (keys.has('d') ? 1 : 0) + (keys.has('arrowleft') ? -0.7 : 0) + (keys.has('arrowright') ? 0.7 : 0);
    const moveY = (keys.has('w') ? 1 : 0) + (keys.has('s') ? -1 : 0) + (keys.has('arrowup') ? 0.7 : 0) + (keys.has('arrowdown') ? -0.7 : 0);
    camera.position.x += (moveX + tiltX*1.2) * 1.2;
    camera.position.y += (moveY + tiltY*1.2) * 1.2;

    // forward
    camera.position.z -= travelSpeed;
    if (camera.position.z < -2400) camera.position.z += 2400;

    // collectibles
    for (let i = collectibles.length - 1; i >= 0; i--) {{
      const c = collectibles[i];
      c.position.z += travelSpeed * 0.9;
      if (c.position.z > 50) {{
        c.position.z -= 2200;
        c.position.x = (Math.random()-0.5)*40;
        c.position.y = (Math.random()-0.5)*40;
      }}
      const dx = c.position.x - camera.position.x;
      const dy = c.position.y - camera.position.y;
      const dz = c.position.z - camera.position.z;
      if (dx*dx + dy*dy + dz*dz < 100) {{
        scene.remove(c);
        collectibles.splice(i,1);
        addScore(10);
        const nc = new THREE.Mesh(c.geometry, new THREE.MeshBasicMaterial({{ color: Math.random()*0xffffff }}));
        nc.position.set((Math.random()-0.5)*40, (Math.random()-0.5)*40, -2000);
        scene.add(nc);
        collectibles.push(nc);
      }}
    }}

    // portal trigger
    for (const obj of innerLayers) {{
      if (!obj.userData.portal) continue;
      const dz = Math.abs(obj.position.z - camera.position.z);
      if (dz < 5) {{
        nextWorld();
        addScore(50);
        break;
      }}
    }}

    // time
    updateTime(dt);

    // render either single view or sbs
    if (sbsVR) {{
      const w = root.clientWidth; const h = root.clientHeight;
      renderer.setViewport(0, 0, w/2, h);
      renderer.setScissor(0, 0, w/2, h);
      renderer.render(scene, leftCam);

      renderer.setViewport(w/2, 0, w/2, h);
      renderer.setScissor(w/2, 0, w/2, h);
      renderer.render(scene, rightCam);
    }} else {{
      renderer.setViewport(0, 0, root.clientWidth, root.clientHeight);
      renderer.setScissor(0, 0, root.clientWidth, root.clientHeight);
      renderer.render(scene, camera);
    }}
  }}

  // responsive
  window.addEventListener('resize', () => {{
    if (!renderer || !camera) return;
    renderer.setSize(root.clientWidth, root.clientHeight);
    camera.aspect = root.clientWidth / root.clientHeight;
    camera.updateProjectionMatrix();
  }});

  // start after gate closes
}})();
</script>
"""
    st.components.v1.html(three_html, height=700)

# some loaders also look for `render`
render = main

if __name__ == "__main__":
    main()
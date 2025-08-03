# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter the Multi-Metaverse")
    st.write("Embark on an immersive journey through mathematical wormholes to explore multiple metaverses. Navigate, collect artifacts, avoid anomalies, and achieve resonance to transcend!")

    # Slider for speed control
    speed = st.slider("Travel Speed", min_value=1, max_value=20, value=5, key="speed_slider")

    # Checkbox for sound
    enable_sound = st.checkbox("Enable Sound Effects", value=True)

    # Embed epilepsy warning and enhanced interactive simulation
    three_js_code = f"""
    <div id="warning" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px; text-align: center; z-index: 2;">
        <p>WARNING: This simulation contains flashing lights, rapid color shifts, and intense movements that may trigger epilepsy or seizures.</p>
        <p>If you have epilepsy or are sensitive, please close this page.</p>
        <p>No medical advice provided. Starting in <span id="countdown">5</span> seconds...</p>
    </div>
    <div id="threejs-container" style="width:100%; height:800px; background: black; position: relative;"></div>
    <div id="hud" style="position: absolute; top: 10px; left: 10px; color: white; font-size: 20px; z-index: 2;">
        <div>Score: <span id="score">0</span></div>
        <div>Level: <span id="level">1</span></div>
        <div>Resonance: <span id="resonance">0%</span></div>
    </div>
    <button id="fullscreen-btn" style="position: absolute; bottom: 10px; left: 10px; z-index: 2;">Go Fullscreen</button>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Epilepsy warning timer
        let timeLeft = 5;
        const countdown = document.getElementById('countdown');
        const warning = document.getElementById('warning');
        const timer = setInterval(() => {{
            timeLeft--;
            countdown.textContent = timeLeft;
            if (timeLeft <= 0) {{
                clearInterval(timer);
                warning.style.display = 'none';
                initThreeJS();
            }}
        }}, 1000);

        function initThreeJS() {{
            const container = document.getElementById('threejs-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 3000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            scene.background = new THREE.Color(0x000000);

            // Wormhole parameters
            let segments = 256;
            let rings = 300;  // Longer tunnel
            let radius = 60;
            let tubeRadius = 25;

            // Function to generate wormhole path (procedural for multi-metaverse)
            function generatePath(level) {{
                return new THREE.CatmullRomCurve3(
                    Array.from({{length: rings}}, (_, i) => {{
                        const t = i / rings * Math.PI * (4 + level);
                        return new THREE.Vector3(
                            Math.sin(t) * radius * (1 + Math.sin(t * (2 + level * 0.5)) * 0.2),
                            Math.cos(t) * radius * (1 + Math.cos(t * (3 + level * 0.5)) * 0.2),
                            -i * 8  // Adjusted spacing
                        );
                    }})
                );
            }}

            let currentLevel = 1;
            let path = generatePath(currentLevel);
            const geometry = new THREE.TubeGeometry(path, segments, tubeRadius, 32, false);
            const material = new THREE.MeshBasicMaterial({{
                color: 0xffffff,
                wireframe: true,
                transparent: true,
                opacity: 0.8,
                side: THREE.DoubleSide
            }});
            const wormhole = new THREE.Mesh(geometry, material);
            scene.add(wormhole);

            // Inner wormholes
            const innerWormholes = [];
            for (let j = 1; j < 5; j++) {{
                const innerPath = generatePath(currentLevel + j);  // Vary per level
                const innerGeometry = new THREE.TubeGeometry(innerPath, segments, tubeRadius / (j + 1), 32, false);
                const innerMaterial = new THREE.MeshBasicMaterial({{
                    color: 0xffffff,
                    wireframe: true,
                    transparent: true,
                    opacity: 0.6 - j * 0.1,
                    side: THREE.DoubleSide
                }});
                const innerWormhole = new THREE.Mesh(innerGeometry, innerMaterial);
                scene.add(innerWormhole);
                innerWormholes.push(innerWormhole);
            }}

            // Grid
            const gridSize = 1000;
            const gridDivisions = 50;
            const grid = new THREE.GridHelper(gridSize, gridDivisions, 0x00ff00, 0x008800);
            grid.rotation.x = Math.PI / 2;
            grid.position.z = -1500;
            scene.add(grid);

            // Lights
            const lights = [];
            for (let l = 0; l = 10; l++) {{  // More lights
                const light = new THREE.PointLight(0xffffff, 2, 600);
                light.position.set(Math.sin(l) * 250, Math.cos(l) * 250, -l * 120);
                scene.add(light);
                lights.push(light);
            }}

            // Collectibles
            const collectibles = [];
            const collectibleGeometry = new THREE.SphereGeometry(5, 32, 32);
            function spawnCollectible(ahead = 0) {{
                const collectibleMaterial = new THREE.MeshBasicMaterial({{ color: Math.random() * 0xffffff }});
                const collectible = new THREE.Mesh(collectibleGeometry, collectibleMaterial);
                const t = Math.random() * rings;
                const pos = path.getPointAt(t / rings);
                collectible.position.set(
                    pos.x + (Math.random() - 0.5) * 30,
                    pos.y + (Math.random() - 0.5) * 30,
                    pos.z - ahead
                );
                scene.add(collectible);
                collectibles.push(collectible);
            }}
            for (let k = 0; k < 100; k++) spawnCollectible();  // More collectibles

            // Obstacles (anomalies to avoid)
            const obstacles = [];
            const obstacleGeometry = new THREE.SphereGeometry(8, 32, 32);
            function spawnObstacle(ahead = 0) {{
                const obstacleMaterial = new THREE.MeshBasicMaterial({{ color: 0xff0000 }});
                const obstacle = new THREE.Mesh(obstacleGeometry, obstacleMaterial);
                const t = Math.random() * rings;
                const pos = path.getPointAt(t / rings);
                obstacle.position.set(
                    pos.x + (Math.random() - 0.5) * 30,
                    pos.y + (Math.random() - 0.5) * 30,
                    pos.z - ahead
                );
                scene.add(obstacle);
                obstacles.push(obstacle);
            }}
            for (let k = 0; k < 50; k++) spawnObstacle();

            // Fog
            scene.fog = new THREE.FogExp2(0x000000, 0.0008);

            camera.position.set(0, 0, 0);

            let time = 0;
            let score = 0;
            let resonance = 0;
            const scoreSpan = document.getElementById('score');
            const levelSpan = document.getElementById('level');
            const resonanceSpan = document.getElementById('resonance');

            // Controls
            let tiltX = 0, tiltY = 0;
            if (window.DeviceOrientationEvent) {{
                window.addEventListener('deviceorientation', (event) => {{
                    tiltX = event.gamma / 90 * 30;
                    tiltY = event.beta / 90 * 30;
                }});
            }}

            // Keyboard controls
            const keys = {{}};
            window.addEventListener('keydown', (e) => keys[e.key] = true);
            window.addEventListener('keyup', (e) => keys[e.key] = false);

            let travelSpeed = {speed};

            // Sound effects (using Web Audio API for simple beeps)
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playSound(frequency, duration) {{
                if (!{enable_sound ? 'true' : 'false'}) return;
                const oscillator = audioCtx.createOscillator();
                oscillator.type = 'sine';
                oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
                oscillator.connect(audioCtx.destination);
                oscillator.start();
                setTimeout(() => oscillator.stop(), duration);
            }}

            // Fullscreen button
            document.getElementById('fullscreen-btn').addEventListener('click', () => {{
                if (container.requestFullscreen) container.requestFullscreen();
                else if (container.webkitRequestFullscreen) container.webkitRequestFullscreen();
                else if (container.msRequestFullscreen) container.msRequestFullscreen();
            }});

            function animate() {{
                requestAnimationFrame(animate);
                time += 0.04;

                // Color shifts
                const hue = Math.sin(time * 4) * 0.5 + 0.5;
                wormhole.material.color.setHSL(hue, 1, 0.5);
                innerWormholes.forEach((wh, idx) => {{
                    wh.material.color.setHSL((hue + idx * 0.15 + currentLevel * 0.1) % 1, 1, 0.5);
                }});

                // Twist
                wormhole.rotation.z += 0.015 * Math.sin(time);
                innerWormholes.forEach((wh, idx) => {{
                    wh.rotation.z += (0.015 + idx * 0.008) * Math.cos(time + idx);
                }});

                // Movement
                let dx = 0, dy = 0;
                if (keys['ArrowLeft'] || keys['a']) dx -= 1;
                if (keys['ArrowRight'] || keys['d']) dx += 1;
                if (keys['ArrowUp'] || keys['w']) dy += 1;
                if (keys['ArrowDown'] || keys['s']) dy -= 1;
                camera.position.x += (tiltX + dx * 5) * 0.2;
                camera.position.y += (tiltY + dy * 5) * 0.2;
                camera.position.z -= travelSpeed;

                // Loop and level up
                if (camera.position.z < -2500) {{
                    camera.position.z += 2500;
                    currentLevel++;
                    levelSpan.textContent = currentLevel;
                    // Regenerate wormhole for new metaverse
                    scene.remove(wormhole);
                    innerWormholes.forEach(wh => scene.remove(wh));
                    innerWormholes.length = 0;
                    path = generatePath(currentLevel);
                    wormhole.geometry = new THREE.TubeGeometry(path, segments, tubeRadius, 32, false);
                    scene.add(wormhole);
                    for (let j = 1; j < 5; j++) {{
                        const innerPath = generatePath(currentLevel + j);
                        const innerGeometry = new THREE.TubeGeometry(innerPath, segments, tubeRadius / (j + 1), 32, false);
                        const innerMaterial = new THREE.MeshBasicMaterial({{
                            color: 0xffffff,
                            wireframe: true,
                            transparent: true,
                            opacity: 0.6 - j * 0.1,
                            side: THREE.DoubleSide
                        }});
                        const innerWormhole = new THREE.Mesh(innerGeometry, innerMaterial);
                        scene.add(innerWormhole);
                        innerWormholes.push(innerWormhole);
                    }}
                    // Respawn items and obstacles ahead
                    collectibles.forEach(col => col.position.z += 2500);
                    obstacles.forEach(obs => obs.position.z += 2500);
                }}

                // Collectibles check
                for (let i = collectibles.length - 1; i >= 0; i--) {{
                    const col = collectibles[i];
                    const dist = camera.position.distanceTo(col.position);
                    if (dist < 12) {{
                        scene.remove(col);
                        collectibles.splice(i, 1);
                        score += 10 * currentLevel;
                        resonance = Math.min(100, resonance + 5);
                        scoreSpan.textContent = score;
                        resonanceSpan.textContent = `${{resonance}}%`;
                        playSound(440, 200);  // Collect sound
                        spawnCollectible(2500);  // Respawn ahead
                    }}
                }}

                // Obstacles check
                for (let i = obstacles.length - 1; i >= 0; i--) {{
                    const obs = obstacles[i];
                    const dist = camera.position.distanceTo(obs.position);
                    if (dist < 12) {{
                        scene.remove(obs);
                        obstacles.splice(i, 1);
                        score = Math.max(0, score - 20 * currentLevel);
                        resonance = Math.max(0, resonance - 10);
                        scoreSpan.textContent = score;
                        resonanceSpan.textContent = `${{resonance}}%`;
                        playSound(220, 300);  // Hit sound
                        spawnObstacle(2500);
                    }}
                }}

                // Lights movement
                lights.forEach((light, idx) => {{
                    light.position.x = Math.sin(time * (2 + idx) + currentLevel) * 250;
                    light.position.y = Math.cos(time * (3 + idx) + currentLevel) * 250;
                    light.position.z -= travelSpeed;
                    if (light.position.z < -2500) light.position.z += 2500;
                    light.color.setHSL(Math.sin(time * 4 + idx) * 0.5 + 0.5, 1, 0.5);
                }});

                // Grid movement
                grid.position.z += travelSpeed;
                if (grid.position.z > 0) grid.position.z -= 3000;

                // Check for transcendence
                if (resonance >= 100) {{
                    // Could redirect or show message
                    alert("Resonance achieved! Welcome to the Multi-Metaverse!");
                    resonance = 0;
                    resonanceSpan.textContent = '0%';
                }}

                renderer.render(scene, camera);
            }}
            animate();
        }}
    </script>
    """
    st.components.v1.html(three_js_code, height=800)

    # VR button
    st.markdown("""
        <style>
            .vr-button {position: fixed; bottom: 80px; right: 20px; z-index: 101;}
        </style>
    """, unsafe_allow_html=True)
    st.button("VR SBS Mode", key="vr_sbs", help="Enter Side-by-Side VR mode (coming soon)")

if __name__ == "__main__":
    main()
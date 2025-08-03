# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter Metaverse")
    st.write("Journey through a mathematical wireframe wormhole – interactive, game-like adventure!")

    # Slider for desktop speed control
    speed = st.slider("Wormhole Travel Speed", min_value=1, max_value=20, value=5, key="speed_slider")

    # Embed epilepsy warning and interactive mathematical wireframe wormhole simulation
    three_js_code = f"""
    <div id="warning" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px; text-align: center; z-index: 2;">
        <p>WARNING: This simulation contains flashing lights, rapid color shifts, and intense movements that may trigger epilepsy or seizures.</p>
        <p>If you have epilepsy or are sensitive, please close this page.</p>
        <p>No medical advice provided. Starting in <span id="countdown">5</span> seconds...</p>
    </div>
    <div id="threejs-container" style="width:100%; height:800px; background: black; position: relative;"></div>
    <div id="score-overlay" style="position: absolute; top: 10px; right: 10px; color: white; font-size: 24px; z-index: 2;">Score: 0</div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Epilepsy warning timer (5 seconds)
        let timeLeft = 5;
        const countdown = document.getElementById('countdown');
        const warning = document.getElementById('warning');
        const timer = setInterval(() => {{
            timeLeft--;
            countdown.textContent = timeLeft;
            if (timeLeft <= 0) {{
                clearInterval(timer);
                warning.style.display = 'none';
                initThreeJS();  // Start the simulation after warning
            }}
        }}, 1000);

        function initThreeJS() {{
            const container = document.getElementById('threejs-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 2000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            scene.background = new THREE.Color(0x000000); // Black void

            // Mathematical wireframe wormhole: Parametric tube with twisting, sucking effect
            const segments = 256;  // High resolution for smooth math curves
            const rings = 200;     // More rings for deeper tunnel
            const radius = 50;     // Base radius
            const tubeRadius = 20; // Tube thickness

            // Create a parametric curve for the wormhole (sinusoidal twist for math feel)
            const path = new THREE.CatmullRomCurve3(
                Array.from({{length: rings}}, (_, i) => {{
                    const t = i / rings * Math.PI * 4;  // Multi-twist
                    return new THREE.Vector3(
                        Math.sin(t) * radius * (1 + Math.sin(t * 2) * 0.2),  // X: sinusoidal variation
                        Math.cos(t) * radius * (1 + Math.cos(t * 3) * 0.2),  // Y: complex math pattern
                        -i * 10  // Z: closer spacing for longer tunnel
                    );
                }})
            );

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

            // Add multiple layered wormholes for crazier, nested math structures
            const innerWormholes = [];
            for (let j = 1; j < 5; j++) {{  // 4 inner layers
                const innerPath = new THREE.CatmullRomCurve3(
                    Array.from({{length: rings}}, (_, i) => {{
                        const t = i / rings * Math.PI * (4 + j);  // Varying twists
                        return new THREE.Vector3(
                            Math.sin(t) * (radius / (j + 1)) * (1 + Math.sin(t * (2 + j)) * 0.3),
                            Math.cos(t) * (radius / (j + 1)) * (1 + Math.cos(t * (3 + j)) * 0.3),
                            -i * 10
                        );
                    }})
                );
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

            // Add mathematical grid planes for structured, game-like environment
            const gridSize = 1000;
            const gridDivisions = 50;
            const grid = new THREE.GridHelper(gridSize, gridDivisions, 0x00ff00, 0x008800);
            grid.rotation.x = Math.PI / 2;  // Lay flat
            grid.position.z = -1000;  // Far in depth
            scene.add(grid);

            // Point lights for dynamic, colorful lighting
            const lights = [];
            for (let l = 0; l < 8; l++) {{
                const light = new THREE.PointLight(0xffffff, 2, 500);
                light.position.set(
                    Math.sin(l) * 200,
                    Math.cos(l) * 200,
                    -l * 100
                );
                scene.add(light);
                lights.push(light);
            }}

            // Collectibles: Random glowing spheres to collect
            const collectibles = [];
            const collectibleGeometry = new THREE.SphereGeometry(5, 32, 32);
            for (let k = 0; k < 50; k++) {{  // 50 collectibles
                const collectibleMaterial = new THREE.MeshBasicMaterial({{ color: Math.random() * 0xffffff }});
                const collectible = new THREE.Mesh(collectibleGeometry, collectibleMaterial);
                // Place along the wormhole path with some offset
                const t = Math.random() * rings;
                const pos = path.getPointAt(t / rings);
                collectible.position.set(
                    pos.x + (Math.random() - 0.5) * 20,
                    pos.y + (Math.random() - 0.5) * 20,
                    pos.z
                );
                scene.add(collectible);
                collectibles.push(collectible);
            }}

            // Fog for depth and mystery
            scene.fog = new THREE.FogExp2(0x000000, 0.001);

            camera.position.set(0, 0, 0);  // Start at entrance

            let time = 0;  // For animations
            let score = 0; // Game score
            const scoreOverlay = document.getElementById('score-overlay');

            // Interactivity: Accelerometer for mobile tilt control
            let tiltX = 0, tiltY = 0;
            if (window.DeviceOrientationEvent) {{
                window.addEventListener('deviceorientation', (event) => {{
                    tiltX = event.gamma / 90 * 20;  // Left-right tilt
                    tiltY = event.beta / 90 * 20;   // Up-down tilt
                }});
            }}

            // Get speed from Streamlit slider (poll for changes)
            let travelSpeed = {speed};  // Initial speed
            setInterval(() => {{
                // Note: In practice, for real-time, might need better integration, but for demo, assume fixed or manual refresh
            }}, 1000);

            function animate() {{
                requestAnimationFrame(animate);
                time += 0.05;  // Fast time step for craziness

                // Epileptic color shifts: Cycle through hues rapidly
                const hue = Math.sin(time * 5) * 0.5 + 0.5;  // Fast sin for flashing
                wormhole.material.color.setHSL(hue, 1, 0.5);
                innerWormholes.forEach((wh, idx) => {{
                    wh.material.color.setHSL((hue + idx * 0.2) % 1, 1, 0.5);
                }});

                // Twist and pulse the wormhole mathematically
                wormhole.rotation.z += 0.02 * Math.sin(time);  // Oscillating rotation
                innerWormholes.forEach((wh, idx) => {{
                    wh.rotation.z += (0.02 + idx * 0.01) * Math.cos(time + idx);
                }});

                // Moving through wormhole: Pull camera deeper, with tilt control
                camera.position.z -= travelSpeed;  // Base forward movement
                camera.position.x += tiltX * 0.1;  // Tilt control
                camera.position.y += tiltY * 0.1;
                if (camera.position.z < -2000) {{
                    camera.position.z += 2000;  // Loop the tunnel for endless journey
                    // Respawn collectibles if needed
                }}

                // Check for collecting items
                collectibles.forEach((col, idx) => {{
                    const dist = camera.position.distanceTo(col.position);
                    if (dist < 10) {{  // Collection proximity
                        scene.remove(col);
                        collectibles.splice(idx, 1);
                        score += 10;
                        scoreOverlay.textContent = `Score: ${{score}}`;
                        // Respawn a new collectible
                        const newCol = new THREE.Mesh(collectibleGeometry, new THREE.MeshBasicMaterial({{ color: Math.random() * 0xffffff }}));
                        const t = Math.random() * rings;
                        const pos = path.getPointAt(t / rings);
                        newCol.position.set(
                            pos.x + (Math.random() - 0.5) * 20,
                            pos.y + (Math.random() - 0.5) * 20,
                            pos.z - 2000  // Ahead in the tunnel
                        );
                        scene.add(newCol);
                        collectibles.push(newCol);
                    }}
                }});

                // Move lights along mathematical paths for trippy shadows
                lights.forEach((light, idx) => {{
                    light.position.x = Math.sin(time * (2 + idx)) * 200;
                    light.position.y = Math.cos(time * (3 + idx)) * 200;
                    light.position.z -= travelSpeed;  // Pull lights too
                    if (light.position.z < -2000) light.position.z += 2000;
                    light.color.setHSL(Math.sin(time * 5 + idx) * 0.5 + 0.5, 1, 0.5);  // Color flash
                }});

                // Grid movement for game-like rush
                grid.position.z += travelSpeed;  // Grid rushes past you
                if (grid.position.z > 0) grid.position.z -= 2000;

                renderer.render(scene, camera);
            }}
            animate();
        }}
    </script>
    """
    st.components.v1.html(three_js_code, height=800)

    # VR SBS button (polished, bottom right)
    st.markdown("""
        <style>
            .vr-button {position: fixed; bottom: 80px; right: 20px; z-index: 101;}
        </style>
    """, unsafe_allow_html=True)
    st.button("VR SBS Mode", key="vr_sbs", help="Enter Side-by-Side VR mode (coming soon)")

if __name__ == "__main__":
    main()
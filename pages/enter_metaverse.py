# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter Metaverse")
    st.write("Sucked into a mathematical wireframe wormhole – trippy, structured chaos awaits!")

    # Embed epilepsy warning and mathematical wireframe wormhole simulation
    three_js_code = """
    <div id="warning" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px; text-align: center; z-index: 2;">
        <p>WARNING: This simulation contains flashing lights, rapid color shifts, and intense movements that may trigger epilepsy or seizures.</p>
        <p>If you have epilepsy or are sensitive, please close this page.</p>
        <p>No medical advice provided. Starting in <span id="countdown">5</span> seconds...</p>
    </div>
    <div id="threejs-container" style="width:100%; height:800px; background: black; position: relative;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Epilepsy warning timer (5 seconds)
        let timeLeft = 5;
        const countdown = document.getElementById('countdown');
        const warning = document.getElementById('warning');
        const timer = setInterval(() => {
            timeLeft--;
            countdown.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timer);
                warning.style.display = 'none';
                initThreeJS();  // Start the simulation after warning
            }
        }, 1000);

        function initThreeJS() {
            const container = document.getElementById('threejs-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 2000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            scene.background = new THREE.Color(0x000000); // Black void

            // Mathematical wireframe wormhole: Parametric tube with twisting, sucking effect
            const segments = 256;  // High resolution for smooth math curves
            const rings = 100;     // More rings for deeper tunnel
            const radius = 50;     // Base radius
            const tubeRadius = 20; // Tube thickness

            // Create a parametric curve for the wormhole (sinusoidal twist for math feel)
            const path = new THREE.CatmullRomCurve3(
                Array.from({length: rings}, (_, i) => {
                    const t = i / rings * Math.PI * 4;  // Multi-twist
                    return new THREE.Vector3(
                        Math.sin(t) * radius * (1 + Math.sin(t * 2) * 0.2),  // X: sinusoidal variation
                        Math.cos(t) * radius * (1 + Math.cos(t * 3) * 0.2),  // Y: complex math pattern
                        -i * 20  // Z: depth into the tunnel
                    );
                })
            );

            const geometry = new THREE.TubeGeometry(path, segments, tubeRadius, 32, false);
            const material = new THREE.MeshBasicMaterial({
                color: 0xffffff,
                wireframe: true,
                transparent: true,
                opacity: 0.8,
                side: THREE.DoubleSide
            });
            const wormhole = new THREE.Mesh(geometry, material);
            scene.add(wormhole);

            // Add multiple layered wormholes for crazier, nested math structures
            const innerWormholes = [];
            for (let j = 1; j < 5; j++) {  // 4 inner layers
                const innerPath = new THREE.CatmullRomCurve3(
                    Array.from({length: rings}, (_, i) => {
                        const t = i / rings * Math.PI * (4 + j);  // Varying twists
                        return new THREE.Vector3(
                            Math.sin(t) * (radius / (j + 1)) * (1 + Math.sin(t * (2 + j)) * 0.3),
                            Math.cos(t) * (radius / (j + 1)) * (1 + Math.cos(t * (3 + j)) * 0.3),
                            -i * 20
                        );
                    })
                );
                const innerGeometry = new THREE.TubeGeometry(innerPath, segments, tubeRadius / (j + 1), 32, false);
                const innerMaterial = new THREE.MeshBasicMaterial({
                    color: 0xffffff,
                    wireframe: true,
                    transparent: true,
                    opacity: 0.6 - j * 0.1,
                    side: THREE.DoubleSide
                });
                const innerWormhole = new THREE.Mesh(innerGeometry, innerMaterial);
                scene.add(innerWormhole);
                innerWormholes.push(innerWormhole);
            }

            // Add mathematical grid planes for structured, game-like environment
            const gridSize = 1000;
            const gridDivisions = 50;
            const grid = new THREE.GridHelper(gridSize, gridDivisions, 0x00ff00, 0x008800);
            grid.rotation.x = Math.PI / 2;  // Lay flat
            grid.position.z = -1000;  // Far in depth
            scene.add(grid);

            // Point lights for dynamic, colorful lighting
            const lights = [];
            for (let l = 0; l < 8; l++) {
                const light = new THREE.PointLight(0xffffff, 2, 500);
                light.position.set(
                    Math.sin(l) * 200,
                    Math.cos(l) * 200,
                    -l * 100
                );
                scene.add(light);
                lights.push(light);
            }

            // Fog for depth and mystery
            scene.fog = new THREE.FogExp2(0x000000, 0.001);

            camera.position.set(0, 0, 100);  // Start outside the wormhole

            let time = 0;  // For animations

            function animate() {
                requestAnimationFrame(animate);
                time += 0.05;  // Fast time step for craziness

                // Epileptic color shifts: Cycle through hues rapidly
                const hue = Math.sin(time * 5) * 0.5 + 0.5;  // Fast sin for flashing
                wormhole.material.color.setHSL(hue, 1, 0.5);
                innerWormholes.forEach((wh, idx) => {
                    wh.material.color.setHSL((hue + idx * 0.2) % 1, 1, 0.5);
                });

                // Twist and pulse the wormhole mathematically
                wormhole.rotation.z += 0.02 * Math.sin(time);  // Oscillating rotation
                innerWormholes.forEach((wh, idx) => {
                    wh.rotation.z += (0.02 + idx * 0.01) * Math.cos(time + idx);
                });

                // Sucking effect: Move camera deeper into the wormhole, with shake
                camera.position.z -= 5 + Math.sin(time * 2) * 2;  // Accelerating pull
                camera.position.x = Math.sin(time * 3) * 10;  // Wobble
                camera.position.y = Math.cos(time * 4) * 10;
                if (camera.position.z < -2000) {
                    camera.position.z = 100;  // Loop back for endless suck
                }

                // Move lights along mathematical paths for trippy shadows
                lights.forEach((light, idx) => {
                    light.position.x = Math.sin(time * (2 + idx)) * 200;
                    light.position.y = Math.cos(time * (3 + idx)) * 200;
                    light.position.z -= 3;  // Pull lights too
                    if (light.position.z < -2000) light.position.z = 0;
                    light.color.setHSL(Math.sin(time * 5 + idx) * 0.5 + 0.5, 1, 0.5);  // Color flash
                });

                // Grid movement for game-like rush
                grid.position.z += 10;  // Grid rushes towards you
                if (grid.position.z > 0) grid.position.z = -1000;

                renderer.render(scene, camera);
            }
            animate();
        }
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
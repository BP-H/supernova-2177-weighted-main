# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter Metaverse")
    st.write("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")

    # Embed epilepsy warning and even crazier Three.js 3D simulation (larger, more particles, faster, more wormholes)
    three_js_code = """
    <div id="warning" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px; text-align: center; z-index: 2;">
        <p>WARNING: This simulation contains flashing lights and rapid movements that may trigger epilepsy or seizures.</p>
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
                initThreeJS();  // Start the crazy simulation after warning
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

            // Insanely crazier colorful particles (massive count, extreme varying sizes/colors, wormhole pulls)
            const particles = 100000;  // Massively increased for ultimate intensity
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particles * 3);
            const colors = new Float32Array(particles * 3);
            const sizes = new Float32Array(particles);  // Extreme varying sizes

            for (let i = 0; i < particles * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 8000;
                positions[i+1] = (Math.random() - 0.5) * 8000;
                positions[i+2] = (Math.random() - 0.5) * 8000;

                // Wilder random colors
                colors[i] = Math.random();
                colors[i + 1] = Math.random();
                colors[i + 2] = Math.random();

                // Extreme varying sizes (bigger range)
                sizes[i / 3] = Math.random() * 50 + 1;  // Sizes from 1 to 51 for more depth
            }
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            const material = new THREE.PointsMaterial({
                size: 6,  // Larger base for more presence
                vertexColors: true,
                sizeAttenuation: true,
                transparent: true,
                opacity: 0.9,
                blending: THREE.AdditiveBlending  // Intense glowing
            });

            const stars = new THREE.Points(geometry, material);
            scene.add(stars);

            // Way more wormholes/black holes (randomly placed, pulling particles ultra-chaotically)
            const wormholes = [];
            for (let j = 0; j < 50; j++) {  // 50 wormholes for absolute chaos
                const whGeometry = new THREE.SphereGeometry(20, 64, 64);
                const whMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
                const wormhole = new THREE.Mesh(whGeometry, whMaterial);
                wormhole.position.set((Math.random() - 0.5) * 3000, (Math.random() - 0.5) * 3000, (Math.random() - 0.5) * 3000);
                scene.add(wormhole);
                wormholes.push(wormhole);
            }

            // Add crazy spinning 3D objects (cubes, spheres) for more 3D madness
            const extras = [];
            for (let k = 0; k < 200; k++) {  // 200 extra objects
                const extraGeometry = Math.random() > 0.5 ? new THREE.BoxGeometry(30, 30, 30) : new THREE.SphereGeometry(15, 32, 32);
                const extraMaterial = new THREE.MeshBasicMaterial({ color: Math.random() * 0xffffff, wireframe: Math.random() > 0.5 });
                const extra = new THREE.Mesh(extraGeometry, extraMaterial);
                extra.position.set((Math.random() - 0.5) * 5000, (Math.random() - 0.5) * 5000, (Math.random() - 0.5) * 5000);
                scene.add(extra);
                extras.push(extra);
            }

            // Add point lights for dynamic lighting and more 3D feel
            const lights = [];
            for (let l = 0; l < 10; l++) {
                const light = new THREE.PointLight(0xffffff, 1, 1000);
                light.position.set((Math.random() - 0.5) * 2000, (Math.random() - 0.5) * 2000, (Math.random() - 0.5) * 2000);
                scene.add(light);
                lights.push(light);
            }

            // Add fog for depth and mystery
            scene.fog = new THREE.FogExp2(0x000000, 0.0005);

            camera.position.z = 1000;

            let time = 0;  // For hyper-fast pulsing

            function animate() {
                requestAnimationFrame(animate);
                time += 0.3;  // Hyper-fast time step

                // Update positions: Multi-wormhole pulls (insane sucking), hyper fast
                const positions = stars.geometry.attributes.position.array;
                const colors = stars.geometry.attributes.color.array;
                const sizes = stars.geometry.attributes.size.array;
                for (let i = 0; i < particles * 3; i += 3) {
                    let dx = positions[i];
                    let dy = positions[i + 1];
                    let dz = positions[i + 2];

                    // Pull to multiple random wormholes for chaos
                    wormholes.forEach(wh => {
                        let wdx = positions[i] - wh.position.x;
                        let wdy = positions[i + 1] - wh.position.y;
                        let wdz = positions[i + 2] - wh.position.z;
                        const dist = Math.sqrt(wdx * wdx + wdy * wdy + wdz * wdz);

                        if (dist > 20 && dist < 500) {  // Variable pull range
                            const pullStrength = 1 / dist * 0.5;  // Inverse distance for stronger close pulls
                            positions[i] -= wdx * pullStrength;
                            positions[i + 1] -= wdy * pullStrength;
                            positions[i + 2] -= wdz * pullStrength;
                        } else if (dist <= 20) {  // Respawn if sucked in
                            positions[i] = (Math.random() - 0.5) * 8000;
                            positions[i + 1] = (Math.random() - 0.5) * 8000;
                            positions[i + 2] = (Math.random() - 0.5) * 8000;
                        }
                    });

                    // Epileptic flashing: Insane color shifts and size pulsing
                    colors[i] = Math.sin(time * 5 + i) * 0.5 + 0.5;  // Hyper sin
                    colors[i + 1] = Math.cos(time * 6 + i * 0.7) * 0.5 + 0.5;
                    colors[i + 2] = Math.sin(time * 7 + i * 0.4) * 0.5 + 0.5;
                    sizes[i / 3] = Math.abs(Math.sin(time * 8 + i / 3)) * 50 + 1;  // Insane pulsing
                }
                stars.geometry.attributes.position.needsUpdate = true;
                stars.geometry.attributes.color.needsUpdate = true;
                stars.geometry.attributes.size.needsUpdate = true;

                // Update extra objects: spinning, moving towards camera for 3D rush
                extras.forEach(extra => {
                    extra.rotation.x += Math.random() * 0.1;
                    extra.rotation.y += Math.random() * 0.1;
                    extra.position.z += 5;  // Rush towards camera
                    if (extra.position.z > 1000) {
                        extra.position.z = -5000;  // Respawn behind
                    }
                });

                // Move lights for dynamic shadows/lighting
                lights.forEach(light => {
                    light.position.x += Math.sin(time + light.position.y) * 2;
                    light.position.y += Math.cos(time + light.position.z) * 2;
                    light.position.z += Math.sin(time + light.position.x) * 2;
                });

                // Camera shake and zoom for more immersion
                camera.position.x = Math.sin(time * 0.5) * 50;
                camera.position.y = Math.cos(time * 0.5) * 50;
                camera.position.z = 1000 + Math.sin(time * 0.2) * 200;  // Zoom in/out

                // Hyper fast rotation/chaos
                stars.rotation.y += 0.05;  // Faster

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
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
    <div id="threejs-container" style="width:100%; height:600px; background: black; position: relative;"></div>
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
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            scene.background = new THREE.Color(0x000000); // Black void

            // Even crazier colorful particles (larger count, varying sizes/colors, wormhole pulls)
            const particles = 30000;  // Increased for intensity
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particles * 3);
            const colors = new Float32Array(particles * 3);
            const sizes = new Float32Array(particles);  // Varying sizes

            for (let i = 0; i < particles * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 4000;
                positions[i+1] = (Math.random() - 0.5) * 4000;
                positions[i+2] = (Math.random() - 0.5) * 4000;

                // Wild random colors
                colors[i] = Math.random();
                colors[i + 1] = Math.random();
                colors[i + 2] = Math.random();

                // Varying sizes (bigger range)
                sizes[i / 3] = Math.random() * 15 + 1;  // Sizes from 1 to 16
            }
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            const material = new THREE.PointsMaterial({
                size: 4,  // Larger base
                vertexColors: true,
                sizeAttenuation: true,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending  // Glowing
            });

            const stars = new THREE.Points(geometry, material);
            scene.add(stars);

            // More wormholes/black holes (randomly placed, pulling particles chaotically)
            const wormholes = [];
            for (let j = 0; j < 10; j++) {  // 10 wormholes for more chaos
                const whGeometry = new THREE.SphereGeometry(15, 32, 32);
                const whMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
                const wormhole = new THREE.Mesh(whGeometry, whMaterial);
                wormhole.position.set((Math.random() - 0.5) * 1500, (Math.random() - 0.5) * 1500, (Math.random() - 0.5) * 1500);
                scene.add(wormhole);
                wormholes.push(wormhole);
            }

            camera.position.z = 600;

            let time = 0;  // For ultra-fast pulsing

            function animate() {
                requestAnimationFrame(animate);
                time += 0.15;  // Even faster time step

                // Update positions: Multi-wormhole pulls (chaotic sucking), ultra fast
                const positions = stars.geometry.attributes.position.array;
                const colors = stars.geometry.attributes.color.array;
                const sizes = stars.geometry.attributes.size.array;
                for (let i = 0; i < particles * 3; i += 3) {
                    let dx = positions[i];
                    let dy = positions[i + 1];
                    let dz = positions[i + 2];

                    // Pull to random wormhole
                    const wh = wormholes[Math.floor(Math.random() * wormholes.length)];
                    dx -= wh.position.x;
                    dy -= wh.position.y;
                    dz -= wh.position.z;
                    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                    if (dist > 30) {  // Fast pull
                        positions[i] -= dx / dist * 0.3;  // Faster
                        positions[i + 1] -= dy / dist * 0.3;
                        positions[i + 2] -= dz / dist * 0.3;
                    } else {  // Respawn if sucked in
                        positions[i] = (Math.random() - 0.5) * 4000;
                        positions[i + 1] = (Math.random() - 0.5) * 4000;
                        positions[i + 2] = (Math.random() - 0.5) * 4000;
                    }

                    // Epileptic flashing: Wild color shifts and size pulsing
                    colors[i] = Math.sin(time * 3 + i) * 0.5 + 0.5;  // Faster sin
                    colors[i + 1] = Math.cos(time * 4 + i * 0.5) * 0.5 + 0.5;
                    colors[i + 2] = Math.sin(time * 5 + i * 0.3) * 0.5 + 0.5;
                    sizes[i / 3] = Math.abs(Math.sin(time * 6 + i / 3)) * 15 + 1;  // Wilder pulsing
                }
                stars.geometry.attributes.position.needsUpdate = true;
                stars.geometry.attributes.color.needsUpdate = true;
                stars.geometry.attributes.size.needsUpdate = true;

                // Ultra fast rotation/chaos
                stars.rotation.y += 0.03;  // Faster

                renderer.render(scene, camera);
            }
            animate();
        }
    </script>
    """
    st.components.v1.html(three_js_code, height=600)

    # VR SBS button (polished, bottom right)
    st.markdown("""
        <style>
            .vr-button {position: fixed; bottom: 80px; right: 20px; z-index: 101;}
        </style>
    """, unsafe_allow_html=True)
    st.button("VR SBS Mode", key="vr_sbs", help="Enter Side-by-Side VR mode (coming soon)")

if __name__ == "__main__":
    main()

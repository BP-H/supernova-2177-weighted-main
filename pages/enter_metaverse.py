# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter Metaverse")
    st.write("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")

    # Embed epilepsy warning and crazy Three.js 3D simulation
    three_js_code = """
    <div id="warning" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px; text-align: center; z-index: 2;">
        <p>WARNING: This simulation contains flashing lights and rapid movements that may trigger epilepsy or seizures.</p>
        <p>If you have epilepsy or are sensitive, please close this page.</p>
        <p>No medical advice provided. Starting in <span id="countdown">5</span> seconds...</p>
    </div>
    <div id="threejs-container" style="width:100%; height:500px; background: black; position: relative;"></div>
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

            // Crazy colorful particles (dots symbolizing people, varying sizes/colors)
            const particles = 10000;  // More for craziness
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particles * 3);
            const colors = new Float32Array(particles * 3);
            const sizes = new Float32Array(particles);  // Varying sizes

            for (let i = 0; i < particles * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 2000;
                positions[i+1] = (Math.random() - 0.5) * 2000;
                positions[i+2] = (Math.random() - 0.5) * 2000;

                // Random vibrant colors
                colors[i] = Math.random();
                colors[i + 1] = Math.random();
                colors[i + 2] = Math.random();

                // Varying sizes (people dots)
                sizes[i / 3] = Math.random() * 5 + 1;  // Sizes from 1 to 6
            }
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            const material = new THREE.PointsMaterial({
                size: 2,  // Base size
                vertexColors: true,
                sizeAttenuation: true,
                transparent: true,
                blending: THREE.AdditiveBlending  // For glowing effect
            });

            const stars = new THREE.Points(geometry, material);
            scene.add(stars);

            // Central black hole/wormhole (glowing sphere pulling particles)
            const blackHoleGeometry = new THREE.SphereGeometry(5, 32, 32);
            const blackHoleMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
            const blackHole = new THREE.Mesh(blackHoleGeometry, blackHoleMaterial);
            scene.add(blackHole);

            camera.position.z = 500;

            let time = 0;  // For epileptic flashing/pulsing

            function animate() {
                requestAnimationFrame(animate);
                time += 0.05;  // Faster time step for craziness

                // Update positions: Suck towards center (wormhole effect), fast
                const positions = stars.geometry.attributes.position.array;
                const sizes = stars.geometry.attributes.size.array;
                for (let i = 0; i < particles * 3; i += 3) {
                    const dx = positions[i];
                    const dy = positions[i + 1];
                    const dz = positions[i + 2];
                    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                    if (dist > 10) {  // Pull if not too close
                        positions[i] -= dx / dist * 0.1;  // Faster pull
                        positions[i + 1] -= dy / dist * 0.1;
                        positions[i + 2] -= dz / dist * 0.1;
                    } else {  // Respawn if sucked in
                        positions[i] = (Math.random() - 0.5) * 2000;
                        positions[i + 1] = (Math.random() - 0.5) * 2000;
                        positions[i + 2] = (Math.random() - 0.5) * 2000;
                    }

                    // Epileptic flashing: Random color changes and size pulsing
                    colors[i] = Math.sin(time + i) * 0.5 + 0.5;
                    colors[i + 1] = Math.cos(time + i * 0.5) * 0.5 + 0.5;
                    colors[i + 2] = Math.sin(time + i * 0.3) * 0.5 + 0.5;
                    sizes[i / 3] = Math.abs(Math.sin(time + i / 3)) * 5 + 1;  // Pulsing sizes
                }
                stars.geometry.attributes.position.needsUpdate = true;
                stars.geometry.attributes.color.needsUpdate = true;
                stars.geometry.attributes.size.needsUpdate = true;

                // Fast rotation for chaos
                stars.rotation.y += 0.01;  // Faster

                renderer.render(scene, camera);
            }
            animate();
        }
    </script>
    """
    st.components.v1.html(three_js_code, height=500)

    # VR SBS button (placeholder)
    if st.button("VR SBS Mode", key="vr_sbs", help="Enter Side-by-Side VR mode (coming soon)"):
        st.write("VR SBS activated – Imagine split-screen immersion into the supernNova_2177 void! (Placeholder)")

if __name__ == "__main__":
    main()

# pages/enter_metaverse.py
import streamlit as st

def main():
    st.markdown("### Enter Metaverse")
    st.write("Stay tuned! You're being mathematically sucked into a supernova void...")
    # Embed Three.js 3D simulation (crazy void with stars/particles)
    three_js_code = """
    <div id="threejs-container" style="width:100%; height:500px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const container = document.getElementById('threejs-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);
        scene.background = new THREE.Color(0x000000); // Black void

        // Stars/particles for supernova effect
        const particles = 5000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particles * 3);
        for (let i = 0; i < particles * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 2000;
            positions[i+1] = (Math.random() - 0.5) * 2000;
            positions[i+2] = (Math.random() - 0.5) * 2000;
        }
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const material = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 2 });
        const stars = new THREE.Points(geometry, material);
        scene.add(stars);

        camera.position.z = 500;

        function animate() {
            requestAnimationFrame(animate);
            stars.rotation.y += 0.0005; // Rotate for sucking void effect
            renderer.render(scene, camera);
        }
        animate();
    </script>
    """
    st.components.v1.html(three_js_code, height=500)

if __name__ == "__main__":
    main()

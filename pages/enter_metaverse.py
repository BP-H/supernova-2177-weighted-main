# pages/enter_metaverse.py
import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(layout="wide", page_title="Multi-Verse Jumper")

    st.markdown("## Multi-Verse Jumper")
    st.write("A serious game prototype. Journey through different metaverse verses, dodge obstacles, and collect energy shards. Use **W/A/S/D** or **Arrow Keys** to navigate.")

    # --- Sidebar for Controls ---
    with st.sidebar:
        st.markdown("### 🚀 Controls")
        speed = st.slider("Base Travel Speed", 1.0, 30.0, 8.0, 0.5, key="speed_slider")
        difficulty = st.select_slider(
            "Select Difficulty",
            options=["Easy", "Medium", "Hard", "Insane"],
            value="Medium"
        )
        st.markdown("---")
        st.info("Your score and verse will be displayed within the game window.")
        st.warning("⚠️ **Epilepsy Warning:** This experience contains flashing lights and rapid motion.")


    # Map difficulty to a numeric value for obstacle density
    difficulty_map = {"Easy": 0.3, "Medium": 0.6, "Hard": 1.0, "Insane": 1.5}
    obstacle_density = difficulty_map[difficulty]

    # --- Main Three.js Game Component ---
    # NOTE: All '{' and '}' for CSS/JS have been doubled to '{{' and '}}' to work with Python's f-string.
    three_js_game = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; }}
            canvas {{ display: block; }}
            #game-container {{ width: 100%; height: 90vh; position: relative; cursor: none; }}
            #hud {{
                position: absolute;
                top: 20px;
                left: 20px;
                color: #fff;
                font-family: 'Courier New', Courier, monospace;
                font-size: 1.5em;
                text-shadow: 0 0 5px #0f0, 0 0 10px #0f0;
                z-index: 100;
                pointer-events: none;
            }}
            #warning {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 24px;
                text-align: center;
                background: rgba(0,0,0,0.8);
                padding: 20px;
                border: 2px solid red;
                z-index: 200;
            }}
        </style>
    </head>
    <body>
        <div id="warning">
            <p>WARNING: This simulation contains flashing lights and intense motion.</p>
            <p>Starting in <span id="countdown">5</span> seconds...</p>
        </div>
        <div id="game-container">
            <div id="hud">
                <div>Score: <span id="score">0</span></div>
                <div>Verse: <span id="verse-name">Genesis</span></div>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            // --- Epilepsy Warning Countdown ---
            let timeLeft = 5;
            const countdownEl = document.getElementById('countdown');
            const warningEl = document.getElementById('warning');
            const timer = setInterval(() => {{
                timeLeft--;
                countdownEl.textContent = timeLeft;
                if (timeLeft <= 0) {{
                    clearInterval(timer);
                    warningEl.style.display = 'none';
                    initGame(); // Start the game
                }}
            }}, 1000);

            // --- Game Constants and State ---
            const CONFIG = {{
                baseSpeed: {speed},
                obstacleDensity: {obstacle_density},
                worldDepth: 4000
            }};

            let scene, camera, renderer, player, clock;
            let score = 0, currentVerseName = 'Genesis';
            let activeObstacles = [], activeCollectibles = [], activePortal = null;
            const keys = {{ w: false, a: false, s: false, d: false, arrowup: false, arrowleft: false, arrowdown: false, arrowright: false }};

            const VERSE_THEMES = {{
                GENESIS: {{
                    name: "Genesis",
                    fogColor: 0x000000,
                    tubeColor: 0x00ff00, // Matrix Green
                    obstacleColor: 0xff0000, // Red
                    collectibleColor: 0x00ffff, // Cyan
                    tubeFunc: (t) => new THREE.Vector3(Math.sin(t * 2) * 60, Math.cos(t * 3) * 60, 0)
                }},
                CRYSTAL_CAVERNS: {{
                    name: "Crystal Caverns",
                    fogColor: 0x1a0033,
                    tubeColor: 0xcc33ff, // Magenta
                    obstacleColor: 0xffd700, // Gold
                    collectibleColor: 0xffffff, // White
                    tubeFunc: (t) => new THREE.Vector3(Math.sin(t * 5) * 40, Math.cos(t * 5) * 40, 0)
                }},
                VORTEX_VOID: {{
                    name: "Vortex Void",
                    fogColor: 0x050505,
                    tubeColor: 0xffffff, // White
                    obstacleColor: 0x888888, // Grey
                    collectibleColor: 0xffa500, // Orange
                    tubeFunc: (t) => new THREE.Vector3(Math.tan(t) * 20, Math.sin(t*8) * 50, 0)
                }}
            }};
            let currentTheme = VERSE_THEMES.GENESIS;


            // --- Core Functions ---
            function initGame() {{
                clock = new THREE.Clock();
                setupScene();
                setupPlayer();
                setupControls();
                generateVerse();
                animate();
            }}

            function setupScene() {{
                const container = document.getElementById('game-container');
                scene = new THREE.Scene();
                camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, CONFIG.worldDepth);
                renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                container.appendChild(renderer.domElement);
                scene.fog = new THREE.FogExp2(currentTheme.fogColor, 0.0015);
            }}

            function setupPlayer() {{
                const geometry = new THREE.ConeGeometry(3, 10, 8);
                const material = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true }});
                player = new THREE.Mesh(geometry, material);
                player.rotation.x = Math.PI / 2;
                player.position.z = -25; // Player ship is just in front of camera
                camera.add(player); // Attach player model to camera
                scene.add(camera);
                camera.position.z = 50;
            }}

            function generateVerse() {{
                // Update UI and Fog
                document.getElementById('verse-name').textContent = currentTheme.name;
                scene.fog.color.setHex(currentTheme.fogColor);

                // Create the Wormhole Tube
                const path = new THREE.Curve.create(
                    function(t) {{ return currentTheme.tubeFunc(t); }},
                    CONFIG.worldDepth / 100 // Scale of the curve
                );
                const geometry = new THREE.TubeGeometry(path, 256, 40, 16, false);
                const material = new THREE.MeshBasicMaterial({{ color: currentTheme.tubeColor, wireframe: true, side: THREE.DoubleSide }});
                const tube = new THREE.Mesh(geometry, material);
                tube.position.z = -CONFIG.worldDepth;
                scene.add(tube);

                // Generate Obstacles
                const obstacleGeometry = new THREE.BoxGeometry(20, 20, 20);
                for (let i = 0; i < 100 * CONFIG.obstacleDensity; i++) {{
                    const obstacleMaterial = new THREE.MeshBasicMaterial({{ color: currentTheme.obstacleColor, wireframe: true }});
                    const obstacle = new THREE.Mesh(obstacleGeometry, obstacleMaterial);
                    const point = path.getPoint(i / 100);
                    obstacle.position.set(point.x, point.y, -i * (CONFIG.worldDepth / 100) - 200);
                    obstacle.userData.isObstacle = true;
                    scene.add(obstacle);
                    activeObstacles.push(obstacle);
                }}

                // Generate Collectibles
                const collectibleGeometry = new THREE.OctahedronGeometry(5, 0);
                 for (let i = 0; i < 75; i++) {{
                    const collectibleMaterial = new THREE.MeshBasicMaterial({{ color: currentTheme.collectibleColor }});
                    const collectible = new THREE.Mesh(collectibleGeometry, collectibleMaterial);
                    const radius = 35;
                    const angle = Math.random() * Math.PI * 2;
                    collectible.position.set(
                        Math.cos(angle) * radius,
                        Math.sin(angle) * radius,
                        -Math.random() * CONFIG.worldDepth
                    );
                    collectible.userData.isCollectible = true;
                    scene.add(collectible);
                    activeCollectibles.push(collectible);
                }}

                // Create a Portal at the end of the verse
                const portalGeometry = new THREE.TorusGeometry(30, 8, 16, 100);
                const portalMaterial = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true }});
                activePortal = new THREE.Mesh(portalGeometry, portalMaterial);
                activePortal.position.z = -CONFIG.worldDepth + 100;
                scene.add(activePortal);
            }}

            function clearVerse() {{
                // Remove old verse objects from the scene
                [...activeObstacles, ...activeCollectibles, activePortal, scene.children.find(c => c.type === 'Mesh' && c.geometry.type === 'TubeGeometry')].forEach(obj => {{
                    if (obj) {{
                        scene.remove(obj);
                        obj.geometry.dispose();
                        obj.material.dispose();
                    }}
                }});
                activeObstacles = [];
                activeCollectibles = [];
                activePortal = null;
            }}

            function transitionToNextVerse() {{
                const verseKeys = Object.keys(VERSE_THEMES);
                const currentIndex = verseKeys.findIndex(key => VERSE_THEMES[key].name === currentTheme.name);
                const nextIndex = (currentIndex + 1) % verseKeys.length;
                currentTheme = VERSE_THEMES[verseKeys[nextIndex]];

                clearVerse();
                generateVerse();
                camera.position.set(0, 0, 50); // Reset camera position
            }}

            // --- Controls & Game Logic ---
            function setupControls() {{
                window.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
                window.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);
            }}

            function updatePlayer(deltaTime) {{
                const moveSpeed = 70 * deltaTime;
                const strafeSpeed = 70 * deltaTime;
                const moveBounds = {{x: 40, y: 40}};

                if (keys.w || keys.arrowup) camera.position.y += moveSpeed;
                if (keys.s || keys.arrowdown) camera.position.y -= moveSpeed;
                if (keys.a || keys.arrowleft) camera.position.x -= strafeSpeed;
                if (keys.d || keys.arrowright) camera.position.x += strafeSpeed;

                // Clamp player position to stay within the tunnel
                camera.position.x = THREE.MathUtils.clamp(camera.position.x, -moveBounds.x, moveBounds.x);
                camera.position.y = THREE.MathUtils.clamp(camera.position.y, -moveBounds.y, moveBounds.y);

                // Smoothly return to center
                camera.position.x -= camera.position.x * 0.02;
                camera.position.y -= camera.position.y * 0.02;
            }}

            function checkCollisions() {{
                const playerBox = new THREE.Box3().setFromObject(player);

                // Obstacles
                activeObstacles.forEach(obstacle => {{
                    const obstacleBox = new THREE.Box3().setFromObject(obstacle);
                    if (playerBox.intersectsBox(obstacleBox)) {{
                        score = Math.max(0, score - 50); // Penalty
                        document.getElementById('score').textContent = score;
                        obstacle.position.z += CONFIG.worldDepth; // "Respawn" it far away
                    }}
                }});

                // Collectibles
                activeCollectibles.forEach((collectible, index) => {{
                    if (camera.position.distanceTo(collectible.position) < 8) {{
                        score += 10;
                        document.getElementById('score').textContent = score;
                        scene.remove(collectible);
                        activeCollectibles.splice(index, 1);
                    }}
                }});

                // Portal
                if (activePortal && camera.position.distanceTo(activePortal.position) < 40) {{
                    score += 1000; // Bonus for completing the verse
                    transitionToNextVerse();
                }}
            }}

            // --- Animation Loop ---
            function animate() {{
                requestAnimationFrame(animate);
                const deltaTime = clock.getDelta();
                const time = clock.getElapsedTime();

                // Forward movement
                camera.position.z -= CONFIG.baseSpeed * (1 + score / 5000); // Speed increases with score

                updatePlayer(deltaTime);
                checkCollisions();

                // Animate portal and collectibles
                if (activePortal) activePortal.rotation.z += 0.02;
                activeCollectibles.forEach(c => c.rotation.y += 0.05);

                // Dynamic color flashing for the tube based on time
                const tube = scene.children.find(c => c.type === 'Mesh' && c.geometry.type === 'TubeGeometry');
                if (tube) {{
                    const hue = (time * 0.1) % 1;
                    tube.material.color.setHSL(hue, 1, 0.5);
                }}

                renderer.render(scene, camera);
            }}
        </script>
    </body>
    </html>
    """
    components.html(three_js_game, height=800)

if __name__ == "__main__":
    main()

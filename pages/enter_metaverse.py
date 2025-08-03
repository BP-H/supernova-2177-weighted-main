# pages/enter_metaverse.py
import streamlit as st
import streamlit.components.v1 as components

def main():
    # Configure the page for a full-screen, immersive experience
    st.set_page_config(layout="wide", page_title="Multi-Verse Jumper")

    # --- Hide Streamlit's default UI elements for a cleaner look ---
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display: none;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # --- Hardcode settings since the UI is removed ---
    speed = 8.0
    obstacle_density = 0.6

    # --- Main Three.js Game Component ---
    # NOTE: All '{' and '}' for CSS/JS have been doubled to '{{' and '}}' to work with Python's f-string.
    three_js_game = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; overflow: hidden; }}
            canvas {{ display: block; }}
            #game-container {{ width: 100vw; height: 100vh; position: relative; cursor: none; }}
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
            <p>Starting in <span id="countdown">3</span> seconds...</p>
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
            let timeLeft = 3;
            const countdownEl = document.getElementById('countdown');
            const warningEl = document.getElementById('warning');
            const timer = setInterval(() => {{
                timeLeft--;
                countdownEl.textContent = timeLeft;
                if (timeLeft <= 0) {{
                    clearInterval(timer);
                    warningEl.style.display = 'none';
                    initGame();
                }}
            }}, 1000);

            // --- Game Constants and State ---
            const CONFIG = {{
                baseSpeed: {speed},
                obstacleDensity: {obstacle_density},
                worldDepth: 4000
            }};

            let scene, camera, renderer, player, clock;
            let score = 0;
            let activeObstacles = [], activeCollectibles = [], activePortal = null;
            const keys = {{ w: false, a: false, s: false, d: false, arrowup: false, arrowleft: false, arrowdown: false, arrowright: false }};
            const playerTargetPosition = new THREE.Vector2(); // Target for player movement
            const moveBounds = {{x: 40, y: 40}};

            const VERSE_THEMES = {{
                GENESIS: {{
                    name: "Genesis",
                    fogColor: 0x000000,
                    tubeColor: 0x00ff00,
                    obstacleColor: 0xff0000,
                    collectibleColor: 0x00ffff,
                    tubeFunc: (t) => new THREE.Vector3(Math.sin(t * 2) * 60, Math.cos(t * 3) * 60, 0)
                }},
                CRYSTAL_CAVERNS: {{
                    name: "Crystal Caverns",
                    fogColor: 0x1a0033,
                    tubeColor: 0xcc33ff,
                    obstacleColor: 0xffd700,
                    collectibleColor: 0xffffff,
                    tubeFunc: (t) => new THREE.Vector3(Math.sin(t * 5) * 40, Math.cos(t * 5) * 40, 0)
                }},
                VORTEX_VOID: {{
                    name: "Vortex Void",
                    fogColor: 0x050505,
                    tubeColor: 0xffffff,
                    obstacleColor: 0x888888,
                    collectibleColor: 0xffa500,
                    tubeFunc: (t) => new THREE.Vector3(Math.tan(t) * 20, Math.sin(t*8) * 50, 0)
                }}
            }};
            let currentTheme = VERSE_THEMES.GENESIS;

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
                window.addEventListener('resize', () => {{
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }}, false);
            }}

            function setupPlayer() {{
                const geometry = new THREE.ConeGeometry(3, 10, 8);
                const material = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true }});
                player = new THREE.Mesh(geometry, material);
                player.rotation.x = Math.PI / 2;
                player.position.z = -25;
                camera.add(player);
                scene.add(camera);
                camera.position.z = 50;
            }}

            function generateVerse() {{
                document.getElementById('verse-name').textContent = currentTheme.name;
                scene.fog.color.setHex(currentTheme.fogColor);
                const path = new THREE.Curve.create(
                    function(t) {{ return currentTheme.tubeFunc(t); }},
                    CONFIG.worldDepth / 100
                );
                const tubeGeometry = new THREE.TubeGeometry(path, 256, 40, 16, false);
                const tubeMaterial = new THREE.MeshBasicMaterial({{ color: currentTheme.tubeColor, wireframe: true, side: THREE.DoubleSide }});
                const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
                tube.position.z = -CONFIG.worldDepth;
                scene.add(tube);
                // Obstacles, Collectibles, Portal generation remains the same
                const obstacleGeometry = new THREE.BoxGeometry(20, 20, 20);
                for (let i = 0; i < 100 * CONFIG.obstacleDensity; i++) {{
                    const obstacleMaterial = new THREE.MeshBasicMaterial({{ color: currentTheme.obstacleColor, wireframe: true }});
                    const obstacle = new THREE.Mesh(obstacleGeometry, obstacleMaterial);
                    const point = path.getPoint(i / 100);
                    obstacle.position.set(point.x, point.y, -i * (CONFIG.worldDepth / 100) - 200);
                    scene.add(obstacle);
                    activeObstacles.push(obstacle);
                }}
                const collectibleGeometry = new THREE.OctahedronGeometry(5, 0);
                 for (let i = 0; i < 75; i++) {{
                    const collectibleMaterial = new THREE.MeshBasicMaterial({{ color: currentTheme.collectibleColor }});
                    const collectible = new THREE.Mesh(collectibleGeometry, collectibleMaterial);
                    const radius = 35;
                    const angle = Math.random() * Math.PI * 2;
                    collectible.position.set(Math.cos(angle) * radius, Math.sin(angle) * radius, -Math.random() * CONFIG.worldDepth);
                    scene.add(collectible);
                    activeCollectibles.push(collectible);
                }}
                const portalGeometry = new THREE.TorusGeometry(30, 8, 16, 100);
                const portalMaterial = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true }});
                activePortal = new THREE.Mesh(portalGeometry, portalMaterial);
                activePortal.position.z = -CONFIG.worldDepth + 100;
                scene.add(activePortal);
            }}

            function clearVerse() {{
                [...activeObstacles, ...activeCollectibles, activePortal, scene.children.find(c => c.geometry.type === 'TubeGeometry')].forEach(obj => {{
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
                camera.position.set(0, 0, 50);
                playerTargetPosition.set(0, 0);
            }}

            function setupControls() {{
                // Keyboard controls for desktop
                window.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
                window.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);
                // Tilt controls for mobile
                window.addEventListener('deviceorientation', (event) => {{
                    // event.gamma: left-to-right tilt (-90 to 90)
                    // event.beta: front-to-back tilt (-180 to 180)
                    const tiltX = THREE.MathUtils.clamp(event.gamma, -45, 45); // Clamp to prevent extreme movement
                    const tiltY = THREE.MathUtils.clamp(event.beta, -45, 45);
                    // Map tilt to player's target position
                    playerTargetPosition.x = THREE.MathUtils.mapLinear(tiltX, -45, 45, -moveBounds.x, moveBounds.x);
                    playerTargetPosition.y = THREE.MathUtils.mapLinear(tiltY, -45, 45, moveBounds.y, -moveBounds.y); // Invert Y
                }}, true);
            }}

            function updatePlayer(deltaTime) {{
                const moveSpeed = 200 * deltaTime;
                // Keyboard input (for desktop)
                if (keys.w || keys.arrowup) playerTargetPosition.y += moveSpeed;
                if (keys.s || keys.arrowdown) playerTargetPosition.y -= moveSpeed;
                if (keys.a || keys.arrowleft) playerTargetPosition.x -= moveSpeed;
                if (keys.d || keys.arrowright) playerTargetPosition.x += moveSpeed;
                // Clamp target position to bounds
                playerTargetPosition.x = THREE.MathUtils.clamp(playerTargetPosition.x, -moveBounds.x, moveBounds.x);
                playerTargetPosition.y = THREE.MathUtils.clamp(playerTargetPosition.y, -moveBounds.y, moveBounds.y);
                // Smoothly interpolate camera to target position
                camera.position.x += (playerTargetPosition.x - camera.position.x) * 0.1;
                camera.position.y += (playerTargetPosition.y - camera.position.y) * 0.1;
            }}

            function checkCollisions() {{
                const playerBox = new THREE.Box3().setFromObject(player);
                activeObstacles.forEach(obstacle => {{
                    const obstacleBox = new THREE.Box3().setFromObject(obstacle);
                    if (playerBox.intersectsBox(obstacleBox)) {{
                        score = Math.max(0, score - 50);
                        document.getElementById('score').textContent = score;
                        obstacle.position.z += CONFIG.worldDepth;
                    }}
                }});
                activeCollectibles.forEach((collectible, index) => {{
                    if (camera.position.distanceTo(collectible.position) < 8) {{
                        score += 10;
                        document.getElementById('score').textContent = score;
                        scene.remove(collectible);
                        activeCollectibles.splice(index, 1);
                    }}
                }});
                if (activePortal && camera.position.distanceTo(activePortal.position) < 40) {{
                    score += 1000;
                    transitionToNextVerse();
                }}
            }}

            function animate() {{
                requestAnimationFrame(animate);
                const deltaTime = clock.getDelta();
                const time = clock.getElapsedTime();
                camera.position.z -= CONFIG.baseSpeed * (1 + score / 5000);
                updatePlayer(deltaTime);
                checkCollisions();
                if (activePortal) activePortal.rotation.z += 0.02;
                activeCollectibles.forEach(c => c.rotation.y += 0.05);
                const tube = scene.children.find(c => c.geometry.type === 'TubeGeometry');
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
    components.html(three_js_game, height=800, scrolling=False)

if __name__ == "__main__":
    main()


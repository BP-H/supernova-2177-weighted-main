# pages/enter_metaverse.py
import streamlit as st
import streamlit.components.v1 as components

def launch_metaverse():
    """Sets the session state to indicate the metaverse should be launched."""
    st.session_state.metaverse_launched = True

def main():
    """
    Main function to configure and run the Streamlit application.
    Manages the state between the "Lobby" and the "Metaverse" view.
    """
    st.set_page_config(page_title="Supernova Metaverse", layout="wide", initial_sidebar_state="collapsed")

    # Initialize session state
    if 'metaverse_launched' not in st.session_state:
        st.session_state.metaverse_launched = False

    st.markdown("""
        <style>
            body { background-color: #000; }
            .stApp {
                background-color: #000;
                overflow: hidden;
            }
            .main > div {
                padding: 0;
            }
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                max-width: 100% !important;
            }
            header, #MainMenu, footer {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Stage 1: Display the Lobby / Control Panel ---
    if not st.session_state.metaverse_launched:
        st.markdown("""
            <div style="text-align: center; z-index: 10;">
                <h1 style="
                    font-family: 'Courier New', monospace;
                    background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff00ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-size: 3.5em;
                    font-weight: bold;
                    text-shadow: 0 0 30px rgba(255, 0, 255, 0.7);
                    animation: pulse 2.5s infinite;
                ">SUPERNOVA METAVERSE</h1>
                <p style="color: #00ffff; font-size: 1.2em; margin-top: -15px; letter-spacing: 2px;">
                    🎮 K-POP × RETRO GAMING × CYBERPUNK 🎮
                </p>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.85; transform: scale(1.02); }
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            st.markdown("<h3 style='text-align: center; color: #00ffff;'>🎛️ GAME SETUP</h3>", unsafe_allow_html=True)
            
            st.session_state.settings = {
                'difficulty': st.select_slider("🔥 Difficulty", ["Easy", "Normal", "Hard"], value="Normal"),
                'volume': st.slider("🔊 Music Volume", 0, 100, 30)
            }

            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
            st.button("🚀 ENTER THE METAVERSE 🚀", on_click=launch_metaverse, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Stage 2: Launch the Metaverse Experience ---
    else:
        settings = st.session_state.settings
        
        three_js_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                body {{ margin: 0; overflow: hidden; background: #000; cursor: crosshair; }}
                #canvas-container {{ width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }}
                #loading-screen, #game-over-screen {{
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); display: flex; flex-direction: column;
                    justify-content: center; align-items: center; z-index: 1000;
                    font-family: 'Courier New', monospace; color: #fff;
                }}
                #game-over-screen {{ display: none; }}
                #game-over-title {{ font-size: 3em; color: #ff0066; text-shadow: 0 0 10px #ff0066; }}
                #final-score {{ font-size: 1.5em; margin: 20px 0; }}
                #restart-button {{
                    padding: 10px 20px; border: 2px solid #00ffff; color: #00ffff;
                    background: transparent; cursor: pointer; font-size: 1em;
                    text-transform: uppercase; letter-spacing: 2px;
                }}
                .loader {{
                    width: 100px; height: 100px; border: 4px solid transparent;
                    border-top: 4px solid #ff00ff; border-right: 4px solid #00ffff;
                    border-radius: 50%; animation: spin 1s linear infinite;
                }}
                @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
                #loading-text {{
                    margin-top: 25px; font-size: 1.1em; text-transform: uppercase;
                    letter-spacing: 4px; animation: glow 2s ease-in-out infinite;
                }}
                @keyframes glow {{
                    0%, 100% {{ text-shadow: 0 0 10px #ff00ff; }}
                    50% {{ text-shadow: 0 0 20px #00ffff; }}
                }}
                #hud {{
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    pointer-events: none; z-index: 10; color: #fff;
                    font-family: 'Courier New', monospace;
                }}
                #score {{ position: absolute; top: 20px; left: 20px; font-size: 24px; color: #ffff00; }}
                #health-bar {{
                    position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
                    width: 300px; height: 20px; border: 2px solid #ff00ff; background: rgba(0,0,0,0.5);
                }}
                #health-fill {{ height: 100%; background: #ff0066; transition: width 0.3s ease; }}
                /* Mobile Controls */
                #mobile-controls {{ display: none; }}
                #joystick-zone {{ position: fixed; left: 80px; bottom: 80px; width: 120px; height: 120px; pointer-events: auto; }}
                #mobile-actions {{ position: fixed; right: 20px; bottom: 50px; display: flex; flex-direction: column; gap: 20px; pointer-events: auto; }}
                .mobile-button {{ width: 60px; height: 60px; border: 2px solid #00ffff; border-radius: 50%; background: rgba(0, 255, 255, 0.2);}}
            </style>
        </head>
        <body>
            <div id="loading-screen"><div class="loader"></div><div id="loading-text">LOADING ASSETS</div></div>
            <div id="game-over-screen">
                <div id="game-over-title">SYSTEM FAILURE</div>
                <div id="final-score">SCORE: 0</div>
                <button id="restart-button">REINITIALIZE</button>
            </div>
            <div id="canvas-container"></div>
            <div id="hud">
                <div id="score">SCORE: 0</div>
                <div id="health-bar"><div id="health-fill"></div></div>
            </div>
            <div id="mobile-controls">
                <div id="joystick-zone"></div>
                <div id="mobile-actions">
                    <div id="mobile-dash" class="mobile-button"></div>
                    <div id="mobile-jump" class="mobile-button"></div>
                </div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/nipplejs@0.10.1/dist/nipplejs.min.js"></script>
            <script type="module">
                import {{ PointerLockControls }} from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/PointerLockControls.js';
                
                try {{
                    const CONFIG = {{
                        difficulty: '{settings['difficulty']}',
                        volume: {settings['volume']} / 100
                    }};

                    let scene, camera, renderer, clock, p_controls;
                    let player, world, audioManager;
                    const entities = [];
                    const keyMap = {{}};

                    class AudioManager {{
                        constructor() {{
                            this.sounds = new Howl({{
                                src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'],
                                sprite: {{
                                    'music': [0, 60000, true], 'jump': [1000, 200], 'dash': [2000, 500],
                                    'collect': [3000, 300], 'damage': [4000, 400], 'gameOver': [5000, 1000]
                                }},
                                volume: CONFIG.volume
                            }});
                        }}
                        play(sound) {{ this.sounds.play(sound); }}
                    }}

                    class Player {{
                        constructor() {{
                            this.mesh = new THREE.Mesh(
                                new THREE.CylinderGeometry(0.5, 0.5, 2, 16),
                                new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.2, metalness: 0.8 }})
                            );
                            this.mesh.position.y = 10;
                            this.velocity = new THREE.Vector3();
                            this.onGround = false;
                            this.dashCooldown = 0;
                            this.health = 100;
                            scene.add(this.mesh);
                            
                            const light = new THREE.PointLight(0x00ffff, 2, 20);
                            this.mesh.add(light);
                        }}
                        update(delta, direction) {{
                            if (this.health <= 0) return;

                            this.dashCooldown = Math.max(0, this.dashCooldown - delta);
                            
                            this.velocity.x += direction.x * 200 * delta;
                            this.velocity.z += direction.z * 200 * delta;
                            
                            this.velocity.y -= 25 * delta;
                            this.mesh.position.add(this.velocity.clone().multiplyScalar(delta));

                            if (this.mesh.position.y < 1) {{
                                this.mesh.position.y = 1;
                                this.velocity.y = 0;
                                this.onGround = true;
                            }} else {{ this.onGround = false; }}

                            this.velocity.x *= 0.9;
                            this.velocity.z *= 0.9;
                        }}
                        jump() {{ if (this.onGround) {{ this.velocity.y = 10; audioManager.play('jump'); }} }}
                        dash() {{
                            if (this.dashCooldown <= 0) {{
                                this.velocity.add(p_controls.getDirection(new THREE.Vector3()).multiplyScalar(20));
                                this.dashCooldown = 2;
                                audioManager.play('dash');
                            }}
                        }}
                        takeDamage(amount) {{
                            this.health = Math.max(0, this.health - amount);
                            document.getElementById('health-fill').style.width = this.health + '%';
                            audioManager.play('damage');
                            if(this.health <= 0) gameManager.gameOver();
                        }}
                    }}
                    
                    class Enemy {{
                        constructor() {{
                            this.mesh = new THREE.Mesh(
                                new THREE.IcosahedronGeometry(1.2, 0),
                                new THREE.MeshStandardMaterial({{ color: 0xff0066, emissive: 0xff0066, roughness: 0.5 }})
                            );
                            this.mesh.position.set((Math.random()-0.5)*100, 1.2, (Math.random()-0.5)*100);
                            scene.add(this.mesh);
                            entities.push(this);
                        }}
                        update(delta, playerPosition) {{
                            const toPlayer = playerPosition.clone().sub(this.mesh.position).normalize();
                            this.mesh.position.add(toPlayer.multiplyScalar(2 * delta));
                            
                            if (this.mesh.position.distanceTo(playerPosition) < 1.5) {{
                                player.takeDamage(5 * delta * 10);
                            }}
                        }}
                    }}

                    class Collectible {{
                         constructor() {{
                            this.mesh = new THREE.Mesh(
                                new THREE.OctahedronGeometry(0.7),
                                new THREE.MeshStandardMaterial({{ color: 0xffff00, emissive: 0xffff00, emissiveIntensity: 0.8 }})
                            );
                            this.respawn();
                            scene.add(this.mesh);
                            entities.push(this);
                        }}
                        update(delta, playerPosition) {{
                            this.mesh.rotation.y += delta;
                            if (this.mesh.position.distanceTo(playerPosition) < 2) {{
                                gameManager.addScore(100);
                                this.respawn();
                                audioManager.play('collect');
                            }}
                        }}
                        respawn() {{ this.mesh.position.set((Math.random()-0.5)*120, 1, (Math.random()-0.5)*120); }}
                    }}

                    class GameManager {{
                        constructor() {{
                            this.score = 0;
                            this.isGameOver = false;
                        }}
                        addScore(points) {{
                            this.score += points;
                            document.getElementById('score').innerText = `SCORE: ${{this.score}}`;
                        }}
                        gameOver() {{
                            this.isGameOver = true;
                            p_controls.unlock();
                            audioManager.play('gameOver');
                            document.getElementById('final-score').innerText = `FINAL SCORE: ${{this.score}}`;
                            document.getElementById('game-over-screen').style.display = 'flex';
                        }}
                        restart() {{
                            this.score = 0;
                            this.isGameOver = false;
                            player.health = 100;
                            player.mesh.position.set(0, 10, 0);
                            player.velocity.set(0,0,0);
                            document.getElementById('health-fill').style.width = '100%';
                            this.addScore(0);
                            document.getElementById('game-over-screen').style.display = 'none';
                            p_controls.lock();
                        }}
                    }}

                    function init() {{
                        scene = new THREE.Scene();
                        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                        renderer = new THREE.WebGLRenderer({{ antialias: true }});
                        renderer.setSize(window.innerWidth, window.innerHeight);
                        document.getElementById('canvas-container').appendChild(renderer.domElement);
                        clock = new THREE.Clock();
                        audioManager = new AudioManager();
                        gameManager = new GameManager();
                        
                        // World, Player, Entities
                        world = createWorld();
                        player = new Player();
                        const enemyCount = CONFIG.difficulty === 'Easy' ? 3 : CONFIG.difficulty === 'Normal' ? 6 : 10;
                        for (let i = 0; i < enemyCount; i++) new Enemy();
                        for (let i = 0; i < 15; i++) new Collectible();
                        
                        // Controls
                        p_controls = new PointerLockControls(camera, renderer.domElement);
                        renderer.domElement.addEventListener('click', () => p_controls.lock());
                        document.addEventListener('keydown', (e) => keyMap[e.code] = true);
                        document.addEventListener('keyup', (e) => keyMap[e.code] = false);

                        // Mobile Controls
                        if ('ontouchstart' in window) {{
                            p_controls.isLocked = true; // Disable pointer lock for mobile
                            document.getElementById('mobile-controls').style.display = 'block';
                            const joystick = nipplejs.create({{ zone: document.getElementById('joystick-zone'), mode: 'static', position: {{left: '50%', top: '50%'}} }});
                            joystick.on('move', (evt, data) => {{
                                keyMap['moveAngle'] = data.angle.radian;
                                keyMap['moveForce'] = data.force;
                            }});
                             joystick.on('end', () => {{
                                keyMap['moveForce'] = 0;
                            }});
                            document.getElementById('mobile-jump').addEventListener('touchstart', () => keyMap['Space'] = true);
                            document.getElementById('mobile-dash').addEventListener('touchstart', () => keyMap['ShiftLeft'] = true);
                            document.getElementById('mobile-dash').addEventListener('touchend', () => keyMap['ShiftLeft'] = false);
                        }}

                        document.getElementById('restart-button').onclick = () => gameManager.restart();

                        const loadingScreen = document.getElementById('loading-screen');
                        loadingScreen.style.opacity = '0';
                        setTimeout(() => {{
                            loadingScreen.style.display = 'none';
                            audioManager.play('music');
                            animate();
                        }}, 1500);
                    }}

                    function createWorld() {{
                        const grid = new THREE.GridHelper(200, 50, 0x00ffff, 0x888888);
                        scene.add(grid);
                        const ambient = new THREE.AmbientLight(0x400080, 1.2);
                        scene.add(ambient);
                        return {{ grid }};
                    }}
                    
                    function animate() {{
                        if (gameManager.isGameOver) return;
                        requestAnimationFrame(animate);

                        const delta = Math.min(clock.getDelta(), 0.1);
                        const moveDirection = new THREE.Vector3();
                        
                        if ('ontouchstart' in window && keyMap['moveForce'] > 0) {{
                            const angle = keyMap['moveAngle'];
                            p_controls.moveForward(Math.sin(angle) * keyMap['moveForce'] * -1); // nipplejs angle is weird
                            p_controls.moveRight(Math.cos(angle) * keyMap['moveForce']);
                        }} else {{
                            if (keyMap['KeyW']) p_controls.moveForward(1);
                            if (keyMap['KeyS']) p_controls.moveForward(-1);
                            if (keyMap['KeyA']) p_controls.moveRight(-1);
                            if (keyMap['KeyD']) p_controls.moveRight(1);
                        }}
                        
                        p_controls.getDirection(moveDirection);
                        player.update(delta, moveDirection);

                        if(keyMap['Space']) player.jump();
                        if(keyMap['ShiftLeft']) player.dash();
                        if ('ontouchstart' in window) keyMap['Space'] = false; // Prevent sticky jump on mobile

                        entities.forEach(e => e.update(delta, player.mesh.position));
                        
                        camera.position.lerp(player.mesh.position.clone().add(new THREE.Vector3(0,2,0)), 0.2);
                        renderer.render(scene, camera);
                    }}

                    init();

                }} catch (e) {{
                    const loadingScreen = document.getElementById('loading-screen');
                    loadingScreen.style.opacity = '1';
                    loadingScreen.innerHTML = `<div id="loading-text" style="color: #ff4444;">ERROR: COULD NOT LOAD METAVERSE.<br>${{e.message}}</div>`;
                }}
            </script>
        </body>
        </html>
        """
        components.html(three_js_code, height=1000, scrolling=False)

if __name__ == "__main__":
    main()

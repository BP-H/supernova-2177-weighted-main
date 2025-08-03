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

    # Custom CSS for a fully immersive, clean look
    st.markdown("""
        <style>
            body { background-color: #000; }
            .stApp {
                background-color: #000;
                overflow: hidden; /* Prevent scrollbars */
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
        # Page Title with a vibrant, animated neon effect
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

        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)  # Spacer

        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            st.markdown("<h3 style='text-align: center; color: #00ffff;'>🎛️ PRE-FLIGHT CHECK</h3>", unsafe_allow_html=True)
            
            # Store settings in session state
            st.session_state.settings = {
                'speed': st.slider("⚡ Player Speed", 1, 20, 10),
                'volume': st.slider("🔊 Music Volume", 0, 100, 40),
                'fx_intensity': st.slider("✨ FX Intensity", 0, 100, 90),
                'game_mode': st.selectbox("🕹️ Game Mode", ["Arcade Rush", "Zen Journey"])
            }

            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
            st.button("🚀 LAUNCH METAVERSE 🚀", on_click=launch_metaverse, use_container_width=True)
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
                body {{ margin: 0; overflow: hidden; background: #000; }}
                #canvas-container {{ width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }}
                #loading-screen {{
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: #000; display: flex; flex-direction: column;
                    justify-content: center; align-items: center; z-index: 1000;
                    transition: opacity 1.5s ease;
                }}
                .loader {{
                    width: 100px; height: 100px; border: 4px solid transparent;
                    border-top: 4px solid #ff00ff; border-right: 4px solid #00ffff;
                    border-radius: 50%; animation: spin 1s linear infinite;
                }}
                @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
                #loading-text {{
                    color: #fff; margin-top: 25px; font-size: 1.1em;
                    font-family: 'Courier New', monospace; text-transform: uppercase;
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
                .hud-element {{ position: absolute; text-shadow: 0 0 8px #000; }}
                #score {{ top: 20px; left: 20px; font-size: 24px; color: #ffff00; }}
                #quit-button {{ 
                    bottom: 20px; left: 20px; font-size: 16px; color: #aaa;
                    pointer-events: auto; cursor: pointer; text-decoration: none;
                }}
                #quit-button:hover {{ color: #fff; text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div id="loading-screen"><div class="loader"></div><div id="loading-text">CONNECTING...</div></div>
            <div id="canvas-container"></div>
            <div id="hud">
                <div id="score" class="hud-element">SCORE: 0</div>
                <div id="quit-button" class="hud-element" onclick="window.location.reload();">QUIT TO LOBBY</div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
            
            <script>
                try {{
                    const CONFIG = {{
                        speed: {settings['speed']},
                        volume: {settings['volume']} / 100,
                        fxIntensity: {settings['fx_intensity']} / 100,
                        gameMode: '{settings['game_mode']}'
                    }};

                    let scene, camera, renderer, clock, player, world;
                    const keyMap = {{}};
                    const playerVelocity = new THREE.Vector3();
                    let onGround = false;

                    function init() {{
                        scene = new THREE.Scene();
                        scene.fog = new THREE.FogExp2(0x0a001a, 0.005 * (2.0 - CONFIG.fxIntensity));
                        
                        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                        
                        renderer = new THREE.WebGLRenderer({{ antialias: true }});
                        renderer.setSize(window.innerWidth, window.innerHeight);
                        document.getElementById('canvas-container').appendChild(renderer.domElement);
                        
                        clock = new THREE.Clock();

                        // --- Audio ---
                        const audio = new Howl({{
                            src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'],
                            loop: true, volume: CONFIG.volume, html5: true
                        }});

                        // --- World ---
                        const gridMaterial = new THREE.ShaderMaterial({{
                            uniforms: {{ time: {{ value: 0 }}, resolution: {{ value: new THREE.Vector2(window.innerWidth, window.innerHeight) }} }},
                            vertexShader: `void main() {{ gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }}`,
                            fragmentShader: `
                                uniform float time;
                                uniform vec2 resolution;
                                void main() {{
                                    vec2 uv = gl_FragCoord.xy / resolution.xy;
                                    float grid = max(step(0.99, fract(uv.x * 50.0)), step(0.99, fract(uv.y * 50.0)));
                                    vec3 color = mix(vec3(1.0, 0.0, 1.0), vec3(0.0, 1.0, 1.0), uv.x + sin(time) * 0.1);
                                    float pulse = sin(length(uv - 0.5) * 15.0 - time * 4.0) * 0.5 + 0.5;
                                    gl_FragColor = vec4(color * (0.5 + pulse * 0.5) * grid, grid * 0.8);
                                }}`,
                            transparent: true
                        }});
                        const grid = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), gridMaterial);
                        grid.rotation.x = -Math.PI / 2; scene.add(grid);
                        world = {{ grid, gridMaterial }};

                        // --- Player (Using CylinderGeometry) ---
                        player = new THREE.Mesh(
                            new THREE.CylinderGeometry(0.5, 0.5, 2, 16), // Replaced Capsule with Cylinder
                            new THREE.MeshStandardMaterial({{ color: 0xffffff, emissive: 0xcccccc, roughness: 0.2, metalness: 0.8 }})
                        );
                        player.position.y = 1; // Adjust position for cylinder's center origin
                        scene.add(player);

                        // --- Lighting ---
                        scene.add(new THREE.AmbientLight(0x400080, 0.8));
                        const playerLight = new THREE.PointLight(0x00ffff, 1.5, 20);
                        player.add(playerLight); // Attach light to player

                        // --- Controls ---
                        document.addEventListener('keydown', (e) => keyMap[e.code] = true);
                        document.addEventListener('keyup', (e) => keyMap[e.code] = false);

                        // --- Finalize ---
                        const loadingScreen = document.getElementById('loading-screen');
                        loadingScreen.style.opacity = '0';
                        setTimeout(() => {{
                            loadingScreen.style.display = 'none';
                            audio.play();
                            animate();
                        }}, 1500);
                    }}
                    
                    function animate() {{
                        requestAnimationFrame(animate);
                        const delta = Math.min(clock.getDelta(), 0.1);
                        const elapsedTime = clock.getElapsedTime();

                        // --- Player Movement ---
                        const moveSpeed = CONFIG.speed * delta;
                        const moveDirection = new THREE.Vector3(
                            (keyMap['KeyD'] || keyMap['ArrowRight'] ? 1 : 0) - (keyMap['KeyA'] || keyMap['ArrowLeft'] ? 1 : 0),
                            0,
                            (keyMap['KeyS'] || keyMap['ArrowDown'] ? 1 : 0) - (keyMap['KeyW'] || keyMap['ArrowUp'] ? 1 : 0)
                        ).normalize();
                        
                        playerVelocity.x = moveDirection.x * moveSpeed * 10;
                        playerVelocity.z = moveDirection.z * moveSpeed * 10;
                        
                        // Gravity & Jump
                        playerVelocity.y -= 20 * delta;
                        if ((keyMap['Space']) && onGround) {{
                            playerVelocity.y = 8;
                        }}

                        player.position.add(playerVelocity.clone().multiplyScalar(delta));

                        // Ground Collision
                        if (player.position.y < 1) {{
                            player.position.y = 1;
                            playerVelocity.y = 0;
                            onGround = true;
                        }} else {{ onGround = false; }}

                        // --- World & Visuals ---
                        world.gridMaterial.uniforms.time.value = elapsedTime;
                        const beat = 0.5 + Math.sin(elapsedTime * 5) * 0.5; // Simulated beat
                        player.children[0].intensity = 1.5 + beat * 2 * CONFIG.fxIntensity; // Pulse player light

                        // --- Camera ---
                        const cameraOffset = new THREE.Vector3(0, 5, 10);
                        const targetPosition = player.position.clone().add(cameraOffset);
                        camera.position.lerp(targetPosition, 0.1);
                        camera.lookAt(player.position);
                        
                        renderer.render(scene, camera);
                    }}

                    init();

                }} catch (e) {{
                    const loadingScreen = document.getElementById('loading-screen');
                    loadingScreen.style.opacity = '1';
                    loadingScreen.innerHTML = `<div id="loading-text" style="color: #ff4444;">ERROR: COULD NOT LOAD METAVERSE.<br>${{e.message}}</div>`;
                    console.error(e);
                }}
            </script>
        </body>
        </html>
        """
        components.html(three_js_code, height=1000, scrolling=False)

if __name__ == "__main__":
    main()

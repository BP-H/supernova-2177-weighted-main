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
            /* Reset Streamlit's default styling for a true full-screen experience */
            body { background-color: #000; }
            .stApp {
                background: #000;
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
            /* Hide Streamlit's default header, menu, and footer */
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
            
            # Store settings in session state to pass to the HTML component
            st.session_state.settings = {
                'speed': st.slider("⚡ Player Speed", 1, 20, 8),
                'volume': st.slider("🔊 Music Volume", 0, 100, 50),
                'fx_intensity': st.slider("✨ FX Intensity", 0, 100, 85),
                'game_mode': st.selectbox("🕹️ Game Mode", ["Arcade Rush", "Zen Journey", "Boss Battle"])
            }

            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            
            # Centered launch button
            st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
            st.button("🚀 LAUNCH METAVERSE 🚀", on_click=launch_metaverse, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Stage 2: Launch the Metaverse Experience ---
    else:
        settings = st.session_state.settings
        
        # NOTE: All curly braces `{` and `}` in the CSS/JS below are DOUBLED `{{` and `}}`
        # to escape them for Python's f-string formatting.
        three_js_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                body {{
                    margin: 0; padding: 0; overflow: hidden;
                    font-family: 'Courier New', monospace; background: #000;
                    touch-action: none; -webkit-user-select: none; user-select: none;
                }}
                #canvas-container {{ width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }}
                #loading-screen {{
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: #000;
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    z-index: 1000; transition: opacity 1.5s ease;
                }}
                .loader {{
                    width: 100px; height: 100px; border: 4px solid transparent;
                    border-top: 4px solid #ff00ff; border-right: 4px solid #00ffff;
                    border-radius: 50%; animation: spin 1s linear infinite;
                }}
                @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
                #loading-text {{
                    color: #fff; margin-top: 25px; font-size: 1.1em;
                    text-transform: uppercase; letter-spacing: 4px;
                    animation: glow 2s ease-in-out infinite;
                }}
                @keyframes glow {{
                    0%, 100% {{ text-shadow: 0 0 10px #ff00ff; }}
                    50% {{ text-shadow: 0 0 20px #00ffff; }}
                }}
                #hud {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; color: #fff; }}
                .hud-element {{
                    position: absolute; text-shadow: 0 0 8px #000;
                }}
                #score {{ top: 20px; left: 20px; font-size: 24px; color: #ffff00; }}
                #health-bar {{ top: 20px; right: 20px; width: 200px; height: 20px; border: 2px solid #ff00ff; background: rgba(0,0,0,0.5); }}
                #health-fill {{ height: 100%; background: linear-gradient(90deg, #ff0066, #ff00ff); transition: width 0.3s ease; }}
                #quit-button {{ 
                    bottom: 20px; left: 20px; font-size: 16px; color: #fff; 
                    pointer-events: auto; cursor: pointer; text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div id="loading-screen">
                <div class="loader"></div>
                <div id="loading-text">INITIALIZING...</div>
            </div>
            <div id="canvas-container"></div>
            <div id="hud">
                <div id="score" class="hud-element">SCORE: 0</div>
                <div id="health-bar" class="hud-element">
                    <div id="health-fill" style="width: 100%;"></div>
                </div>
                <div id="quit-button" class="hud-element" onclick="window.location.reload();">QUIT</div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
            
            <script>
                // Use a try-catch block to prevent the entire page from freezing on an error
                try {{
                    // --- Config & State ---
                    const CONFIG = {{
                        speed: {settings['speed']},
                        volume: {settings['volume']} / 100,
                        fxIntensity: {settings['fx_intensity']} / 100,
                        gameMode: '{settings['game_mode']}'
                    }};
                    const state = {{ score: 0, health: 100 }};
                    let scene, camera, renderer, clock, player, audioSystem;
                    const enemies = [];
                    const playerVelocity = new THREE.Vector3();
                    let onGround = false;

                    // --- Scene Initialization ---
                    function init() {{
                        scene = new THREE.Scene();
                        scene.fog = new THREE.FogExp2(0x0a001a, 0.005 * (2.0 - CONFIG.fxIntensity));
                        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                        renderer = new THREE.WebGLRenderer({{ antialias: true }});
                        renderer.setSize(window.innerWidth, window.innerHeight);
                        document.getElementById('canvas-container').appendChild(renderer.domElement);
                        clock = new THREE.Clock();

                        // --- Audio ---
                        audioSystem = new Howl({{
                            src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'],
                            loop: true, volume: CONFIG.volume, html5: true
                        }});

                        // --- World Creation ---
                        const gridMaterial = new THREE.MeshBasicMaterial({{ color: 0x00ffff, wireframe: true }});
                        const grid = new THREE.Mesh(new THREE.PlaneGeometry(500, 500, 50, 50), gridMaterial);
                        grid.rotation.x = -Math.PI / 2;
                        scene.add(grid);

                        // --- Player ---
                        player = new THREE.Mesh(
                            new THREE.CapsuleGeometry(0.5, 1, 4, 10),
                            new THREE.MeshBasicMaterial({{ color: 0xff00ff }})
                        );
                        player.position.y = 0.5;
                        scene.add(player);

                        // --- Lighting ---
                        scene.add(new THREE.AmbientLight(0x404040, 1.5));
                        
                        // --- Controls ---
                        setupControls();

                        // --- Hide loading screen and start ---
                        const loadingScreen = document.getElementById('loading-screen');
                        loadingScreen.style.opacity = '0';
                        setTimeout(() => {{
                            loadingScreen.style.display = 'none';
                            audioSystem.play();
                            animate();
                        }}, 1500);
                    }}
                    
                    // --- Controls Setup ---
                    const keyMap = {{}};
                    function setupControls() {{
                        document.addEventListener('keydown', (e) => keyMap[e.code] = true);
                        document.addEventListener('keyup', (e) => keyMap[e.code] = false);
                    }}

                    // --- Game Loop ---
                    function animate() {{
                        requestAnimationFrame(animate);
                        const delta = Math.min(clock.getDelta(), 0.1); // Cap delta to prevent physics bugs

                        // --- Player Movement ---
                        const moveDirection = new THREE.Vector3(
                            (keyMap['KeyD'] ? 1 : 0) - (keyMap['KeyA'] ? 1 : 0),
                            0,
                            (keyMap['KeyS'] ? 1 : 0) - (keyMap['KeyW'] ? 1 : 0)
                        ).normalize();
                        
                        playerVelocity.x += moveDirection.x * CONFIG.speed * delta;
                        playerVelocity.z += moveDirection.z * CONFIG.speed * delta;
                        
                        // Gravity & Jump
                        playerVelocity.y -= 9.8 * delta;
                        if (keyMap['Space'] && onGround) {{
                            playerVelocity.y = 5;
                        }}

                        player.position.add(playerVelocity.clone().multiplyScalar(delta));

                        // Ground Collision
                        if (player.position.y < 0.5) {{
                            player.position.y = 0.5;
                            playerVelocity.y = 0;
                            onGround = true;
                        }} else {{
                            onGround = false;
                        }}

                        // Friction
                        playerVelocity.x *= 0.92;
                        playerVelocity.z *= 0.92;
                        
                        // --- Camera ---
                        const cameraOffset = new THREE.Vector3(0, 4, 8);
                        camera.position.lerp(player.position.clone().add(cameraOffset), 0.1);
                        camera.lookAt(player.position);
                        
                        renderer.render(scene, camera);
                    }}

                    init();

                }} catch (e) {{
                    // Show a friendly error message if something goes wrong
                    document.getElementById('loading-screen').style.opacity = '1';
                    document.querySelector('.loader').style.display = 'none';
                    document.getElementById('loading-text').innerText = 'ERROR: COULD NOT LOAD METAVERSE.\\n' + e.message;
                    console.error(e);
                }}
            </script>
        </body>
        </html>
        """
        components.html(three_js_code, height=1000, scrolling=False)

if __name__ == "__main__":
    main()

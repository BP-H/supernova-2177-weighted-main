# pages/enter_metaverse.py
import streamlit as st
import streamlit.components.v1 as components

def main():
    """
    Main function to configure and run the Streamlit application for the Supernova Metaverse.
    """
    st.set_page_config(page_title="Enter Metaverse", layout="wide", initial_sidebar_state="collapsed")
    
    # Custom CSS for a fully immersive, clean look
    st.markdown("""
        <style>
            /* Reset Streamlit's default styling for a true full-screen experience */
            .stApp {
                background: #000;
                overflow: hidden; /* Prevent scrollbars */
            }
            .main > div {
                padding: 0;
            }
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            /* Hide Streamlit's default header, menu, and footer */
            header, #MainMenu, footer {
                display: none !important;
            }
            /* Style for the control panel's launch button */
            .stButton > button {
                background: linear-gradient(135deg, #ff00ff, #00ffff);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 30px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                transition: all 0.3s ease;
                box-shadow: 0 0 20px rgba(255, 0, 255, 0.6);
                cursor: pointer;
            }
            .stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 35px rgba(0, 255, 255, 0.8);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Page Title with a vibrant, animated neon effect
    st.markdown("""
        <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10;">
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
    
    # Control Panel placed below the title
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True) # Spacer
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #00ffff;'>🎛️ CONTROL PANEL</h3>", unsafe_allow_html=True)
        
        # Gameplay settings
        speed = st.slider("⚡ Player Speed", min_value=1, max_value=20, value=8, key="speed_slider")
        volume = st.slider("🔊 Music Volume", min_value=0, max_value=100, value=60, key="volume_slider")
        fx_intensity = st.slider("✨ FX Intensity", min_value=0, max_value=100, value=85, key="fx_slider")
        game_mode = st.selectbox(
            "🕹️ Game Mode",
            ["Arcade Rush", "Story Mode", "Boss Battle", "Zen Journey"],
            key="game_mode",
            help="Select your desired game experience."
        )

    # The main Three.js scene, integrating all features into a single HTML component
    three_js_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            /* --- Core Styles --- */
            body {{
                margin: 0; padding: 0; overflow: hidden;
                font-family: 'Courier New', monospace; background: #000;
                touch-action: none; -webkit-user-select: none; user-select: none;
            }}
            #threejs-container {{ width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; z-index: -1; }}

            /* --- Loading Screen --- */
            #loading-screen {{
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(135deg, #0a0a0a, #1a0033);
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                z-index: 1000; transition: opacity 1.5s ease;
            }}
            .loader {{
                width: 120px; height: 120px; border: 4px solid transparent;
                border-top: 4px solid #ff00ff; border-right: 4px solid #00ffff;
                border-radius: 50%; animation: spin 1s linear infinite;
            }}
            @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
            #loading-text {{
                color: #fff; margin-top: 25px; font-size: 1.3em;
                text-transform: uppercase; letter-spacing: 4px;
                animation: glow 2s ease-in-out infinite;
            }}
            @keyframes glow {{
                0%, 100% {{ text-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff; }}
                50% {{ text-shadow: 0 0 20px #ff00ff, 0 0 40px #00ffff; }}
            }}

            /* --- HUD Elements --- */
            #hud {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100; }}
            .hud-element {{
                position: absolute; color: #fff; font-size: 18px; font-weight: bold;
                text-shadow: 0 0 8px rgba(255, 0, 255, 0.8);
            }}
            #score {{ top: 20px; left: 20px; font-size: 24px; color: #ffff00; }}
            #health-bar {{
                top: 20px; right: 20px; width: 200px; height: 20px;
                border: 2px solid #ff00ff; background: rgba(0, 0, 0, 0.5);
            }}
            #health-fill {{
                height: 100%; background: linear-gradient(90deg, #ff0066, #ff00ff);
                transition: width 0.3s ease; box-shadow: 0 0 10px #ff00ff;
            }}
            #combo-counter {{
                top: 60px; left: 20px; font-size: 32px; color: #00ffff; display: none;
                animation: combo-pop 0.3s ease;
            }}
            @keyframes combo-pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.2)}} 100%{{transform:scale(1)}} }}
            #power-ups {{
                bottom: 120px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px;
            }}
            .power-up-icon {{
                width: 50px; height: 50px; background: linear-gradient(135deg, #ff00ff, #00ffff);
                border-radius: 10px; display: flex; align-items: center; justify-content: center;
                font-size: 24px; box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
                animation: float 2s ease-in-out infinite;
            }}
            @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
            
            /* --- Mobile Controls --- */
            .joystick-zone {{
                position: absolute; width: 120px; height: 120px;
                border-radius: 50%; z-index: 200; touch-action: none;
                display: none; /* Hidden by default, enabled by JS */
            }}
            #left-joystick {{ left: 40px; bottom: 40px; }}
            #right-joystick {{ right: 40px; bottom: 40px; }}
            #action-buttons {{
                position: absolute; right: 40px; bottom: 180px;
                display: none; flex-direction: column; gap: 15px; z-index: 200;
            }}
            .action-btn {{
                width: 60px; height: 60px; border-radius: 50%;
                border: 2px solid #00ffff;
                background: radial-gradient(circle, rgba(0, 255, 255, 0.3) 0%, transparent 70%);
                color: #fff; font-size: 28px; display: flex; align-items: center; justify-content: center;
                cursor: pointer; touch-action: manipulation; transition: all 0.1s ease;
            }}
            .action-btn:active {{ transform: scale(0.9); background: radial-gradient(circle, rgba(0, 255, 255, 0.6) 0%, transparent 70%); }}

            /* --- Notification System --- */
            #notifications {{
                position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                pointer-events: none; z-index: 500;
            }}
            .notification {{
                color: #fff; font-size: 36px; font-weight: bold; text-align: center;
                animation: notification-pop 2s ease-out forwards; text-shadow: 0 0 20px currentColor;
            }}
            @keyframes notification-pop {{
                0% {{ transform: scale(0); opacity: 0; }}
                50% {{ transform: scale(1.2) rotate(3deg); opacity: 1; }}
                100% {{ transform: scale(1) translateY(-100px); opacity: 0; }}
            }}
        </style>
    </head>
    <body>
        <div id="loading-screen">
            <div class="loader"></div>
            <div id="loading-text">ENTERING METAVERSE</div>
        </div>
        
        <div id="threejs-container"></div>
        
        <div id="hud">
            <div id="score" class="hud-element">SCORE: 0</div>
            <div id="health-bar" class="hud-element">
                <div id="health-fill" style="width: 100%;"></div>
            </div>
            <div id="combo-counter" class="hud-element">COMBO x1</div>
            <div id="power-ups" class="hud-element"></div>
        </div>
        
        <div id="left-joystick" class="joystick-zone"></div>
        <div id="right-joystick" class="joystick-zone"></div>
        <div id="action-buttons">
            <button class="action-btn" id="attack-btn">⚡</button>
            <button class="action-btn" id="dash-btn">💨</button>
            <button class="action-btn" id="jump-btn">⬆️</button>
        </div>
        
        <div id="notifications"></div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/nipplejs@0.10.1/dist/nipplejs.min.js"></script>
        
        <script>
            // ==========================================
            //  CORE SETUP & CONFIGURATION
            // ==========================================
            let scene, camera, renderer, clock, player, world, audioSystem;
            let enemies = [], collectibles = [];
            let leftJoystick, rightJoystick;
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

            // Config from Streamlit sliders
            const CONFIG = {{
                speed: {speed} / 10,
                volume: {volume} / 100,
                fxIntensity: {fx_intensity} / 100,
                gameMode: '{game_mode}'
            }};

            // Game state
            const state = {{
                score: 0, health: 100, combo: 0, powerUps: [],
                isPaused: false, isGameOver: false
            }};
            const playerInput = {{ move: new THREE.Vector2(), look: new THREE.Vector2(), jump: false, dash: false, attack: false }};

            // ==========================================
            //  AUDIO SYSTEM (Retro SFX + Music)
            // ==========================================
            class AudioSystem {{
                constructor() {{
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    this.sfxVolume = CONFIG.volume * 1.2;
                    // Placeholder K-Pop style synth loop
                    this.bgMusic = new Howl({{
                        src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAİlgh/nipplejs/dist/nipplejs.min.js"></script>
        
        <script>
            // ==========================================
            //  CORE SETUP & CONFIGURATION
            // ==========================================
            let scene, camera, renderer, clock, player, world, audioSystem;
            let enemies = [], collectibles = [];
            let leftJoystick, rightJoystick;
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

            // Config from Streamlit sliders
            const CONFIG = {{
                speed: {speed} / 10,
                volume: {volume} / 100,
                fxIntensity: {fx_intensity} / 100,
                gameMode: '{game_mode}'
            }};

            // Game state
            const state = {{
                score: 0, health: 100, combo: 0, powerUps: [],
                isPaused: false, isGameOver: false
            }};
            const playerInput = {{ move: new THREE.Vector2(), look: new THREE.Vector2(), jump: false, dash: false, attack: false }};

            // ==========================================
            //  AUDIO SYSTEM (Retro SFX + Music)
            // ==========================================
            class AudioSystem {{
                constructor() {{
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    this.sfxVolume = CONFIG.volume * 1.2;
                    // Placeholder K-Pop style synth loop
                    this.bgMusic = new Howl({{
                        src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-gth/nipplejs.min.js"></script>
        
        <script>
            // ==========================================
            //  CORE SETUP & CONFIGURATION
            // ==========================================
            let scene, camera, renderer, clock, player, world, audioSystem;
            let enemies = [], collectibles = [];
            let leftJoystick, rightJoystick;
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

            // Config from Streamlit sliders
            const CONFIG = {{
                speed: {speed} / 10,
                volume: {volume} / 100,
                fxIntensity: {fx_intensity} / 100,
                gameMode: '{game_mode}'
            }};

            // Game state
            const state = {{
                score: 0, health: 100, combo: 0, powerUps: [],
                isPaused: false, isGameOver: false
            }};
            const playerInput = {{ move: new THREE.Vector2(), look: new THREE.Vector2(), jump: false, dash: false, attack: false }};

            // ==========================================
            //  AUDIO SYSTEM (Retro SFX + Music)
            // ==========================================
            class AudioSystem {{
                constructor() {{
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    this.sfxVolume = CONFIG.volume * 1.2;
                    // Placeholder K-Pop style synth loop
                    this.bgMusic = new Howl({{
                        src: ['data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU3LjgyLjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1B0AAABJAAAAHkAAAGwDRUREVFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//uR4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-'],
                        loop: true, volume: CONFIG.volume, html5: true
                    }});
                    const source = this.audioContext.createMediaElementSource(this.bgMusic._sounds[0]._node);
                    this.analyser = this.audioContext.createAnalyser();
                    source.connect(this.analyser);
                    this.analyser.connect(this.audioContext.destination);
                    this.analyser.fftSize = 128;
                    this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
                }}
                play(sound) {{
                    const time = this.audioContext.currentTime;
                    const osc = this.audioContext.createOscillator();
                    const gain = this.audioContext.createGain();
                    osc.connect(gain);
                    gain.connect(this.audioContext.destination);
                    gain.gain.setValueAtTime(0.3 * this.sfxVolume, time);

                    switch(sound) {{
                        case 'collect':
                            osc.frequency.setValueAtTime(880, time);
                            osc.type = 'sine';
                            gain.gain.exponentialRampToValueAtTime(0.01, time + 0.1);
                            osc.stop(time + 0.1);
                            break;
                        case 'dash':
                            osc.type = 'sawtooth';
                            osc.frequency.setValueAtTime(2000, time);
                            osc.frequency.exponentialRampToValueAtTime(100, time + 0.2);
                            gain.gain.exponentialRampToValueAtTime(0.01, time + 0.2);
                            osc.stop(time + 0.2);
                            break;
                        case 'hit':
                            osc.type = 'square';
                            osc.frequency.setValueAtTime(440, time);
                            osc.frequency.exponentialRampToValueAtTime(50, time + 0.15);
                            gain.gain.exponentialRampToValueAtTime(0.01, time + 0.15);
                            osc.stop(time + 0.15);
                            break;
                        case 'jump':
                            osc.type = 'triangle';
                            osc.frequency.setValueAtTime(440, time);
                            osc.frequency.exponentialRampToValueAtTime(880, time + 0.1);
                             gain.gain.exponentialRampToValueAtTime(0.01, time + 0.1);
                            osc.stop(time + 0.1);
                            break;
                    }}
                    osc.start(time);
                }}
                detectBeat() {{
                    this.analyser.getByteFrequencyData(this.dataArray);
                    const bass = this.dataArray.slice(0, 8).reduce((a, b) => a + b) / 8;
                    return bass / 255;
                }}
                startMusic() {{ this.bgMusic.play(); }}
            }}

            // ==========================================
            //  INITIALIZATION
            // ==========================================
            function init() {{
                scene = new THREE.Scene();
                scene.fog = new THREE.FogExp2(0x0a001a, 0.002 * (1.2 - CONFIG.fxIntensity));
                
                camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                
                renderer = new THREE.WebGLRenderer({{ antialias: !isMobile, powerPreference: "high-performance" }});
                renderer.setSize(window.innerWidth, window.innerHeight);
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
                renderer.shadowMap.enabled = !isMobile;
                document.getElementById('threejs-container').appendChild(renderer.domElement);
                
                clock = new THREE.Clock();
                audioSystem = new AudioSystem();

                createWorld();
                createPlayer();
                createLighting();
                if (CONFIG.gameMode !== 'Zen Journey') {{
                    createEnemies(CONFIG.gameMode === 'Boss Battle' ? 1 : 15);
                    createCollectibles(50);
                }}

                if (isMobile) {{
                    setupMobileControls();
                }} else {{
                    setupDesktopControls();
                }}
                
                window.addEventListener('resize', onWindowResize, false);
                
                const loadingScreen = document.getElementById('loading-screen');
                loadingScreen.style.opacity = '0';
                setTimeout(() => {{
                    loadingScreen.style.display = 'none';
                    audioSystem.startMusic();
                    animate();
                }}, 1500);
            }}

            // ==========================================
            //  WORLD & ENTITY CREATION
            // ==========================================
            function createWorld() {{
                const gridMaterial = new THREE.ShaderMaterial({{
                    uniforms: {{ time: {{ value: 0 }}, color1: {{ value: new THREE.Color(0xff00ff) }}, color2: {{ value: new THREE.Color(0x00ffff) }} }},
                    vertexShader: `varying vec2 vUv; void main() {{ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }}`,
                    fragmentShader: `
                        uniform float time; uniform vec3 color1; uniform vec3 color2; varying vec2 vUv;
                        void main() {{
                            float grid = max(step(0.98, fract(vUv.x * 50.0)), step(0.98, fract(vUv.y * 50.0)));
                            vec3 color = mix(color1, color2, vUv.x + sin(time) * 0.1);
                            float pulse = sin(length(vUv - 0.5) * 10.0 - time * 4.0) * 0.5 + 0.5;
                            gl_FragColor = vec4(color * (0.5 + pulse * 0.5) * grid, grid * 0.8);
                        }}`,
                    transparent: true, side: THREE.DoubleSide
                }});
                const grid = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), gridMaterial);
                grid.rotation.x = -Math.PI / 2; grid.position.y = -2; scene.add(grid);
                world = {{ grid, gridMaterial }};
            }}

            function createPlayer() {{
                const group = new THREE.Group();
                const body = new THREE.Mesh(
                    new THREE.CapsuleGeometry(0.5, 1, 4, 10),
                    new THREE.MeshStandardMaterial({{ color: 0xffffff, emissive: 0xcccccc, emissiveIntensity: 0.2, metalness: 0.8, roughness: 0.2 }})
                );
                body.position.y = 0.5;
                group.add(body);
                
                const light = new THREE.PointLight(0x00ffff, 2, 10);
                light.position.y = 1;
                group.add(light);
                
                player = {{ group, body, light, velocity: new THREE.Vector3(), onGround: true, dashCooldown: 0, attackCooldown: 0 }};
                scene.add(player.group);
            }}

            function createLighting() {{
                scene.add(new THREE.AmbientLight(0x400080, 0.5));
                const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
                dirLight.position.set(50, 100, 50);
                scene.add(dirLight);
            }}

            function createEnemies(count) {{
                for (let i = 0; i < count; i++) {{
                    const isBoss = (i === 0 && CONFIG.gameMode === 'Boss Battle');
                    const size = isBoss ? 4 : 1;
                    const health = isBoss ? 200 : 10;
                    const enemy = new THREE.Mesh(
                        new THREE.IcosahedronGeometry(size, 0),
                        new THREE.MeshStandardMaterial({{ color: 0xff0066, emissive: 0xff0066, emissiveIntensity: 0.4, roughness: 0.5 }})
                    );
                    enemy.position.set((Math.random() - 0.5) * 150, size, (Math.random() - 0.5) * 150);
                    enemy.userData = {{ health, maxHealth: health, type: isBoss ? 'boss' : 'grunt', velocity: new THREE.Vector3() }};
                    scene.add(enemy);
                    enemies.push(enemy);
                }}
            }}

            function createCollectibles(count) {{
                for (let i = 0; i < count; i++) {{
                    const collectible = new THREE.Mesh(
                        new THREE.OctahedronGeometry(0.5),
                        new THREE.MeshStandardMaterial({{ color: 0xffff00, emissive: 0xffff00, emissiveIntensity: 0.6 }})
                    );
                    collectible.position.set((Math.random() - 0.5) * 200, Math.random() * 10 + 1, (Math.random() - 0.5) * 200);
                    scene.add(collectible);
                    collectibles.push(collectible);
                }}
            }}

            // ==========================================
            //  CONTROLS
            // ==========================================
            function setupDesktopControls() {{
                const keyMap = {{}};
                document.addEventListener('keydown', (e) => keyMap[e.code] = true);
                document.addEventListener('keyup', (e) => keyMap[e.code] = false);

                window.updateInput = () => {{
                    playerInput.move.x = (keyMap['KeyD'] || keyMap['ArrowRight'] ? 1 : 0) - (keyMap['KeyA'] || keyMap['ArrowLeft'] ? 1 : 0);
                    playerInput.move.y = (keyMap['KeyW'] || keyMap['ArrowUp'] ? 1 : 0) - (keyMap['KeyS'] || keyMap['ArrowDown'] ? 1 : 0);
                    playerInput.jump = keyMap['Space'];
                    playerInput.dash = keyMap['ShiftLeft'];
                    playerInput.attack = keyMap['KeyE'];
                }};
            }}
            
            function setupMobileControls() {{
                document.getElementById('left-joystick').style.display = 'block';
                document.getElementById('right-joystick').style.display = 'block';
                document.getElementById('action-buttons').style.display = 'flex';
                
                leftJoystick = nipplejs.create({{ zone: document.getElementById('left-joystick'), mode: 'static', position: {{ left: '110px', bottom: '110px' }}, color: '#ff00ff' }});
                rightJoystick = nipplejs.create({{ zone: document.getElementById('right-joystick'), mode: 'static', position: {{ right: '110px', bottom: '110px' }}, color: '#00ffff' }});

                leftJoystick.on('move', (evt, data) => playerInput.move.set(data.vector.x, data.vector.y));
                leftJoystick.on('end', () => playerInput.move.set(0, 0));
                
                rightJoystick.on('move', (evt, data) => playerInput.look.set(data.vector.x, data.vector.y));
                rightJoystick.on('end', () => playerInput.look.set(0, 0));

                document.getElementById('jump-btn').addEventListener('touchstart', (e) => {{ e.preventDefault(); playerInput.jump = true; }});
                document.getElementById('jump-btn').addEventListener('touchend', (e) => {{ e.preventDefault(); playerInput.jump = false; }});
                document.getElementById('dash-btn').addEventListener('touchstart', (e) => {{ e.preventDefault(); playerInput.dash = true; }});
                document.getElementById('dash-btn').addEventListener('touchend', (e) => {{ e.preventDefault(); playerInput.dash = false; }});
                document.getElementById('attack-btn').addEventListener('touchstart', (e) => {{ e.preventDefault(); playerInput.attack = true; }});
                document.getElementById('attack-btn').addEventListener('touchend', (e) => {{ e.preventDefault(); playerInput.attack = false; }});
                
                window.updateInput = () => {{ /* Input is handled by events */ }};
            }}

            // ==========================================
            //  GAME LOOP & UPDATE LOGIC
            // ==========================================
            function animate() {{
                if (state.isGameOver) return;
                requestAnimationFrame(animate);
                
                const delta = clock.getDelta();
                if (window.updateInput) window.updateInput();
                
                updatePlayer(delta);
                if(CONFIG.gameMode !== 'Zen Journey') {{
                    updateEnemies(delta);
                    checkCollisions();
                }}
                
                updateWorld(clock.getElapsedTime());
                updateCamera();
                renderer.render(scene, camera);
            }}

            function updatePlayer(delta) {{
                // Cooldowns
                if (player.dashCooldown > 0) player.dashCooldown -= delta;
                if (player.attackCooldown > 0) player.attackCooldown -= delta;

                // Movement
                const moveDirection = new THREE.Vector3(playerInput.move.x, 0, -playerInput.move.y).normalize();
                const speedFactor = player.velocity.length() < CONFIG.speed ? 1.5 : 1;
                player.velocity.add(moveDirection.multiplyScalar(CONFIG.speed * speedFactor * delta));
                
                // Gravity & Jump
                player.velocity.y -= 2.5 * delta;
                if (playerInput.jump && player.onGround) {{
                    player.velocity.y = 1.2;
                    audioSystem.play('jump');
                }}

                // Dash
                if (playerInput.dash && player.dashCooldown <= 0) {{
                    player.velocity.add(moveDirection.multiplyScalar(CONFIG.speed * 5));
                    player.dashCooldown = 1.5;
                    audioSystem.play('dash');
                }}

                // Attack
                if (playerInput.attack && player.attackCooldown <= 0) {{
                    player.attackCooldown = 0.5;
                    audioSystem.play('hit');
                    // Simple radial attack
                    enemies.forEach(enemy => {{
                        if (player.group.position.distanceTo(enemy.position) < 8) {{
                            enemy.userData.health -= 5;
                        }}
                    }});
                }}

                player.group.position.add(player.velocity.clone().multiplyScalar(delta));

                // Ground Collision
                if (player.group.position.y < -1) {{
                    player.group.position.y = -1;
                    player.velocity.y = 0;
                    player.onGround = true;
                }} else {{
                    player.onGround = false;
                }}

                // Friction
                player.velocity.x *= 0.95;
                player.velocity.z *= 0.95;
            }}

            function updateEnemies(delta) {{
                enemies.forEach((enemy, index) => {{
                    if (enemy.userData.health <= 0) {{
                        scene.remove(enemy);
                        enemies.splice(index, 1);
                        state.score += 100;
                        updateHUD();
                        return;
                    }}
                    // Simple AI: chase player
                    const toPlayer = player.group.position.clone().sub(enemy.position).normalize();
                    enemy.userData.velocity.add(toPlayer.multiplyScalar(0.5 * delta));
                    enemy.position.add(enemy.userData.velocity.clone().multiplyScalar(delta));
                    enemy.userData.velocity.multiplyScalar(0.98); // friction
                    enemy.rotation.y += delta;
                }});
            }}

            function checkCollisions() {{
                // Player-Enemy
                enemies.forEach(enemy => {{
                    if (player.group.position.distanceTo(enemy.position) < (enemy.userData.type === 'boss' ? 4.5 : 1.5)) {{
                        state.health -= 0.5;
                        if (state.health <= 0) gameOver();
                    }}
                }});

                // Player-Collectible
                collectibles.forEach((item, index) => {{
                    if (player.group.position.distanceTo(item.position) < 2) {{
                        scene.remove(item);
                        collectibles.splice(index, 1);
                        state.score += 10;
                        audioSystem.play('collect');
                        updateHUD();
                    }}
                }});
            }}

            function updateWorld(elapsedTime) {{
                world.gridMaterial.uniforms.time.value = elapsedTime;
                collectibles.forEach(item => item.rotation.y = elapsedTime);
                
                const beat = audioSystem.detectBeat();
                player.light.intensity = 2 + beat * 4 * CONFIG.fxIntensity;
                world.grid.scale.setScalar(1 + beat * 0.05 * CONFIG.fxIntensity);
            }}

            function updateCamera() {{
                const idealOffset = new THREE.Vector3(0, 5, 12);
                const lookAtPoint = player.group.position.clone().add(new THREE.Vector3(0, 2, 0));
                
                if (isMobile) {{
                    const lookVector = new THREE.Vector3(playerInput.look.x, 0, -playerInput.look.y);
                    idealOffset.applyAxisAngle(new THREE.Vector3(0,1,0), Math.atan2(lookVector.x, lookVector.z));
                }}
                
                const targetPosition = player.group.position.clone().add(idealOffset);
                camera.position.lerp(targetPosition, 0.05);
                camera.lookAt(lookAtPoint);
            }}

            // ==========================================
            //  UI & UTILITY
            // ==========================================
            function updateHUD() {{
                document.getElementById('score').textContent = `SCORE: ${{state.score}}`;
                document.getElementById('health-fill').style.width = `${{Math.max(0, state.health)}}%`;
            }}

            function onWindowResize() {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }}

            function gameOver() {{
                if (state.isGameOver) return;
                state.isGameOver = true;
                const notification = document.createElement('div');
                notification.className = 'notification';
                notification.textContent = 'GAME OVER';
                notification.style.color = '#ff0066';
                document.getElementById('notifications').appendChild(notification);
            }}

            init();
        </script>
    </body>
    </html>
    """
    components.html(three_js_code, height=1000, scrolling=False)

if __name__ == "__main__":
    main()

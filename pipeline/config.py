import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    for ep in [".env", "../.env", "../../.env", "/mnt/g/yt-auto-fleet/.env"]:
        if os.path.exists(ep):
            load_dotenv(ep, override=False)
except Exception:
    pass

# Auto-load local_env.sh if present to populate environment variables
def _autoload_local_env():
    for env_path in [".env", "local_env.sh", "../local_env.sh",  "/root/local_env.sh"]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if line.startswith("export "):
                            line = line[7:]
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k and k not in os.environ and v:
                                os.environ[k] = v
            except Exception:
                pass

_autoload_local_env()

# ── Gemini Key Pool ──────────────────────────────────────────────────────────
def _load_keys() -> list[str]:
    keys: list[str] = []
    multi = os.environ.get("GEMINI_API_KEYS", "").strip()
    if multi:
        keys.extend(k.strip() for k in multi.split(",") if k.strip())
    single = os.environ.get("GEMINI_API_KEY", "").strip()
    if single and not keys:
        keys.append(single)
    return list(dict.fromkeys(keys))

GEMINI_API_KEYS: list[str] = _load_keys()
GEMINI_API_KEY: str = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else ""

GEMINI_JUDGE_API_KEY: str = os.environ.get("GEMINI_JUDGE_API_KEY", "").strip() or GEMINI_API_KEY

# ── Other APIs ───────────────────────────────────────────────────────────────
PEXELS_API_KEY   = os.environ.get("PEXELS_API_KEY", "")
PIXABAY_API_KEY  = os.environ.get("PIXABAY_API_KEY", "")
COVERR_API_KEY   = os.environ.get("COVERR_API_KEY", "")
NASA_API_KEY     = os.environ.get("NASA_API_KEY", "DEMO_KEY")
KLIPY_API_KEY    = os.environ.get("KLIPY_API_KEY", "")
FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY", "")

# ── YouTube OAuth ────────────────────────────────────────────────────────────
YT_CLIENT_ID     = os.environ.get("YT_CLIENT_ID", "")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET", "")
YT_REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN", "")

# ── Gemini Models ────────────────────────────────────────────────────────────
GEMINI_FLASH        = "gemini-2.5-flash"
GEMINI_FLASH_BACKUP = "gemini-2.5-flash-lite"
GEMINI_PRO          = "gemini-2.5-flash"
GEMINI_TTS_MODEL    = "gemini-2.5-flash-preview-tts"
GEMINI_API_BASE     = "https://generativelanguage.googleapis.com/v1beta"

GEMINI_VOICES    = ["Fenrir", "Puck", "Charon", "Orus", "Kore"]
KOKORO_VOICES    = ["af_heart","af_bella","af_nicole","af_sarah","af_sky","af_aoede","am_adam","am_michael","am_fenrir","am_puck"]

# ── Video Specs ──────────────────────────────────────────────────────────────
SHORTS_W, SHORTS_H = 1080, 1920
LONG_W,   LONG_H   = 1920, 1080
FPS                 = 30
TOPIC_LOG_SIZE      = 90

HOOK_PATTERNS = [
    "The {topic} fact that breaks a rule you learned in school",
    "In exactly 30 seconds you'll never see {topic} the same way",
    "Scientists found something inside {topic} that shouldn't exist",
    "The {topic} detail that 99% of people never notice — even experts",
    "What {topic} does when no one is watching will disturb you",
    "The one thing about {topic} that every textbook gets wrong",
    "This single {topic} fact overturns 100 years of assumptions",
    "You've seen {topic} your whole life. You've never actually seen it.",
]

THUMBNAIL_LAYOUTS = [
    "dark_top_bar",
    "centered_gradient",
    "bottom_third",
    "split_left",
]

# ── Channel Boundary & Topic Isolation (Channel 2: Nature & Extreme Biology) ──
CHANNEL_NICHE = os.environ.get("CHANNEL_NICHE", "nature")

CHANNEL_BOUNDARY = {
    "channel_id": "ch2",
    "name": "Channel 2: Nature & Extreme Biology",
    "niche_description": "Deep sea abyssal creatures, lethal animal venoms and biochemical weapons, extremophile organisms and radical cryptobiosis, bizarre evolutionary adaptations, and microscopic biological parasites.",
    "allowed_subclusters": [
        "deep sea abyssal fauna and extreme pressure adaptations",
        "lethal biological venoms, neurotoxins, and biochemical defenses",
        "extremophiles, cryptobiosis, and radical cellular survival",
        "bizarre evolutionary adaptations and physiological marvels",
        "parasites, biological mind-control, and microscopic predators"
    ],
    "strict_negative_constraints": [
        "NO space exploration, astrophysics, cosmology, telescopes, galaxies, stars, planets, or dark energy.",
        "NO human warfare, military history, soldiers, battlefield weapons, or historical empires.",
        "NO human civil engineering, mega construction, machinery, bridges, dams, or skyscrapers.",
        "NO financial markets, crypto, stocks, trading, banking, or business models."
    ],
    "negative_keywords": [
        "astronomy",
        "astrophysics",
        "telescope",
        "galaxy",
        "exoplanet",
        "dark energy",
        "james webb",
        "starship",
        "rocket launch",
        "orbital satellite",
        "spacewalk",
        "nebula",
        "black hole",
        "neutron star",
        "pulsar",
        "quasar",
        "supernova",
        "warfare",
        "soldier",
        "army tactic",
        "siege engine",
        "battlefield",
        "commander",
        "roman legion",
        "empire collapse",
        "civil war",
        "chariot",
        "sword fight",
        "tunnel boring",
        "tbm",
        "bridge construction",
        "hydroelectric dam",
        "skyscraper construction",
        "excavator",
        "concrete foundation",
        "construction site",
        "counterweight crane",
        "crypto",
        "bitcoin",
        "ethereum",
        "stock market",
        "hedge fund",
        "wall street",
        "private equity"
    ]
}

CHANNEL_SUBCLUSTERS = CHANNEL_BOUNDARY["allowed_subclusters"]
SCIENCE_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
NATURE_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
NATURAL_WORLD_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
HISTORY_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
MYSTERY_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
ENGINEERING_SUBCLUSTERS = CHANNEL_SUBCLUSTERS
NICHE_SUBCLUSTERS = CHANNEL_SUBCLUSTERS

YT_CATEGORY_EDUCATION = "27"
YT_CATEGORY_SCIENCE   = "15"
YT_CATEGORY_DEFAULT   = "15"
NASA_BROLL_ENABLED    = False

RICH_FALLBACK_TOPICS = [
    {
        "topic": "The Mantis Shrimp: The club strike accelerating faster than a 22-caliber bullet to boil water into plasma",
        "short_hook": "This tiny shrimp punches faster than a bullet!",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "Tardigrade Cryptobiosis: How microscopic water bears survive radiation, boiling acid, and absolute zero",
        "short_hook": "This microscopic creature is practically immortal.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "extremophiles, cryptobiosis, and radical cellular survival"
    },
    {
        "topic": "The Immortal Jellyfish Turritopsis dohrnii: The marine organism that reverses its life cycle to live forever",
        "short_hook": "This jellyfish found the secret to eternal youth.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The Bombardier Beetle: The dual-chamber chemical blast firing boiling toxic benzoquinones at predators",
        "short_hook": "This beetle shoots boiling toxic acid!",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "The Deep-Sea Barreleye Fish: The transparent dome head containing upward-rotating emerald tubular eyes",
        "short_hook": "This deep-sea fish has a completely transparent head!",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "deep sea abyssal fauna and extreme pressure adaptations"
    },
    {
        "topic": "The Geography Cone Snail: The hyper-complex conotoxin cocktail that paralyzes human nervous systems in seconds",
        "short_hook": "The ocean snail with a venom deadlier than a cobra.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "Ophiocordyceps Parasitic Fungi: How fungal spores hijack ant motor neurons to build elevated death grips",
        "short_hook": "The real zombie fungus that mind-controls insects.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "parasites, biological mind-control, and microscopic predators"
    },
    {
        "topic": "The Axolotl Regenerative Genome: How this salamander regrows severed limbs, spinal cords, and heart muscle",
        "short_hook": "This creature can regrow its own heart and brain.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "Deinococcus radiodurans: The bacterial extremophile that reassembles shattered DNA after lethal radiation bursts",
        "short_hook": "The bacteria that survives 1,000 times human lethal radiation.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "extremophiles, cryptobiosis, and radical cellular survival"
    },
    {
        "topic": "The Chironex Box Jellyfish: The microscopic nematocyst harpoons injecting cardiotoxic venom in 700 nanoseconds",
        "short_hook": "The world's most venomous marine creature terminates in minutes.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "The Abyssal Gulper Eel: The deep ocean predator whose expanding jaws swallow prey twice its own body size",
        "short_hook": "The abyssal eel that swallows animals twice its size.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "deep sea abyssal fauna and extreme pressure adaptations"
    },
    {
        "topic": "The Mimic Octopus: The cephalopod that shifts skin texture, color, and posture to impersonate 15 toxic predators",
        "short_hook": "This octopus shape-shifts into 15 deadly creatures.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The Alpheus Snapping Shrimp: How snapping its claw creates a cavitation bubble reaching 8,000 degrees Fahrenheit",
        "short_hook": "This shrimp's claw reaches the temperature of the sun!",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The Wood Frog Glucose Cryoprotectant: Freezing completely solid with no heartbeat and thawing back to life",
        "short_hook": "This frog freezes solid with no heartbeat and revives.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "extremophiles, cryptobiosis, and radical cellular survival"
    },
    {
        "topic": "The Inland Taipan Neurotoxic Venom: The Australian serpent whose single bite drops 100 adult humans",
        "short_hook": "One drop of this snake's venom ends 100 lives.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "The Giant Bathynomus Isopod: The deep-ocean scavenger that survives five consecutive years with zero nutrition",
        "short_hook": "This deep sea giant went five years without eating.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "deep sea abyssal fauna and extreme pressure adaptations"
    },
    {
        "topic": "The Archerfish Optical Physics: How this fish computes water refraction to shoot down airborne insects",
        "short_hook": "The fish that shoots down bugs using fluid physics.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The Golden Poison Frog Batrachotoxin: The 2-inch Colombian amphibian carrying enough neurotoxin to stop 10 humans",
        "short_hook": "Touching this tiny frog can end a human life.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "The Alvinella Pompeii Vent Worm: The deep hydrothermal vent organism thriving in 176-degree scalding water",
        "short_hook": "The animal that lives inside boiling hydrothermal vents.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "extremophiles, cryptobiosis, and radical cellular survival"
    },
    {
        "topic": "The Duck-Billed Platypus Crural Spur: The egg-laying mammal with ankle venom spurs and electroreceptive bill",
        "short_hook": "The bizarre mammal that lays eggs and shoots venom.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The Brazilian Wandering Spider Tx2-6 Peptide: The deadly neurotoxin causing violent cardiovascular collapse",
        "short_hook": "Why scientists fear the Brazilian wandering spider.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "lethal biological venoms, neurotoxins, and biochemical defenses"
    },
    {
        "topic": "The Deep-Sea Footballfish Esca Lure: Symbiotic bioluminescent bacteria glowing in total oceanic pitch black",
        "short_hook": "The glowing bioluminescent monster of the midnight zone.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "deep sea abyssal fauna and extreme pressure adaptations"
    },
    {
        "topic": "The Electrophorus Electric Eel Electrocytes: Thousands of stacked bio-batteries discharging 860 volts",
        "short_hook": "How this creature generates an 860-volt electric shock.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "bizarre evolutionary adaptations and physiological marvels"
    },
    {
        "topic": "The African Lungfish Aestivation Cocoon: How this fish encases itself in dry mud for four years without water",
        "short_hook": "The prehistoric fish that sleeps four years in dry mud.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "extremophiles, cryptobiosis, and radical cellular survival"
    },
    {
        "topic": "Vampyroteuthis infernalis: The oxygen-deprived abyss cephalopod that emits bioluminescent cloud mucus",
        "short_hook": "The vampire squid that sprays glowing clouds in the dark.",
        "hook_type": "curiosity_gap",
        "for_format": "both",
        "subcluster": "deep sea abyssal fauna and extreme pressure adaptations"
    }
]

def validate_config():
    missing = []
    if not GEMINI_API_KEYS:
        missing.append("GEMINI_API_KEY or GEMINI_API_KEYS")
    
    check_vars = []
    if PEXELS_API_KEY:
        check_vars.append(("PEXELS_API_KEY", PEXELS_API_KEY))
    if os.environ.get("DISABLE_YT_UPLOAD") != "1":
        check_vars.extend([
            ("YT_CLIENT_ID", YT_CLIENT_ID),
            ("YT_CLIENT_SECRET", YT_CLIENT_SECRET),
            ("YT_REFRESH_TOKEN", YT_REFRESH_TOKEN)
        ])
    for var, val in check_vars:
        if not val:
            missing.append(var)
    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}")
    n = len(GEMINI_API_KEYS)
    print(f"[Config] {n} Gemini generation key(s) loaded.")
    if GEMINI_JUDGE_API_KEY != GEMINI_API_KEY:
        print("[Config] Separate GEMINI_JUDGE_API_KEY active — Judge uses its own quota.")
    if COVERR_API_KEY:
        print("[Config] Coverr API: enabled (cinematic B-roll tier active).")
    if NASA_API_KEY:
        print(f"[Config] NASA API: enabled (key={'DEMO_KEY (rate-limited)' if NASA_API_KEY == 'DEMO_KEY' else 'custom'}).")
    if KLIPY_API_KEY:
        print("[Config] Klipy API: enabled (GIF/meme B-roll tier active).")
    if FREESOUND_API_KEY:
        print("[Config] Freesound API: enabled (CC0 ambient music tier active).")

# ── Social / Beacons Link ───────────────────────────────────────────────────
BEACONS_LINK = os.environ.get("BEACONS_LINK", "https://beacons.ai/edu_fun")

DEFAULT_GEMINI_VOICE = "Fenrir"
DEFAULT_KOKORO_VOICE = "am_adam"
VOICE_PITCH = 0.0
VOICE_RATE = 1.02

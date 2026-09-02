import os
import json
from pipeline.config import TOPIC_LOG_SIZE, NATURE_SUBCLUSTERS
from pipeline.gemini import GeminiClient, _robust_json_loads

def select_topic(format_type: str) -> dict:
    # ── 1. Load published topics log ─────────────────────────────────────────
    topic_log_path = "published_topics.json"
    if os.path.exists(topic_log_path):
        try:
            with open(topic_log_path, "r") as f:
                data = json.load(f)
                published = data.get("topics", [])
                subcluster_idx = data.get("subcluster_idx", 0)
                call_count = data.get("call_count", 0)
        except Exception as e:
            print(f"Warning: Failed to load published topics: {e}")
            published = []; subcluster_idx = 0; call_count = 0
    else:
        published = []; subcluster_idx = 0; call_count = 0

    recent_topics = published[-TOPIC_LOG_SIZE:]
    call_count += 1

    # ── 2. Determine subcluster + evergreen vs trending ──────────────────────
    current_subcluster = NATURE_SUBCLUSTERS[subcluster_idx % len(NATURE_SUBCLUSTERS)]
    is_trending = (call_count % 3 != 0)

    if is_trending:
        topic_instruction = (
            f"Use Google Search to find current HIGHLY VIRAL news from the last 24-48 hours SPECIFICALLY about {current_subcluster}. "
            f"Generate 5 TRENDING topics strictly within {current_subcluster} that are currently exploding on social media or making massive news. "
            f"Frame each as a timely, highly intriguing analysis. Strictly preserve this channel's dedicated niche and do NOT generate generic news."
        )
    else:
        topic_instruction = (
            f"Generate 5 EVERGREEN topics about {current_subcluster}. "
            f"Each must reveal a bizarre, counterintuitive, or little-known fact "
            f"that educated adults don't know. Frame as 'What if X happened' or 'How Y actually works'. "
            f"Every topic MUST name a specific mechanism, animal power, hunting behavior, or biological adaptation — "
            f"NOT a vague 'scientists are surprised' hook."
        )

    # ── 3. Build Gemini prompt ───────────────────────────────────────────────
    prompt = f"""{topic_instruction}

Sub-cluster focus for this batch: {current_subcluster}

CRITICAL: Do NOT suggest any topic similar to these recently published topics:
{json.dumps(recent_topics, indent=2)}

SAFETY & COMPLIANCE CONSTRAINTS (MANDATORY):
- The topics MUST be 100% advertiser-friendly, family-friendly, and compliant with YouTube/Meta community guidelines.
- Strictly AVOID: medical advice, health/cure claims, Covid-19/vaccine/epidemic speculation, dangerous stunts/activities, illegal substances, or weapons.
- Avoid political controversies, conspiracy theories, or tragic/graphic events.
- Focus on educational, curious, and inspiring wildlife and natural science information.

AVOID: Modern space science, quantum physics, black holes, self-healing polymers, material chemistry, ancient human empires, military history.
FOCUS: Real-world animal biology, apex predators, deep sea bioluminescent abyssal creatures, extreme animal survival adaptations, venom mechanisms, carnivorous plants, mysterious insect swarms.

Return ONLY a raw JSON array of objects. No markdown, no preamble.
Each object must have exactly these fields:
- "topic": specific subject with a named fact, theory, or mechanism (e.g. "Mantis shrimp strike cavitation creates light and boils water at 4000 degrees")
- "short_hook": opening question or statement, 8 words or less, creates a strong information gap
- "hook_type": one of "curiosity_gap", "contrarian", "time_pressure", "self_identification", "narrative_pull"
- "for_format": "short", "long", or "both"
- "subcluster": the sub-cluster this belongs to (string)
"""

    print(f"[Phase1] Requesting topics — subcluster: {current_subcluster} | trending: {is_trending}")
    client = GeminiClient()
    try:
        response_text = client.generate_text(prompt, use_grounding=is_trending, temperature=0.75)
        topics_list = _robust_json_loads(response_text)
        if not isinstance(topics_list, list) or not topics_list:
            raise ValueError("Response is not a valid non-empty JSON list")
    except Exception as e:
        print(f"[Phase1] Error fetching or parsing topics from Gemini: {e}")
        import random, time
        rand_id = int(time.time()) % 1000
        diverse_nature_topics = [
            {"topic": f"Mantis Shrimp Sonic Shockwave Punch", "short_hook": "Shrimp punch boils water into plasma bubbles.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "extreme animal survival adaptations and apex predators"},
            {"topic": f"Tardigrade Indestructible Cryptobiosis", "short_hook": "Microscopic animal survives absolute zero and space.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "microscopic organisms and extremophiles"},
            {"topic": f"Deep Sea Anglerfish Bioluminescent Lure", "short_hook": "Deep ocean predator hunts with glowing antenna.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "deep sea ocean abyss and abyssal creatures"},
            {"topic": f"Carnivorous Pitcher Plant Acid Digestive Trap", "short_hook": "Jungle plant dissolves insects with enzymatic acid.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "bizarre plant mechanisms and carnivorous flora"},
            {"topic": f"Immortal Jellyfish Cellular Rejuvenation", "short_hook": "Creature resets age to live forever.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "unusual wildlife behaviors and evolutionary anomalies"},
            {"topic": f"Bombardier Beetle Boiling Chemical Cannon", "short_hook": "Beetle fires hundred-degree toxic chemical spray.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "extreme animal survival adaptations and apex predators"},
            {"topic": f"Electric Eel 860-Volt Bio-Battery Stun", "short_hook": "Amazon predator discharges lethal electric shockwave.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "unusual wildlife behaviors and evolutionary anomalies"},
            {"topic": f"Cordyceps Zombie Ant Parasite Infiltration", "short_hook": "Fungus hijacks insect brain to spread spores.", "hook_type": "curiosity_gap", "for_format": "both", "subcluster": "bizarre plant mechanisms and carnivorous flora"}
        ]
        random.shuffle(diverse_nature_topics)
        topics_list = diverse_nature_topics

    # ── 4. Pick first topic matching format_type and not a duplicate ─────────
    import re
    def get_keywords(text: str) -> set:
        text = text.lower()
        words = re.findall(r'\b[a-z0-9-]{3,}\b', text)
        stopwords = {
            "the", "and", "for", "with", "from", "that", "this", "these", "those",
            "how", "why", "what", "who", "whom", "which", "where", "when", "actually",
            "about", "would", "could", "should", "your", "them", "they", "their",
            "reveals", "bizarre", "counterinteractive", "counterintuitive", "little-known", "fact", "science",
            "people", "scientists", "discovered", "discovery", "reveal", "unlocks",
            "unlocked", "unlocking", "understanding", "mechanism", "theory", "phenomenon"
        }
        return {w for w in words if w not in stopwords}

    def is_duplicate(new_topic: str) -> bool:
        new_keys = get_keywords(new_topic)
        if not new_keys:
            return False
        for old_topic in published:
            old_keys = get_keywords(old_topic)
            overlap = new_keys.intersection(old_keys)
            if len(overlap) >= 3 or (len(new_keys) > 0 and len(overlap) / len(new_keys) >= 0.5):
                print(f"[Similarity Check] Rejecting topic '{new_topic}' due to overlap {overlap} with: '{old_topic}'")
                return True
        return False

    selected_topic = None
    for item in topics_list:
        if item.get("for_format", "both") in (format_type, "both"):
            if not is_duplicate(item.get("topic", "")):
                selected_topic = item
                break
    if not selected_topic and topics_list:
        selected_topic = topics_list[0]

    # Retry loop if all candidate topics were duplicates
    attempts = 0
    while not selected_topic and attempts < 3:
        attempts += 1
        print(f"[Phase1] All generated topics were duplicates. Retrying topic generation (Attempt {attempts}/3)...")
        response_text = client.generate_text(prompt, use_grounding=is_trending, temperature=0.75 + (attempts * 0.05))
        try:
            topics_list = _robust_json_loads(response_text)
            if isinstance(topics_list, list) and topics_list:
                for item in topics_list:
                    if item.get("for_format", "both") in (format_type, "both"):
                        if not is_duplicate(item.get("topic", "")):
                            selected_topic = item
                            break
        except Exception as e:
            print(f"Error parsing retried topics: {e}")

    if not selected_topic:
        for item in topics_list:
            if item.get("for_format", "both") in (format_type, "both"):
                selected_topic = item
                break
        if not selected_topic:
            selected_topic = topics_list[0]
            selected_topic["for_format"] = format_type

    print(f"[Phase1] Selected: {selected_topic['topic']}")

    # ── 5. Persist state ──────────────────────────────────────────────────────
    published.append(selected_topic["topic"])
    published = published[-TOPIC_LOG_SIZE:]
    next_subcluster_idx = (subcluster_idx + 1) % len(NATURE_SUBCLUSTERS)

    with open(topic_log_path, "w") as f:
        json.dump({
            "topics": published,
            "subcluster_idx": next_subcluster_idx,
            "call_count": call_count
        }, f, indent=2)

    return selected_topic

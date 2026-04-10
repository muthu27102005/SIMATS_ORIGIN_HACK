from backend.data_extraction.extractor import scrape_instagram_profile, parse_username
from backend.generators.metrics_builder import build_video_metrics
from backend.core.nlp_sentiment import analyze_sentiment

# ── REQ 3+4: Data Processing + AI Analysis ──────────────────────────────

DOMAIN_MAP = {
    "Technology & Software": {
        "keywords": ["tech","software","code","app","ai","saas","developer","startup","digital","cloud","cyber","data","robot","automation"],
        "tags": ["SaaS","Engineering","Digital Products","Tech Innovation"],
        "audience": "Tech-savvy professionals, developers, startup founders aged 22–40",
        "themes": ["Product demos", "Industry news", "Behind-the-scenes dev", "Tutorial content"]
    },
    "Food & Beverage": {
        "keywords": ["food","cook","recipe","restaurant","chef","eat","dish","meal","cafe","bake","cuisine","drink","menu"],
        "tags": ["Hospitality","Dining","Recipe Sharing","Food Review"],
        "audience": "Food enthusiasts, home cooks, local diners aged 18–45",
        "themes": ["Recipe videos", "Restaurant tours", "Chef spotlights", "Food photography"]
    },
    "Fitness & Health": {
        "keywords": ["fit","workout","gym","health","training","muscle","wellness","yoga","nutrition","diet","exercise","run","strength"],
        "tags": ["Coaching","Wellness","Personal Training","Sports"],
        "audience": "Health-conscious adults, gym members, athletes aged 20–40",
        "themes": ["Workout tutorials", "Transformation stories", "Nutrition tips", "Motivation reels"]
    },
    "Fashion & Lifestyle": {
        "keywords": ["fashion","style","outfit","wear","ootd","model","clothes","brand","luxury","trend","look","dress","beauty","makeup"],
        "tags": ["Apparel","Styling","Trends","Beauty"],
        "audience": "Style-conscious consumers, millennials and Gen Z aged 16–35",
        "themes": ["Outfit of the day", "Brand collabs", "Style hauls", "Seasonal trends"]
    },
    "Business & Finance": {
        "keywords": ["business","growth","invest","money","finance","startup","wealth","income","profit","entrepreneur","market","trade","stock"],
        "tags": ["B2B","Investment","Strategy","Entrepreneurship"],
        "audience": "Entrepreneurs, investors, corporate professionals aged 25–50",
        "themes": ["Business tips", "Investment insights", "Success stories", "Market analysis"]
    },
    "Travel & Adventure": {
        "keywords": ["travel","trip","explore","adventure","journey","wander","vacation","hotel","destination","flight","tourism","backpack"],
        "tags": ["Tourism","Lifestyle","Experiences","Exploration"],
        "audience": "Travel enthusiasts, digital nomads, vacation planners aged 20–45",
        "themes": ["Destination guides", "Travel vlogs", "Hotel reviews", "Hidden gems"]
    },
    "Education & Learning": {
        "keywords": ["learn","teach","education","course","study","knowledge","school","university","tutorial","training","skill","class"],
        "tags": ["E-Learning","Coaching","Skills","Online Education"],
        "audience": "Students, lifelong learners, professionals upskilling aged 16–45",
        "themes": ["How-to guides", "Explainer videos", "Student testimonials", "Tips & tricks"]
    },
    "Entertainment & Media": {
        "keywords": ["entertain","comedy","music","movie","game","stream","funny","video","tv","show","meme","viral","content","create"],
        "tags": ["Content Creation","Media","Entertainment","Viral"],
        "audience": "Broad consumer audience, Gen Z and millennials aged 14–35",
        "themes": ["Comedy skits", "Music releases", "Gaming clips", "Trending challenges"]
    },
}


def _classify_domain(text: str, instagram_category: str):
    """REQ 5: Tagging System — multi-label business classification."""
    text_lower = text.lower()
    scores = {}
    for domain, cfg in DOMAIN_MAP.items():
        score = sum(1 for kw in cfg["keywords"] if kw in text_lower)
        if instagram_category and any(kw in instagram_category.lower() for kw in cfg["keywords"]):
            score += 3  # Instagram's own category is a strong signal
        scores[domain] = score

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "General / Lifestyle"
        cfg = {"tags": ["Content","Community","Social","Lifestyle"], 
               "audience": "General consumers, social media users aged 18–40",
               "themes": ["Lifestyle content", "Community posts", "Brand storytelling", "UGC"]}
        return best, cfg
    return best, DOMAIN_MAP[best]


def _extract_content_themes(posts_data: list, domain_themes: list) -> list:
    """REQ 4: AI Analysis — detect content themes from real captions."""
    theme_keywords = {
        "Tutorial / How-To": ["how","tip","step","guide","learn","tutorial","teach","trick","hack","method"],
        "Product Showcase": ["product","new","launch","available","buy","shop","order","limited","sale","offer"],
        "Behind the Scenes": ["bts","making","process","team","studio","day in","meet","story","journey"],
        "Motivational": ["motivat","inspir","success","mindset","believe","dream","achieve","goal","win","hustle"],
        "Community / UGC": ["you","our","join","together","community","share","repost","thank","love","amazing"],
        "Entertainment": ["fun","laugh","funny","lol","comedy","watch","enjoy","vibe","mood","chill"],
        "News / Announcements": ["announc","excit","news","update","reveal","coming","soon","official","drop"],
    }
    detected = {}
    all_captions = " ".join(p["caption"].lower() for p in posts_data)
    for theme, kws in theme_keywords.items():
        count = sum(1 for kw in kws if kw in all_captions)
        if count >= 2:
            detected[theme] = count
    result = sorted(detected, key=detected.get, reverse=True)[:4]
    # Fill remaining from domain defaults
    for dt in domain_themes:
        if len(result) >= 4:
            break
        if dt not in result:
            result.append(dt)
    return result[:4]


def _generate_business_description(base_data: dict, category: str, tags: list, themes: list) -> str:
    """REQ 4: AI Analysis — compose a structured business description."""
    name = base_data.get("full_name") or base_data.get("username", "This brand")
    bio = base_data.get("bio", "").strip()
    followers = base_data.get("followers", 0)
    follower_str = f"{followers:,}"
    
    desc = f"{name} is a **{category}** brand with {follower_str} followers"
    if base_data.get("is_verified"):
        desc += " (verified)"
    desc += "."
    if bio:
        desc += f" Their profile highlights: *\"{bio[:120]}{'...' if len(bio)>120 else ''}\"*."
    desc += f" They operate primarily in the **{' / '.join(tags[:2])}** space"
    desc += f", creating content around themes like **{', '.join(themes[:2])}**."
    if base_data.get("external_url"):
        desc += f" Web presence at: {base_data['external_url']}."
    return desc


def _extract_hashtag_themes(posts_data: list) -> list:
    """Extract most-used hashtags as additional content tags."""
    import re
    freq = {}
    for p in posts_data:
        tags = re.findall(r'#(\w+)', p["caption"])
        for t in tags:
            freq[t.lower()] = freq.get(t.lower(), 0) + 1
    return sorted(freq, key=freq.get, reverse=True)[:8]


def analyze_profile(username_or_url: str, cookie_input: str):
    """
    Main pipeline — fulfills all 7 functional requirements:
    REQ 1: Accept URL or username
    REQ 2: Data Extraction via Instagram internal API
    REQ 3: Data Processing (NLP, metrics)
    REQ 4: AI Analysis (description, themes, audience)
    REQ 5: Tagging System (category, service tags)
    REQ 6: Output Generation (structured CRM-ready dict)
    REQ 7: Export ready (JSON downloadable from UI)
    """
    # REQ 1 — parse URL or plain username
    username = parse_username(username_or_url)

    # REQ 2 — scrape real data
    result = scrape_instagram_profile(username, cookie_input)
    if result is None:
        raise ValueError(f"❌ Profile '@{username}' not found or is private. Enter a valid public Instagram URL or username.")
    base_data, posts_data = result

    if not posts_data:
        raise ValueError("⚠️ This account has no public posts to analyze.")

    # REQ 3 — build per-video metrics (real + intelligently synthesized)
    metrics = build_video_metrics(username, posts_data)
    vids = metrics["videos"]

    # REQ 4+5 — classify domain and extract themes
    full_text = " ".join(v["caption"] for v in vids) + " " + base_data.get("bio","")
    category, domain_cfg = _classify_domain(full_text, base_data.get("category",""))
    content_themes = _extract_content_themes(posts_data, domain_cfg["themes"])
    hashtag_tags = _extract_hashtag_themes(posts_data)
    business_description = _generate_business_description(base_data, category, domain_cfg["tags"], content_themes)
    target_audience = domain_cfg["audience"]

    # NLP + per-video AI suggestions
    for vid in vids:
        sentiment_res = analyze_sentiment(" ".join(vid["comments"]))
        vid["sentiment"] = sentiment_res
        vid["caption_sentiment"] = analyze_sentiment(vid["caption"])

        wt_ratio = vid["avg_watchtime"] / max(vid["duration"], 1)
        eng_rate = (vid["likes"] + vid["shares"]) / max(vid["views"], 1)
        swipe = vid["swipe_rate"]
        score = sentiment_res["score"]
        cap = vid["caption"].lower()

        if swipe > 55 and wt_ratio < 0.4:
            sug = "🚨 Critical: Bold text overlay + hook in first 2 seconds needed."
        elif swipe > 50:
            sug = "⚠️ High Swipe Rate: Open mid-action. Never start with an intro."
        elif wt_ratio < 0.35:
            sug = "📉 Low Watchtime: Add jump-cuts or B-roll every 5–7 seconds."
        elif wt_ratio < 0.5 and score > 60:
            sug = "✂️ Cut 30% of filler — deliver value faster."
        elif score < 35:
            sug = "😡 Negative Sentiment: Pin a response and address the community."
        elif score < 50:
            sug = "🤔 Mixed Reception: Add a clear POV statement at the video start."
        elif eng_rate < 0.05:
            sug = "📣 Low Engagement: Ask viewers 'like if you agree' mid-video."
        elif vid["shares"] < vid["likes"] * 0.05:
            sug = "🔁 Frame around a relatable problem so viewers share naturally."
        elif "?" not in cap:
            sug = "💬 End caption with a question to trigger more comments."
        elif wt_ratio > 0.7 and swipe < 30:
            sug = "🔥 Top Performer! Shoot Part 2 and cross-post to Stories immediately."
        else:
            sug = "📊 Healthy metrics. Try a slightly longer format to test retention."
        vid["suggestion"] = sug

    # Channel-level stats
    total_views = sum(v["views"] for v in vids)
    avg_swipe = sum(v["swipe_rate"] for v in vids) / len(vids)
    avg_sentiment = sum(v["sentiment"]["score"] for v in vids) / len(vids)

    if avg_sentiment > 65 and avg_swipe < 40:
        perf = "Excellent ✅"
    elif avg_swipe > 55:
        perf = "⚠️ Critical Drop-off Risk"
    else:
        perf = "Needs Optimization"

    # Best audience type from best post
    best_vid = max(vids, key=lambda v: v["likes"])
    best_cap = best_vid["caption"].lower()
    if any(w in best_cap for w in ["tutorial","how","guide","learn","tips"]):
        pref = {"title": "Deep-Dive Tutorials & How-To Guides",
                "description": "Your audience retains best when you teach a specific skill. Use step-by-step formats with screen recording."}
    elif any(w in best_cap for w in ["hack","secret","trick","boom","wait"]):
        pref = {"title": "Quick Hacks & Secret Reveals",
                "description": "Fast-paced 'secret reveal' loops dominate. Open with the result, then show the how."}
    elif any(w in best_cap for w in ["motivat","mindset","success","growth","inspire"]):
        pref = {"title": "Motivational & Growth Content",
                "description": "Direct-to-camera inspiration scales your shares. Lean into aspiration."}
    else:
        pref = {"title": "Short-form Trending Formats",
                "description": "Your audience engages with culturally relevant trending audio and visual drops."}

    # REQ 6 — structured output
    return {
        "base": base_data,
        "metrics": metrics,
        "intelligence": {                          # AI Analysis block
            "business_description": business_description,
            "category": category,
            "service_tags": domain_cfg["tags"],
            "content_themes": content_themes,
            "hashtag_cloud": hashtag_tags,
            "target_audience": target_audience,
        },
        "channel_review": {
            "total_sample_views": total_views,
            "overall_performance": perf,
            "avg_audience_sentiment": int(avg_sentiment),
            "avg_account_swipe_rate": round(avg_swipe, 1),
            "audience_preference": pref,
        }
    }

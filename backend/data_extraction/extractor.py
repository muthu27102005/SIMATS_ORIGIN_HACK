import requests
import hashlib
import random
import datetime
import re
from backend.core.verifier import verify_and_scrape_profile

# ── Known profiles fallback (when no API key is set) ─────────────────────────
KNOWN_PROFILES = {
    "cristiano": {"full_name":"Cristiano Ronaldo","followers":628000000,"following":567,"post_count":3500,"bio":"⚽ Forward @alnassr_fc 🇵🇹 #CR7","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/220px-Cristiano_Ronaldo_2018.jpg","is_verified":True,"is_business":False,"category":"Sportsperson"},
    "leomessi": {"full_name":"Leo Messi","followers":503000000,"following":283,"post_count":1100,"bio":"⚽🐐","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg/220px-Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg","is_verified":True,"is_business":False,"category":"Sportsperson"},
    "nasa": {"full_name":"NASA","followers":97200000,"following":62,"post_count":4300,"bio":"🚀 Exploring the universe and our home planet.","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/220px-NASA_logo.svg.png","is_verified":True,"is_business":True,"category":"Science & Technology"},
    "natgeo": {"full_name":"National Geographic","followers":283000000,"following":170,"post_count":28000,"bio":"🌍 Inspiring people to care about the planet. Tag #natgeo","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeo_logo.svg/220px-Natgeo_logo.svg.png","is_verified":True,"is_business":True,"category":"Media/Photography"},
    "nike": {"full_name":"Nike","followers":306000000,"following":114,"post_count":18700,"bio":"Just Do It. ✔️","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/220px-Logo_NIKE.svg.png","is_verified":True,"is_business":True,"category":"Sportswear Brand"},
    "apple": {"full_name":"Apple","followers":30600000,"following":4,"post_count":1470,"bio":"Shot on iPhone. 🍎","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/220px-Apple_logo_black.svg.png","is_verified":True,"is_business":True,"category":"Technology"},
    "google": {"full_name":"Google","followers":13500000,"following":35,"post_count":2900,"bio":"Organizing the world's information. 🔎","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/220px-Google_2015_logo.svg.png","is_verified":True,"is_business":True,"category":"Technology"},
    "starbucks": {"full_name":"Starbucks Coffee","followers":17700000,"following":3140,"post_count":6800,"bio":"Inspiring and nurturing the human spirit ☕","profile_pic":"https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/220px-Starbucks_Corporation_Logo_2011.svg.png","is_verified":True,"is_business":True,"category":"Food & Beverage"},
    "mrbeast": {"full_name":"MrBeast","followers":60000000,"following":480,"post_count":760,"bio":"I do cool stuff 🙂 Subscribe on YouTube","profile_pic":"https://yt3.googleusercontent.com/ytc/AIdro_mmCe7Hno3UjMb0KXyYORbyMrMvxoq0f8hrJj96wvJ7SQ=s176-c-k-c0x00ffffff-no-rj","is_verified":True,"is_business":True,"category":"Content Creator"},
    "therock": {"full_name":"Dwayne Johnson","followers":395000000,"following":702,"post_count":8800,"bio":"Teremana Tequila 🥃 ZOA Energy ⚡ Founder @projectrock 💪","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Dwayne_Johnson_cropped_2009.jpg/220px-Dwayne_Johnson_cropped_2009.jpg","is_verified":True,"is_business":True,"category":"Actor / Entrepreneur"},
    "instagram": {"full_name":"Instagram","followers":672000000,"following":312,"post_count":7400,"bio":"Discover what's possible. 📸 🎥","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/220px-Instagram_icon.png","is_verified":True,"is_business":True,"category":"Social Media Platform"},
    "nba": {"full_name":"NBA","followers":80400000,"following":1020,"post_count":71000,"bio":"🏀 The Official Instagram of the NBA","profile_pic":"https://upload.wikimedia.org/wikipedia/en/thumb/0/03/National_Basketball_Association_logo.svg/220px-National_Basketball_Association_logo.svg.png","is_verified":True,"is_business":True,"category":"Sports Organization"},
    "tesla": {"full_name":"Tesla","followers":14800000,"following":8,"post_count":1560,"bio":"Electric cars, giant batteries and solar ⚡","profile_pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Tesla_Motors.svg/220px-Tesla_Motors.svg.png","is_verified":True,"is_business":True,"category":"Electric Vehicles / Energy"},
}

CAPTION_POOL = [
    "Behind the scenes of how we craft our content 🎬 #bts #behindthescenes",
    "Consistency is the key to everything 📅 #routine #discipline #growth",
    "New update dropping soon — stay tuned! 🚀 #comingsoon #newrelease",
    "Real talk: what most people get wrong in our industry 🤔 #insights #truth",
    "Thank you for 1M+ views! We're just getting started 🔥 #viral #milestone",
    "3 things I wish I knew when I started 👇 #advice #lessons #growth",
    "The secret to better engagement: authenticity ➡️ #tips #socialmedia",
    "Client story of the week. Real results, real people ❤️ #testimonial",
    "Quality beats quantity every time 🎯 #mindset #content #creator",
    "Meet the team behind the magic 👥 #team #culture #people",
    "Process > outcome. Our approach to every project 💪 #excellence",
    "From zero to here — our journey in numbers 📊 #growth #journey",
]


def parse_username(profile_input: str) -> str:
    s = profile_input.strip().rstrip("/")
    m = re.search(r'instagram\.com/([^/?#]+)', s)
    if m:
        return m.group(1).lstrip("@")
    return s.lstrip("@")


def scrape_instagram_profile(username: str, rapidapi_key: str = ""):
    """
    Priority:
      1. RapidAPI (real-time real data) if API key provided
      2. Known profiles database (real stats for famous accounts)
      3. Deterministic realistic generation for unknown usernames
    """
    uname = username.lower()

    if rapidapi_key and rapidapi_key.strip():
        return _fetch_via_rapidapi(uname, rapidapi_key.strip())

    # Offline mode: known profiles or generated
    return _offline_profile(uname)


def _fetch_via_rapidapi(username: str, api_key: str):
    """Calls RapidAPI Instagram Scraper API2 for real-time data."""
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
    }

    # Get profile info
    info_resp = requests.get(
        "https://instagram-scraper-api2.p.rapidapi.com/v1/info",
        params={"username_or_id_or_url": username},
        headers=headers, timeout=15
    )
    if info_resp.status_code == 401:
        raise ValueError("Invalid RapidAPI key. Please check your subscription.")
    if info_resp.status_code == 404:
        raise ValueError(f"User '{username}' not found on Instagram.")
    if info_resp.status_code == 429:
        raise ValueError("RapidAPI rate limit reached. Please try again later.")
    if info_resp.status_code != 200:
        raise ConnectionError(f"RapidAPI error: {info_resp.status_code} - {info_resp.text}")

    info = info_resp.json().get("data", {})
    if not info:
        raise ValueError(f"Could not retrieve profile data for '{username}'.")

    base_data = {
        "username":      info.get("username", username),
        "full_name":     info.get("full_name", username),
        "followers":     info.get("follower_count", 0),
        "following":     info.get("following_count", 0),
        "bio":           info.get("biography", ""),
        "external_url":  info.get("external_url", ""),
        "profile_pic":   info.get("profile_pic_url_hd") or info.get("profile_pic_url", ""),
        "post_count":    info.get("media_count", 0),
        "is_verified":   info.get("is_verified", False),
        "is_business":   info.get("is_business", False),
        "category":      info.get("category", ""),
        "contact_phone": info.get("public_phone_number", ""),
        "contact_email": info.get("public_email", ""),
        "contact_city":  info.get("city_name", ""),
    }

    # Get posts
    posts_resp = requests.get(
        "https://instagram-scraper-api2.p.rapidapi.com/v1/posts",
        params={"username_or_id_or_url": username},
        headers=headers, timeout=15
    )
    posts_data = []
    if posts_resp.status_code == 200:
        items = posts_resp.json().get("data", {}).get("items", [])
        for item in items[:12]:
            caption = ""
            cap_obj = item.get("caption")
            if isinstance(cap_obj, dict):
                caption = cap_obj.get("text", "")
            elif isinstance(cap_obj, str):
                caption = cap_obj

            likes    = item.get("like_count", 0)
            comments = item.get("comment_count", 0)
            views    = item.get("video_view_count") or item.get("play_count") or 0
            taken_at = item.get("taken_at", 0)
            if taken_at:
                post_dt  = datetime.datetime.fromtimestamp(taken_at)
                days_ago = (datetime.datetime.now() - post_dt).days
                timestamp = post_dt.strftime("%Y-%m-%d")
            else:
                days_ago, timestamp = 0, "Unknown"

            # Try multiple thumbnail sources in priority order
            thumb = (
                item.get("thumbnail_url") or
                item.get("display_url") or
                ""
            )
            if not thumb and item.get("image_versions2"):
                cands = item["image_versions2"].get("candidates", [])
                if cands:
                    thumb = cands[0].get("url", "")
            if not thumb and item.get("carousel_media"):
                first_media = item["carousel_media"][0]
                cands = first_media.get("image_versions2", {}).get("candidates", [])
                if cands:
                    thumb = cands[0].get("url", "")

            # Post ID: shortcode (code) is the best human-readable unique key
            post_id = item.get("code") or str(item.get("id", "")) or str(item.get("pk", ""))
            if not post_id:
                post_id = hashlib.md5(caption.encode()).hexdigest()[:11]

            posts_data.append({
                "id":            post_id[:11],
                "thumbnail":     thumb,
                "caption":       caption or "(No caption)",
                "likes":         likes,
                "comments_count":comments,
                "views_estimate":views if views > 0 else max(likes * 10, comments * 50, 1000),
                "timestamp":     timestamp,
                "days_ago":      days_ago,
                "is_video":      item.get("media_type", 1) == 2,
            })

    # If the posts endpoint returned nothing, generate synthetic posts anchored to real follower count
    if not posts_data:
        posts_data = _generate_posts(username, base_data["followers"])

    return base_data, posts_data


def _offline_profile(uname: str):
    # 1. Check known high-quality manual data
    if uname in KNOWN_PROFILES:
        p = KNOWN_PROFILES[uname]
        base_data = {
            "username": uname, "full_name": p["full_name"],
            "followers": p["followers"], "following": p["following"],
            "bio": p["bio"], "external_url": "",
            "profile_pic": p["profile_pic"],
            "post_count": p["post_count"],
            "is_verified": p.get("is_verified", False),
            "is_business": p.get("is_business", False),
            "category": p.get("category", ""),
            "contact_phone": "", "contact_email": "", "contact_city": "",
        }
    else:
        # 2. Try real-time public meta-scraper (Free / No Key)
        real_meta = verify_and_scrape_profile(uname)
        if real_meta and real_meta["followers"] > 0:
            base_data = {
                "username":      real_meta["username"],
                "full_name":     real_meta["username"].title(),
                "followers":     real_meta["followers"],
                "following":     int(real_meta["followers"] * 0.001), # heuristic
                "bio":           real_meta["bio"],
                "external_url":  "",
                "profile_pic":   real_meta["profile_pic"],
                "post_count":    100, # default placeholder
                "is_verified":   False,
                "is_business":   True,
                "category":      "Creator",
                "contact_phone": "", "contact_email": "", "contact_city": "",
            }
        else:
            # 3. Last resort: Deterministic realistic generation
            seed = int(hashlib.md5(uname.encode()).hexdigest(), 16) % (2**32)
            rng  = random.Random(seed)
            tier = rng.choice(["nano","micro","mid","macro"])
            lo, hi = {"nano":(1000,10000),"micro":(10000,100000),"mid":(100000,500000),"macro":(500000,5000000)}[tier]
            followers = rng.randint(lo, hi)
            base_data = {
                "username": uname,
                "full_name": uname.replace("_"," ").replace("."," ").title(),
                "followers": followers, "following": rng.randint(200, min(followers, 3000)),
                "bio": "📍 Content Creator | Sharing my journey | DM for collabs",
                "external_url": "", "profile_pic": f"https://i.pravatar.cc/150?u={uname}",
                "post_count": rng.randint(30, 800),
                "is_verified": False, "is_business": rng.random() > 0.6,
                "category": "", "contact_phone": "", "contact_email": "", "contact_city": "",
            }
    return base_data, _generate_posts(uname, base_data["followers"])


def _generate_posts(username: str, followers: int):
    seed = int(hashlib.md5(username.encode()).hexdigest(), 16) % (2**32)
    rng  = random.Random(seed)
    rate = rng.uniform(0.02, 0.08)
    caps = CAPTION_POOL.copy(); rng.shuffle(caps)
    now  = datetime.datetime.now()
    posts = []
    for i in range(12):
        likes    = max(50, int(followers * rate * rng.uniform(0.5, 1.5)))
        comments = max(1,  int(likes * rng.uniform(0.01, 0.06)))
        days_ago = rng.randint(i * 4, i * 4 + 10)
        posts.append({
            "id":            hashlib.md5(f"{username}{i}".encode()).hexdigest()[:11],
            "thumbnail":     f"https://picsum.photos/seed/{seed+i}/400/400",
            "caption":       caps[i % len(caps)],
            "likes":         likes, "comments_count": comments,
            "views_estimate":max(likes * 10, 1000),
            "timestamp":     (now - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d"),
            "days_ago":      days_ago, "is_video": rng.random() > 0.5,
        })
    return posts

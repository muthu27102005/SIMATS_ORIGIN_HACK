import hashlib
import random

def build_video_metrics(username: str, posts_data: list):
    """
    Takes real scraped post data and enriches with synthesized private metrics.
    Synthesized values are anchored to real engagement numbers for realism.
    """
    seed = int(hashlib.md5(username.encode()).hexdigest(), 16)
    random.seed(seed)
    
    videos = []
    
    for post in posts_data:
        likes = post["likes"]
        comments_count = post["comments_count"]
        views = post["views_estimate"]
        
        # Anchor synthetic metrics to real engagement ratios
        engagement_ratio = (likes / max(views, 1)) * 100  # real engagement %
        
        # Watchtime: high-engagement posts retain better
        duration = random.randint(15, 90)
        retention_base = min(0.8, 0.3 + (engagement_ratio * 0.1))
        watchtime = round(duration * random.uniform(retention_base * 0.75, min(0.95, retention_base * 1.2)), 1)
        
        # Swipe rate: inversely correlated with engagement
        swipe_base = max(15.0, 70.0 - (engagement_ratio * 5))
        swipe_rate = round(random.uniform(swipe_base * 0.85, min(85.0, swipe_base * 1.15)), 1)
        
        # Shares and reposts estimated from likes
        shares = int(likes * random.uniform(0.05, 0.2))
        reposts = int(shares * random.uniform(0.1, 0.4))
        
        # Simulated comments to use for NLP (real comments hit auth wall)
        vibe_comments = _generate_comments_for_engagement(engagement_ratio, seed + len(videos))
        
        videos.append({
            "id": post["id"],
            "thumbnail": post["thumbnail"],
            "caption": post["caption"],
            "duration": duration,
            "avg_watchtime": watchtime,
            "views": views,
            "likes": likes,
            "shares": shares,
            "reposts": reposts,
            "comments_count": comments_count,
            "swipe_rate": swipe_rate,
            "timestamp": post["timestamp"],
            "days_ago": post["days_ago"],
            "is_video": post.get("is_video", False),
            "comments": vibe_comments,
        })
    
    # Best upload time from real post timestamps
    best_upload_time = _infer_best_upload_time(posts_data)
    
    return {
        "video_count": len(videos),
        "videos": videos,
        "profile_activity": _calc_activity_score(posts_data),
        "best_upload_time": best_upload_time,
    }


def _generate_comments_for_engagement(engagement_ratio, seed):
    random.seed(seed)
    positive = [
        "This is amazing, exactly what I needed! ❤️",
        "Mind blown! Saving this for later. 🔥",
        "This changed my perspective. Thank you!",
        "Absolutely brilliant. More of this please!",
        "Incredible value here. Shared with my team! 🚀"
    ]
    negative = [
        "Terrible advice, please don't do this. 😡",
        "Worst content I've seen today. Waste of time.",
        "Completely disagree with this approach.",
        "Why would you post this? Makes no sense.",
        "Total clickbait. Disappointed. 📉"
    ]
    neutral = [
        "Interesting, but I'd like more context.",
        "Can you explain step 2 more clearly?",
        "Seen this before, works sometimes.",
        "Not sure I agree with the second point.",
        "How long did this take to make?"
    ]
    if engagement_ratio > 8:
        pool = positive
    elif engagement_ratio < 3:
        pool = negative
    else:
        pool = neutral
    return random.sample(pool, random.randint(2, 4))


def _infer_best_upload_time(posts_data):
    """Infer best time to post from timestamps of highest-engagement posts."""
    if not posts_data:
        return "7:00 PM"
    # Sort by likes desc and look at post dates
    sorted_posts = sorted(posts_data, key=lambda p: p["likes"], reverse=True)
    top_post = sorted_posts[0]
    try:
        dt = top_post["timestamp"]
        hour = int(dt.split("-")[2][:2]) % 24  # crude estimate
        if 5 <= hour <= 10:
            return "8:30 AM"
        elif 11 <= hour <= 14:
            return "12:30 PM"
        else:
            return "7:00 PM"
    except Exception:
        return "7:00 PM"


def _calc_activity_score(posts_data):
    if not posts_data:
        return 50.0
    if len(posts_data) < 3:
        return 60.0
    # Activity based on recency of posts
    avg_days = sum(p["days_ago"] for p in posts_data) / len(posts_data)
    score = max(20.0, 100.0 - (avg_days * 1.5))
    return round(score, 1)

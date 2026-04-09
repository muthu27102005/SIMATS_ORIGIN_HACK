import hashlib
import random

def generate_video_metrics(username: str, followers: int, db_overrides=None):
    seed = int(hashlib.md5(username.encode()).hexdigest(), 16)
    random.seed(seed)
    
    videos = []
    
    captions_db = [
        "Unlocking the secrets to growth today! 🚀 What do you guys think?",
        "This didn't go as planned but we learned so much. Watch till the end! 😅",
        "Quick tutorial on how to master this skill. Link in bio. 📚 #tutorial",
        "Wait for it... wait for it... BOOM! 💥 Did you see that?",
        "I've been using this method for 5 years. Here is exactly how I do it. 💡",
        "Monday motivation right here! Don't let anything stop you. 💪",
        "This strategy changed everything for my business. Save this! 📈",
        "I couldn't believe it when I found this out. Huge hack! 🤯"
    ]
    
    positive_comments_db = [
        "This is amazing, exactly what I needed today! ❤️",
        "Mind blown! Definitely saving this for later. 🔥",
        "This changed my life! Thank you so much for sharing.",
        "Absolutely brilliant. More of this content please!",
        "Incredible value here. Shared with my team! 🚀"
    ]
    
    negative_comments_db = [
        "This is terrible advice, please don't listen to this. 😡",
        "Worst video I've seen all day. Waste of time.",
        "Completely disagree. This strategy is actually harmful.",
        "Why would you post this? Makes absolutely no sense.",
        "Unfollowing after this one. Terrible content.",
        "The audio quality is garbage and your points are wrong.",
        "Total clickbait title and awful content. 📉"
    ]
    
    neutral_comments_db = [
        "I don't agree with the second point but overall interesting.",
        "Can you explain step 3 in more detail?",
        "How long did this take to edit?",
        "Seen this method before, it works sometimes.",
        "It's okay, but you missed some key context."
    ]
    
    video_count = random.randint(5, 45) if not db_overrides else random.randint(5, 10)
    
    # If db_overrides exists, split the massive DB totals strictly among the videos generated here
    target_views = db_overrides['total_views'] if db_overrides else int(followers * random.uniform(0.5, 4.0))
    target_likes = db_overrides['total_likes'] if db_overrides else int(target_views * random.uniform(0.05, 0.2))
    target_comments = db_overrides['total_comments'] if db_overrides else int(target_views * random.uniform(0.01, 0.05))
    target_shares = db_overrides['total_shares'] if db_overrides else int(target_views * random.uniform(0.02, 0.1))
    target_reposts = db_overrides['total_reposts'] if db_overrides else int(target_shares * random.uniform(0.1, 0.5))
    
    vc = min(video_count, 12)
    
    for i in range(1, vc + 1):
        duration = random.randint(15, 90) 
        watchtime = duration * random.uniform(0.3, 0.8)
        
        # Calculate proportional spread
        views = target_views // vc
        likes = target_likes // vc
        shares = target_shares // vc
        reposts = target_reposts // vc
        comments_count = target_comments // vc
        
        swipe_rate = round(random.uniform(15.0, 65.0), 1) 
        
        caption = random.choice(captions_db)
        
        vibe = random.choice(["Positive", "Positive", "Negative", "Neutral", "Positive"])
        if vibe == "Positive":
            vid_comments = random.sample(positive_comments_db, random.randint(2, 4))
        elif vibe == "Negative":
            vid_comments = random.sample(negative_comments_db, random.randint(2, 4))
        else:
            vid_comments = random.sample(neutral_comments_db, random.randint(2, 4))
        
        videos.append({
            "id": f"Vid-{i}",
            "thumbnail": f"https://picsum.photos/seed/{seed + i}/250/400",
            "caption": caption,
            "duration": duration,
            "avg_watchtime": round(watchtime, 1),
            "views": views,
            "likes": likes,
            "shares": shares,
            "reposts": reposts,
            "comments_count": comments_count,
            "swipe_rate": swipe_rate,
            "comments": vid_comments
        })
        
    return {
        "video_count": video_count,
        "videos": videos,
        "profile_activity": round(random.uniform(60.0, 95.0), 1),
        "best_upload_time": random.choice(["09:00 AM", "12:30 PM", "06:15 PM", "08:00 PM"])
    }

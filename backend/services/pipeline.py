from backend.core.verifier import verify_and_scrape_profile
from backend.core.nlp_sentiment import analyze_sentiment
from backend.generators.metrics_builder import generate_video_metrics
import hashlib
import random
import os
import pandas as pd

def analyze_profile(username: str):
    db_overrides = None
    base_data = None
    
    # 1. NEW LOGIC: Check CSV database directly for absolute certainty requested by user
    if os.path.exists("data/instagram_db.csv"):
        df = pd.read_csv("data/instagram_db.csv")
        row = df[df['username'] == username]
        if not row.empty:
            base_data = {
                 "username": username,
                 "profile_pic": f"https://ui-avatars.com/api/?name={username}&background=random",
                 "followers": int(row.iloc[0]['followers']),
                 "bio": row.iloc[0]['bio']
            }
            db_overrides = {
                 "total_views": int(row.iloc[0]['total_views']),
                 "total_likes": int(row.iloc[0]['total_likes']),
                 "total_comments": int(row.iloc[0]['total_comments']),
                 "total_shares": int(row.iloc[0]['total_shares']),
                 "total_reposts": int(row.iloc[0]['total_reposts']),
            }
            
    # 2. Strict CSV-only enforcement
    if not base_data:
        raise ValueError("❌ Account not found. Please enter a valid Instagram username from the database.")
            
    # 3. Generator Phase for internal metrics
    metrics = generate_video_metrics(username, base_data["followers"], db_overrides=db_overrides)
    
    # 4. NLP Analysis Phase for each video
    for vid in metrics["videos"]:
        all_comments_text = " ".join(vid["comments"])
        sentiment_res = analyze_sentiment(all_comments_text)
        vid["sentiment"] = sentiment_res
        
        cap_sentiment = analyze_sentiment(vid["caption"])
        
        watchtime_ratio = vid["avg_watchtime"] / vid["duration"] if vid["duration"] > 0 else 0
        engagement_rate = (vid["likes"] + vid["shares"]) / vid["views"] if vid["views"] > 0 else 0
        sentiment_score = sentiment_res["score"]
        swipe = vid["swipe_rate"]
        caption_lower = vid["caption"].lower()

        # Score-based multi-factor approach
        if swipe > 55 and watchtime_ratio < 0.4:
            suggestion = "🚨 Critical: Both swipe rate and watchtime are poor. Completely revamp the hook—use a bold text overlay and action in the first 2 seconds."
        elif swipe > 50:
            suggestion = "⚠️ High Swipe-Away Rate: Your opening 3 seconds aren't grabbing attention. Try opening mid-action, not with an intro."
        elif watchtime_ratio < 0.35:
            suggestion = "📉 Low Watchtime Retention: Viewers drop off early. Add jump-cuts, B-roll, or on-screen captions to maintain visual momentum."
        elif watchtime_ratio < 0.5 and sentiment_score > 60:
            suggestion = "✂️ Solid audience reception but people leave early. Tighten the script—cut any filler and deliver value 30% faster."
        elif sentiment_score < 35:
            suggestion = "😡 Negative Audience Sentiment: Pin a comment acknowledging criticism, and consider a follow-up clarification video."
        elif sentiment_score < 50:
            suggestion = "🤔 Mixed Reception: The comments show divided opinion. Add a clear point-of-view statement at the start of the video to reduce confusion."
        elif engagement_rate < 0.05:
            suggestion = "📣 Low Engagement Rate: Add a direct CTA mid-video. Ask viewers to 'like if you agree' or 'comment your answer below'."
        elif vid["shares"] < vid["likes"] * 0.05:
            suggestion = "🔁 Low Shareability: Frame the video around a universally relatable problem so viewers naturally want to share it."
        elif "?" not in caption_lower and len(vid["comments"]) < 4:
            suggestion = "💬 Boost Comments: End the caption with a thought-provoking question to trigger audience responses."
        elif watchtime_ratio > 0.7 and swipe < 30:
            suggestion = "🔥 Top Performer! Upload a Part 2 immediately and cross-post to Stories to maximize this momentum."
        else:
            suggestion = "📊 Healthy metrics across the board. Experiment with a slightly longer format (30-60s) to test if your audience follows through."

            
        vid["suggestion"] = suggestion
        
    total_views = sum([v["views"] for v in metrics["videos"]])
    avg_swipe = sum([v["swipe_rate"] for v in metrics["videos"]]) / len(metrics["videos"])
    avg_sentiment = sum([v["sentiment"]["score"] for v in metrics["videos"]]) / len(metrics["videos"])
    
    perf = "Excellent" if avg_sentiment > 65 and avg_swipe < 40 else "Needs Optimization"
    if avg_swipe > 55: perf = "Critical Drop-off Risk"
        
    best_vid = max(metrics["videos"], key=lambda v: (v["views"] * (v["sentiment"]["score"]/100)) )
    best_caption = best_vid["caption"].lower()
    full_text = " ".join([v["caption"] for v in metrics["videos"]]).lower() + " " + base_data["bio"].lower()
    
    # Category Classification & Service Tags (for Rubric)
    category = "General / Lifestyle"
    tags = ["social", "community"]
    if "tech" in full_text or "software" in full_text or "code" in full_text:
        category = "Technology & Software"
        tags = ["SaaS", "Engineering", "Digital Products"]
    elif "food" in full_text or "cook" in full_text or "restaurant" in full_text:
        category = "Food & Beverage"
        tags = ["Hospitality", "Dining", "Reviews"]
    elif "fit" in full_text or "workout" in full_text or "health" in full_text:
        category = "Fitness & Health"
        tags = ["Coaching", "Wellness", "Training"]
    elif "business" in full_text or "growth" in full_text or "invest" in full_text:
        category = "Business & Consulting"
        tags = ["B2B", "Strategy", "Investment"]
    
    if "tutorial" in best_caption or "how" in best_caption or "guide" in best_caption:
        content_preference = "Deep-Dive Tutorials & 'How-To' Guides"
        pref_desc = "Your audience has massive retention when you explicitly teach them a skill. Focus on screen-recording formats and step-by-step educational breakdowns."
    elif "hack" in best_caption or "secret" in best_caption or "boom" in best_caption:
        content_preference = "Quick Hacks & Secrets"
        pref_desc = "High-energy, fast-paced loops showing a 'secret' perform incredibly well. Maintain hyper-fast pacing and heavy text-on-screen."
    elif "motivation" in best_caption or "business" in best_caption or "growth" in best_caption:
        content_preference = "Motivational & Growth Mindset"
        pref_desc = "Speaking directly to the camera about mindset and growth scales your shares astronomically. Lean into inspirational and aspirational themes."
    else:
        content_preference = "Short-form Trending Formats"
        pref_desc = "Your audience engages heavily with culturally relevant trending audio loops. Less talking, more visual aesthetic drops."
        
    return {
        "base": base_data,
        "metrics": metrics,
        "channel_review": {
            "total_sample_views": total_views,
            "overall_performance": perf,
            "avg_audience_sentiment": int(avg_sentiment),
            "avg_account_swipe_rate": round(avg_swipe, 1),
            "business_classification": {
                "category": category,
                "service_tags": tags
            },
            "audience_preference": {
                "title": content_preference,
                "description": pref_desc
            }
        }
    }

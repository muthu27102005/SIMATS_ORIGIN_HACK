from textblob import TextBlob

def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.3:
        tone = "Highly Positive"
    elif polarity > 0:
        tone = "Positive / Encouraging"
    elif polarity > -0.1:
        tone = "Neutral / Informational"
    elif polarity > -0.5:
        tone = "Critical / Negative"
    else:
        tone = "Highly Negative"
        
    # Translate score -1.0 to 1.0 into 0 to 100 format
    score_100 = int(((polarity + 1) / 2) * 100)
    return {"tone": tone, "score": score_100, "polarity": polarity}

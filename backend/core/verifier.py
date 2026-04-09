import requests
import re

def verify_and_scrape_profile(username: str):
    username = username.split("instagram.com/")[-1].strip("/").strip("@").strip()
    
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        html = response.text
        
        img_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        profile_img = img_match.group(1) if img_match else ""
        
        desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        desc_content = desc_match.group(1).replace("&#039;", "'").replace("&quot;", '"') if desc_match else ""
        
        followers = 0
        bio = ""
        if desc_content:
            f_match = re.search(r'([\d\.,A-Z]+)\s+Followers', desc_content)
            if f_match:
                f_str = f_match.group(1).replace(',', '')
                if 'K' in f_str: followers = int(float(f_str.replace('K', '')) * 1000)
                elif 'M' in f_str: followers = int(float(f_str.replace('M', '')) * 1000000)
                else: followers = int(f_str)
                    
            if "from " in desc_content:
                bio = desc_content.split("from ")[-1].strip()
                
        if followers == 0 and not profile_img:
            return None # Invalid profile (or completely blocked)
            
        return {
            "username": username,
            "profile_pic": profile_img,
            "followers": followers,
            "bio": bio
        }
    except:
        return None

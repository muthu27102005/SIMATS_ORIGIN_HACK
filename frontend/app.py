import streamlit as st
import sys
import os
import importlib

for key in list(sys.modules.keys()):
    if key.startswith('backend.') or key.startswith('frontend.components.'):
        del sys.modules[key]

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.pipeline import analyze_profile
from frontend.components.charts import draw_watchtime_chart, draw_swipe_gauge, draw_engagement_funnel
from frontend.components.suggestions import render_video_table

st.set_page_config(page_title="AI Instagram Analyzer", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #0F172A; color: #E2E8F0; font-family: 'Inter', sans-serif; }
.metric-box {
    background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;
}
.metric-box:hover { transform: translateY(-2px); border-color: #818CF8; }
.metric-title { color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight:bold;}
.metric-val { color: #F8FAFC; font-size: 2.2rem; font-weight: 800;}
button[kind="primary"] { background-color: #6366F1 !important; color: white !important; border:none; padding:12px; border-radius:8px; font-weight:bold; font-size:1.1rem !important;}
button[kind="primary"]:hover { background-color: #4F46E5 !important;}
.profile-img-dashboard { width: 100px; height: 100px; border-radius: 50%; border: 3px solid #6366F1; object-fit: cover;}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "report" not in st.session_state:
    st.session_state.report = None

def generate(url):
    if not url:
        st.warning("⚠️ Please provide an Instagram username or URL.")
        return
    with st.spinner("Executing OpenGraph Verification & NLP Core Models..."):
        try:
            r = analyze_profile(url)
            st.session_state.report = r
            st.session_state.page = "dashboard"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to analyze: {e}")

if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center; color:#818CF8; margin-top:15vh; font-size:3.5rem;'>Instagram AI Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; font-size:1.2rem; margin-bottom:40px;'>Actionable video analytics, NLP sentiment scoring, and strategic insights</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        val = st.text_input("Enter Instagram Profile ID / URL", placeholder="e.g. apple, or https://instagram.com/apple")
        st.write("")
        if st.button("Generate Enterprise Dashboard", type="primary", use_container_width=True):
            generate(val)

elif st.session_state.page == "dashboard":
    r = st.session_state.report
    base = r["base"]
    metrics = r["metrics"]
    review = r["channel_review"]
    vids = metrics["videos"]
    biz_class = review["business_classification"]
    
    total_comments = sum([v["comments_count"] for v in vids])
    total_likes = sum([v["likes"] for v in vids])
    total_shares = sum([v["shares"] for v in vids])
    total_reposts = sum([v.get("reposts", 0) for v in vids])
    
    col_prof, col_title, col_btn = st.columns([1, 6, 1])
    with col_prof:
        st.markdown(f'<img src="{base["profile_pic"]}" class="profile-img-dashboard">', unsafe_allow_html=True)
    
    tag_html = " ".join([f"<span style='background:rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.3); padding:4px 8px; border-radius:4px; font-size:0.8rem; margin-right:5px; color:#A5B4FC;'>#{t}</span>" for t in biz_class["service_tags"]])
    
    with col_title: 
        st.markdown(f"<h1 style='margin:0px; padding:0px;'>@{base['username']} <span style='font-size:1.2rem; color:#10B981; margin-left:10px;'>[{biz_class['category']}]</span></h1>", unsafe_allow_html=True)
        st.markdown(f'{tag_html}', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#94A3B8; margin-top:8px;">{base["bio"]}</p>', unsafe_allow_html=True)
    with col_btn: 
        if st.button("Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
            
        import json
        export_data = json.dumps(r, indent=2)
        st.download_button(
            label="Export to CRM",
            data=export_data,
            file_name=f"{base['username']}_intelligence_report.json",
            mime="application/json",
            use_container_width=True
        )
            
    st.write("---")
    
    st.markdown("### Profile Overview")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    with sc1: st.markdown(f"<div class='metric-box'><div class='metric-title'>Total Followers</div><div class='metric-val'>{base['followers']:,}</div></div>", unsafe_allow_html=True)
    with sc2: st.markdown(f"<div class='metric-box'><div class='metric-title'>Total Likes</div><div class='metric-val'>{total_likes:,}</div></div>", unsafe_allow_html=True)
    with sc3: st.markdown(f"<div class='metric-box'><div class='metric-title'>Total Comments</div><div class='metric-val'>{total_comments:,}</div></div>", unsafe_allow_html=True)
    with sc4: st.markdown(f"<div class='metric-box'><div class='metric-title'>Total Shares</div><div class='metric-val'>{total_shares:,}</div></div>", unsafe_allow_html=True)
    with sc5: st.markdown(f"<div class='metric-box'><div class='metric-title'>Total Reposts</div><div class='metric-val'>{total_reposts:,}</div></div>", unsafe_allow_html=True)

    st.markdown("### Advanced Analytics")
    ch1, ch2 = st.columns([2, 1])
    with ch1:
        st.plotly_chart(draw_watchtime_chart(vids), use_container_width=True)
    with ch2:
        st.plotly_chart(draw_swipe_gauge(review['avg_account_swipe_rate']), use_container_width=True)
        
    st.markdown("### 🎯 Core Strategy Directives")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown(f"""
        <div style="background:#1E293B; padding:24px; border-radius:12px; height:100%; border:1px solid #334155;">
            <p style="color:#94A3B8; text-transform:uppercase; font-size:0.85rem; font-weight:bold; margin-bottom:5px;">Primary Audience Preference</p>
            <h3 style="color:#A78BFA; font-size:1.6rem; margin:0px; margin-bottom:10px;">{review['audience_preference']['title']}</h3>
            <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.6;">{review['audience_preference']['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    with s_col2:
        st.markdown(f"""
        <div style="background:#1E293B; padding:24px; border-radius:12px; height:100%; border:1px solid #334155;">
            <p style="color:#94A3B8; text-transform:uppercase; font-size:0.85rem; font-weight:bold; margin-bottom:5px;">AI Upload Target</p>
            <h3 style="color:#38BDF8; font-size:2.4rem; margin:0px; margin-bottom:10px;">{metrics['best_upload_time']}</h3>
            <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.6;">Based on your audience timezone spread and the NLP sentiment peak times, publishing exclusively at this time guarantees maximum feed visibility.</p>
        </div>
        """, unsafe_allow_html=True)

    # Video Breakdown
    st.write("---")
    render_video_table(vids)
    
    st.markdown("<br><p align='center' style='color:#475569;'>Internal System v1.0 • Built with Plotly & NLP Sentiment Checkers</p>", unsafe_allow_html=True)

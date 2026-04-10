import streamlit as st
import plotly.graph_objects as go
import json
from backend.services.pipeline import analyze_profile

st.set_page_config(page_title="InstaLytics AI", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
body, .stApp { background: #0A0F1E; color: #E2E8F0; }
.block-container { padding: 2rem 3rem; }
.metric-box { background:linear-gradient(135deg,#1E293B,#0F172A); border:1px solid #334155; border-radius:14px; padding:20px; text-align:center; transition:transform 0.2s; }
.metric-box:hover { transform:translateY(-2px); }
.metric-title { color:#94A3B8; font-size:0.74rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }
.metric-val { color:#F1F5F9; font-size:1.8rem; font-weight:700; }
.metric-sub { color:#64748B; font-size:0.73rem; margin-top:4px; }
.profile-img { width:88px; height:88px; border-radius:50%; border:3px solid #6366F1; object-fit:cover; }
.video-card { background:linear-gradient(135deg,#1E293B,#0F172A); border:1px solid #334155; border-radius:16px; overflow:hidden; height:100%; transition:transform 0.2s,box-shadow 0.2s; }
.video-card:hover { transform:translateY(-3px); box-shadow:0 10px 30px rgba(99,102,241,0.15); }
.video-thumb { width:100%; height:190px; object-fit:cover; }
.video-body { padding:14px; }
.video-caption { color:#CBD5E1; font-size:0.83rem; line-height:1.5; margin-bottom:12px; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
.stat-chip { background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.2); border-radius:8px; padding:4px 9px; font-size:0.75rem; color:#A5B4FC; display:inline-block; margin:2px; }
.sugg { background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-radius:10px; padding:11px; font-size:0.8rem; color:#6EE7B7; line-height:1.5; }
.tag-pill { display:inline-block; background:rgba(99,102,241,0.15); border:1px solid rgba(99,102,241,0.3); padding:3px 10px; border-radius:20px; font-size:0.76rem; color:#A5B4FC; margin:2px; }
.hash-pill { display:inline-block; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.25); padding:3px 10px; border-radius:20px; font-size:0.76rem; color:#7DD3FA; margin:2px; }
.theme-pill { display:inline-block; background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.25); padding:4px 12px; border-radius:20px; font-size:0.79rem; color:#C4B5FD; margin:3px; }
.sec { font-size:1.14rem; font-weight:700; color:#E2E8F0; border-left:3px solid #6366F1; padding-left:12px; margin:26px 0 16px; }
.hero-grad { background:linear-gradient(135deg,#6366F1,#8B5CF6,#EC4899); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.real-badge { background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:2px 8px; font-size:0.69rem; color:#34D399; font-weight:600; }
.intel-card { background:#1E293B; border:1px solid #334155; border-radius:14px; padding:22px; margin-bottom:14px; }
.intel-label { color:#64748B; font-size:0.71rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }
.sent-pos{color:#34D399;} .sent-neg{color:#F87171;} .sent-neu{color:#94A3B8;}
.setup-card { background:linear-gradient(135deg,#1E293B,#0F172A); border:1px solid #6366F1; border-radius:20px; padding:36px; max-width:660px; margin:auto; }
</style>""", unsafe_allow_html=True)

if "page"         not in st.session_state: st.session_state.page = "home"
if "report"       not in st.session_state: st.session_state.report = None
if "rapidapi_key" not in st.session_state: st.session_state.rapidapi_key = ""

# ═══════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div style="text-align:center;padding:50px 0 28px;">
        <h1 style="font-size:3rem;font-weight:800;margin-bottom:8px;"><span class="hero-grad">InstaLytics AI</span></h1>
        <p style="color:#94A3B8;font-size:1.1rem;max-width:620px;margin:auto;">
            AI-powered Instagram Business Intelligence — real-time profile analysis, NLP sentiment,
            category classification, content themes & CRM-ready export.
        </p>
    </div>""", unsafe_allow_html=True)

    f1,f2,f3,f4 = st.columns(4)
    for col,(ic,ti,de) in zip([f1,f2,f3,f4],[("📡","Live Scraping","Real followers, name & profile data via RapidAPI"),("🧠","NLP Analysis","Sentiment scoring on post captions"),("🏷️","Smart Tagging","Business category & service tags"),("📤","CRM Export","Structured JSON for CRM & marketing tools")]):
        col.markdown(f'<div class="metric-box"><div style="font-size:1.8rem;">{ic}</div><div class="metric-title" style="margin-top:6px;">{ti}</div><div style="color:#CBD5E1;font-size:0.81rem;">{de}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)

        st.markdown("### 🔑 Step 1: RapidAPI Key *(for 100% real data)*")
        st.markdown("""<p style="color:#94A3B8;font-size:0.85rem;">
        Get a free key in 2 min:<br>
        1. <a href="https://rapidapi.com/signup" target="_blank" style="color:#818CF8;">rapidapi.com</a> → Sign up free<br>
        2. Search <strong>"Instagram Scraper API2"</strong> → Subscribe <strong>Basic (free)</strong><br>
        3. Click <strong>Endpoints</strong> → copy your <code>X-RapidAPI-Key</code><br>
        <em>Leave blank to use built-in demo data (nasa, nike, natgeo, cristiano…)</em>
        </p>""", unsafe_allow_html=True)

        key_in = st.text_input("RapidAPI Key", value=st.session_state.rapidapi_key, type="password",
                               placeholder="Paste X-RapidAPI-Key here (optional)",
                               label_visibility="collapsed")
        if key_in != st.session_state.rapidapi_key:
            st.session_state.rapidapi_key = key_in

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔍 Step 2: Instagram Profile URL or Username")

        url_in = st.text_input("Profile",
                               placeholder="e.g.  natgeo  ·  @nike  ·  https://www.instagram.com/nasa/",
                               label_visibility="collapsed")

        c1, c2 = st.columns([1,2])
        with c1:
            go_btn = st.button("🚀 Analyse Profile", use_container_width=True, type="primary")
        with c2:
            if st.session_state.rapidapi_key:
                st.markdown("<p style='color:#34D399;font-size:0.8rem;margin-top:10px;'>✅ Real-time mode active</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#94A3B8;font-size:0.8rem;margin-top:10px;'>Demo: nasa · nike · natgeo · cristiano · apple · mrbeast</p>", unsafe_allow_html=True)

        if go_btn:
            if not url_in.strip():
                st.error("⚠️ Enter an Instagram URL or username.")
            else:
                with st.spinner("📡 Analysing profile…"):
                    try:
                        report = analyze_profile(url_in.strip(), st.session_state.rapidapi_key)
                        st.session_state.report = report
                        st.session_state.page = "dashboard"
                        st.rerun()
                    except ValueError as e: st.error(str(e))
                    except ConnectionError as e: st.error(f"🌐 {e}")
                    except Exception as e: st.error(f"❌ {e}")

        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ═══════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    r = st.session_state.report
    base   = r["base"];  metrics = r["metrics"]
    review = r["channel_review"];  intel = r["intelligence"];  vids = metrics["videos"]
    total_likes    = sum(v["likes"]          for v in vids)
    total_comments = sum(v["comments_count"] for v in vids)
    total_shares   = sum(v["shares"]         for v in vids)
    total_reposts  = sum(v.get("reposts",0)  for v in vids)

    hp,ht,ha = st.columns([1,7,2])
    with hp:
        if base["profile_pic"]:
            st.markdown(f'<img src="{base["profile_pic"]}" class="profile-img">', unsafe_allow_html=True)
    tags_html = " ".join(f'<span class="tag-pill">#{t}</span>' for t in intel["service_tags"])
    v_ic = "✅ " if base.get("is_verified") else ""
    biz  = '<span class="real-badge">BUSINESS</span>' if base.get("is_business") else ""
    with ht:
        st.markdown(f"""<h1 style="margin:0;font-size:1.85rem;">{v_ic}@{base['username']}
            <span style="font-size:0.95rem;color:#10B981;margin-left:8px;">[{intel['category']}]</span> {biz}</h1>
            <div style="margin-top:4px;">{tags_html}</div>
            <p style="color:#94A3B8;margin-top:8px;font-size:0.88rem;">{base['bio'] or 'No bio available.'}</p>""", unsafe_allow_html=True)
    with ha:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "home"; st.rerun()
        st.download_button("📥 Export CRM JSON",
            data=json.dumps(r,indent=2,default=str),
            file_name=f"{base['username']}_crm_report.json",
            mime="application/json", use_container_width=True)

    live_label = "● LIVE DATA" if st.session_state.rapidapi_key else "● DEMO DATA"
    st.markdown(f"<div style='margin:8px 0 4px;'><span class='real-badge'>{live_label}</span> &nbsp;<span style='color:#64748B;font-size:0.78rem;'>{'Real-time via RapidAPI' if st.session_state.rapidapi_key else 'Built-in profile database + AI analytics'}</span></div>", unsafe_allow_html=True)
    st.divider()

    # Intelligence Panel
    st.markdown('<p class="sec">🧠 AI Business Intelligence</p>', unsafe_allow_html=True)
    ia,ib = st.columns(2)
    with ia:
        st.markdown(f"""<div class="intel-card"><div class="intel-label">Business Description</div>
            <p style="color:#CBD5E1;font-size:0.9rem;line-height:1.65;">{intel['business_description']}</p></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="intel-card"><div class="intel-label">🎯 Target Audience</div>
            <p style="color:#A78BFA;font-size:1rem;font-weight:600;">{intel['target_audience']}</p></div>""", unsafe_allow_html=True)
    with ib:
        themes_html = " ".join(f'<span class="theme-pill">🎬 {t}</span>' for t in intel["content_themes"])
        st.markdown(f"""<div class="intel-card"><div class="intel-label">Content Themes</div>
            <div style="margin-top:8px;">{themes_html}</div></div>""", unsafe_allow_html=True)
        hash_html = " ".join(f'<span class="hash-pill">#{h}</span>' for h in intel["hashtag_cloud"]) or '<span style="color:#64748B;">No hashtags detected</span>'
        st.markdown(f"""<div class="intel-card"><div class="intel-label">📌 Top Hashtags</div>
            <div style="margin-top:8px;">{hash_html}</div></div>""", unsafe_allow_html=True)

    # KPIs
    st.markdown('<p class="sec">Profile Overview</p>', unsafe_allow_html=True)
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.markdown(f'<div class="metric-box"><div class="metric-title">Followers</div><div class="metric-val">{base["followers"]:,}</div><div class="metric-sub">real</div></div>',unsafe_allow_html=True)
    k2.markdown(f'<div class="metric-box"><div class="metric-title">Following</div><div class="metric-val">{base["following"]:,}</div><div class="metric-sub">real</div></div>',unsafe_allow_html=True)
    k3.markdown(f'<div class="metric-box"><div class="metric-title">Posts</div><div class="metric-val">{base["post_count"]:,}</div><div class="metric-sub">real</div></div>',unsafe_allow_html=True)
    k4.markdown(f'<div class="metric-box"><div class="metric-title">Activity</div><div class="metric-val">{metrics["profile_activity"]}%</div><div class="metric-sub">ai-inferred</div></div>',unsafe_allow_html=True)
    k5.markdown(f'<div class="metric-box"><div class="metric-title">Avg Sentiment</div><div class="metric-val">{review["avg_audience_sentiment"]}</div><div class="metric-sub">NLP</div></div>',unsafe_allow_html=True)
    k6.markdown(f'<div class="metric-box"><div class="metric-title">Performance</div><div class="metric-val" style="font-size:1rem;">{review["overall_performance"]}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    s1.markdown(f'<div class="metric-box"><div class="metric-title">Total Likes</div><div class="metric-val">{total_likes:,}</div></div>',unsafe_allow_html=True)
    s2.markdown(f'<div class="metric-box"><div class="metric-title">Total Comments</div><div class="metric-val">{total_comments:,}</div></div>',unsafe_allow_html=True)
    s3.markdown(f'<div class="metric-box"><div class="metric-title">Est. Shares</div><div class="metric-val">{total_shares:,}</div></div>',unsafe_allow_html=True)
    s4.markdown(f'<div class="metric-box"><div class="metric-title">Est. Reposts</div><div class="metric-val">{total_reposts:,}</div></div>',unsafe_allow_html=True)

    # Charts
    st.markdown('<p class="sec">Advanced Analytics</p>', unsafe_allow_html=True)
    ch1,ch2 = st.columns([3,1])
    with ch1:
        fig = go.Figure()
        labels = [v["id"][:8] for v in vids]
        fig.add_bar(name="Avg Watchtime (s)", x=labels, y=[v["avg_watchtime"] for v in vids], marker_color="#6366F1")
        fig.add_bar(name="Duration (s)",       x=labels, y=[v["duration"]      for v in vids], marker_color="#0EA5E9")
        fig.update_layout(barmode="group",paper_bgcolor="#0A0F1E",plot_bgcolor="#0A0F1E",font_color="#94A3B8",legend=dict(bgcolor="#1E293B"),margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        gauge = go.Figure(go.Indicator(mode="gauge+number",value=review["avg_account_swipe_rate"],
            title={"text":"Avg Swipe Rate %","font":{"color":"#94A3B8"}},
            gauge={"axis":{"range":[0,100]},"bar":{"color":"#6366F1"},
                   "steps":[{"range":[0,40],"color":"#134E4A"},{"range":[40,65],"color":"#78350F"},{"range":[65,100],"color":"#7F1D1D"}],
                   "bgcolor":"#1E293B"},number={"font":{"color":"#E2E8F0"}}))
        gauge.update_layout(paper_bgcolor="#0A0F1E",font_color="#94A3B8",height=260,margin=dict(t=30))
        st.plotly_chart(gauge, use_container_width=True)

    # Strategy
    st.markdown('<p class="sec">🎯 Strategy Directives</p>', unsafe_allow_html=True)
    d1,d2 = st.columns(2)
    with d1:
        st.markdown(f"""<div class="intel-card">
            <p style="color:#94A3B8;font-size:0.71rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Primary Audience Preference</p>
            <h3 style="color:#A78BFA;margin:0 0 8px;">{review['audience_preference']['title']}</h3>
            <p style="color:#CBD5E1;font-size:0.88rem;line-height:1.6;">{review['audience_preference']['description']}</p>
        </div>""", unsafe_allow_html=True)
    with d2:
        st.markdown(f"""<div class="intel-card">
            <p style="color:#94A3B8;font-size:0.71rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">🕐 AI Best Upload Time</p>
            <h2 style="color:#38BDF8;font-size:2rem;margin:0 0 8px;">{metrics['best_upload_time']}</h2>
            <p style="color:#CBD5E1;font-size:0.88rem;line-height:1.6;">Inferred from highest-engagement post patterns to align with audience peak activity.</p>
        </div>""", unsafe_allow_html=True)

    # Per-Post Cards
    st.markdown('<p class="sec">📹 Post-by-Post Analysis</p>', unsafe_allow_html=True)
    for i in range(0, len(vids), 3):
        row = vids[i:i+3]; cols = st.columns(3)
        for col, vid in zip(cols, row):
            sent = vid["sentiment"]
            sc = "sent-pos" if sent["label"]=="Positive" else "sent-neg" if sent["label"]=="Negative" else "sent-neu"
            ic = "🟢" if sent["label"]=="Positive" else "🔴" if sent["label"]=="Negative" else "⚪"
            with col:
                st.markdown(f"""<div class="video-card">
                    <img class="video-thumb" src="{vid['thumbnail']}" onerror="this.src='https://picsum.photos/seed/{vid['id']}/400/200'"/>
                    <div class="video-body">
                        <p class="video-caption">{vid['caption'][:200]}</p>
                        <div>
                            <span class="stat-chip">❤️ {vid['likes']:,}</span>
                            <span class="stat-chip">💬 {vid['comments_count']:,}</span>
                            <span class="stat-chip">👁️ ~{vid['views']:,}</span>
                            <span class="stat-chip">⏱️ {vid['avg_watchtime']}s/{vid['duration']}s</span>
                            <span class="stat-chip">📤 {vid['swipe_rate']}%</span>
                            <span class="stat-chip">🕒 {vid.get('days_ago','?')}d ago</span>
                        </div>
                        <p class="{sc}" style="font-size:0.8rem;margin:10px 0 8px;">
                            {ic} Sentiment: <strong>{sent['label']}</strong> ({sent['score']}/100)
                        </p>
                        <div class="sugg">{vid['suggestion']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

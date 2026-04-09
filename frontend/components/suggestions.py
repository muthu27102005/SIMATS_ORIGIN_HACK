import streamlit as st

def render_video_table(videos):
    st.markdown("### 🎬 Video Breakdown & Visual Analytics")
    
    for vid in videos:
        sent_color = "🟢" if vid["sentiment"]["score"] >= 60 else "🟠" if vid["sentiment"]["score"] >= 30 else "🔴"
        
        # Raw HTML container for beautiful layout with thumbnail
        html_str = f"""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 20px; display: flex; gap: 24px;">
            <div style="flex-shrink: 0;">
                <img src="{vid['thumbnail']}" style="width: 120px; height: 180px; object-fit: cover; border-radius: 8px; border: 2px solid #475569;">
            </div>
            <div style="flex-grow: 1;">
                <h4 style="margin-top: 0; color: #F8FAFC;">{vid['id']} | Sentiment Tone: {sent_color} {vid['sentiment']['tone']}</h4>
                <p style="color: #94A3B8; font-style: italic; margin-bottom: 12px;">"{vid['caption']}"</p>
                <div style="display: flex; gap: 40px; margin-bottom: 16px;">
                    <div>
                        <div style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Duration / Watch</div>
                        <div style="color: #E2E8F0; font-weight: bold;">{vid['duration']}s / {vid['avg_watchtime']}s</div>
                    </div>
                    <div>
                        <div style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Swipe Rate</div>
                        <div style="color: #EF4444; font-weight: bold;">{vid['swipe_rate']}%</div>
                    </div>
                    <div>
                        <div style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Engagement</div>
                        <div style="color: #E2E8F0; font-weight: bold;">{vid['likes']:,} 🤍 | {vid['comments_count']:,} 💬 | {vid['shares']:,} 🔗</div>
                    </div>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 12px; border-radius: 0 8px 8px 0;">
                    <strong style="color: #34D399;">💡 AI Optimization Suggestion:</strong> <span style="color: #E2E8F0;">{vid['suggestion']}</span>
                </div>
            </div>
        </div>
        """
        st.markdown(html_str, unsafe_allow_html=True)

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def draw_watchtime_chart(videos):
    df = pd.DataFrame(videos)
    fig = px.bar(df, x='id', y=['avg_watchtime', 'duration'], 
                 barmode='group',
                 title='Average Watchtime vs Total Duration (Seconds)',
                 color_discrete_sequence=['#38BDF8', '#475569'])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#CBD5E1',
        title_font_color='#F8FAFC',
        legend_title_text='Metric',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def draw_swipe_gauge(avg_swipe):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = avg_swipe,
        title = {'text': "Avg Channel Swipe Rate (%)", 'font': {'color': '#F8FAFC'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "#475569"},
            'bar': {'color': "#EF4444" if avg_swipe > 50 else "#10B981"},
            'steps': [
                {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.2)"},
                {'range': [35, 60], 'color': "rgba(245, 158, 11, 0.2)"},
                {'range': [60, 100], 'color': "rgba(239, 68, 68, 0.2)"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#CBD5E1"}, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def draw_engagement_funnel(videos):
    total_views = sum([v["views"] for v in videos])
    total_likes = sum([v["likes"] for v in videos])
    total_shares = sum([v["shares"] for v in videos])
    
    fig = go.Figure(go.Funnel(
        y = ["Views", "Likes", "Shares"],
        x = [total_views, total_likes, total_shares],
        textinfo = "value+percent initial",
        marker = {"color": ["#3B82F6", "#8B5CF6", "#EC4899"]}
    ))
    fig.update_layout(
        title='Aggregated Engagement Conversion',
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#CBD5E1',
        title_font_color='#F8FAFC',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

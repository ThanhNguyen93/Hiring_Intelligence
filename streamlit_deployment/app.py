import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hiring Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Main area ── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="block-container"] {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
}
h1, h2, h3, h4 {
    color: #111111 !important;
    font-family: 'DM Serif Display', serif !important;
}
p, span, label, div, li { color: #222222 !important; }

/* ── Dark sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #1C1C1E !important;
    border-right: 1px solid #2A2A2A !important;
}
[data-testid="stSidebar"] * { color: #F0F0F0 !important; }
[data-testid="stSidebar"] hr { border-color: #3A3A3A !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background-color: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] p {
    color: #6B7280 !important;
    font-size: 13px !important;
}
[data-testid="stMetricValue"] div {
    color: #111111 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ── Selectbox input field ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #F9FAFB !important;
    color: #111111 !important;
    border: 1px solid #D1D5DB !important;
}
[data-testid="stSelectbox"] > div > div > div {
    color: #111111 !important;
}

/* ── Dropdown popover menu (the dark popup) ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[role="listbox"],
[role="listbox"] *,
[role="option"],
[role="option"] * {
    background-color: #FFFFFF !important;
    color: #111111 !important;
}

/* Hover state for dropdown options */
[role="option"]:hover,
[data-baseweb="menu-item"]:hover {
    background-color: #F0FDF4 !important;
    color: #111111 !important;
}

/* Selected option highlight */
[aria-selected="true"] {
    background-color: #D1FAE5 !important;
    color: #065F46 !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] * { color: #111111 !important; }
/* Track background — light grey */
[data-testid="stSlider"] [data-baseweb="slider"] > div {
    background-color: #E5E7EB !important;
}
/* Filled portion — green */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background-color: #2D6A4F !important;
}
/* Thumb handle */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #2D6A4F !important;
    border-color: #2D6A4F !important;
}

/* ── Radio (sidebar) ── */
[data-testid="stRadio"] label { color: #F0F0F0 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background-color: #2EC4B6 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 12px 0 !important;
}
[data-testid="stButton"] > button:hover {
    background-color: #20A4A0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background-color: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
}

hr { border-color: #E5E7EB !important; }
.stCaption { color: #9CA3AF !important; }

/* ── Custom components ── */
.hired-badge {
    background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
    color: #065F46 !important;
    border: 1px solid #34D399;
    border-radius: 12px;
    padding: 20px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 2px 12px rgba(52,211,153,0.2);
    margin-bottom: 12px;
}
.not-hired-badge {
    background: linear-gradient(135deg, #FEE2E2, #FECACA);
    color: #7F1D1D !important;
    border: 1px solid #F87171;
    border-radius: 12px;
    padding: 20px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 2px 12px rgba(248,113,113,0.2);
    margin-bottom: 12px;
}
.insight-box {
    background: #ECFDF5;
    border-left: 3px solid #2D6A4F;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 14px;
    color: #065F46 !important;
}
.warning-box {
    background: #FFFBEB;
    border-left: 3px solid #F59E0B;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 14px;
    color: #78350F !important;
}
.placeholder-box {
    background: #F9FAFB;
    border: 1px dashed #D1D5DB;
    border-radius: 12px;
    padding: 60px 24px;
    text-align: center;
}
.source-box {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    font-size: 20px;
    color: #14532D !important;
}
.corr-note {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 8px;
    font-size: 13.5px;
    color: #334155 !important;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── Shared plot styling ────────────────────────────────────────────────────────
HIRED_COLOR  = "#2D6A4F"
REJECT_COLOR = "#DC2626"
CARD_BG      = "#FFFFFF"
PLOT_BG      = "#F9FAFB"
PLOT_TMPL    = "plotly_white"
AXIS_FONT    = dict(size=18, color="#111111")
TICK_FONT    = dict(size=18, color="#333333")
TITLE_FONT   = dict(size=18, color="#111111")
LEGEND_FONT  = dict(size=18, color="#111111")

def base_layout(**kwargs):
    """Shared layout — no xaxis/yaxis so callers can set them freely."""
    return dict(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=PLOT_BG,
        title_font=TITLE_FONT,
        legend=dict(font=LEGEND_FONT),
        **kwargs
    )

def ax(title=''):
    """Consistent axis style."""
    return dict(title=title, title_font=AXIS_FONT, tickfont=TICK_FONT)

# ── Load resources ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load(Path(__file__).parent / "tuned_gb_hiring_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv(Path(__file__).parent / "recruitment_data.csv")

model = load_model()
df    = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Hiring Intelligence")
    st.markdown("---")
    page = st.radio("Navigate", ["📊 EDA Explorer", "🤖 Hiring Predictor"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Model:** Tuned Gradient Boosting")
    st.markdown("**Precision (Hired):** 0.9474")
    st.markdown("**F1-macro:** 0.8970")
    st.markdown("**ROC-AUC:** 0.9331")
    st.markdown("---")
    st.caption("Built with Streamlit · Recruitment Dataset")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EDA Explorer
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 EDA Explorer":
    st.markdown("<h1>Recruitment Data Explorer</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="source-box">
    📂 <strong>Data source:</strong>
    <a href="https://www.kaggle.com/datasets/rabieelkharoua/predicting-hiring-decisions-in-recruitment-data/data"
       target="_blank" style="color:#2D6A4F;">
       Predicting Hiring Decisions in Recruitment — Kaggle
    </a><br>
    A synthetic dataset of 1,500 candidates with demographic, experience, and assessment features,
    used to model binary hiring decisions across three recruitment strategies.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Dataset overview ──────────────────────────────────────────────────────
    st.markdown("### Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Candidates", f"{len(df):,}")
    c2.metric("Hired Rate", f"{df['HiringDecision'].mean()*100:.1f}%")
    c3.metric("Features", f"{df.shape[1]-1}")
    c4.metric("Missing Values", f"{df.isnull().sum().sum()}")
    st.markdown("---")

    # ── Feature distributions ─────────────────────────────────────────────────
    st.markdown("### Feature Distribution by Hiring Outcome")
    
    numeric_features = ['InterviewScore', 'SkillScore', 'PersonalityScore',
                        'ExperienceYears', 'Age', 'DistanceFromCompany']
    feat = st.selectbox("Select feature", numeric_features)

    df_viz = df.copy()
    df_viz['Outcome'] = df_viz['HiringDecision'].map({1: 'Hired', 0: 'Not Hired'})

    cl, cr = st.columns(2)
    with cl:
        fig_line = go.Figure()
        for outcome, color in [('Not Hired', REJECT_COLOR), ('Hired', HIRED_COLOR)]:
            subset = df_viz[df_viz['Outcome'] == outcome][feat].sort_values()
            counts_line, bins = np.histogram(subset, bins=25)
            bin_centers = (bins[:-1] + bins[1:]) / 2
            fig_line.add_trace(go.Scatter(
                x=bin_centers, y=counts_line,
                mode='lines', name=outcome,
                line=dict(color=color, width=2.5),
                hovertemplate=f'{feat}: %{{x:.1f}}<br>Count: %{{y}}<extra>{outcome}</extra>'
            ))
        fig_line.update_layout(
            title=f'{feat} — Distribution by Outcome',
            title_font=TITLE_FONT, paper_bgcolor=CARD_BG, plot_bgcolor=PLOT_BG,
            legend=dict(font=LEGEND_FONT),
            xaxis=ax(feat), yaxis=ax('Count'),
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with cr:
        fig_box = px.box(
            df_viz, x='Outcome', y=feat, color='Outcome', points='outliers',
            template=PLOT_TMPL,
            color_discrete_map={'Hired': HIRED_COLOR, 'Not Hired': REJECT_COLOR},
            title=f'{feat} — Box Plot'
        )
        fig_box.update_layout(
            showlegend=False,
            title_font=TITLE_FONT, paper_bgcolor=CARD_BG, plot_bgcolor=PLOT_BG,
            legend=dict(font=LEGEND_FONT),
            xaxis=ax('Outcome'), yaxis=ax(feat),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # ── Recruitment strategy breakdown ────────────────────────────────────────
    st.markdown("### Recruitment Strategy vs Hiring Outcome")

    df_viz['Strategy'] = df_viz['RecruitmentStrategy'].map(
        {1: 'Aggressive', 2: 'Moderate', 3: 'Conservative'})
    order  = ['Aggressive', 'Moderate', 'Conservative']
    counts = df_viz.groupby(['Strategy', 'Outcome']).size().reset_index(name='Count')
    #rates  = df_viz.groupby('Strategy')['HiringDecision'].mean().reindex(order) * 100
    total_hired = df_viz['HiringDecision'].sum()
    rates = (df_viz[df_viz['HiringDecision'] == 1]
            .groupby('Strategy').size()
            .reindex(order) / total_hired * 100)

    sl, sr = st.columns(2)
    with sl:
        fig_stacked = px.bar(
            counts, x='Strategy', y='Count', color='Outcome',
            template=PLOT_TMPL, title='Headcount by Strategy',
            color_discrete_map={'Hired': HIRED_COLOR, 'Not Hired': REJECT_COLOR},
            category_orders={'Strategy': order}
        )
        fig_stacked.update_layout(
            title_font=TITLE_FONT, paper_bgcolor=CARD_BG, plot_bgcolor=PLOT_BG,
            legend=dict(font=LEGEND_FONT),
            xaxis=ax('Strategy'), yaxis=ax('Count'),
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

    with sr:
        fig_rate = go.Figure(go.Bar(
            x=order,
            y=[rates[s] for s in order],
            marker_color=[HIRED_COLOR, '#F59E0B', REJECT_COLOR],
            text=[f'{rates[s]:.1f}%' for s in order],
            textposition='outside',
            textfont=dict(color='#111111', size=14)
        ))
        fig_rate.update_layout(
            title='Hire Rate by Strategy',
            title_font=TITLE_FONT,
            paper_bgcolor=CARD_BG,
            plot_bgcolor=PLOT_BG,
            showlegend=False,
            legend=dict(font=LEGEND_FONT),
            xaxis=dict(title='Strategy', title_font=AXIS_FONT, tickfont=TICK_FONT),
            yaxis=dict(range=[0, 100], title='Hire Rate (%)',
                       title_font=AXIS_FONT, tickfont=TICK_FONT),
        )
        st.plotly_chart(fig_rate, use_container_width=True)

    st.markdown("""<div class="insight-box" style="font-size:18px;">
    💡 <strong>Key insight:</strong> Recruitment strategy is the #1 predictor (SHAP = 3.052) —
    stronger than any candidate quality signal. Aggressive strategy yields the highest hire rate.
    </div>""", unsafe_allow_html=True)

    # ── Feature signal strength ───────────────────────────────────────────────
    st.markdown("### Feature Signal Strength")

    df_corr = df.copy()
    df_corr['RecruitmentStrategy_2'] = (df_corr['RecruitmentStrategy'] == 2).astype(int)
    df_corr['RecruitmentStrategy_3'] = (df_corr['RecruitmentStrategy'] == 3).astype(int)

    corr_cols = ['InterviewScore', 'SkillScore', 'PersonalityScore', 'ExperienceYears',
                 'EducationLevel', 'RecruitmentStrategy_2', 'RecruitmentStrategy_3',
                 'Age', 'DistanceFromCompany', 'PreviousCompanies', 'Gender']

    abs_corr = (df_corr[corr_cols + ['HiringDecision']]
                .corr()['HiringDecision']
                .drop('HiringDecision')
                .abs()
                .sort_values())

    STRONG_T = 0.10
    WEAK_T   = 0.05
    bar_colors = [
    'bisque' if v >= STRONG_T else   # summer (green-yellow range)
    'darkorange' if v >= WEAK_T  else    # autumn (red-orange)
    'burlywood'                          # cool (cyan-blue)
    for v in abs_corr.values
    ]

    fig_corr = go.Figure(go.Bar(
        x=abs_corr.values, y=abs_corr.index, orientation='h',
        marker_color=bar_colors,
        text=[f'{v:.4f}' for v in abs_corr.values],
        textfont=dict(color='#111111', size=14),
        textposition='auto',                          # ← was 'outside', caused overlap
        hovertemplate='%{y}<br>|r| = %{x:.4f}<extra></extra>'
    ))
    fig_corr.add_vline(x=STRONG_T, line_dash='dash', line_color='#60AB5E', line_width=1.5,
                   annotation_text='Strong (>0.10)', annotation_font_color='#60AB5E',
                   annotation_position='top right', annotation_font_size=15)
    fig_corr.add_vline(x=WEAK_T, line_dash='dash', line_color='#E07B39', line_width=1.5,
                   annotation_text='Weak (>0.05)', annotation_font_color='#E07B39',
                   annotation_position='top right', annotation_font_size=15)
    fig_corr.update_layout(
        xaxis=dict(title='|Pearson r| with HiringDecision',
                range=[0, abs_corr.max() + 0.06],
                title_font=dict(size=18, color='#111111'),
                tickfont=dict(size=18, color='#333333')),
        yaxis=dict(title_font=dict(size=18, color='#111111'),
                tickfont=dict(size=18, color='#333333')),
        height=550,
        uniformtext=dict(minsize=20, mode='show'),  # ← controls the bar label size
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    <div class="corr-note" style="font-size:18px;">
    📐 <strong>What this shows:</strong> This is the <strong>absolute Pearson correlation</strong>
    between each feature and <code>HiringDecision</code>. It answers:
    <em>"How much does knowing this feature tell you about whether someone gets hired?"</em><br><br>
    — <strong style="color:#60AB5E;">Summer bars</strong> (|r| > 0.10): strong linear signal<br>
    — <strong style="color:#E07B39;">Autumn bars</strong> (0.05–0.10): weak but present signal<br>
    — <strong style="color:#88C9D4;">Cool bars</strong> (|r| < 0.05): near-zero, model largely ignores these<br><br>
    Note: Pearson only captures <em>linear</em> relationships. The Gradient Boosting model can also
    detect non-linear patterns, which is why SHAP importance may differ from this ranking.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("View raw data"):
        st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Hiring Predictor
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("<h1>Hiring Predictor</h1>", unsafe_allow_html=True)
    st.markdown("Enter candidate details to get a model-based hiring recommendation.")
    st.markdown("---")

    col_form, col_result = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown("### Candidate Profile")
        st.markdown("**Recruitment**")
        recruitment_strategy = st.selectbox(
            "Recruitment Strategy", [1, 2, 3],
            format_func=lambda x: {1: "Aggressive", 2: "Moderate", 3: "Conservative"}[x]
        )

        st.markdown("**Background**")
        b1, b2 = st.columns(2)
        with b1:
            age              = st.slider("Age", 18, 65, 30)
            education_level  = st.selectbox("Education Level", [1, 2, 3, 4, 5],
                format_func=lambda x: {
                    1: "1 — High School", 2: "2 — Diploma",
                    3: "3 — Bachelor's",  4: "4 — Master's", 5: "5 — PhD"
                }[x], index=2)
            experience_years = st.slider("Experience (Years)", 0, 15, 3)
        with b2:
            gender             = st.selectbox("Gender", [0, 1],
                                    format_func=lambda x: "Female" if x == 0 else "Male")
            previous_companies = st.slider("Previous Companies", 0, 5, 1)
            distance           = st.slider("Distance from Company (km)", 1, 100, 20)

        st.markdown("**Assessment Scores**")
        s1, s2, s3 = st.columns(3)
        with s1: interview_score   = st.slider("Interview",   0, 100, 70)
        with s2: skill_score       = st.slider("Skill",       0, 100, 70)
        with s3: personality_score = st.slider("Personality", 0, 100, 70)

        predict_btn = st.button("🎯 Generate Prediction", use_container_width=True, type="primary")

    with col_result:
        st.markdown("### Prediction Result")

        if predict_btn:
            rs2       = 1 if recruitment_strategy == 2 else 0
            rs3       = 1 if recruitment_strategy == 3 else 0
            composite = interview_score * 0.4 + skill_score * 0.4 + personality_score * 0.2

            input_df = pd.DataFrame([{
                'Age': age, 'Gender': gender,
                'EducationLevel': education_level,
                'ExperienceYears': experience_years,
                'PreviousCompanies': previous_companies,
                'DistanceFromCompany': distance,
                'InterviewScore': interview_score,
                'SkillScore': skill_score,
                'PersonalityScore': personality_score,
                'RecruitmentStrategy_2': rs2,
                'RecruitmentStrategy_3': rs3,
                'composite_score': composite
            }])

            prediction = model.predict(input_df)[0]
            proba      = model.predict_proba(input_df)[0]
            hire_prob  = proba[1]

            if prediction == 1:
                st.markdown('<div class="hired-badge">✅ Recommended to Hire</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="not-hired-badge">❌ Not Recommended</div>',
                            unsafe_allow_html=True)

            m1, m2 = st.columns(2)
            m1.metric("Hire Probability",   f"{hire_prob*100:.1f}%")
            m2.metric("Reject Probability", f"{(1-hire_prob)*100:.1f}%")

            # Gauge
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(hire_prob * 100, 1),
                number={'suffix': '%', 'font': {'size': 32, 'color': '#111111'}},
                title={'text': 'Hire Probability', 'font': {'color': '#6B7280', 'size': 14}},
                gauge={
                    'axis': {'range': [0, 100],
                             'tickfont': {'size': 13, 'color': '#333333'},
                             'tickcolor': '#6B7280'},
                    'bar': {'color': HIRED_COLOR if prediction == 1 else REJECT_COLOR},
                    'bgcolor': '#F3F4F6', 'bordercolor': '#E5E7EB',
                    'steps': [
                        {'range': [0, 40],   'color': '#FEE2E2'},
                        {'range': [40, 65],  'color': '#FEF9C3'},
                        {'range': [65, 100], 'color': '#D1FAE5'}
                    ],
                    'threshold': {'line': {'color': '#111111', 'width': 2},
                                  'thickness': 0.75, 'value': 50}
                }
            ))
            fig_g.update_layout(
                paper_bgcolor=CARD_BG, height=220,
                margin=dict(t=50, b=10, l=20, r=20)
            )
            st.plotly_chart(fig_g, use_container_width=True)

            # Radar
            fig_r = go.Figure(go.Scatterpolar(
                r=[interview_score, skill_score, personality_score,
                   education_level * 20, experience_years / 15 * 100],
                theta=['Interview', 'Skill', 'Personality', 'Education', 'Experience'],
                fill='toself',
                fillcolor=('rgba(45,106,79,0.15)' if prediction == 1
                           else 'rgba(220,38,38,0.15)'),
                line=dict(color=HIRED_COLOR if prediction == 1 else REJECT_COLOR, width=2)
            ))
            fig_r.update_layout(
                polar=dict(
                    bgcolor='#F9FAFB',
                    radialaxis=dict(visible=True, range=[0, 100],
                                   tickfont=dict(size=12, color='#555555'),
                                   color='#555555'),
                    angularaxis=dict(tickfont=dict(size=13, color='#111111'))
                ),
                paper_bgcolor=CARD_BG,
                title=dict(text='Profile Radar', font=dict(color='#111111', size=14)),
                height=280, margin=dict(t=50, b=10, l=40, r=40),
                showlegend=False
            )
            st.plotly_chart(fig_r, use_container_width=True)

            strat_label = {1: "Aggressive ✅", 2: "Moderate ⚠️", 3: "Conservative ❌"}
            st.markdown(f"**Strategy:** {strat_label[recruitment_strategy]} &nbsp;|&nbsp; "
                        f"**Composite Score:** {composite:.0f}/100")

            if prediction == 1 and recruitment_strategy in [2, 3]:
                st.markdown("""<div class="warning-box">
                ⚠️ Hired despite strategy penalty — strong scores overcame the disadvantage.
                </div>""", unsafe_allow_html=True)
            elif prediction == 0 and hire_prob > 0.35:
                st.markdown("""<div class="warning-box">
                ⚠️ Borderline rejection (hire prob > 35%). Consider manual review.
                </div>""", unsafe_allow_html=True)
            elif prediction == 1:
                st.markdown("""<div class="insight-box">
                ✅ High confidence recommendation. Profile aligns with historical hire patterns.
                </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""<div class="placeholder-box">
                <div style="font-size:52px; margin-bottom:12px;">🎯</div>
                <div style="font-size:15px; color:#6B7280;">
                Fill in the candidate profile and click<br>
                <strong style="color:#374151;">Generate Prediction</strong>
                </div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Model Performance")
        p1, p2, p3 = st.columns(3)
        p1.metric("Hired Precision", "94.7%",
                  help="When model says hire, correct 94.7% of the time")
        p2.metric("F1-macro", "89.7%",
                  help="Balanced score across both classes")
        p3.metric("ROC-AUC", "93.3%",
                  help="Overall discrimination ability")

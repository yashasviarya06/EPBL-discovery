import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EPBL Lead Discovery Engine",
    page_icon="♻️",
    layout="wide"
)


# ============================================================
# LOAD DATA AND MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "opportunity_signals.csv"
MODEL_PATH = BASE_DIR / "lead_model.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"

df = pd.read_csv(DATA_PATH)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ============================================================
# TITLE
# ============================================================

st.title("♻️ EPBL Lead Discovery & Opportunity Scoring Engine")

st.markdown(
    """
    ### AI-powered identification of potential decentralized sanitation opportunities

    The system analyzes public-style project signals and uses NLP-based
    machine learning to identify and prioritize potential EPBL opportunities.
    """
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Lead Filters")

selected_states = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["state"].unique()),
    default=sorted(df["state"].unique())
)

selected_signal_types = st.sidebar.multiselect(
    "Select Sector / Signal Type",
    options=sorted(df["signal_type"].unique()),
    default=sorted(df["signal_type"].unique())
)

min_score = st.sidebar.slider(
    "Minimum Opportunity Score (%)",
    min_value=0,
    max_value=100,
    value=50
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["state"].isin(selected_states)) &
    (df["signal_type"].isin(selected_signal_types))
].copy()


# ============================================================
# CALCULATE OPPORTUNITY SCORES
# ============================================================

filtered_text = vectorizer.transform(
    filtered_df["signal_text"]
)

filtered_df["opportunity_score"] = (
    model.predict_proba(filtered_text)[:, 1] * 100
)

filtered_df["opportunity_score"] = filtered_df[
    "opportunity_score"
].round(2)


# Apply minimum score

high_score_df = filtered_df[
    filtered_df["opportunity_score"] >= min_score
].copy()


# Sort highest opportunity first

high_score_df = high_score_df.sort_values(
    by="opportunity_score",
    ascending=False
)


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Signals",
        f"{len(df):,}"
    )


with col2:
    st.metric(
        "Filtered Signals",
        f"{len(filtered_df):,}"
    )


with col3:
    st.metric(
        "High-Priority Leads",
        f"{len(high_score_df):,}"
    )


with col4:
    if len(high_score_df) > 0:
        avg_score = high_score_df["opportunity_score"].mean()
    else:
        avg_score = 0

    st.metric(
        "Average Opportunity Score",
        f"{avg_score:.1f}%"
    )


st.divider()


# ============================================================
# LEAD RANKING
# ============================================================

st.subheader("🏆 Ranked Opportunity Leads")

if len(high_score_df) > 0:

    display_df = high_score_df[
        [
            "state",
            "city",
            "signal_type",
            "signal_text",
            "opportunity_score"
        ]
    ].copy()

    display_df.columns = [
        "State",
        "City",
        "Sector",
        "Signal",
        "Opportunity Score (%)"
    ]

    st.dataframe(
        display_df.head(50),
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No opportunities match the current filters."
    )


st.divider()


# ============================================================
# LEAD INTELLIGENCE
# ============================================================

st.subheader("🎯 Lead Intelligence")


if len(high_score_df) > 0:

    selected_index = st.selectbox(
        "Select a lead to analyze",
        high_score_df.index,
        format_func=lambda x:
        f"{high_score_df.loc[x, 'city']} — "
        f"{high_score_df.loc[x, 'signal_type']} — "
        f"{high_score_df.loc[x, 'opportunity_score']}%"
    )

    selected_lead = high_score_df.loc[selected_index]


    col1, col2 = st.columns(2)


    with col1:

        st.markdown("### 📍 Location")

        st.write(
            f"**State:** {selected_lead['state']}"
        )

        st.write(
            f"**City:** {selected_lead['city']}"
        )

        st.write(
            f"**Sector:** {selected_lead['signal_type']}"
        )


    with col2:

        score = selected_lead["opportunity_score"]

        st.markdown("### 🤖 AI Assessment")

        if score >= 80:

            st.success(
                f"🔥 HIGH PRIORITY\n\n"
                f"Opportunity Score: {score}%"
            )

        elif score >= 60:

            st.warning(
                f"🟡 MEDIUM PRIORITY\n\n"
                f"Opportunity Score: {score}%"
            )

        else:

            st.info(
                f"🟢 LOW PRIORITY\n\n"
                f"Opportunity Score: {score}%"
            )


    st.markdown("### 📝 Detected Signal")

    st.info(
        selected_lead["signal_text"]
    )


    # ========================================================
    # RECOMMENDED OUTREACH PERSONA
    # ========================================================

    st.markdown("### 👤 Recommended Outreach Persona")


    persona_map = {

        "Residential":
            "Real Estate Developer / Project Developer",

        "Hospitality":
            "Hotel Developer / Resort Operator",

        "Healthcare":
            "Hospital Administrator / Healthcare Developer",

        "Education":
            "Institutional Administrator / Campus Management",

        "Industrial":
            "Industrial Facility Manager / Plant Head",

        "Logistics":
            "Logistics Park Developer / Facility Manager",

        "Commercial":
            "Commercial Property Developer / Facility Manager",

        "Institutional":
            "Institutional Facility Manager",

        "Tourism":
            "Tourism Project Developer / Resort Operator",

        "Senior Living":
            "Senior Living Developer / Facility Operator"
    }


    persona = persona_map.get(
        selected_lead["signal_type"],
        "Project Developer / Facility Manager"
    )


    st.success(
        f"🎯 **Suggested Contact:** {persona}"
    )


else:

    st.info(
        "Select filters that produce at least one lead."
    )


st.divider()


# ============================================================
# ANALYTICS
# ============================================================

st.subheader("📊 Opportunity Analytics")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# STATE ANALYSIS
# ------------------------------------------------------------

with col1:

    st.markdown("### Opportunities by State")

    state_counts = (
        high_score_df
        .groupby("state")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(state_counts)


# ------------------------------------------------------------
# SECTOR ANALYSIS
# ------------------------------------------------------------

with col2:

    st.markdown("### Opportunities by Sector")

    sector_counts = (
        high_score_df
        .groupby("signal_type")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(sector_counts)


st.divider()


# ============================================================
# TOP 10 LEADS
# ============================================================

st.subheader("🔥 Top 10 Highest-Scoring Opportunities")


if len(high_score_df) > 0:

    top10 = high_score_df.head(10)[
        [
            "state",
            "city",
            "signal_type",
            "opportunity_score"
        ]
    ].copy()

    top10.columns = [
        "State",
        "City",
        "Sector",
        "Opportunity Score (%)"
    ]

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EPBL Lead Discovery Engine | NLP + TF-IDF + Logistic Regression | "
    "Prototype using synthetically generated opportunity signals"
)

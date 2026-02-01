import streamlit as st
import pandas as pd
import joblib

# -------------------------------
# Load Models & Artifacts
# -------------------------------
@st.cache_resource
def load_models():
    rating_model = joblib.load("models/rating_regression_model.pkl")
    visit_mode_model = joblib.load("models/visit_mode_baseline_model.pkl")
    user_item_matrix = joblib.load("models/user_item_matrix.pkl")
    top_k_similar_users = joblib.load("models/top_k_user_similarity.pkl")
    attraction_map = joblib.load("models/attraction_map.pkl")
    return rating_model, visit_mode_model, user_item_matrix, top_k_similar_users, attraction_map


rating_model, visit_mode_model, user_item_matrix, top_k_similar_users, attraction_map = load_models()

popular_recs = list(
    user_item_matrix.mean()
    .sort_values(ascending=False)
    .head(10)
    .items()
)

# -------------------------------
# Recommendation Function
# -------------------------------
def recommend_attractions(
    user_id,
    user_item_matrix,
    top_k_similar_users,
    popular_recs,
    top_n=5
):
    # Cold-start: user not in matrix
    if user_id not in user_item_matrix.index:
        return popular_recs[:top_n], "popular"

    # Get top-K similar users (already precomputed)
    similar_users = top_k_similar_users.get(user_id, [])

    user_ratings = user_item_matrix.loc[user_id]
    unseen_items = user_ratings[user_ratings.isna()].index

    scores = {}

    for item in unseen_items:
        weighted_sum = 0
        sim_sum = 0

        for sim_user, sim in similar_users:
            rating = user_item_matrix.loc[sim_user, item]
            if not pd.isna(rating):
                weighted_sum += sim * rating
                sim_sum += abs(sim)

        if sim_sum > 0:
            scores[item] = weighted_sum / sim_sum

    # Personalized CF recommendations
    personalized = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Fill with popular if not enough CF results
    recommended = personalized[:top_n]

    if len(recommended) < top_n:
        needed = top_n - len(recommended)
        popular_fill = [
            (aid, score) for aid, score in popular_recs
            if aid not in [x[0] for x in recommended]
        ][:needed]
        recommended.extend(popular_fill)
        return recommended, "hybrid"

    return recommended, "cf"
def readable_recommendations(recs):
    return [
        (attraction_map.get(aid, aid), score)
        for aid, score in recs
    ]



# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Tourism Experience Analytics", layout="wide")

st.title("🌍 Tourism Experience Analytics Platform")
st.write("Predict ratings, explore visit patterns, and get personalized attraction recommendations.")

tab1, tab2, tab3 = st.tabs(
    ["⭐ Rating Prediction", "🧳 Visit Mode (Indicative)", "🎯 Attraction Recommendations"]
)

# -------------------------------
# TAB 1: Regression
# -------------------------------
with tab1:
    st.header("⭐ Predict Attraction Rating")

    col1, col2 = st.columns(2)
    ATTRACTION_TYPE_MAP = {
        2: "Ancient Ruins",
        10: "Ballets",
        13: "Beaches",
        19: "Caverns & Caves",
        34: "Flea & Street Markets",
        44: "Historic Sites",
        45: "History Museums",
        61: "National Parks",
        63: "Nature & Wildlife Areas",
        64: "Neighborhoods",
        72: "Points of Interest & Landmarks",
        76: "Religious Sites",
        82: "Spas",
        84: "Speciality Museums",
        91: "Volcanos",
        92: "Water Parks",
        93: "Waterfalls",
        5: "Museum",
        6: "Beach",
        7: "Park",
        8: "Temple",
        9: "Market"
    }
    attraction_type_options = {
        f"{k} - {v}": k for k, v in ATTRACTION_TYPE_MAP.items()
    }


    with col1:
        year = st.number_input("Visit Year", min_value=2010, max_value=2035, value=2024)
        month = st.number_input("Visit Month", min_value=1, max_value=12, value=6)
        visit_mode = st.selectbox("Visit Mode",["Business", "Couples", "Family", "Friends", "Solo"])
        selected_attraction_type = st.selectbox(
            "Attraction Type",
            options=list(attraction_type_options.keys())
        )
        attraction_type_id = attraction_type_options[selected_attraction_type]


    with col2:
        country = st.text_input("Country", "India")
        region = st.text_input("Region", "Asia")
        continent = st.text_input("Continent", "Asia")

    if st.button("Predict Rating"):
        input_df = pd.DataFrame([{
            "VisitYear": year,
            "VisitMonth": month,
            "AttractionTypeId": attraction_type_id,
            "VisitMode": visit_mode,
            "Country": country,
            "Region": region,
            "Continent": continent
        }])

        rating = rating_model.predict(input_df)[0]
        st.success(f"⭐ Predicted Rating: **{round(rating, 2)} / 5**")

# -------------------------------
# TAB 2: Classification
# -------------------------------
with tab2:
    st.header("🧳 Likely Visit Mode (Baseline / Indicative)")
    st.info(
        "This prediction reflects dominant historical travel patterns "
        "and is intended for indicative insights, not definitive classification."
    )

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input("Visit Year ", min_value=2010, max_value=2035, value=2024, key="c1")
        month = st.number_input("Visit Month ", min_value=1, max_value=12, value=6, key="c2")  
        # attraction_type = st.number_input("Attraction Type ID ", min_value=1, value=1, key="c3")
        selected_attraction_type = st.selectbox(
            "Attraction Type",
            options=list(attraction_type_options.keys()),key="c3")
        attraction_type_id2 = attraction_type_options[selected_attraction_type]


    with col2:
        country = st.text_input("Country ", "India", key="c4")
        region = st.text_input("Region ", "Asia", key="c5")
        continent = st.text_input("Continent ", "Asia", key="c6")

    if st.button("Predict Visit Mode"):
        input_df = pd.DataFrame([{
            "VisitYear": year,
            "VisitMonth": month,
            "AttractionTypeId": attraction_type_id2,
            "Country": country,
            "Region": region,
            "Continent": continent
        }])

        visit_mode = visit_mode_model.predict(input_df)[0]
        st.success(f"🧳 Likely Visit Mode: **{visit_mode}**")

# -------------------------------
# TAB 3: Recommendation
# -------------------------------
with tab3:
    st.header("🎯 Personalized Attraction Recommendations")
    user_id = st.number_input("Enter User ID", min_value=1, value=10)

    if st.button("Get Recommendations"):
        recs, rec_type = recommend_attractions(
            user_id=user_id,
            user_item_matrix=user_item_matrix,
            top_k_similar_users=top_k_similar_users,
            popular_recs=popular_recs,
            top_n=5
        )
        readable = readable_recommendations(recs)

        # Messaging based on recommendation type
        if rec_type == "cf":
            st.success("Personalized recommendations based on similar users.")
        elif rec_type == "hybrid":
            st.info("Mixed recommendations: personalized + popular attractions.")
        else:
            st.info("Popular attractions (cold-start fallback).")

        st.subheader("Top Recommended Attractions")
        for i, (name, score) in enumerate(readable_recommendations(recs), start=1):
            st.write(f"**{i}. {name}** — Preference Score: {round(score, 2)}")



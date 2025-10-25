import pickle
import streamlit as st
import requests

# ===================== Utility Functions ===================== #

@st.cache_data
def load_movie_data():
    return pickle.load(open("dataset.pkl", "rb"))

@st.cache_data
def load_similarity():
    return pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    for index in movies_list[1:6]:
        movie_id = movies.iloc[index[0]]['movie_id']
        recommended_movies.append(movies.iloc[index[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ===================== Streamlit UI ===================== #

def main():
    st.set_page_config(
        page_title="🎥 Movie Recommender",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # ---- Custom CSS ----
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #000428, #004e92);
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        .movie-card {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            transition: 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.03);
            background-color: rgba(255, 255, 255, 0.15);
        }
        .movie-title {
            font-size: 16px;
            font-weight: 600;
            color: #f2f2f2;
            margin-top: 8px;
        }
        h1 {
            text-align: center;
            color: #fff;
            padding-top: 10px;
        }
        .stSelectbox label {
            color: #fff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- Header ----
    st.markdown("<h1>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ccc;'>Find movies similar to your favorites 🍿</p>", unsafe_allow_html=True)
    st.write("---")

    # ---- Load Data ----
    movies = load_movie_data()
    similarity = load_similarity()

    # ---- Movie Selection ----
    selected_movie = st.selectbox(
        "Select a movie to get recommendations 👇",
        movies['title'].values
    )

    st.write("")
    st.write("")

    # ---- Recommend Button ----
    if st.button("✨ Recommend"):
        with st.spinner("Fetching your recommendations... 🍿"):
            recommended_movies, recommended_posters = recommend(selected_movie, movies, similarity)

        st.success("Here are your recommendations! 👇")

        # ---- Display Recommendations ----
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <div class='movie-card'>
                        <img src='{recommended_posters[idx]}' width='150' style='border-radius:10px;'>
                        <div class='movie-title'>{recommended_movies[idx]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


if __name__ == "__main__":
    main()

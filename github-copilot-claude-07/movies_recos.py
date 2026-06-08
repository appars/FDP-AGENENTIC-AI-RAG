import streamlit as st

# -----------------------------
# Poster helper (no external URLs needed)
# -----------------------------
_POSTER_COLORS = ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#2d6a4f", "#b5451b"]

def poster_html(title: str) -> str:
    color = _POSTER_COLORS[hash(title) % len(_POSTER_COLORS)]
    return f"""
    <div style="background:{color};width:100%;padding-top:150%;position:relative;
                border-radius:8px;margin-bottom:6px;">
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                  color:#fff;text-align:center;font-size:13px;font-weight:bold;
                  padding:8px;width:85%;line-height:1.4;">{title}</div>
    </div>"""

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Movie Recommendation Chatbot",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation Chatbot")
st.write("Tell me your favorite genre and I'll recommend movies!")

# -----------------------------
# Movie Database
# -----------------------------

movies_db = {

    "action": [
        {
            "title": "Inception",
            "rating": 8.8,
            "summary": "A skilled thief enters dreams to steal secrets.",
            "poster": "https://placehold.co/300x450?text=Inception"
        },
        {
            "title": "Mad Max: Fury Road",
            "rating": 8.1,
            "summary": "Survivors fight for freedom in a desert wasteland.",
            "poster": "https://placehold.co/300x450?text=Mad+Max"
        },
        {
            "title": "John Wick",
            "rating": 7.4,
            "summary": "A retired assassin returns for revenge.",
            "poster": "https://placehold.co/300x450?text=John+Wick"
        },
        {
            "title": "KGF Chapter 1",
            "rating": 8.2,
            "summary": "A man rises through the underworld for power.",
            "poster": "https://placehold.co/300x450?text=KGF"
        },
        {
            "title": "Vikrant Rona",
            "rating": 7.0,
            "summary": "A mysterious inspector investigates strange killings.",
            "poster": "https://placehold.co/300x450?text=Vikrant+Rona"
        }
    ],

    "comedy": [
        {
            "title": "The Hangover",
            "rating": 7.7,
            "summary": "Friends retrace a crazy bachelor party.",
            "poster": "https://placehold.co/300x450?text=Hangover"
        },
        {
            "title": "3 Idiots",
            "rating": 8.4,
            "summary": "Engineering students navigate friendship and education.",
            "poster": "https://placehold.co/300x450?text=3+Idiots"
        },
        {
            "title": "Hera Pheri",
            "rating": 8.2,
            "summary": "Three struggling men land in hilarious trouble.",
            "poster": "https://placehold.co/300x450?text=Hera+Pheri"
        },
        {
            "title": "French Biryani",
            "rating": 6.0,
            "summary": "A quirky comedy set in Bengaluru.",
            "poster": "https://placehold.co/300x450?text=French+Biryani"
        },
        {
            "title": "Superbad",
            "rating": 7.6,
            "summary": "Teenagers chase one unforgettable night.",
            "poster": "https://placehold.co/300x450?text=Superbad"
        }
    ],

    "sci-fi": [
        {
            "title": "Interstellar",
            "rating": 8.7,
            "summary": "Astronauts search for humanity's future.",
            "poster": "https://placehold.co/300x450?text=Interstellar"
        },
        {
            "title": "The Matrix",
            "rating": 8.7,
            "summary": "A hacker discovers reality is simulated.",
            "poster": "https://placehold.co/300x450?text=Matrix"
        },
        {
            "title": "Dune",
            "rating": 8.0,
            "summary": "A noble family battles for a desert planet.",
            "poster": "https://placehold.co/300x450?text=Dune"
        },
        {
            "title": "Arrival",
            "rating": 7.9,
            "summary": "A linguist deciphers alien communication.",
            "poster": "https://placehold.co/300x450?text=Arrival"
        },
        {
            "title": "Blade Runner 2049",
            "rating": 8.0,
            "summary": "A replicant hunter uncovers dangerous secrets.",
            "poster": "https://placehold.co/300x450?text=Blade+Runner"
        }
    ],

    "drama": [
        {
            "title": "Forrest Gump",
            "rating": 8.8,
            "summary": "A kind-hearted man witnesses history.",
            "poster": "https://placehold.co/300x450?text=Forrest+Gump"
        },
        {
            "title": "The Pursuit of Happyness",
            "rating": 8.0,
            "summary": "A struggling father seeks a better future.",
            "poster": "https://placehold.co/300x450?text=Happyness"
        },
        {
            "title": "Udaan",
            "rating": 8.1,
            "summary": "A teenager rebels against his strict father.",
            "poster": "https://placehold.co/300x450?text=Udaan"
        },
        {
            "title": "Lucia",
            "rating": 8.3,
            "summary": "A Kannada psychological drama about dreams.",
            "poster": "https://placehold.co/300x450?text=Lucia"
        },
        {
            "title": "Taare Zameen Par",
            "rating": 8.3,
            "summary": "A dyslexic child discovers confidence through art.",
            "poster": "https://placehold.co/300x450?text=Taare+Zameen+Par"
        }
    ],

    "thriller": [
        {"title": "Drishyam", "rating": 8.2, "summary": "A father protects his family.", "poster": "https://placehold.co/300x450?text=Drishyam"},
        {"title": "Kahaani", "rating": 8.1, "summary": "A woman searches for her missing husband.", "poster": "https://placehold.co/300x450?text=Kahaani"},
        {"title": "Se7en", "rating": 8.6, "summary": "Detectives hunt a serial killer.", "poster": "https://placehold.co/300x450?text=Se7en"},
        {"title": "Prisoners", "rating": 8.1, "summary": "A father searches for kidnapped children.", "poster": "https://placehold.co/300x450?text=Prisoners"},
        {"title": "Ratsasan", "rating": 8.3, "summary": "A cop hunts a brutal serial killer.", "poster": "https://placehold.co/300x450?text=Ratsasan"}
    ],

    "romance": [
        {"title": "DDLJ", "rating": 8.0, "summary": "Classic Bollywood romance.", "poster": "https://placehold.co/300x450?text=DDLJ"},
        {"title": "Jab We Met", "rating": 7.9, "summary": "A lively woman changes a man's life.", "poster": "https://placehold.co/300x450?text=Jab+We+Met"},
        {"title": "La La Land", "rating": 8.0, "summary": "Love and dreams collide.", "poster": "https://placehold.co/300x450?text=La+La+Land"},
        {"title": "Love Mocktail", "rating": 8.1, "summary": "Kannada romantic drama.", "poster": "https://placehold.co/300x450?text=Love+Mocktail"},
        {"title": "Titanic", "rating": 7.9, "summary": "Love story aboard a doomed ship.", "poster": "https://placehold.co/300x450?text=Titanic"}
    ],

    "horror": [
        {"title": "The Conjuring", "rating": 7.5, "summary": "Paranormal investigators face evil.", "poster": "https://placehold.co/300x450?text=Conjuring"},
        {"title": "Tumbbad", "rating": 8.2, "summary": "A dark Indian fantasy horror.", "poster": "https://placehold.co/300x450?text=Tumbbad"},
        {"title": "Kantara", "rating": 8.3, "summary": "Myth and folklore collide in Karnataka.", "poster": "https://placehold.co/300x450?text=Kantara"},
        {"title": "It", "rating": 7.3, "summary": "Children face a terrifying clown.", "poster": "https://placehold.co/300x450?text=IT"},
        {"title": "Stree", "rating": 7.5, "summary": "A ghost haunts a small town.", "poster": "https://placehold.co/300x450?text=Stree"}
    ],

    "animation": [
        {"title": "Coco", "rating": 8.4, "summary": "A boy journeys into the land of the dead.", "poster": "https://placehold.co/300x450?text=Coco"},
        {"title": "Toy Story", "rating": 8.3, "summary": "Toys secretly come alive.", "poster": "https://placehold.co/300x450?text=Toy+Story"},
        {"title": "Spider-Man: Into the Spider-Verse", "rating": 8.4, "summary": "Multiple Spider-Men unite.", "poster": "https://placehold.co/300x450?text=SpiderVerse"},
        {"title": "Frozen", "rating": 7.4, "summary": "A magical princess adventure.", "poster": "https://placehold.co/300x450?text=Frozen"},
        {"title": "Up", "rating": 8.3, "summary": "An old man flies his house.", "poster": "https://placehold.co/300x450?text=Up"}
    ],

    "crime": [
        {"title": "The Godfather", "rating": 9.2, "summary": "Mafia family saga.", "poster": "https://placehold.co/300x450?text=Godfather"},
        {"title": "Goodfellas", "rating": 8.7, "summary": "Rise and fall in organized crime.", "poster": "https://placehold.co/300x450?text=Goodfellas"},
        {"title": "Gangs of Wasseypur", "rating": 8.2, "summary": "Crime and revenge in India.", "poster": "https://placehold.co/300x450?text=Wasseypur"},
        {"title": "Omerta", "rating": 7.1, "summary": "Story of a terrorist operative.", "poster": "https://placehold.co/300x450?text=Omerta"},
        {"title": "Tagaru", "rating": 7.8, "summary": "Kannada gangster thriller.", "poster": "https://placehold.co/300x450?text=Tagaru"}
    ],

    "family": [
        {"title": "Home Alone", "rating": 7.7, "summary": "A child defends his house.", "poster": "https://placehold.co/300x450?text=Home+Alone"},
        {"title": "Finding Nemo", "rating": 8.2, "summary": "A fish searches for his son.", "poster": "https://placehold.co/300x450?text=Nemo"},
        {"title": "Rajakumara", "rating": 8.1, "summary": "Kannada emotional family drama.", "poster": "https://placehold.co/300x450?text=Rajakumara"},
        {"title": "Dangal", "rating": 8.3, "summary": "Father trains daughters in wrestling.", "poster": "https://placehold.co/300x450?text=Dangal"},
        {"title": "777 Charlie", "rating": 8.8, "summary": "A lonely man bonds with a dog.", "poster": "https://placehold.co/300x450?text=777+Charlie"}
    ]
}

# -----------------------------
# Session State for Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input(
    "Enter a genre (action, comedy, sci-fi, drama)"
)

if user_input:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    genre = user_input.lower().strip()

    # Bot Response
    if genre in movies_db:

        bot_message = (
            f"Great choice! Here are some "
            f"**{genre.title()}** movie recommendations 🎥"
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_message
        })

        with st.chat_message("assistant"):
            st.write(bot_message)

            movies = movies_db[genre]

            cols = st.columns(3)  # 3 cards per row

            for i, movie in enumerate(movies):
                with cols[i % 3]:

                    with st.container(border=True):
                        st.markdown(poster_html(movie["title"]), unsafe_allow_html=True)
                        st.subheader(movie["title"])
                        st.markdown(f"⭐ **IMDb Rating:** {movie['rating']}")
                        st.write(movie["summary"])

    else:
        bot_message = (
            "Sorry, I don't recognise that genre. "
            "Try: action, comedy, sci-fi, drama, thriller, romance, horror, animation, crime, or family."
        )
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_message
        })
        with st.chat_message("assistant"):
            st.write(bot_message)


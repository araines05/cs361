import streamlit as stream
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def get_mood_playlist(mood):

    mood_keywords = {
        # moods
        "happy": ["feel good", "upbeat", "pop", "summer hits", "good vibes"],
        "sad": ["sad songs", "emotional", "acoustic ballad", "piano", "heartbreak"],
        "chill": ["lofi", "acoustic", "ambient", "relax", "coffeehouse"],
        "romantic": ["love songs", "soft pop", "r&b slow jam", "acoustic love"],
        "angry": ["metal", "hard rock", "punk", "rage", "aggressive"],
        "motivated": ["inspirational", "anthem", "motivational pop", "empowerment"],
        "nostalgic": ["throwback", "90s hits", "80s classics", "oldies", "retro"],
        "melancholy": ["indie sad", "lofi chill", "piano", "soft rock", "dream pop"],
        "peaceful": ["ambient", "instrumental", "yoga music", "calm vibes"],
        "energetic": ["edm", "dance pop", "high energy", "workout mix"],

        # activites
        "workout": ["edm", "hip hop", "pump up", "gym motivation", "high energy"],
        "study": ["focus", "instrumental", "lofi", "ambient study", "piano"],
        "sleep": ["sleep", "calm", "ambient", "white noise", "relaxing"],
        "driving": ["driving rock", "road trip", "car songs", "classic rock", "pop rock"],
        "party": ["dance", "club", "pop", "house", "party anthems"],
        "cooking": ["indie pop", "acoustic", "chill vibes", "feel good"],
        "cleaning": ["pop hits", "dance pop", "throwback", "happy tunes"],
        "running": ["fast tempo", "running mix", "edm", "upbeat"],
        "studying": ["lofi hip hop", "ambient focus", "instrumental chill"],
        "gaming": ["gaming soundtrack", "trap beats", "synthwave", "cyberpunk"]
    }

    tracks = []
    for keyword in mood_keywords.get(mood, ["pop"]): 
        results = sp.search(q=keyword, type="track", limit=5)
        for item in results["tracks"]["items"]:
            tracks.append({
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "album": item["album"]["name"],
                "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                "url": item["external_urls"]["spotify"]
            })

    return tracks

# Streamlit --
stream.set_page_config(page_title="Mood Playlist Generator", page_icon="🎧")

stream.title("🎧 Playlist Generator")
stream.write("Select a mood or activity to generate a playlist:")

mood = stream.selectbox("Choose a mood:", ["happy", "sad", "chill", "romantic", "angry", "motivated", "nostalgic", 
                                        "melancholy", "peaceful", "energetic", "workout", "study", "sleep", 
                                        "driving", "party", "cooking", "cleaning", "running", "studying", "gaming"])

if stream.button("Generate Playlist"):
    playlist = get_mood_playlist(mood)
    stream.subheader(f"Playlist for {mood.capitalize()}")
    for t in playlist:
        col1, col2 = stream.columns([1, 3])
        with col1:
            stream.image(t["image"], width=80)
        with col2:
            stream.markdown(f"**{t['name']}**  \nby {t['artist']}")
            stream.markdown(f"[Listen on Spotify]({t['url']})")
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
        "sad": ["sad songs", "blues", "heartbreak", "gloomy"],
        "chill": ["lofi", "acoustic", "ambient", "relax", "coffeehouse"],
        "romantic": ["love songs", "soft pop", "r&b slow jam", "acoustic love"],
        "angry": ["metal", "hard rock", "punk", "rage", "aggressive"],
        "motivated": ["inspirational", "anthem", "motivational pop", "empowerment"],
        "nostalgic": ["throwback", "90s hits", "80s classics", "oldies", "retro"],
        "melancholy": ["indie sad", "lofi chill", "piano", "soft rock", "dream pop"],
        "peaceful": ["ambient", "instrumental", "yoga music", "calm vibes"],
        "energetic": ["edm", "dance pop", "high energy", "workout mix"],

        # activities
        "workout": ["edm", "hip hop", "pump up", "gym motivation", "high energy"],
        "study": ["focus", "instrumental", "lofi", "ambient study", "piano"],
        "sleep": ["sleep", "calm", "ambient", "white noise", "relaxing"],
        "driving": ["driving rock", "road trip", "car songs", "classic rock", "pop rock"],
        "party": ["party mix", "club", "pop", "house", "party anthems"],
        "cooking": ["indie pop", "acoustic", "chill vibes", "feel good"],
        "cleaning": ["pop hits", "dance pop", "throwback", "happy tunes"],
        "running": ["fast tempo", "running mix", "edm", "upbeat"],
        "studying": ["lofi hip hop", "ambient focus", "instrumental chill"],
        "gaming": ["gaming soundtrack", "trap beats", "synthwave", "cyberpunk"]
    }

    # Use song name + artist to remove duplicates
    unique_tracks = {}
    for keyword in mood_keywords.get(mood, ["pop"]):
        results = sp.search(q=keyword, type="track", limit=5)
        for item in results["tracks"]["items"]:
            key = f"{item['name'].lower()}_{item['artists'][0]['name'].lower()}"
            if key not in unique_tracks:
                unique_tracks[key] = {
                    "name": item["name"],
                    "artist": item["artists"][0]["name"],
                    "album": item["album"]["name"],
                    "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                    "url": item["external_urls"]["spotify"]
                }

    return list(unique_tracks.values())


def display_playlist(playlist):
    for i, track in enumerate(playlist, start=1):
        print(f"{i}. {track['name']} by {track['artist']} ({track['album']})")
        if track["image"]:
            print(f"   Album Artwork: {track['image']}")
        print(f"   Spotify URL: {track['url']}\n")

def welcome_message():
    welcome_art = """
  _____  _             _ _     _      _____                           _             
 |  __ \| |           | (_)   | |    / ____|                         | |            
 | |__) | | __ _ _   _| |_ ___| |_  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
 |  ___/| |/ _` | | | | | / __| __| | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |    | | (_| | |_| | | \__ \ |_  | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
 |_|    |_|\__,_|\__, |_|_|___/\__|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                  __/ |                                                             
                 |___/                                                              
"""
    print(welcome_art, "\n")
    print("Welcome to the Playlist Generator! Here you can generate and save a music playlist based on your selcted mood or activity!")

def generate_playlist(moods):
    print("\nAvailable moods/activities:")
    for mood in moods:
        print(f"- {mood}")

    choice = input("\nEnter the mood or activity for the playlist: ").strip().lower()
    if choice not in moods:
        print("Invalid choice! Returning to menu.\n")
        return

    playlist = get_mood_playlist(choice)
    print(f"\n Your {choice} playlist:\n")
    display_playlist(playlist)

    # Remove songs with confirmation (IH)
    while True:
        remove_choice = input("Enter the number of a song to remove it, or press Enter to save your playlist: ").strip()
        if not remove_choice:
            break
        if remove_choice.isdigit():
            idx = int(remove_choice) - 1
            if 0 <= idx < len(playlist):
                track_to_remove = playlist[idx]
                confirm = input(f"Are you sure you want to remove '{track_to_remove['name']}' by {track_to_remove['artist']}? Removing a song with completely delete it from your playlist, you cannot undo this. (y/n): ").strip().lower()
                if confirm == "y":
                    removed_track = playlist.pop(idx)
                    print(f"Removed: {removed_track['name']} by {removed_track['artist']}\n")
                    display_playlist(playlist)
                else:
                    print("Song not removed.\n")
            else:
                print("Invalid track number.\n")
        else:
            print("Please enter a valid number.\n")

    # Save playlist to a text file (user story)
    filename = f"{choice}_playlist.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for i, track in enumerate(playlist, start=1):
            f.write(f"{i}. {track['name']} by {track['artist']} ({track['album']})\n")
            if track["image"]:
                f.write(f"   Album Artwork: {track['image']}\n")
            f.write(f"   Spotify URL: {track['url']}\n\n")
    print(f"\nPlaylist saved to '{filename}'")

def show_info(moods):
    print("\nThis app generates playlists based on moods or activities and saves them to a text file. You can also remove songs from your playlist before saving them.")
    print("To get started, select 'Generate a playlist' from the main menu. Then, select a mood or activity to create your playlist!")
    print("Available moods/activities you can choose from:")
    for mood in moods:
        print(f"- {mood}")
    print()

def main():
    welcome_message()

    moods = ["happy", "sad", "chill", "romantic", "angry", "motivated", "nostalgic",
             "melancholy", "peaceful", "energetic", "workout", "study", "sleep",
             "driving", "party", "cooking", "cleaning", "running", "studying", "gaming"]

    while True:
        print("\n=== Playlist Generator ===")
        print("1. Generate a playlist")
        print("2. Help/More Info")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            generate_playlist(moods)
        elif choice == "2":
            show_info(moods)
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()

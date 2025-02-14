import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

client_id = ""
client_secret = ""

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Genres and Moods
genres_list = ["Blues", "Classical", "Country", "Electronic", "Hip hop", "Jazz", "Pop", "Reggae", "Rock", "Soul"]
moods = ["Happy", "Sad", "Energetic", "Chill", "Dark"]

# Music Industry
industries = {
    "Hollywood": "Hollywood",
    "Mollywood": "Mollywood",
    "Bollywood": "Bollywood",
    "Korean": "Korean"
}

artists = [
    {"name": "Taylor Swift", "genre": "Pop", "industry": "Hollywood"},
    {"name": "Drake", "genre": "Hip hop", "industry": "Hollywood"},
    {"name": "Ariana Grande", "genre": "Pop", "industry": "Hollywood"},
    {"name": "Beyoncé", "genre": "Pop", "industry": "Hollywood"},
    {"name": "Ed Sheeran", "genre": "Pop", "industry": "Hollywood"},
    {"name": "Adele", "genre": "Soul","industry": "Hollywood"},
    {"name": "Coldplay", "genre": "Rock","industry": "Hollywood"},
    {"name": "The Rolling Stones", "genre": "Rock","industry": "Hollywood"},
    {"name": "Stormzy", "genre": "Hip hop","industry": "Hollywood"},
    {"name": "The Beatles", "genre": "Rock","industry": "Hollywood"},
    {"name": "David Bowie", "genre": "Rock","industry": "Hollywood"},
    {"name": "Lily Allen", "genre": "Pop","industry": "Hollywood"},
    {"name": "Sam Smith", "genre": "Pop","industry": "Hollywood"},
    {"name": "The Cure", "genre": "Rock","industry": "Hollywood"},
    {"name": "B.B. King", "genre": "Blues","industry": "Hollywood"},
    {"name": "Ludwig van Beethoven", "genre": "Classical","industry": "Hollywood"},
    {"name": "Johnny Cash", "genre": "Country","industry": "Hollywood"},
    {"name": "Daft Punk", "genre": "Electronic","industry": "Hollywood"},
    {"name": "Kendrick Lamar", "genre": "Hip Hop","industry": "Hollywood"},
    {"name": "Miles Davis", "genre": "Jazz","industry": "Hollywood"},
    {"name": "Michael Jackson", "genre": "Pop","industry": "Hollywood"},
    {"name": "Bob Marley", "genre": "Reggae","industry": "Hollywood"},
    {"name": "Aretha Franklin", "genre": "Soul","industry": "Hollywood"},
    {"name": "James Brown", "genre": "Soul","industry": "Hollywood"},
    {"name": "Lata Mangeshkar", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "Arijit Singh", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "Amit Trivedi", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "Shreya Ghoshal", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "Neha Kakkar", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "Atif Aslam", "genre": "Bollywood", "industry": "Bollywood"},
    {"name": "K. J. Yesudas", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "M. G. Sreekumar", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "Vineeth Sreenivasan", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "K. S. Chitra", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "Vijay Yesudas", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "Sudeep Kumar", "genre": "Mollywood", "industry": "Mollywood"},
    {"name": "BTS", "genre": "Korean", "industry": "Korean"},
    {"name": "BLACKPINK", "genre": "Korean", "industry": "Korean"},
    {"name": "EXO", "genre": "Korean", "industry": "Korean"},
    {"name": "TWICE", "genre": "Korean", "industry": "Korean"},
    {"name": "IU", "genre": "Korean", "industry": "Korean"},
]

# Fetch Songs for an Artist
def fetch_songs(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="track", limit=25)
    return [{"name": track["name"], "id": track["id"]} for track in results["tracks"]["items"]]

# Generate Turtle Data
def generate_ttl(artists):
    ttl_data = """
@prefix : <http://spotify.com/music#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://spotify.com/music#> .

<http://www.music.com/ontologies/recommendation> rdf:type owl:Ontology ;
                                                  rdfs:comment "This Ontology is built for a music recommendation website" .

# Classes
:Artist rdf:type rdfs:Class .
:Song rdf:type rdfs:Class .
:Genre rdf:type rdfs:Class .
:Mood rdf:type rdfs:Class .
:Industry rdf:type rdfs:Class .

# Properties
:hasGenre rdf:type rdf:Property ;
    rdfs:domain :Song ;
    rdfs:range :Genre .

:hasProduced rdf:type rdf:Property ;
    rdfs:domain :Song ;
    rdfs:range :Artist .

:hasMood rdf:type rdf:Property ;
    rdfs:domain :Song ;
    rdfs:range :Mood .

:hasIndustry rdf:type rdf:Property ;
    rdfs:domain :Song ;
    rdfs:range :Industry .
"""

    for artist in artists:
        artist_name = artist["name"]
        genre = artist["genre"]
        industry = artist["industry"]

        # Artist
        ttl_data += f"""
:artist_{artist_name.replace(" ", "_").lower()} rdf:type :Artist ;
    rdfs:label "{artist_name}"^^xsd:string ;
    :hasIndustry :industry_{industry.lower()} .
"""

        # Fetch songs for the artist
        songs = fetch_songs(artist_name)
        for song in songs:
            song_id = song["id"]
            song_name = song["name"]
            song_mood = random.choice(moods)
            industry_type = industries[industry]

            ttl_data += f"""
:song_{song_id} rdf:type :Song ;
    rdfs:label "{song_name}"^^xsd:string ;
    :hasProduced :artist_{artist_name.replace(" ", "_").lower()} ;
    :hasGenre :genre_{genre.replace(" ", "_").lower()} ;
    :hasMood :mood_{song_mood.lower()}.
"""

            # Genre, Mood, and Industry
            ttl_data += f"""
:genre_{genre.replace(" ", "_").lower()} rdf:type :Genre ;
    rdfs:label "{genre}"^^xsd:string .

:mood_{song_mood.lower()} rdf:type :Mood ;
    rdfs:label "{song_mood}"^^xsd:string .

:industry_{industry_type.lower()} rdf:type :Industry ;
    rdfs:label "{industry_type}"^^xsd:string .
"""

    return ttl_data

ttl_content = generate_ttl(artists)


with open("music_ontology_1.ttl", "w", encoding="utf-8") as file:
    file.write(ttl_content)

print("Ontology written to music_ontology.ttl")

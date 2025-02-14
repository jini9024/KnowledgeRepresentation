from flask import Flask, render_template, request
from rdflib import Graph


app = Flask(__name__)

# Load RDF data from file
rdf_file_path = r'music_ontology.ttl'
graph = Graph()
graph.parse(rdf_file_path, format='turtle')

@app.route('/')
def home():
    genre_query = """
        PREFIX sp: <http://spotify.com/music#>
        SELECT DISTINCT ?genre
        WHERE {
            ?song sp:hasGenre ?genreResource .
            ?genreResource rdfs:label ?genre .
        }
    """
    genres = [str(row.genre) for row in graph.query(genre_query)]

    artist_query = """
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?artist
        WHERE {
            ?song sp:hasProduced ?artistResource ;
                  sp:hasIndustry ?industryResource .
            ?artistResource rdfs:label ?artist . 
            ?industryResource rdfs:label "Hollywood" .
        }
    """
    hollywood_artists = [str(row.artist) for row in graph.query(artist_query)]

    return render_template("home.html", genres=genres, artists=hollywood_artists)



@app.route('/playlists/hollywood', methods=["GET"])
def hollywood():
    industry = "Hollywood"
    query_hollywood = """
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {
            ?song rdf:type sp:Song ; 
                  rdfs:label ?songLabel ;
                  sp:hasIndustry sp:industry_hollywood ;
                  sp:hasProduced ?artistResource .
            ?artistResource rdfs:label ?artist .
        }
    """
    results = graph.query(query_hollywood)
    tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]
    return render_template("hollywood.html", tracks=tracks)


@app.route('/playlists/bollywood', methods=["GET"])
def bollywood():
    industry = "Bollywood"
    query_bollywood = """
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {
            ?song rdf:type sp:Song ; 
                  rdfs:label ?songLabel ;
                  sp:hasIndustry sp:industry_bollywood ;
                  sp:hasProduced ?artistResource .
            ?artistResource rdfs:label ?artist .
        }
    """
    results = graph.query(query_bollywood)
    tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]
    return render_template("bollywood.html", tracks=tracks)


@app.route('/playlists/mollywood', methods=["GET"])
def mollywood():
    industry = "Mollywood"
    query_mollywood = """
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {
            ?song rdf:type sp:Song ; 
                  rdfs:label ?songLabel ;
                  sp:hasIndustry sp:industry_mollywood ;
                  sp:hasProduced ?artistResource .
            ?artistResource rdfs:label ?artist .
        }
    """
    results = graph.query(query_mollywood)
    tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]
    return render_template("mollywood.html", tracks=tracks)


@app.route('/playlists/korean', methods=["GET"])
def korean():
    industry = "Korean"
    query_korean = """
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {
            ?song rdf:type sp:Song ; 
                  rdfs:label ?songLabel ;
                  sp:hasIndustry sp:industry_korean ;
                  sp:hasProduced ?artistResource .
            ?artistResource rdfs:label ?artist .
        }
    """
    results = graph.query(query_korean)
    tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]
    return render_template("korean.html", tracks=tracks)


@app.route('/search', methods=["POST"])
def search():
    genre = request.form.get("genre") or ""
    artist = request.form.get("artist") or ""

    query = f"""
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {{
            ?song rdf:type sp:Song ; 
                  rdfs:label ?songLabel ;
                  sp:hasProduced ?artistResource ;
                  sp:hasGenre ?genreResource .
            ?artistResource rdfs:label ?artistLabel .
            ?genreResource rdfs:label ?genreLabel .
            FILTER regex(str(?artistLabel), "{artist}")
            FILTER regex(str(?genreLabel), "{genre}")
        }}
    """
    try:
        results = graph.query(query)
        tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]

        # Handle empty results
        if not tracks:
            tracks = [{"label": "No results found"}]

    except Exception as e:
        tracks = [{"label": f"Error: {str(e)}"}]

    return render_template("search.html", tracks=tracks)


@app.route('/mood', methods=['POST'])
def mood():
    mood = request.form.get("mood")

    query_mood = """ 
        PREFIX sp: <http://spotify.com/music#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?song ?songLabel ?artist
        WHERE {
            ?song rdf:type sp:Song ;
                  rdfs:label ?songLabel ;
                  sp:hasMood ?moodResource ;
                  sp:hasProduced ?artistResource .
            ?moodResource rdfs:label ?mood .
            ?artistResource rdfs:label ?artist .
            FILTER regex(str(?mood), \"""" + mood + """\")
        }
        LIMIT 10
    """
    results = graph.query(query_mood)
    tracks = [{"label": str(row.songLabel), "artist": str(row.artist)} for row in results]

    return render_template("mood.html", tracks=tracks, mood=mood)


if __name__ == '__main__':
    app.run(debug=True)

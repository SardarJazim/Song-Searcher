from flask import Flask, request, render_template
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import pickle
import pandas as pd
import nltk

nltk.download('punkt')

app = Flask(__name__)

# =======================
# Load Models and Data
# =======================

# Load the fine-tuned SBERT model
print("Loading SBERT model...")
sbert_model = SentenceTransformer('./sbert_finetuned')  # Path to SBERT model folder

# Load precomputed song data with embeddings
print("Loading precomputed song data with embeddings...")
with open('./models/song_data_with_embeddings.pkl', 'rb') as f:
    song_data = pickle.load(f)

# Normalize mxm_track_id in song_data for consistency
for song in song_data:
    song['mxm_track_id'] = str(int(float(song['mxm_track_id']))).strip()  # Convert to string for consistency

# Debug: Check mxm_track_id values in song_data
print("First 5 mxm_track_id values in song_data:")
for song in song_data[:5]:
    print(song['mxm_track_id'])

# Load the cleaned mapping file (pandas DataFrame)
print("Loading cleaned mapping file...")
mapping = pd.read_pickle('./models/cleaned_mapping.pkl')

# Normalize mapping data and convert to dictionary for quick lookups
print("Normalizing mapping data...")
mapping_dict = {}
for _, row in mapping.iterrows():
    mxm_id = str(int(float(row['mxm_track_id']))).strip()  # Normalize to string
    mapping_dict[mxm_id] = {
        'artist_name_mxm': row['artist_name_mxm'].strip(),
        'title_mxm': row['title_mxm'].strip()
    }

# Debug: Check the first few entries in mapping_dict
print("First 5 keys in mapping_dict:")
for key in list(mapping_dict.keys())[:5]:
    print(key, mapping_dict[key])

# Initialize BM25 for tokenized lyrics
print("Initializing BM25...")
tokenized_corpus = [nltk.word_tokenize(song['processed_lyrics']) for song in song_data]
bm25 = BM25Okapi(tokenized_corpus)

print("Models and data loaded successfully!")

# =======================
# Flask Routes
# =======================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # Get user query
    query = request.form['lyrics']
    tokenized_query = nltk.word_tokenize(query.lower())

    # BM25 Scores
    bm25_scores = bm25.get_scores(tokenized_query)

    # SBERT Scores
    query_embedding = sbert_model.encode(query, convert_to_tensor=False)
    sbert_scores = [query_embedding @ song["embedding"] for song in song_data]

    # Combine BM25 and SBERT Scores
    combined_scores = [
        (i, 0.5 * bm25_scores[i] + 0.5 * sbert_scores[i]) for i in range(len(song_data))
    ]
    combined_scores = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    # Get Top Results with Titles and Artists
    top_results = []
    for i, _ in combined_scores[:5]:
        track_id = song_data[i]["mxm_track_id"]

        # Check if track_id exists in mapping_dict
        if track_id in mapping_dict:
            artist = mapping_dict[track_id]['artist_name_mxm']
            title = mapping_dict[track_id]['title_mxm']
        else:
            print(f"Track ID {track_id} not found in mapping_dict!")  # Debugging
            artist = "Unknown Artist"
            title = "Unknown Title"

        top_results.append({
            "track_id": track_id,
            "artist": artist,
            "title": title
        })

    # Render Results
    return render_template('index.html', query=query, results=top_results)


if __name__ == '__main__':
    app.run(debug=True)

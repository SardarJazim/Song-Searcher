# 🎵 Song Searcher Flask Application

**Song Searcher** is a web-based application that helps users find song titles and artists by entering partial lyrics. This app uses a combination of **Sentence-BERT (SBERT)** for semantic search and **BM25** for keyword-based matching to deliver accurate and relevant search results.

---

## 📋 **Features**

- Enter **partial song lyrics** to search for matching song titles and artists.
- Utilizes a combination of **BM25** and **SBERT** for efficient and accurate retrieval.
- Displays the **top 5 matching results** with the song title and artist name.
- Handles large datasets using preprocessed data for faster performance.

---

## 🛠️ **Technologies Used**

### **Backend**
- **Flask**: Python-based web framework.
- **Sentence-BERT (SBERT)**: For semantic similarity search.
- **BM25**: For keyword-based retrieval.

### **Data Processing**
- **Pandas**: For cleaning and managing datasets.
- **Pickle**: For saving and loading preprocessed data.
- **NLTK**: For tokenizing song lyrics.

### **Data**
- Preprocessed **MusiXmatch dataset**: Contains song IDs, lyrics, titles, and artist names.

---

## 🚀 **Setup Instructions**

Follow the steps below to set up and run the project locally:

### 1. **Project Structure**
```yaml
song_searcher/
  ├── app.py                    # Flask application
  ├── sbert_finetuned/          # Folder containing fine-tuned SBERT model
  ├── models/                   # Folder for preprocessed data
  │   ├── song_data_with_embeddings.pkl  # Preprocessed song data with embeddings
  │   └── cleaned_mapping.pkl            # Mapping file (song ID to title/artist)
  ├── static/                   # Folder for static files
  │   └── style.css             # Optional CSS for styling
  └── templates/                # Folder for HTML templates
      ├── base.html             # Base HTML template
      └── index.html            # Main search page
```
## 2. **Environment Setup**

### Create and activate a virtual environment:

#### For **Windows**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### For **Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### Requirement.txt
flask
sentence-transformers
rank-bm25
nltk
pandas

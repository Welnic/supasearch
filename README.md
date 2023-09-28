# Supasearch - Image Search Engine

## About

This web app is an image search engine that allows users to search for specific images and upload their own images for searching. It leverages the power of Streamlit, Supabase with pgvector, and the OpenAI CLIP model to enable efficient image searching and retrieval.

## Access the App

You can access the web app by clicking [here](https://supasearch.streamlit.app/?page=success).

## Features

- **Image Search**: Users can search for specific images by entering text queries.
- **Image Upload**: Registered users can upload their own images to search through the existing collection.
- **Vector-based Search**: The app uses pgvector and CLIP to perform similarity-based image searches, providing accurate and relevant results.
- **User Authentication**: Users can register and log in to access additional features like image upload.
- **Free & open-source**: The app is free to use and the code is available for anyone to view and contribute to.

## See also

[Storing OpenAI embeddings in Postgres with pgvector
](https://supabase.com/blog/openai-embeddings-postgres-vector)

## Development guide

_This app is built with [Streamlit](https://docs.streamlit.io/)._

### Pre-requisites

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Supabase](https://supabase.io/)
- [pgvector](https://supabase.com/docs/guides/database/extensions/pgvector)
- [vecs](https://supabase.com/docs/guides/ai/vecs-python-client)
- [OpenAI CLIP Model](https://github.com/openai/CLIP)

## Setup

1. **Clone the Repository:**

```bash
   git clone https://github.com/Welnic/supasearch.git
   cd your-repo
```

2. **Install dependencies:**

```bash
   pip install -r requirements.txt
```

3. **Configure Supabase**:

- Create a Supabase project and set up your database. Add pgvector extension to your database.
- Obtain your Supabase URL and API Key and update the .env file with your credentials as followings:

# .env.example

SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_KEY = "xxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxx.xxxxxxxxx-xxxxxx"
DB_USER = "xxxxxxx"
PASSWORD = "xxxxxxxx"
HOST = "db.xxxxxxxxx.supabase.co"
PORT = "5432"
DB_NAME = "xxxxx"

4. **Run the App**:

```bash
  poetry run streamlit run app.py
```

⭐ Happy image searching! ⭐

## Author

- **Author**: Catalina

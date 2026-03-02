# HackerNews Sentiment Analysis API

A FastAPI-based REST API that fetches posts from HackerNews and performs sentiment analysis on them. This project analyzes the sentiment of HackerNews stories based on their titles and content, helping you understand the overall tone of discussions around specific topics.

## What Does It Do?

This API lets you search for HackerNews posts by keyword and returns sentiment analysis for each post. It uses TextBlob to analyze the polarity of the text and categorizes each post as Positive, Negative, or Neutral.

## Features

- Search HackerNews posts by keyword
- Retrieve a customizable number of posts (default: 5)
- Sentiment analysis powered by TextBlob
- Get polarity scores and sentiment categories for each post
- Returns post metadata including title, author, score, and URL

## Installation

First, clone this repository:

```bash
git clone https://github.com/HitenAnand2207/hackernews-sentiment-api.git
cd hackernews-sentiment-api
```

Create a virtual environment and activate it:

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

Install the required dependencies:

```bash
pip install fastapi uvicorn textblob requests
```

## Running the API

Start the API server with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

You can access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### GET /

Returns a welcome message to confirm the API is running.

**Response:**
```json
{
  "message": "HackerNews Sentiment Prediction API is running!"
}
```

### POST /fetch_tweets/

Fetches HackerNews posts for a given keyword and returns sentiment analysis.

**Request Body:**
```json
{
  "keyword": "python",
  "count": 5
}
```

**Parameters:**
- `keyword` (string, required): The search term
- `count` (integer, optional): Number of posts to fetch (default: 5)

**Response:**
```json
{
  "keyword": "python",
  "total_fetched": 5,
  "results": [
    {
      "title": "Post Title",
      "text": "Post content...",
      "posted_by": "username",
      "score": 42,
      "url": "https://example.com",
      "polarity": 0.5,
      "sentiment": "Positive"
    }
  ]
}
```

## How Sentiment Analysis Works

The API analyzes text using TextBlob's sentiment analysis:

- **Positive**: Polarity score > 0.1
- **Negative**: Polarity score < -0.1
- **Neutral**: Polarity score between -0.1 and 0.1

Polarity scores range from -1 (most negative) to 1 (most positive).

## Example Usage

Using curl:

```bash
curl -X POST "http://localhost:8000/fetch_tweets/" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "artificial intelligence", "count": 10}'
```

Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/fetch_tweets/",
    json={"keyword": "machine learning", "count": 5}
)

print(response.json())
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- TextBlob
- Requests

## Project Structure

```
hackernews-sentiment-api/
├── main.py          # Main API application
├── .gitignore       # Git ignore file
└── README.md        # This file
```

## Author

Hiten Anand (Roll: 2330373)

## Acknowledgments

- Uses the HackerNews Algolia Search API
- Sentiment analysis powered by TextBlob

## License

This project is open source and available for educational purposes.

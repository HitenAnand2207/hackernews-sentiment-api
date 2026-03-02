from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob
import requests


app = FastAPI(title="Sentiment Prediction API - HackerNews Edition\n Name-Hiten Anand Roll-2330373")


HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"


class PostRequest(BaseModel):
    keyword: str
    count: int = 5


def analyze_sentiment(text: str) -> dict:
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        category = "Positive"
    elif polarity < -0.1:
        category = "Negative"
    else:
        category = "Neutral"

    return {
        "polarity": round(polarity, 4),
        "sentiment": category
    }


@app.get("/")
def root():
    return {"message": "HackerNews Sentiment Prediction API is running!"}


@app.post("/fetch_tweets/")
def fetch_posts(request: PostRequest):
    try:
       
        params = {
            "query": request.keyword,
            "tags": "story",
            "hitsPerPage": request.count
        }

        response = requests.get(HN_SEARCH_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch from HackerNews.")

        data = response.json()
        hits = data.get("hits", [])

        if not hits:
            raise HTTPException(
                status_code=404,
                detail=f"No posts found for keyword '{request.keyword}'."
            )

        results = []
        for hit in hits:
            title = hit.get("title", "") or ""
            text = hit.get("story_text", "") or ""
            url = hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            by = hit.get("author", "unknown")
            score = hit.get("points", 0)

            full_text = title + " " + text
            sentiment = analyze_sentiment(full_text)

            results.append({
                "title": title,
                "text": text[:300] if text else "No body text",
                "posted_by": by,
                "score": score,
                "url": url,
                "polarity": sentiment["polarity"],
                "sentiment": sentiment["sentiment"]
            })

        return {
            "keyword": request.keyword,
            "total_fetched": len(results),
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
from config import LIHKG_KEYWORDS
from src.apify_runner import run_actor

ACTOR_ID = "claude_code_reviewer/lihkg-scraper-en"


def search_stock(symbol, keywords):
    """Find recent LIHKG threads mentioning one stock."""
    run_input = {
        "mode": "search",
        "keywords": keywords,
        "order": "desc_reply_time",
        "dateFrom": "10d",
        "maxItems": 20,
    }
    items = run_actor(ACTOR_ID, run_input, f"lihkg_search_{symbol}")
    for item in items:
        print(f"  {item['created_at'][:10]}  replies={item['reply_count']:<5} {item['title']}")
    return items


if __name__ == "__main__":
    for symbol, keywords in LIHKG_KEYWORDS.items():
        print(f"\n=== {symbol} ===")
        search_stock(symbol, keywords)
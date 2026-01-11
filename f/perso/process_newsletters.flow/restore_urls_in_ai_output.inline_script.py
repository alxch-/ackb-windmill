def main(ai_output: dict, url_mapping: dict) -> dict:
    # Restore URLs in each article
    for article in ai_output.get("articles", []):
        url = article.get("url", "")
        if url in url_mapping:
            article["url"] = url_mapping[url]

    return ai_output

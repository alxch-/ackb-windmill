#requirements:
#openai
#supabase

from openai import OpenAI
from supabase import create_client


def main(
    openai_resource: dict,
    supabase_resource: dict,
    type: str,
    source: str,
    newsletter_summary: str,
    language: str,
    articles: list[dict],
    subject: str = "",
    date: str = "",
) -> dict:
    """
    Generate embeddings and store newsletter.

    Args:
        openai_resource: OpenAI resource {api_key, organization_id}
        supabase_resource: Supabase resource {url, key}
        type: "links" or "text-only"
        source: Newsletter name
        newsletter_summary: Summary from LLM
        language: Language code
        articles: List of {title, summary, url, topics}
        subject: Original email subject
        date: Email received date (ISO format)
    """
    # --- Generate embeddings ---
    openai_client = OpenAI(
        base_url=openai_resource["base_url"],
        api_key=openai_resource["api_key"]
    )

    texts = [newsletter_summary]
    for article in articles:
        texts.append(f"{article['title']}. {article['summary']}")

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    embeddings = [item.embedding for item in sorted(response.data, key=lambda x: x.index)]

    # --- Store in Supabase ---
    supabase = create_client(
        supabase_resource["url"],
        supabase_resource["key"]
    )

    # Insert newsletter
    newsletter_data = {
        "source": source,
        "subject": subject,
        "summary": newsletter_summary,
        "type": type,
        "language": language,
        "embedding": embeddings[0]
    }

    if date:
        newsletter_data["received_at"] = date

    newsletter = supabase.table("newsletters").insert(newsletter_data).execute()

    newsletter_id = newsletter.data[0]["id"]

    # Insert articles
    articles_created = 0
    for i, article in enumerate(articles):
        supabase.table("articles").insert({
            "newsletter_id": newsletter_id,
            "title": article["title"],
            "url": article["url"],
            "summary": article["summary"],
            "topics": article.get("topics", []),
            "embedding": embeddings[i + 1] if i + 1 < len(embeddings) else None
        }).execute()
        articles_created += 1

    return {
        "newsletter_id": newsletter_id,
        "articles_created": articles_created,
        "success": True
    }
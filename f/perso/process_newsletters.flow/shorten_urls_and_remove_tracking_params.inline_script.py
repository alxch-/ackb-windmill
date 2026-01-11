def main(text_html: str) -> dict:
    import re
    from urllib.parse import urlparse, urlunparse

    def strip_query_params(url: str) -> str:
        """Remove query parameters from URL (usually tracking junk)"""
        parsed = urlparse(url)
        # Keep only scheme, netloc, and path
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    url_pattern = r'https?://[^\s<>"\']+(?=[<"\'\s]|$)'
    urls = re.findall(url_pattern, text_html)

    url_mapping = {}
    shortened_html = text_html

    for i, url in enumerate(set(urls)):  # dedupe
        placeholder = f"[URL_{i}]"
        clean_url = strip_query_params(url)
        url_mapping[placeholder] = clean_url  # Store cleaned URL
        shortened_html = shortened_html.replace(url, placeholder)

    return {
        "shortened_html": shortened_html,
        "url_mapping": url_mapping
    }

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

TIMEOUT_SECONDS = 8
MAX_RESULTS = 5
USER_AGENT = "LocationInfoMap/1.0 (link search)"


def search_site_links(base_url, keyword):
    """Search matching links on one configured location website's home page."""
    parsed_base = urlparse(base_url)
    if parsed_base.scheme != "https" or not parsed_base.hostname or parsed_base.username:
        return []

    try:
        response = requests.get(
            base_url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
            allow_redirects=False,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        matches = []
        seen = set()
        normalized_keyword = keyword.casefold()

        for anchor in soup.find_all("a", href=True):
            title = anchor.get_text(" ", strip=True)
            link_url = urljoin(base_url, anchor["href"].strip())
            parsed_link = urlparse(link_url)
            if parsed_link.scheme not in ("http", "https") or not title:
                continue
            if normalized_keyword not in title.casefold() and normalized_keyword not in link_url.casefold():
                continue
            if link_url not in seen:
                seen.add(link_url)
                matches.append({"title": title[:300], "url": link_url})
            if len(matches) >= MAX_RESULTS:
                break

        return matches
    except requests.RequestException:
        return []
    except (ValueError, TypeError):
        return []

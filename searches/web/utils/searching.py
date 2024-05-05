import typing
import requests
from ...config import BASE_URL, MAX_RESULTS
from .parsing import parse_result


def fetch_search_results(query: str, language: str) -> dict:
    url = BASE_URL.format(query=query, kl=language)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return None


def search(query: str, language: str) -> typing.List[typing.Dict[str, str]]:
    results_list = []
    data = fetch_search_results(query, language)

    if data and 'RelatedTopics' in data:
        related_topics = data['RelatedTopics']
        if related_topics:
            for topic in related_topics[:MAX_RESULTS]:
                result_html = topic.get('Result', '')
                if result_html:
                    title, preview, url = parse_result(result_html)
                    result = {
                        'title': title,
                        'preview': preview,
                        'url': url
                    }
                    results_list.append(result)

    return results_list
import typing
from bs4 import BeautifulSoup


def parse_result(result_html: str) -> typing.Tuple[str, str, str]:
    soup = BeautifulSoup(result_html, 'html.parser')
    title = soup.a.get_text()
    preview = soup.get_text().strip()

    if preview.startswith(title):
        preview = preview[len(title):].strip()

    preview = preview.lstrip(' -')

    url = soup.a['href']
    return title, preview, url
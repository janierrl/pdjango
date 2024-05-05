import typing


BASE_URL: typing.Final[str] = "https://api.duckduckgo.com/?q={query}&format=json&kl={kl}"
MAX_RESULTS: typing.Final[int] = 10
LANGUAGES: typing.Final[dict] = {
    'en-en': 'en',
    'es-es': 'es',
}

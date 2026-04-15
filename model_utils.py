import re
from urllib.parse import urlparse

URL_FEATURE_COLUMNS = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_at',
    'nb_qm', 'nb_and', 'nb_or', 'nb_eq', 'nb_underscore', 'nb_tilde',
    'nb_percent', 'nb_slash', 'nb_star', 'nb_colon', 'nb_comma', 'nb_semicolumn',
    'nb_dollar', 'nb_space', 'nb_www', 'nb_com', 'nb_dslash', 'http_in_path',
    'https_token', 'ratio_digits_url', 'ratio_digits_host', 'punycode', 'port',
    'tld_in_path', 'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains',
    'prefix_suffix', 'random_domain', 'shortening_service', 'path_extension',
    'nb_redirection', 'nb_external_redirection', 'length_words_raw', 'char_repeat',
    'shortest_words_raw', 'shortest_word_host', 'shortest_word_path',
    'longest_words_raw', 'longest_word_host', 'longest_word_path',
    'avg_words_raw', 'avg_word_host', 'avg_word_path',
]

CLASS_MAP = {'legitimate': 0, 'phishing': 1}
CLASS_LABELS = {0: 'legitimate', 1: 'phishing'}

SHORTENER_DOMAINS = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'tiny.cc', 'is.gd',
    'buff.ly', 'adf.ly', 'bit.do', 'shorte.st', 't.ly', 'cutt.ly', 'lc.chat',
}

COMMON_TLDS = {
    '.com', '.net', '.org', '.biz', '.info', '.co', '.us', '.uk', '.edu', '.gov',
    '.io', '.me', '.tv', '.xyz', '.online', '.site', '.tech', '.store', '.blog',
}


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    if not re.match(r'^[a-zA-Z]+://', url):
        url = 'http://' + url
    return url


def is_ip_address(host: str) -> bool:
    return bool(re.fullmatch(r'\d{1,3}(?:\.\d{1,3}){3}', host))


def split_words(text: str) -> list[str]:
    tokens = re.split(r'[^a-zA-Z0-9]+', text)
    return [token for token in tokens if token]


def token_stats(tokens: list[str]) -> tuple[int, int, int, float]:
    if not tokens:
        return 0, 0, 0, 0.0
    lengths = [len(token) for token in tokens]
    return len(tokens), min(lengths), max(lengths), sum(lengths) / len(lengths)


def max_repeat_run(text: str) -> int:
    if not text:
        return 0
    max_run = current = 1
    last = text[0]
    for char in text[1:]:
        if char == last:
            current += 1
        else:
            max_run = max(max_run, current)
            current = 1
            last = char
    return max(max_run, current)


def contains_tld_segment(text: str) -> int:
    lower = text.lower()
    return int(any(tld in lower for tld in COMMON_TLDS))


def extract_url_features(url: str) -> dict[str, float]:
    url = normalize_url(url)
    parsed = urlparse(url)
    host = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''
    fragment = parsed.fragment or ''
    full_path = path + query + fragment
    raw_text = url

    host_tokens = split_words(host)
    path_tokens = split_words(path)
    raw_tokens = split_words(raw_text)

    host_digits = sum(ch.isdigit() for ch in host)
    url_digits = sum(ch.isdigit() for ch in raw_text)

    subdomain_parts = host.split('.') if host else []
    nb_subdomains = max(0, len(subdomain_parts) - 2) if host and not is_ip_address(host) else 0
    tld_in_subdomain = 0
    for part in subdomain_parts[:-2]:
        if any(part.lower().endswith(tld.lstrip('.')) for tld in COMMON_TLDS):
            tld_in_subdomain = 1
            break

    shortened = host.lower()
    shortening_service = int(any(short in shortened for short in SHORTENER_DOMAINS))
    random_domain = 0
    letters = re.findall(r'[a-zA-Z]', host)
    if letters:
        vowel_ratio = sum(ch in 'aeiouAEIOU' for ch in letters) / len(letters)
        if vowel_ratio < 0.3 and len(letters) >= 6:
            random_domain = 1
        elif len(re.findall(r'\d', host)) >= 4:
            random_domain = 1

    return {
        'length_url': len(raw_text),
        'length_hostname': len(host),
        'ip': int(is_ip_address(host)),
        'nb_dots': raw_text.count('.'),
        'nb_hyphens': raw_text.count('-'),
        'nb_at': raw_text.count('@'),
        'nb_qm': raw_text.count('?'),
        'nb_and': raw_text.count('&'),
        'nb_or': raw_text.count('|'),
        'nb_eq': raw_text.count('='),
        'nb_underscore': raw_text.count('_'),
        'nb_tilde': raw_text.count('~'),
        'nb_percent': raw_text.count('%'),
        'nb_slash': raw_text.count('/'),
        'nb_star': raw_text.count('*'),
        'nb_colon': raw_text.count(':'),
        'nb_comma': raw_text.count(','),
        'nb_semicolumn': raw_text.count(';'),
        'nb_dollar': raw_text.count('$'),
        'nb_space': raw_text.count(' '),
        'nb_www': raw_text.lower().count('www'),
        'nb_com': raw_text.lower().count('.com'),
        'nb_dslash': raw_text.count('//'),
        'http_in_path': int('http' in full_path.lower()),
        'https_token': int('https' in raw_text.lower()),
        'ratio_digits_url': url_digits / len(raw_text) if raw_text else 0.0,
        'ratio_digits_host': host_digits / len(host) if host else 0.0,
        'punycode': int('xn--' in host.lower()),
        'port': int(parsed.port is not None),
        'tld_in_path': contains_tld_segment(path),
        'tld_in_subdomain': tld_in_subdomain,
        'abnormal_subdomain': int('@' in raw_text or nb_subdomains > 2),
        'nb_subdomains': nb_subdomains,
        'prefix_suffix': int('-' in host),
        'random_domain': random_domain,
        'shortening_service': shortening_service,
        'path_extension': int(bool(re.search(r'\.[a-zA-Z0-9]{1,5}$', path))),
        'nb_redirection': 0,
        'nb_external_redirection': 0,
        'length_words_raw': len(raw_tokens),
        'char_repeat': max_repeat_run(raw_text),
        'shortest_words_raw': min((len(token) for token in raw_tokens), default=0),
        'shortest_word_host': min((len(token) for token in host_tokens), default=0),
        'shortest_word_path': min((len(token) for token in path_tokens), default=0),
        'longest_words_raw': max((len(token) for token in raw_tokens), default=0),
        'longest_word_host': max((len(token) for token in host_tokens), default=0),
        'longest_word_path': max((len(token) for token in path_tokens), default=0),
        'avg_words_raw': sum((len(token) for token in raw_tokens), 0) / len(raw_tokens) if raw_tokens else 0.0,
        'avg_word_host': sum((len(token) for token in host_tokens), 0) / len(host_tokens) if host_tokens else 0.0,
        'avg_word_path': sum((len(token) for token in path_tokens), 0) / len(path_tokens) if path_tokens else 0.0,
    }

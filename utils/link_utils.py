import urlparse


def resolve_relative_paths(base_url, pages):
    resolved_pages = set()
    for page in pages:
            resolved_page = resolve_one_relative_page(base_url, page)
            resolved_pages.add(resolved_page)
    return resolved_pages


def resolve_one_relative_page(base_url, page):
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "http://{b}".format(b=base_url)
    hostname = urlparse.urlparse(base_url).scheme + "://" + urlparse.urlparse(base_url).hostname
    if page.startswith("http://") or page.startswith("https://"):
        return page
    else:
        if page.startswith("/"):
            resolved_page = hostname + page
        else:
            if base_url.endswith("/"):
                resolved_page = base_url + page
            else:
                resolved_page = base_url + "/" + page
    return resolved_page
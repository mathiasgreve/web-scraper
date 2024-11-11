"""
Task 1.2, 1.3

Filtering URLs from HTML
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str | None = None,
) -> set[str]:
    """
    Find all the url links in a html text using regex

    Arguments:
        html (str): html string to parse
        base_url (str): the base url to the wikipedia.org pages
        output (Optional[str]): file to write to if wanted
    Returns:
        urls (Set[str]) : set with all the urls found in html text
    """
    # create and compile regular expression(s)

    urls = set()
    
    
    # 1. find all the anchor tags, then
    anchor_pattern = re.compile(r'<a[^>]+>', flags=re.IGNORECASE)

    # 2. find the urls href attributes
    href_pattern = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    
    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output,"w", encoding="utf-8") as file:
            file.write(html)

    for a_tag in anchor_pattern.findall(html):
        match = href_pattern.search(a_tag)
        if match:
            url = match.group(1)

            if url.startswith('#'):
                continue

            url = url.split('#')[0]

            if url.startswith('/'):
                url = urljoin(base_url, url)

            urls.add(url)

    return urls


def find_articles(
    html: str,
    output: str | None = None,
    base_url: str = "https://en.wikipedia.org",
) -> set[str]:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - html (str) : the html text to parse
        - output (str, optional): the file to write the output to if wanted
        - base_url (str, optional): the base_url to pass through to find_urls
    returns:
        - (Set[str]) : a set with urls to all the articles found
    """
    urls = find_urls(html, base_url)
    pattern = re.compile(
        r"https?://[a-z]+\.wikipedia\.org/wiki/[^:]+$", flags=re.IGNORECASE
    )
    articles = {url for url in urls if pattern.match(url)}

    # Write to file if wanted
    if output:
        print(f"Writing Wikipedia article URLs to: {output}")
        with open(output, "w", encoding="utf-8") as file:
            for article_url in articles:
                file.write(article_url + "\n")

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attribute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set

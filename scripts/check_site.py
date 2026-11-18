#!/usr/bin/env python3
"""Validate SEO metadata and discovery against an actual Jekyll build."""
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.schemas = []
        self.schema_text = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema_text = ''

    def handle_data(self, data):
        if self.schema_text is not None:
            self.schema_text += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.schema_text is not None:
            self.schemas.append(json.loads(self.schema_text))
            self.schema_text = None

    def select(self, tag, **attrs):
        return [a for t, a in self.elements if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def check(condition, message):
    if not condition:
        failures.append(message)


root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
if not (root / 'index.html').exists():
    sys.exit(f'Build the site first: no {root / "index.html"}')
failures = []
pages = {file: Page(file.read_text()) for file in root.rglob('*.html')}
canonical_home = pages[root / 'index.html'].select('link', rel='canonical')[0]['href']
origin = urlsplit(canonical_home).netloc
indexable = set()
descriptions = set()
posts = set()
for file, page in pages.items():
    label = str(file.relative_to(root))
    robots = page.select('meta', name='robots')
    noindex = any('noindex' in m.get('content', '') for m in robots)
    if noindex:
        continue
    check(len(page.select('h1')) == 1, f'{label}: expected one H1')
    check(len(page.select('main')) == 1, f'{label}: expected one main landmark')
    check(len(page.select('title')) == 1, f'{label}: expected one title')
    description = page.select('meta', name='description')
    check(len(description) == 1 and bool(description[0].get('content')), f'{label}: missing description')
    if description:
        value = description[0].get('content', '')
        check(value not in descriptions, f'{label}: duplicate description')
        descriptions.add(value)
    canonical = page.select('link', rel='canonical')
    check(len(canonical) == 1, f'{label}: expected one canonical')
    if not canonical:
        continue
    url = canonical[0]['href']
    check(url.startswith('https://' + origin + '/'), f'{label}: noncanonical origin')
    indexable.add(url)
    check(bool(page.schemas), f'{label}: missing JSON-LD')
    for schema in page.schemas:
        check(schema.get('@context') == 'https://schema.org', f'{label}: invalid schema context')
        if schema.get('@type') == 'BlogPosting':
            posts.add(url)
            author = schema.get('author', {})
            check(author.get('@type') == 'Person' and author.get('url'), f'{label}: incomplete author')
            times = {t.get('datetime') for t in page.select('time')}
            check(schema.get('datePublished') in times, f'{label}: publication date not visible')
            check(schema.get('dateModified') in times, f'{label}: modification date not visible')
    for image in page.select('img'):
        check(bool(image.get('alt')), f'{label}: image missing descriptive alt')
        if image.get('src', '').startswith('/'):
            check(image.get('width', '').isdigit() and image.get('height', '').isdigit(), f'{label}: local image missing dimensions')
    for image in page.select('meta', property='og:image'):
        image_url = urlsplit(image.get('content', ''))
        check(image_url.path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif')), f'{label}: invalid social image URL')
        if image_url.netloc == origin:
            check((root / unquote(image_url.path).lstrip('/')).is_file(), f'{label}: missing social image')
    for tag, attrs in page.elements:
        target = attrs.get('href') if tag in ('a', 'link') else attrs.get('src') if tag in ('img', 'script', 'iframe') else None
        if not target:
            continue
        link = urlsplit(urljoin(url, target))
        if link.netloc != origin or link.scheme not in ('http', 'https'):
            continue
        destination = root / unquote(link.path).lstrip('/')
        if destination.is_dir():
            destination /= 'index.html'
        check(destination.is_file(), f'{label}: missing internal target {target}')
        if destination in pages and link.fragment:
            ids = {a.get('id') for _, a in pages[destination].elements}
            check(unquote(link.fragment) in ids, f'{label}: missing anchor {target}')

sitemap = ET.parse(root / 'sitemap.xml')
namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap_urls = {node.text for node in sitemap.findall('sm:url/sm:loc', namespace)}
check(sitemap_urls == indexable, 'Sitemap does not exactly match indexable HTML pages')
rss = ET.parse(root / 'feed.xml')
channel = rss.getroot().find('channel')
for name in ('title', 'link', 'description', 'language'):
    check(bool(channel.findtext(name)), f'RSS missing channel {name}')
check({item.findtext('link') for item in channel.findall('item')} == posts, 'RSS does not match public articles')
robots = (root / 'robots.txt').read_text()
check('Sitemap: ' + urljoin(canonical_home, 'sitemap.xml') in robots, 'robots.txt missing sitemap')
llms = (root / 'llms.txt').read_text()
check(all(url in llms for url in posts), 'llms.txt missing a public article')
check('/2015/08/09/example-content/' not in llms, 'llms.txt includes sample post')
for hidden in ('404.html', '2015/08/09/example-content/index.html'):
    page = pages[root / hidden]
    check(any('noindex' in m.get('content', '') for m in page.select('meta', name='robots')), f'{hidden}: missing noindex')
if failures:
    sys.exit('\n'.join(failures))
print(f'Passed: {len(pages)} HTML pages, {len(indexable)} indexable pages, {len(posts)} articles; metadata, JSON-LD, dates, local links, sitemap, RSS, robots, and llms.txt.')

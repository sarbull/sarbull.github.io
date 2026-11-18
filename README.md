# sarbull’s blog

Personal web development notes published at [sarbull.github.io](https://sarbull.github.io/), built with Jekyll and hosted on GitHub Pages.

## Local development

Use Ruby 3.3 or newer and Bundler. The Gemfile uses GitHub Pages’ Jekyll 3.10 and supported SEO/sitemap plugins.

```sh
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`. To validate a production build:

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
python3 scripts/check_site.py _site
```

The checker validates generated descriptions, canonicals, headings, author/date structured data, local links and anchors, sitemap membership, RSS, crawler discovery, and noindex exclusions. It needs only Python’s standard library. JavaScript behavior and mobile layout should also be checked in a browser after layout or script changes.

## Writing articles

Keep the original `_posts/YYYY-MM-DD-slug.md` filename when editing an existing article so its URL remains stable. Add an accurate title, a unique `description`, and a few relevant `tags`. Start with an explanation of the problem and approach before the code. Link to relevant articles with Jekyll’s `post_url` tag and cite upstream documentation for technical claims.

Authorship comes from `_data/authors.yml` and `_config.yml`. Add `last_modified_at: YYYY-MM-DD` when a substantive correction or update occurs; the post layout displays it separately from the original publication date. For an article screenshot, use a real `image` path and descriptive alt text. Omit empty image fields. Reserve image dimensions to reduce layout shifts.

For a page that should stay reachable but outside search/listings, use `noindex: true`, `sitemap: false`, and `unlisted: true`. The theme sample and 404 page are excluded from indexing; the sample is also excluded from the homepage, related articles, RSS, and article map.

`jekyll-seo-tag` generates canonical, social, and JSON-LD metadata. `jekyll-sitemap` generates `/sitemap.xml`; `robots.txt` declares it. RSS and the optional `/llms.txt` article map are generated from current post data. The article map is an informational convenience; it does not guarantee AI citations or search visibility. Comments load from Disqus when the reader selects the button.

## After deployment

Check `/robots.txt`, `/sitemap.xml`, `/feed.xml`, and `/llms.txt` over HTTPS, then submit the sitemap in Google Search Console and Bing Webmaster Tools. Inspect a representative article and the About page using URL Inspection/Rich Results Test. Review search queries, impressions, clicks, and referrals after recrawling; changes in ranking and AI citations require real measurement.

## Theme attribution

Originally based on [Kiko](https://github.com/gfjaru/Kiko) by [gfjaru](https://github.com/gfjaru), with references to [Kiko-plus](https://github.com/AWEEKJ/Kiko-plus). The original theme is released under the MIT License.

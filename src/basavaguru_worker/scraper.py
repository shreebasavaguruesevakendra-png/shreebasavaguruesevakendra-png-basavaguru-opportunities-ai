from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from basavaguru_worker.storage import OpportunityStore


KEYWORDS = (
    "scholarship",
    "ssp",
    "scheme",
    "yojana",
    "application",
    "apply",
    "recruitment",
    "admission",
    "notification",
    "benefit",
    "subsidy",
    "pension",
    "last date",
    "deadline",
)


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    category_hint: str = "general"
    enabled: bool = True


@dataclass(frozen=True)
class Opportunity:
    title: str
    category: str
    audience: str
    source_name: str
    source_url: str
    opportunity_url: str
    summary: str


class LinkExtractor(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return

        attrs_dict = dict(attrs)
        href = attrs_dict.get("href")
        if href:
            self._current_href = urljoin(self.base_url, href)
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or not self._current_href:
            return

        text = normalize_text(" ".join(self._current_text))
        if text:
            self.links.append((text, self._current_href))

        self._current_href = None
        self._current_text = []


def run_worker(root: Path) -> None:
    sources = load_sources(root / "config" / "sources.json")
    categories = load_categories(root / "config" / "categories.json")
    store = OpportunityStore(root / "data" / "opportunities.sqlite")

    total_new = 0
    for source in sources:
        if not source.enabled:
            continue

        print(f"Checking {source.name}: {source.url}")
        try:
            opportunities = list(scrape_source(source, categories))
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"Could not check {source.name}: {error}")
            continue

        for opportunity in opportunities:
            created = store.upsert(opportunity)
            if created:
                total_new += 1
                print(f"New opportunity: {opportunity.title}")

    export_path = root / "data" / "opportunities.json"
    store.export_json(export_path)
    print(f"Worker finished. New opportunities: {total_new}")
    print(f"Exported database snapshot: {export_path}")


def load_sources(path: Path) -> list[Source]:
    raw_sources = json.loads(path.read_text(encoding="utf-8"))
    return [
        Source(
            name=item["name"],
            url=item["url"],
            category_hint=item.get("category_hint", "general"),
            enabled=item.get("enabled", True),
        )
        for item in raw_sources
    ]


def load_categories(path: Path) -> dict[str, dict[str, object]]:
    raw_categories = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in raw_categories}


def scrape_source(
    source: Source,
    categories: dict[str, dict[str, object]],
) -> Iterable[Opportunity]:
    html = fetch_html(source.url)
    extractor = LinkExtractor(source.url)
    extractor.feed(html)

    seen: set[str] = set()
    for title, href in extractor.links:
        category = categorize(title, href, source.category_hint, categories)
        if href in seen or category == "general":
            continue

        seen.add(href)
        audience = str(categories.get(category, {}).get("label", "General Public"))
        yield Opportunity(
            title=title,
            category=category,
            audience=audience,
            source_name=source.name,
            source_url=source.url,
            opportunity_url=href,
            summary=build_summary(title, source.name, audience),
        )


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "BasavaguruAIWorker/0.1 "
                "(opportunity monitoring; contact: update-contact@example.com)"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get("content-type", "")
        charset_match = re.search(r"charset=([\w-]+)", content_type)
        charset = charset_match.group(1) if charset_match else "utf-8"
        return response.read().decode(charset, errors="replace")


def categorize(
    title: str,
    href: str,
    category_hint: str,
    categories: dict[str, dict[str, object]],
) -> str:
    text = f"{title} {href}".lower()
    for category_id, category in categories.items():
        keywords = category.get("keywords", [])
        if any(str(keyword).lower() in text for keyword in keywords):
            return category_id

    if any(keyword in text for keyword in KEYWORDS):
        return category_hint

    return "general"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def build_summary(title: str, source_name: str, audience: str) -> str:
    return f"Potential {audience} opportunity found on {source_name}: {title}"

print(">>> researcher.py LOADING")

from concurrent.futures import ThreadPoolExecutor
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from core.credibility import score_source
import uuid


class ResearcherAgent:
    def __init__(self):
        self.ddg = DuckDuckGoTools()
        self.news = Newspaper4kTools()

    def _search_ddg(self, query: str):
        # agno tools must be called via .run()
        return self.ddg.run(query)

    def _search_news(self, query: str):
        return self.news.run(query)

    def collect_sources(self, plan: list[str]):
        from core.models import Source  # lazy import

        if not plan:
            raise RuntimeError("ResearcherAgent received empty research plan")

        raw_results = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for step in plan:
                futures.append(executor.submit(self._search_ddg, step))
                futures.append(executor.submit(self._search_news, step))

            for f in futures:
                try:
                    result = f.result()
                    if isinstance(result, list):
                        raw_results.extend(result)
                except Exception as e:
                    # IMPORTANT: surface the real error
                    print(f"⚠ Tool call failed: {e}")

        seen_urls = set()
        sources = []

        for r in raw_results:
            url = r.get("url")
            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            credibility = score_source(url, r.get("source", ""))

            sources.append(
                Source(
                    id=str(uuid.uuid4()),
                    title=r.get("title", ""),
                    url=url,
                    publisher=r.get("source", ""),
                    published_date=r.get("date"),
                    credibility_score=credibility,
                    tool=r.get("tool", "agno"),
                )
            )

        if not sources:
            raise RuntimeError(
                "ResearcherAgent failed to retrieve sources. "
                "All tool calls returned errors or empty results."
            )

        return sources

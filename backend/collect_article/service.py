import asyncio
from typing import List, Set

from ..article.service import ArticleService
from ..article.dto import CreateArticleDTO
from .tracker import AbstractTracker


async def _worker(
    queue: asyncio.Queue[List[CreateArticleDTO]], tracker: AbstractTracker
):
    tracker_result = await tracker.track()
    await queue.put(tracker_result)


class CollectArticleService:
    def __init__(
        self, article_service: ArticleService, trackers: list[AbstractTracker]
    ):
        self.article_service = article_service
        self.trackers = trackers

    async def collect(self):
        plan_articles: list[CreateArticleDTO] = []
        visited_urls: Set[str] = set()

        queue = asyncio.Queue()
        for tracker in self.trackers:
            asyncio.create_task(_worker(queue, tracker))

        for _ in self.trackers:
            tracker_result = await queue.get()
            filtered_tracker_result = [
                article for article in tracker_result if article.url not in visited_urls
            ]
            plan_articles.extend(filtered_tracker_result)
            visited_urls.update(article.url for article in filtered_tracker_result)

        await self.article_service.create_many(plan_articles)

import asyncio
import traceback
from typing import Callable, List, Set

from ..article.service import ArticleService
from ..article.dto import CreateArticleDTO, ArticleDTO
from .tracker import AbstractTracker


async def _worker(
    queue: asyncio.Queue[List[CreateArticleDTO]], tracker: AbstractTracker
):
    tracker_result = []
    try:
        tracker_result = await tracker.track()
    except Exception as e:
        print(f"Error in tracker {tracker.__class__.__name__}: {e.__new__}")
        traceback.print_exc()
    finally:
        await queue.put(tracker_result)


class CollectArticleService:
    def __init__(
        self,
        article_service: Callable[..., ArticleService],
        trackers: list[AbstractTracker],
    ):
        self.article_service = article_service()
        self.trackers = trackers

    async def collect(self) -> List[ArticleDTO]:
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

        queryDuplicated = await self.article_service.filter_by_url(visited_urls)
        non_duplicated_urls = visited_urls.difference(
            article.url for article in queryDuplicated
        )
        filtered_plan_articles = filter(
            lambda a: bool(a.url in non_duplicated_urls), plan_articles
        )

        return await self.article_service.create_many(filtered_plan_articles)

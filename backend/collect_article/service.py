from datetime import datetime
from typing import List

from ..article.dto import CreateArticleDTO, SearchArticleDTO
from ..database import Database
from ..twikit import Twikit
from ..article.container import ArticleContainer
import traceback


class CollectArticleService:
    def __init__(
        self,
        twikit: Twikit,
        article: ArticleContainer,
        database: Database
    ):
        self._twikit = twikit
        self._article = article
        self._database = database

    async def collect_articles_by_keyword(self, keyword: str, limit: int = 10) -> List[SearchArticleDTO]:
        """
        키워드로 기사를 검색하고 수집하는 메서드
        """
        # Twikit을 사용해 검색
        search_results = await self._twikit.search_tweet(keyword, limit)
        collected_articles = []
        for result in search_results:
            try:
                # Parse the date string into a datetime object
                # The format is like: "Thu Feb 06 15:08:25 +0000 2025"
                published_at = datetime.strptime(result.created_at, "%a %b %d %H:%M:%S %z %Y")
                
                article_dto = SearchArticleDTO(
                    content=result.text,
                    author=result.user.name,
                    published_at=published_at,
                    urls=result.urls,
                )
                saved_article = await self._article.service().save_search_article(article_dto)
                collected_articles.append(saved_article)
            # 데이터베이스에 저장
            except Exception as e:
                print(f"Error saving article: {str(e)}")
                continue

        return collected_articles
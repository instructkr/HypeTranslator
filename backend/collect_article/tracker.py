from typing import List
from ..article.dto import CreateArticleDTO


class AbstractTracker:
    async def track(self) -> List[CreateArticleDTO]:
        raise NotImplementedError

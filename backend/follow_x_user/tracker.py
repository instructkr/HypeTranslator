from typing import List
from random import shuffle
from twikit import Client as TwikitClient

from ..collect_article.tracker import AbstractTracker
from ..article.dto import CreateArticleDTO
from ..twikit import action_delay
from .service import FollowXUserService


class FollowXUserTracker(AbstractTracker):
    def __init__(self, twikitClient: TwikitClient, service: FollowXUserService):
        self._twikitClient = twikitClient
        self._service = service

    async def track(self) -> List[CreateArticleDTO]:
        followed_x_users = await self._service.get_all_followed_x_users()
        # mixed order
        shuffle(followed_x_users)
        result: List[CreateArticleDTO] = []
        for followed_x_user in followed_x_users:
            try:
                tweets = await self._twikitClient.get_user_tweets(
                    followed_x_user.real_x_user_id, "Tweets"
                )
                result.extend(
                    [
                        CreateArticleDTO(
                            url=f"https://x.com/{followed_x_user.username}/status/{tweet.id}",
                            author=tweet.user.screen_name,
                            published_at=tweet.created_at_datetime,
                            related_to_organizer=followed_x_user.organizer,
                        )
                        for tweet in tweets
                    ]
                )
                await action_delay()
            except Exception as e:
                print(f"Error in tracker {self.__class__.__name__}: {e}")

        return result

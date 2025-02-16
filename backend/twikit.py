from twikit import Client


class Twikit:
    def __init__(self, id, second_auth, password):
        self.client = Client("en-US")
        self._id = id
        self._second_auth = second_auth
        self._password = password

    async def login(self):
        await self.client.login(
            auth_info_1=self._id,
            auth_info_2=self._second_auth,
            password=self._password,
            cookies_file="cookies.json",
        )

        self.client.save_cookies("cookies.json")

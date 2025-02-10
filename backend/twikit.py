from twikit import Client


class Twikit:
    def __init__(self, id, email, password):
        self.client = Client("en-US")
        self._id = id
        self._email = email
        self._password = password

    async def login(self):
        await self.client.login(
            auth_info_1=self._id,
            auth_info_2=self._email,
            password=self._password,
            cookies_file="cookies.json",
        )
        self.client.save_cookies("cookies.json")

import asyncio

from twikit import Client

class Twikit:
    def __init__(self, id, email, password):
        self.client = Client('en-US')
        asyncio.run(
            self.client.login(
                auth_info_1=id,
                auth_info_2=email,
                password=password,
                cookies_file='cookies.json'
            )
        )
        self.client.save_cookies('cookies.json')

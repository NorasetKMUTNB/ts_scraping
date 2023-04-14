import requests


class RequestTS:

    def __init__(self):
        # replace CHANNEL_ID with your ThingSpeak channel ID
        self.url: str = "https://api.thingspeak.com/channels/{}/feeds".format(
            "2067797")
        # replace YOUR_READ_API_KEY with your ThingSpeak read API key
        self.params: dict = {"api_key": "IFAWF16ANKS12UHK"}

    def get_data(self) -> dict:
        """
        Get data from ThingSpeak Cloud API
        """
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error: {}".format(response.status_code))

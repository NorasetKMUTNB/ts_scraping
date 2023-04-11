import requests

# replace CHANNEL_ID with your ThingSpeak channel ID
# url = "https://api.thingspeak.com/channels/{}/feeds/last.json".format("2067797")
# msg = requests.get("https://thingspeak.com/channels/2067797/field/1")
url = "https://api.thingspeak.com/channels/{}/feeds".format("2067797")

# replace YOUR_READ_API_KEY with your ThingSpeak read API key
params = {"api_key": "IFAWF16ANKS12UHK"}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # do something with the data
    print(data)
    print("\n")
    print(data["feeds"])    # main list dict
    print("\n")
    print(len(data["feeds"]))
    print("\n")
    print(data["feeds"][-1])
    # print(len(data["channel"]))
    # print(data["channel"])
else:
    print("Error: {}".format(response.status_code))

# ref: https://medium.com/geekculture/the-naivest-way-to-send-and-retrieve-data-from-cloud-using-python-52a3e4b5fe24
# request parameters form cloud ThingSpeak service

import requests
msg = requests.get(
    "https://thingspeak.com/channels/2067797/field/1")

# msg1 = requests.get(
#     "https://thingspeak.com/channels/2067797/field/1").json()['feeds'][-1]
# msg2 = requests.get(
#     "https://thingspeak.com/channels/2067797/field/2").json()['feeds'][-1]

# msg = msg.json()['feeds'][-1]
msg = msg.json()

# print("\nThe Message sent was: \n\n"+str(msg1)+"\n"+str(msg2))
print("\nThe Message sent was: \n\n"+str(msg))

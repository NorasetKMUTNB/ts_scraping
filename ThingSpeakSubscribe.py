import utime as time
from MyMQTT_ThingSpeak import myThingSpeak


def mqttCallback(topic, msg):
    if msg != "":
        data = json().loads(msg)
        print("*** Callback ===> Channel:{}, Temp:{}, Humi:{}, Created:{}".format(
            data['channel_id'], data['field1'], data['field2'], data['created_at']))


mq = myThingSpeak(id=TS_CHANNEL_ID, read=TS_READ_KEY, password=TS_MQTT_KEY)
mq.setCallback(mqttCallback)
mq.connect()
mq.subscribe()

while True:
    mq.subCheck()  # check if new subscribed message published
    time.sleep_ms(300)

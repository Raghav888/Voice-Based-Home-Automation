import time
import paho.mqtt.client as paho

broker = "broker.shiftr.io"



def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))


def mqtt(dev_id, message):
    client = paho.Client(dev_id)

    client.username_pw_set("try", "try")
    client.on_message = on_message

    print("connecting to broker ", broker)
    client.connect(broker)  # connect

    time.sleep(1)
    print("publishing ")
    client.publish(dev_id+"/strange/pin", message)  # publish
    time.sleep(2)
    client.disconnect()  # disconnect
    
    return True

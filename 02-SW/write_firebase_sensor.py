from firebase import firebase
import time
import Adafruit_DHT as DHT


# the generated root for your project
FIREBASE_ROOT = 'https://ms-iot.firebaseio.com'
# init Firebase Database instance
firebase = firebase.FirebaseApplication(FIREBASE_ROOT, None)


while True:
    humidity, temperature = DHT.read_retry(DHT.DHT22, 4)

    sensor = {'temperature': temperature, 'humidity': humidity}

    result = firebase.patch('/sensor', sensor)

    print result

    time.sleep(1)

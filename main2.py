from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import paho.mqtt.client as mqtt

class MQTTSubscriberApp(App):
    def build(self):
        # MQTT configuration
        self.broker_address = "test.mosquitto.org"
        self.broker_port = 1883
        self.topic = "example/new/test"

        # Create MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        # Connect to the broker
        self.mqtt_client.connect(self.broker_address, self.broker_port, 60)

        # Start the MQTT loop in a separate thread
        self.mqtt_client.loop_start()

        # UI setup
        layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Waiting for MQTT messages...")
        layout.add_widget(self.label)

        return layout

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to the topic upon successful connection
        self.mqtt_client.subscribe(self.topic)
        print(f"Subscribed to topic: {self.topic}")

    def on_message(self, client, userdata, msg):
        # Callback for when a message is received
        message = f"Received message: {msg.payload.decode()}"
        print(message)
        self.label.text = message

if __name__ == "__main__":
    MQTTSubscriberApp().run()
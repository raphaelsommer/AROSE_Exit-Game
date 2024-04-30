extends Object

var mqtt_client = null
var is_connected = false

func _ready():
	mqtt_client = WebSocketClient.new()
	mqtt_client.connect("connected", self, "_on_connected")
	mqtt_client.connect("connection_closed", self, "_on_connection_closed")
	mqtt_client.connect("connection_error", self, "_on_connection_error")
	mqtt_client.connect("data_received", self, "_on_data_received")

func connect(url: String, port: int):
	mqtt_client.connect_to_url(url, port)

func disconnect():
	if is_connected:
		mqtt_client.disconnect_from_host()
	else:
		print("Fehler: Nicht mit dem MQTT-Broker verbunden")

func publish(topic: String, message: String):
	if is_connected:
		var json_message = {
			"topic": topic,
			"message": message
		}
		var json_string = JSON.print(json_message)
		mqtt_client.put_data(json_string)
	else:
		print("Fehler: Nicht mit dem MQTT-Broker verbunden")

func _on_connected():
	print("Verbunden mit MQTT-Broker")
	is_connected = true

func _on_connection_closed():
	print("Verbindung zum MQTT-Broker getrennt")
	is_connected = false

func _on_connection_error():
	print("Fehler bei der Verbindung zum MQTT-Broker")
	is_connected = false

func _on_data_received(data: PoolByteArray):
	var json_string = data.get_string_from_ascii()
	var json_data = JSON.parse(json_string)
	var topic = json_data["topic"]
	var message = json_data["message"]
	print("Nachricht erhalten - Thema:", topic, "Nachricht:", message)

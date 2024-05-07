extends Node

var mqttClient = load("res://Skripte/MQTT.gd").new()

# Called when the node enters the scene tree for the first time.
func _ready():
	mqttClient.connect_to_broker("localhost")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	mqttClient._process(delta)


#func _on_mqtt_broker_connected():
	#print("Connected") # Replace with function body.
#
#
#func _on_mqtt_broker_connection_failed():
	#print("Connection failed") # Replace with function body.

func sub():
	mqttClient.subscribe("/gen/global", 2)
	mqttClient.subscribe("/a3/buttons", 2)
	mqttClient.subscribe("/b3/morse", 2)
	mqttClient.subscribe("/c1/rfid", 2)
	mqttClient.subscribe("/c0/ip", 2)
	mqttClient.subscribe("/rk/wire", 2)
	
func pub(topic, message):
	mqttClient.publish(topic, message, false, 2)

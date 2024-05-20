extends Node

var mqttClient = load("res://Skripte/MQTT.gd").new()

# Called when the node enters the scene tree for the first time.
func _ready():
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if (Global.startMqtt):
		mqttClient._process(delta)


#func _on_mqtt_broker_connected():
	#print("Connected") # Replace with function body.
#
#
#func _on_mqtt_broker_connection_failed():
	#print("Connection failed") # Replace with function body.

#func checkConnection():
	#var error = mqttClient.checkConnect()
	#print(error)
	#if (error == 0):
		#Global.mqtt_connect = true
		
func tryConnect():
	var E = mqttClient.connect_to_broker("192.168.0.102")
	await get_tree().create_timer(2).timeout
	if (Global.mqtt_status < 2):
		mqttClient.cleanupsockets()
		print("Connection to Raspi-Network failed, trying local...")
		E = mqttClient.connect_to_broker("localhost")
		Global.mqtt_local = true
	return E

func sub():
	mqttClient.subscribe("/gen/global", 2)
	mqttClient.subscribe("/a3/buttons", 2)
	mqttClient.subscribe("/b3/morse", 2)
	mqttClient.subscribe("/c1/rfid", 2)
	mqttClient.subscribe("/c0/ip", 2)
	mqttClient.subscribe("/rk/wire", 2)
	
func pub(topic, message):
	mqttClient.publish(topic, message, false, 2)

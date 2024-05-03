extends Node2D

const MQTT = preload("res://addons/mqtt/mqtt.gd")
var mqtt = MQTT.new()




func _ready():
	mqtt.connect_to_broker("localhost")
	#mqtt.user = "rsMac"
	#mqtt.pswd = "rsMacArose1234!"
	#mqtt.client_id = "rsMac"
	mqtt.publish("/test", "hallo", false, 0)
	
	
	
	
	
func _on_mqtt_connection_error():
	print ("Fehler beim Verbinden")
	
	
	
	



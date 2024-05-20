extends Node2D
var text_edit

func _on_button_pressed():
	if(Global.ki_destroyed): #Wenn button gedrückt wird und die KI zerstört wurde gibt es einen anderen Abspann
		get_tree().change_scene_to_file("res://Szenen/Abspann-Kapsel.tscn")
	else: #Wenn ki nicht zerstört wurde normaler Abspann
		get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")
	if Global.mqtt_connect: #Mqtt verbindung wird getrennt
		MQTT_Client.pub("/gen/global", "stop")
		MQTT_Client.mqttClient.disconnect_from_server()


func _process(delta):   #Wenn die Aufgaben im Spiel erfüllt wurden erscheinen die Texte
	if(Global.ki_destroyed):
		$TextEdit4.visible = true
	if(Global.animals):
		$TextEdit3.visible = true
	if(Global.sauerstoff):
		$TextEdit2.visible = true
	

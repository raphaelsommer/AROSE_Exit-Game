extends Node2D

func _on_quit_pressed(): #Wenn spieler auf exit drückt wird die abspann szene geladen
	get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")
	MQTT_Client.pub("/gen/global", "stop")

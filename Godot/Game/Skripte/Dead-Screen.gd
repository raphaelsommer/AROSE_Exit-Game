extends Node2D

func _on_quit_pressed():
	get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")
	MQTT_Client.pub("/gen/global", "stop")

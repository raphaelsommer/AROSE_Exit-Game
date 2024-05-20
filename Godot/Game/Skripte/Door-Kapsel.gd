extends Node2D


func _process(delta): #Wenn wire game erfolgreich abgeschlossen wird, wird der zustand der tür 1 und die türe ist zu
	if(Global.door_rk == 1):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 1
		await get_tree().create_timer(0.5).timeout
		Global.door_rk = 0
		$AnimatedSprite2D.play("close")
		await get_tree().create_timer(2).timeout #Nach 2 sekunden wechselt der Screen zum winner screen
		get_tree().change_scene_to_file("res://Szenen/Winner-Screen.tscn")
		if Global.mqtt_connect:
			MQTT_Client.pub("/gen/global", "stop") #Mqtt broker wird gestoppt




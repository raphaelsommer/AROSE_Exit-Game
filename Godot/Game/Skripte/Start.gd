extends Node2D


func _process(delta):
	await get_tree().create_timer(5).timeout
	$RichTextLabel.visible = true
	if Input.is_action_just_pressed("skipIntro"):
		get_tree().change_scene_to_file("res://Szenen/Splitscreen.tscn")
		Global.timer_on = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/gen/global", "start")




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Spaceship")):
		get_tree().change_scene_to_file("res://Szenen/Splitscreen.tscn")
		Global.timer_on = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/gen/global", "start")

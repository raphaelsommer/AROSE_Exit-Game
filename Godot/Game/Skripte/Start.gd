extends Node2D


func _process(delta):
	await get_tree().create_timer(5).timeout #Zeitverzögerung von 5 sekunden
	$RichTextLabel.visible = true  #Text wird sichtbar
	if Input.is_action_just_pressed("skipIntro"): #Intro kann geskippt werden und dierekt in SPielbildschrim kommen
		get_tree().change_scene_to_file("res://Szenen/Splitscreen.tscn")
		Global.timer_on = true #Sauerstofftimer wird aktiviert
		if(Global.mqtt_connect):
			MQTT_Client.pub("/gen/global", "start")		#MQtt wird gestartet




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Spaceship")):
		get_tree().change_scene_to_file("res://Szenen/Splitscreen.tscn")	#Wenn Spaceship in area kommt wird die Szene gewechselt und der Timer wird erneut gestartet um abgelaufene zeit hinzuzufügen
		Global.timer_on = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/gen/global", "start") #Mqtt wird nur für die Games gestartet

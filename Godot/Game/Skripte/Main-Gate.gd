extends Node2D


var sauerstoff = false
var refilledSauerstoff = false
var shoot = false
var button = false
var buttonPressed = false
var morse = false
var morsePressed = false
var piano = false
var pianoPressed = false

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = true
		sauerstoff = true
	
		
func _ready():
	await get_tree().create_timer(5).timeout


func _process(delta):
	if(Input.is_action_just_pressed("Sauerstoff") and sauerstoff and !refilledSauerstoff):
		Global.sauerstoff = true
		Global.timer.set_wait_time(Global.timer.get_time_left() + float(9 * 60))
		Global.timer.start()
		print(Global.timer.get_time_left())
		$pc/Area2D.queue_free()
		$pc/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$pc/RichTextLabel.queue_free()
		sauerstoff = false
		refilledSauerstoff = true
	$CharacterBody2D3.position.x += 3
	if(shoot):
		$Rocket.position.x += 10
		$Rocket2.position.x += 10
		$Ship2.position.x -= 10
	if(Input.is_action_just_pressed("Button") and button and !buttonPressed):
		$"Comp_2/3".visible = false
		$Comp_2/Button.visible = false
		$Comp_2/Button2.visible = false
		$Comp_2/Button3.visible = false
		$Comp_2/RichTextLabel.visible = true
		buttonPressed = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/b2/gravity", "off")
		await get_tree().create_timer(2).timeout
		$Comp_2/RichTextLabel.visible = false
	elif(Input.is_action_just_pressed("Button") and buttonPressed):
		$"Comp_2/3".visible = false
		$Comp_2/Button.visible = false
		$Comp_2/Button2.visible = false
		$Comp_2/Button3.visible = false
		$Comp_2/RichTextLabel.set_text("Already started...")
		$Comp_2/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$Comp_2/RichTextLabel.visible = false
	#if(Input.is_action_just_pressed("Morse") and morse and !morsePressed):
		#$Comp_1/Sprite2D.visible = false
		#$Comp_1/Sprite2D2.visible = false
		#$Comp_1/RichTextLabel.visible = true
		#morsePressed = true
		#MQTT_Client.pub("/b3/morse", "start")
		#await get_tree().create_timer(2).timeout
		#$Comp_1/RichTextLabel.visible = false
	#elif(Input.is_action_just_pressed("Morse") and morsePressed):
		#$Comp_1/Sprite2D.visible = false
		#$Comp_1/Sprite2D2.visible = false
		#$Comp_1/RichTextLabel.set_text("Already started...")
		#$Comp_1/RichTextLabel.visible = true
		#await get_tree().create_timer(2).timeout
		#$Comp_1/RichTextLabel.visible = false
	if(Input.is_action_just_pressed("Piano") and piano and !pianoPressed):
		$Piano1/Piano.visible = false
		$Piano1/Sprite2D.visible = false
		$Piano1/RichTextLabel.visible = true
		pianoPressed = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/a5/piano", "start")
		await get_tree().create_timer(2).timeout
		$Piano1/RichTextLabel.visible = false
	elif(Input.is_action_just_pressed("Piano") and pianoPressed):
		$Piano1/Piano.visible = false
		$Piano1/Sprite2D.visible = false
		$Piano1/RichTextLabel.set_text("Already started...")
		$Piano1/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$Piano1/RichTextLabel.visible = false
	if(Global.door_c1_left == 0):
		$RFID/RichTextLabel.visible = true
	if(Global.door_c1_right == 0):
		$RFID2/RichTextLabel2.visible = true
	if (Global.door_b3 == 0):
		$Lamp.visible = false
		$Light_Lamp.visible = false



func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = false
		
		




func _on_gravity_body_entered(body):
	if(body.is_in_group("Player2")):
		Global.gravity = false
		$Gravity.queue_free()



	
	
	



#func _on_comp_body_entered(body):
	#if(body.is_in_group("Player")):
		#$Comp_1/Sprite2D.visible = true
		#$Comp_1/Sprite2D2.visible = true
		#morse = true
#
#
#func _on_comp_body_exited(body):
	#if(body.is_in_group("Player")):
		#$Comp_1/Sprite2D.visible = false
		#$Comp_1/Sprite2D2.visible = false
		#morse = false
		
		


func _on_piano_1_body_entered(body):
	if(body.is_in_group("Player")):
		$Piano1/Piano.visible = true
		$Piano1/Sprite2D.visible = true
		piano = true
		


func _on_piano_1_body_exited(body):
	if(body.is_in_group("Player")):
		$Piano1/Piano.visible = false
		$Piano1/Sprite2D.visible = false
		piano = false
		
		



func _on_shoot_body_entered(body):
	if(body.is_in_group("Ship")):
		shoot = true
		
		






func _on_dead_body_entered(body):
	if(body.is_in_group("Dead")):
		$CharacterBody2D3/Ship/AnimatedSprite2D.play("explosion")
		$AudioStreamPlayer3.play()
		$Rocket.visible = false
		$Rocket2.visible = false
		await get_tree().create_timer(0.4).timeout
		$CharacterBody2D3.visible = false
		

		


func _on_comp_2_body_entered(body):
	if(body.is_in_group("Player") and !Global.gravity):
		$Comp_2/Button.visible = true
		$Comp_2/Button2.visible = true
		$Comp_2/Button3.visible = true
		$"Comp_2/3".visible = true
		button = true
		
	


func _on_comp_2_body_exited(body):
	if(body.is_in_group("Player")):
		$Comp_2/Button.visible = false
		$Comp_2/Button2.visible = false
		$Comp_2/Button3.visible = false
		$"Comp_2/3".visible = false
		button = false
		


func _on_rfid_body_entered(body):
	if(body.is_in_group("Player")):
		$RFID/Sprite2D.visible = true
		$RFID2/RichTextLabel.visible = true


func _on_rfid_body_exited(body):
	if(body.is_in_group("Player")):
		$RFID/Sprite2D.visible = false
		$RFID2/RichTextLabel.visible = false


func _on_rfid_2_body_entered(body):
	if(body.is_in_group("Player")):
		$RFID2/Sprite2D.visible = true
		$RFID2/RichTextLabel.visible = true


func _on_rfid_2_body_exited(body):
	if(body.is_in_group("Player")):
		$RFID2/Sprite2D.visible = false
		$RFID2/RichTextLabel.visible = false

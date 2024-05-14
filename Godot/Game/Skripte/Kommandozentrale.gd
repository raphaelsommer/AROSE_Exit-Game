extends Node2D
var ip = false
var ipPressed = false
var draht = false 
var drahtPressed = false

func _physics_process(delta):
	await get_tree().create_timer(2).timeout
	$door.visible = false
	if(Global.animals):
		$CharacterBody2D4.visible = true
		$CharacterBody2D5.visible = true
	if(Input.is_action_just_pressed("IP") and ip and !ipPressed):
		$RichTextLabel.visible = true
		$Ip/Sprite2D.visible = false
		ipPressed = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/c0/ip", "start")
		await get_tree().create_timer(2).timeout
		$RichTextLabel.visible = false
	elif(Input.is_action_just_pressed("IP") and ipPressed):
		$RichTextLabel.set_text("Already started...")
		$RichTextLabel.visible = true
		$Ip/Sprite2D.visible = false
		await get_tree().create_timer(2).timeout
		$RichTextLabel.visible = false
	if(Input.is_action_just_pressed("Draht") and draht and !drahtPressed):
		$Kapsel/Sprite2D.visible = false
		$Kapsel/RichTextLabel.visible = true
		drahtPressed = true
		if(Global.mqtt_connect):
			MQTT_Client.pub("/rk/wire", "start")
		await get_tree().create_timer(2).timeout
		$Kapsel/RichTextLabel.visible = false
	elif(Input.is_action_just_pressed("Draht") and drahtPressed):
		$Kapsel/Sprite2D.visible = false
		$Kapsel/RichTextLabel.set_text("Already started...")
		$Kapsel/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$Kapsel/RichTextLabel.visible = false


func _ready():
	Global.animal_move_not = false

func _on_ip_body_entered(body):
	if(body.is_in_group("Player")):
		$Ip/Sprite2D.visible = true
		ip = true


func _on_ip_body_exited(body):
	if(body.is_in_group("Player")):
		$Ip/Sprite2D.visible = false
		
		



func _on_kapsel_body_entered(body):
	if(body.is_in_group("Player")):
		$Kapsel/Sprite2D.visible = true
		draht = true


func _on_kapsel_body_exited(body):
	if(body.is_in_group("Player")):
		$Kapsel/Sprite2D.visible = false
		draht = false

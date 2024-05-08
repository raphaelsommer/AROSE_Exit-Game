extends Node2D
var ip = false
var draht = false 

func _physics_process(delta):
	await get_tree().create_timer(2).timeout
	$door.visible = false
	if(Global.animals):
		$CharacterBody2D4.visible = true
		$CharacterBody2D5.visible = true
	if(Input.is_action_just_pressed("IP") and ip):
		$RichTextLabel.visible = true
		$Ip/Sprite2D.visible = false
		await get_tree().create_timer(2).timeout
		$RichTextLabel.visible = false
	if(Input.is_action_just_pressed("Draht") and draht):
		$Kapsel/Sprite2D.visible = false
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
	$Kapsel/Sprite2D.visible = true
	draht = true


func _on_kapsel_body_exited(body):
	$Kapsel/Sprite2D.visible = false
	draht = false

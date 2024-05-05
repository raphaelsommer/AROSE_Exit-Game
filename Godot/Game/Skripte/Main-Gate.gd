extends Node2D


var sauerstoff = false
var shoot = false

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = true
		sauerstoff = true


func _process(delta):
	if(Input.is_action_just_pressed("Sauerstoff") and sauerstoff):
		Global.sauerstoff = true
		$pc/Area2D.queue_free()
		Global.timer.wait_time+= float(9 * 60)
		$pc/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$pc/RichTextLabel.queue_free()
		sauerstoff = false
	$CharacterBody2D3.position.x += 3
	if(shoot):
		$Rocket.position.x += 10
		$Rocket2.position.x += 10
		$Ship2.position.x -= 10
	
	
	



func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = false
		




func _on_gravity_body_entered(body):
	if(body.is_in_group("Player2")):
		Global.gravity = false
		


func _ready():
	#await get_tree().create_timer(5).timeout
	pass


func _on_audio_stream_player_ready():
	$AudioStreamPlayer2.play()
	
	
	



func _on_comp_body_entered(body):
	if(body.is_in_group("Player")):
		$Comp_1/Sprite2D.visible = true


func _on_comp_body_exited(body):
	if(body.is_in_group("Player")):
		$Comp_1/Sprite2D.visible = false
		
		
		


func _on_piano_1_body_entered(body):
	if(body.is_in_group("Player")):
		$Piano1/Piano.visible = true


func _on_piano_1_body_exited(body):
	if(body.is_in_group("Player")):
		$Piano1/Piano.visible = false
		
		



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
	if(body.is_in_group("Player")):
		$Comp_2/Button.visible = true
		



func _on_comp_2_body_exited(body):
	if(body.is_in_group("Player")):
		$Comp_2/Button.visible = false


func _on_rfid_body_entered(body):
	if(body.is_in_group("Player")):
		$RFID/Sprite2D.visible = true


func _on_rfid_body_exited(body):
	if(body.is_in_group("Player")):
		$RFID/Sprite2D.visible = false


func _on_rfid_2_body_entered(body):
	if(body.is_in_group("Player")):
		$RFID2/Sprite2D.visible = true


func _on_rfid_2_body_exited(body):
	if(body.is_in_group("Player")):
		$RFID2/Sprite2D.visible = false

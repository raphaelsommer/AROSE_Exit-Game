extends Node2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$Sprite2D.visible = true


		
	
		
func _physics_process(delta):
	if(Input.is_action_just_pressed("door_open")):
		$Sprite2D.visible = false
		Global.door_open = true
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.queue_free()
		$Sprite2D.queue_free()
		$Area2D.queue_free()
	

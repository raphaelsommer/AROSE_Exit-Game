extends CharacterBody2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$"../Sprite2D".visible = true
		
		
		
func _physics_process(delta):
	if(Input.is_action_just_pressed("Door-k-2")):
		$"../AnimatedSprite2D".play("opens")
		
		$".".queue_free()


func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$"../Sprite2D".visible = false

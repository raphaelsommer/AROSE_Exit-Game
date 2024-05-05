extends Node2D


func _on_area_2d_body_entered(body):
	if(body.is_in_group("Animal")):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()

func _on_area_2d_body_exited(body):
	if(body.is_in_group("Animal")):
		await get_tree().create_timer(1).timeout
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		
		
func _process(delta):
	if(Global.door_c1 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		Global.door_c1 = 1
		await get_tree().create_timer(2).timeout
		if(Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game 3.tscn")
		elif(!Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game.tscn")
		
	

extends Node2D





func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$Sprite2D.visible = true
		
func _physics_process(delta):
	if(Input.is_action_just_pressed("Enter_Switch")):
		$Sprite2D.visible = false
		$AnimatedSprite2D.play("on")
		await get_tree().create_timer(1).timeout
		get_tree().change_scene_to_file("res://Szenen/Kommandozentrale.tscn")


func _on_area_2d_body_exited(body):
	$Sprite2D.visible = false

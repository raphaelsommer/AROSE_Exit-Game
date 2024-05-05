extends Node2D





func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		


func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()

extends Node2D


#Diese Türe ist immer offen und wenn die spieler in den bereich kommen öffnet sich die türe und wenn sie den bereich verlassen schliesst sich die türe wieder


func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		


func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()

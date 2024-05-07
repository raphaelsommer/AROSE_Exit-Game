extends Node2D




<<<<<<< Updated upstream
func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player") and Global.door_c0 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.queue_free()
		$Area2D.queue_free()
		$AnimatedSprite2D2.play("on")
=======
func _process(delta):
	if(Global.door_c0 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.queue_free()
		$AnimatedSprite2D2.play("on")
		Global.door_c0 = 1


>>>>>>> Stashed changes

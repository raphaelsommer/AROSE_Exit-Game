extends Node2D


<<<<<<< Updated upstream



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player") and Global.door_rk == 1):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 1
		$Area2D.queue_free()
=======
func _process(delta):
	if(Global.door_rk == 1):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 1
		await get_tree().create_timer(0.5).timeout
		$AnimatedSprite2D.play("close")



>>>>>>> Stashed changes

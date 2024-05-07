extends Node2D


func _process(delta):
	if(Global.door_rk == 1):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 1
		await get_tree().create_timer(0.5).timeout
		$AnimatedSprite2D.play("close")




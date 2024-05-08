extends Node2D


func _process(delta):
	if(Global.door_rk == 1):
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 1
		await get_tree().create_timer(0.5).timeout
		Global.door_rk = 0
		$AnimatedSprite2D.play("close")
		await get_tree().create_timer(2).timeout
		get_tree().change_scene_to_file("res://Szenen/Winner-Screen.tscn")




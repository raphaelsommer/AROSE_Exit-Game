extends Node2D


func _process(delta):
	if(Global.door_a5 == 0):
		$AnimatedSprite2D.play("Opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 2
		Global.door_a5 = 1




extends Node2D


func _process(delta):
	if(Global.door_b2 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 2
		Global.door_b2 = 1

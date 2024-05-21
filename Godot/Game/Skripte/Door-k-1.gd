extends Node2D




func _process(delta):
	if(Global.door_c0 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.queue_free()
		$AnimatedSprite2D2.play("on")
		Global.door_c0 = 1



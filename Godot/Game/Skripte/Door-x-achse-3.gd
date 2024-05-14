extends Node2D

func _process(delta):
	if(Global.door_a3 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$CharacterBody2D.collision_layer = 2
		Global.door_a3 = 1
		Global.gravity = true
		spwan(self.position)


func spwan(targetLocation):
	
	var newItem = null
	newItem = preload("res://Szenen/Coin.tscn")
		
	if(newItem != null):
		var newItemInstance = newItem.instantiate()
		newItemInstance.position = targetLocation
		get_parent().add_child(newItemInstance)

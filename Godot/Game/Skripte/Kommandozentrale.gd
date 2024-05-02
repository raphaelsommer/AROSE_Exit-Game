extends Node2D


func _physics_process(delta):
	await get_tree().create_timer(2).timeout
	$door.visible = false
	if(Global.animals):
		$CharacterBody2D4.visible = true
		$CharacterBody2D5.visible = true

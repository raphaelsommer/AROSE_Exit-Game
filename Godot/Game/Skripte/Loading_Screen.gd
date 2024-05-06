extends Node2D


func _ready():
	await get_tree().create_timer(5).timeout
	if(Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game 3.tscn")
	elif(!Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game.tscn")

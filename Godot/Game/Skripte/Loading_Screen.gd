extends Node2D


func _ready(): #Wenn die szene geladen wird beginnt der timer von 5 sekunden und dann wechselt der screen zu dem level was am anfang ausgewählt wurde
	await get_tree().create_timer(5).timeout 
	if(Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game 3.tscn")
	elif(!Global.game_hard):
			get_tree().change_scene_to_file("res://Szenen/Dino-Game.tscn")

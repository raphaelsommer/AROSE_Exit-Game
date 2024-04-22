extends Node2D




func _on_restart_pressed():
	get_tree().change_scene_to_file("res://Szenen/Main-Gate.tscn")



func _on_menü_pressed():
	get_tree().change_scene_to_file("res://Szenen/Menü.tscn")




func _on_quit_pressed():
	get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")

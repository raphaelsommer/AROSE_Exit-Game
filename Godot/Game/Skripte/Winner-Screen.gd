extends Node2D
var text_edit

func _on_button_pressed():
	if(Global.ki_destroyed):
		get_tree().change_scene_to_file("res://Szenen/Abspann-Kapsel.tscn")
	else:
		get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")


func _process(delta):
	if(Global.ki_destroyed):
		$TextEdit4.visible = true
	if(Global.animals):
		$TextEdit3.visible = true
	if(Global.sauerstoff):
		$TextEdit2.visible = true
	

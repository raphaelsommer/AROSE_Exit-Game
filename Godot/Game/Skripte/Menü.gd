extends Node2D




func _on_start_pressed():
	get_tree().change_scene_to_file("res://Szenen/Start.tscn")
	





func _on_exit_pressed():
	get_tree().quit()
	




func _on_faq_pressed():
	pass # Replace with function body.
	




func _on_rating_pressed():
	$Rating/Sprite2D.visible = true
	



func _on_exit_list_pressed():
	$Rating/Sprite2D.visible = false
	



func _on_info_pressed():
	$Info/Sprite2D.visible = true

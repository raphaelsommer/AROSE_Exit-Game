extends Node2D


func _process(delta):
	await get_tree().create_timer(5).timeout
	$RichTextLabel.visible = true




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Spaceship")):
		get_tree().change_scene_to_file("res://Szenen/Main-Gate.tscn")

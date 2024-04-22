extends Node2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player1_hp -= 1 # Replace with function 

extends Node2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 1 # Replace with function 
		Global.player_hp2 -= 1
		$AudioStreamPlayer2D.play()
		

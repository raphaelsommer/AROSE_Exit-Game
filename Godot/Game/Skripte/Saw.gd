extends Node2D


#Wenn Spieler in die Area von der Säge kommen bekommen sie minus 1 leben und eine Audio wird abgespielt

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 1 # Replace with function 
		Global.player_hp2 -= 1
		$AudioStreamPlayer2D.play()
		

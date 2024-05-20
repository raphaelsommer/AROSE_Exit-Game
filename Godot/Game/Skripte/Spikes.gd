extends Node2D



func _on_area_2d_body_entered(body): #Wenn spieler in die Area von den Spikes kommen verlieren sie ein leben und Sound wird ausgeführt
	if(body.is_in_group("Player")):
		Global.player_hp -= 1
		Global.player_hp2 -= 1
		$AudioStreamPlayer2D.play()

extends Node2D



#Wenn Spieler in den Coin läuft bekommen sie einen coin dau und der coin verschwindet
func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.coins += 1
		$AudioStreamPlayer2D.play()
		await get_tree().create_timer(0.1).timeout
		queue_free()
		print(Global.coins)

extends Node2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.coins += 1
		await get_tree().create_timer(0.1).timeout
		queue_free()
		print(Global.coins)

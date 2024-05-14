extends Node2D





func _on_area_2d_body_entered(body):
	Global.key = true
	$AudioStreamPlayer2D.play()
	await get_tree().create_timer(0.1).timeout
	$".".queue_free()

extends Node2D



func _process(delta):
	pass
	
	



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Kapsel")):
		$Node2D/Sprite2D3.queue_free()
		$Node2D/Evil.visible = true

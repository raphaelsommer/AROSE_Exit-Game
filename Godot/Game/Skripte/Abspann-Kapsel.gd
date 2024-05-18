extends Node2D



func _process(delta):
	pass
	
	



func _on_area_2d_body_entered(body):	
	if(body.is_in_group("Kapsel")):			#Wenn body in der Gruppe spieler ist, und den Bereich erreicht soll der Roboter verschwinden und die KI erscheinen. 
		$Node2D/Sprite2D3.queue_free()
		$Node2D/Evil.visible = true

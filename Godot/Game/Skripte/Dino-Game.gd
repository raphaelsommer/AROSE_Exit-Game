extends Node2D



func _physics_process(delta):
	if(Global.szenen_wechsel):
		get_tree().change_scene_to_file("res://Szenen/Winner-Screen.tscn")
		
	

func _ready():
	await get_tree().create_timer(1).timeout
	$"Door-Anfang".queue_free()
	



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 5
		



func _on_area_2d_2_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 5
		



		


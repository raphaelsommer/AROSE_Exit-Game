extends Node2D


func _ready():
	await get_tree().create_timer(1).timeout
	$"Door-Anfang".queue_free()



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 5
		



func _on_area_2d_2_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 5
		



		


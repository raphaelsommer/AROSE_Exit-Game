extends Node2D



func _physics_process(delta): #Wenn ki zerstört wird wechselt der screnn direkt zum winner screen
	if(Global.szenen_wechsel):
		get_tree().change_scene_to_file("res://Szenen/Winner-Screen.tscn")
	
	

func _ready(): #Die türe über die, die spieler gekommen sind verschwindet
	await get_tree().create_timer(1).timeout
	$"Door-Anfang".queue_free()


#Wenn spieler in säure fällt sterben sie bzw. bekommen -10 leben
func _on_area_2d_body_entered(body): 
	if(body.is_in_group("Player")):
		Global.player_hp -= 10
		



func _on_area_2d_2_body_entered(body):
	if(body.is_in_group("Player")):
		Global.player_hp -= 10
		
		




		





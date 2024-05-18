extends Node2D
var door_open = false

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Animal")): #Wenn tiere in den bereich kommen öffnet sich die türe und sie können durch gehen
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
	elif(body.is_in_group("Player") and Global.door_c1_left == 0 and Global.door_c1_right == 0 and Global.door_c1 == 0):
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		await get_tree().create_timer(1.5).timeout
		get_tree().change_scene_to_file("res://Szenen/Loading_Screen.tscn")#wenn spieler alle level abgrschlossen haben können sie auch durch die türe gehen und die szene wechselt zum nächsten level



func _on_area_2d_body_exited(body): #sobald die tiere durch die tür gegangen sind schließt sie sich wieder
	if(body.is_in_group("Animal")):
		await get_tree().create_timer(1).timeout
		$AnimatedSprite2D.play("closes")
		$AudioStreamPlayer2D.play()
		
		
func _process(delta):
	pass
		
	


func _on_door_open_body_entered(body):
	pass

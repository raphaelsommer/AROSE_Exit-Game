extends Node2D





func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$Sprite2D.visible = true #Wenn Spieler den bereich betritt taste wird sichtbar
		
func _physics_process(delta):
	if(Input.is_action_just_pressed("Enter_Switch")): #Wenn eine benutzereingabe folgt "P" dann wird das P unsichtbar
		$Sprite2D.visible = false
		$AnimatedSprite2D.play("on") #Der Switch wird grün
		$AudioStreamPlayer2D.play() #Sound wird abgespielt
		await get_tree().create_timer(1).timeout
		get_tree().change_scene_to_file("res://Szenen/Kommandozentrale.tscn") #Szenen wechsel zur Kommandozentrale


func _on_area_2d_body_exited(body):
	$Sprite2D.visible = false #Wenn spieler bereich verlässt "P" wird unsichtbar

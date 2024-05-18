extends Node2D




func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$Sprite2D.visible = true
		
		
func _process(delta): #Das ist die Türe zu den tieren wenn die spieler den schlüssel haben und den button drücken öffnet sich die türe 
	if(Input.is_action_just_pressed("Door-8") and Global.key):
		$CharacterBody2D.queue_free()
		$AnimatedSprite2D.play("opens")
		$AudioStreamPlayer2D.play()
		$Area2D.queue_free()
		$AnimatedSprite2D2.play("on")
		Global.key = false
		Global.animals = true
	elif(Input.is_action_just_pressed("Door-8")): #wenn button gedrück wird aber kein schlüssel vorhanden ist öffnet sich die türe nicht
		$RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$RichTextLabel.visible = false



func _on_area_2d_body_exited(body): #Wenn spiele area verlassen können sie den button nicht mehr drücken
	$Sprite2D.visible = false

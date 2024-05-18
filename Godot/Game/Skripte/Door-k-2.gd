extends CharacterBody2D




func _on_area_2d_body_entered(body): #Wenn spieler area betreten wird ihnen angezeigt was sie drücken sollen um die türe zu öffnen
	if(body.is_in_group("Player")):
		$"../Sprite2D".visible = true
		
		
		
func _physics_process(delta):#Wenn spieler den button dann gedrückt haben öffnet sich die türe
	if(Input.is_action_just_pressed("Door-k-2")):
		$"../AnimatedSprite2D".play("opens")
		$"../AudioStreamPlayer2D".play()
		
		$".".queue_free()


func _on_area_2d_body_exited(body): #Wenn spieler area verlässt verschindet der knopf wo gezeigt wird was zu drücken ist
	if(body.is_in_group("Player")):
		$"../Sprite2D".visible = false

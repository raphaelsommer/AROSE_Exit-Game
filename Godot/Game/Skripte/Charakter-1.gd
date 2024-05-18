extends CharacterBody2D


const SPEED = 200.0 #Geschwindigkeit des Charakter
const JUMP_VELOCITY = -400.0 #Sprunghöhe

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


@onready var animSprite = $AnimatedSprite2D #Animationen werden geladen


func spawnBullet(): #Wenn spiler auf schißen drückt kommt aus der waffe die bullet raus/spawnt in der waffe
	var b = preload("res://Szenen/Bullets.tscn").instantiate()
	
	b.position = self.position
	get_parent().add_child(b)



func _physics_process(delta):
	# Add the gravity.
	if(Input.is_action_just_pressed("Shoot_player1") and Global.gun_on): #Wenn waffen aktiviert sind kann spieler nach button gedrückt shcießen
		animSprite.play("shoot")
		spawnBullet()
		
	
	
	
	
	if not is_on_floor(): #Movement des Spielers 
		velocity.y += gravity * delta
		
		if(velocity.y > 0): #Wenn y größer als 0 ist muss die fallanimation gespielt werden
			animSprite.play("fall")
		else:
			animSprite.play("jump") #sonst immer die sprung animation spielen wenn nicht auf boden
			
	else:
		if(velocity.x == 0): 
			animSprite.play("idle") #Wenn ich mich nicht bewege soll die idle animation gespielt werden
		else:
			animSprite.play("run") #Wenn ich mich bewge die run animation
			
	
	if Input.is_action_just_pressed("Player_jump") and is_on_floor(): #Wenn jump gedückt wird springt der charaker
		velocity.y = JUMP_VELOCITY

	
	var direction = Input.get_axis("ui_left", "ui_right") #Jenachdem welche richtung gedrückt wird dahin läuft der Charakter
	if direction and Global.player1_canMove:
		velocity.x = direction * SPEED
		
		if(velocity.x < 0): #animation soll auch spiegelverkehrt funktionieren
			animSprite.flip_h = true
		else:
			animSprite.flip_h = false
		
		
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
	if(Global.player_hp <= 0): #Wenn spieler keine leben mehr hat stirbt er. Und der Dead screen wird abgespielt
		
		animSprite.play("dead")
		await get_tree().create_timer(0.5).timeout
		get_tree().change_scene_to_file("res://Szenen/Dead-Screen.tscn")
		Global.player_hp = 1 #Früher war noch eine resatart funktion, eingebaut die das spiel neu startet und die leben der spieler wieder auf 1 setzt
		Global.player_hp2 = 1
		Global.player1_canMove = true
		

	move_and_slide()

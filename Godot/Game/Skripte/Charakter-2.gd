extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0

#Siehe Dokumentation Charakter-1

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

@onready var animSprite = $AnimatedSprite2D


func spawnBullet():
	var b = preload("res://Szenen/Bullets.tscn").instantiate()
	
	b.position = self.position
	get_parent().add_child(b)




func _physics_process(delta):
	
	if(Input.is_action_just_pressed("Shoot_player2") and Global.gun_on):
		animSprite.play("shoot")
		spawnBullet()
	
	if(Global.gravity):
		if not is_on_floor():
			velocity.y += gravity * delta
			
			if(velocity.y > 0):
				animSprite.play("fall")
			else:
				animSprite.play("jump")
		else:
			if(velocity.x == 0):
				animSprite.play("idle")
			else:
				animSprite.play("run")
				
	else:
		$".".position.y -= 1
		
		
	
	
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	
	var direction = Input.get_axis("move_left", "move_right")
	if direction and Global.player2_canMove:
		velocity.x = direction * SPEED
		
		if(velocity.x < 0):
			animSprite.flip_h = true
		else:
			animSprite.flip_h = false
		
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
		
		
	if(Global.player_hp2 <= 0):
		
		animSprite.play("dead")

	move_and_slide()

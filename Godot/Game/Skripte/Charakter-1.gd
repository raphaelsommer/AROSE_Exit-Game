extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


@onready var animSprite = $AnimatedSprite2D


func spawnBullet():
	var b = preload("res://Szenen/Bullets.tscn").instantiate()
	
	b.position = self.position
	get_parent().add_child(b)



func _physics_process(delta):
	# Add the gravity.
	if(Input.is_action_just_pressed("Shoot_player1") and Global.gun_on):
		animSprite.play("shoot")
		spawnBullet()
		
	
	
	
	
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
			
	# Handle jump.
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction = Input.get_axis("ui_left", "ui_right")
	if direction and Global.player1_canMove:
		velocity.x = direction * SPEED
		
		if(velocity.x < 0):
			animSprite.flip_h = true
		else:
			animSprite.flip_h = false
		
		
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
	if(Global.player_hp <= 0):
		
		animSprite.play("dead")
		await get_tree().create_timer(0.5).timeout
		get_tree().change_scene_to_file("res://Szenen/Dead-Screen.tscn")
		Global.player_hp = 1
		Global.player_hp2 = 1
		Global.player1_canMove = true
		

	move_and_slide()

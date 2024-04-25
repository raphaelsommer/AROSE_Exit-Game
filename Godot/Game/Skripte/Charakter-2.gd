extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

@onready var animSprite = $AnimatedSprite2D

func _physics_process(delta):
	# Add the gravity.
	if(Input.is_action_just_pressed("Shoot_player2") and Global.gun_on):
		animSprite.play("shoot")
	
	
	
	if not is_on_floor():
		velocity.y += gravity * delta
		
		if(velocity.y > 0):
			animSprite.play("idle")
		else:
			animSprite.play("jump")
	else:
		if(velocity.x == 0):
			animSprite.play("idle")
		else:
			animSprite.play("run")
		
		

	# Handle jump.
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction = Input.get_axis("move_left", "move_right")
	if direction and Global.player1_canMove:
		velocity.x = direction * SPEED
		
		if(velocity.x < 0):
			animSprite.flip_h = true
		else:
			animSprite.flip_h = false
		
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
		
		
	if(Global.player_hp2 <= 0):
		Global.player1_canMove = false
		animSprite.play("dead")

	move_and_slide()
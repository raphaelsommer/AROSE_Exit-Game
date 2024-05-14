extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0
var move = false
var meow = false

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _ready():
	pass


func _physics_process(delta):
	if(Global.animal_move and Global.animal_move_not):
		$AnimatedSprite2D.play("run")
		$".".position.x -= 2
		await get_tree().create_timer(18.5).timeout
		$".".queue_free()
		move = false
	
	

	move_and_slide()





func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		move = true
		meow = true
		Global.animal_move = true

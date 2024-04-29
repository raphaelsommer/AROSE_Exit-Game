extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0
var move = false
# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	if(move):
		$AnimatedSprite2D.play("run")
		$".".position.x -= 2
		await get_tree().create_timer(18.7).timeout
		$".".queue_free()

	move_and_slide()



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		move = true

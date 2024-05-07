extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	await get_tree().create_timer(2).timeout
	$".".position.x += 2
	await get_tree().create_timer(12).timeout
	$Area2D.position.x += 4

	move_and_slide()



func _on_area_2d_body_entered(body):
	if(body.is_in_group("Kapsel")):
		get_tree().change_scene_to_file("res://Szenen/Abspann.tscn")

extends CharacterBody2D

var canMove = true
const SPEED = 50.0
const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	if(Global.robot_hp <= 0 and canMove):
		await get_tree().create_timer(1).timeout
		$".".visible = true
		$".".position.x -= 1
		$AnimatedSprite2D.play("run")
		await get_tree().create_timer(2.5).timeout
		canMove = false
	if(!canMove):
		$".".position.x -= 0
		#$AnimatedSprite2D.play("idle")
		await get_tree().create_timer(0.5).timeout
		$AnimatedSprite2D.play("erschrocken")
		await get_tree().create_timer(0.5).timeout
		#$AnimatedSprite2D.play("idle")
		$Sprite2D.visible = true
		await get_tree().create_timer(5).timeout
		Global.szenen_wechsel = true
		
	
	

	move_and_slide()

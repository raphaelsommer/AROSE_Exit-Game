extends CharacterBody2D

var robot_drive = false
const SPEED = 100
const JUMP_VELOCITY = -400.0
var canMove = false
var actWeapons = false

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _process(delta):
	if(Global.robot_hp <= 0):
		$AnimatedSprite2D2.play("explosion")
		Global.ki_destroyed = true
		await get_tree().create_timer(0.5).timeout
		$".".queue_free()
	







#func dead():
	#$AnimatedSprite2D2.play("explosion")
	#await get_tree().create_timer(0.5).timeout
	#$".".queue_free()
	


func _physics_process(delta):
	if(Input.is_action_just_pressed("Waffen_aktivieren") and actWeapons):
		actWeapons = false
		$Sprite2D2.visible = false
		$Sprite2D.visible = false
		Global.gun_on = true
		$RichTextLabel.visible = true
		await get_tree().create_timer(1).timeout
		#$s.visible = true
		$n.visible = true
		await get_tree().create_timer(1).timeout
		#$s.visible = false
		$n.visible = false
		#$s.queue_free()
		$n.queue_free()
		$RichTextLabel.queue_free()
		$Area2D.queue_free()
		$Sprite2D.queue_free()
		canMove = true
	if(canMove):
		$".".position.x -= 1
	move_and_slide()
 

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player") and !actWeapons):
		actWeapons = true
		$".".visible = true
		await get_tree().create_timer(0.5).timeout
		$Sprite2D.visible = true
		$AudioStreamPlayer2D.play()
		await get_tree().create_timer(2).timeout
		$Sprite2D2.visible = true
		
		
		


		
		




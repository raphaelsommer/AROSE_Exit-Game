extends CharacterBody2D

var robot_drive = false
const SPEED = 200
const JUMP_VELOCITY = -400.0
var dead1 = 0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


#func dead():
	#if(Global.robot_hp <= 0):
		#$explosion.visible = true
		#$explosion.play("explosion")
		#await get_tree().create_timer(0.5).timeout
		#$".".queue_free()
	


func _physics_process(delta):
	if(Input.is_action_just_pressed("Waffen_aktivieren")):
		$Sprite2D2.visible = false
		$Sprite2D.visible = false
		Global.gun_on = true
		$RichTextLabel.visible = true
		await get_tree().create_timer(1).timeout
		$RichTextLabel.queue_free()
		$Area2D.queue_free()
		$Sprite2D.queue_free()

	move_and_slide()
 

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$".".visible = true
		await get_tree().create_timer(0.5).timeout
		$Sprite2D.visible = true
		await get_tree().create_timer(2).timeout
		$Sprite2D2.visible = true
		
		

		
		




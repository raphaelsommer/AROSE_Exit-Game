extends CharacterBody2D

var canMove = true
const SPEED = 50.0 #Geschwindigkeit 50
const JUMP_VELOCITY = -400.0 #Springen könnte er, wird aber nicht benutzt

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta): #Wenn die Ki zerstört ist erscheint der roboter und Läuft auf die Spieler zu
	if(Global.robot_hp <= 0 and canMove):
		await get_tree().create_timer(1).timeout
		$".".visible = true
		$".".position.x -= 1
		$AnimatedSprite2D.play("run")
		await get_tree().create_timer(2.5).timeout
		canMove = false
	if(!canMove): #Wenn er angekommen ist redet er mit den spieler und gratuliert ihnen
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

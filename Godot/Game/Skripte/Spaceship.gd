extends CharacterBody2D


const SPEED = 200.0 #Geschwindigkeit des Schiffes
const JUMP_VELOCITY = -400.0 #Könnte reintheoretisch springen macht es aber nicht

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

#Nach 1,5 Sekunden im Spiel startet das Schiff von der Erde 
func _physics_process(delta):
	await get_tree().create_timer(1.5).timeout
	$".".position.x += 2			
	
	
	move_and_slide()

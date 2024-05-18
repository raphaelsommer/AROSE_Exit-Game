extends CharacterBody2D


const SPEED = 200.0  #Katze geschwindigkeit 200
const JUMP_VELOCITY = -400.0 #Katze Sprunghöhe
var move = false
var meow = false 

#Schwerkraft aus den Projekteinstellungen laden und mit RigidBody-Knoten zu verbinden.

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _ready():
	pass


func _physics_process(delta): #Wenn Katzen befreit wurden werden variablen true und sie bewegen sich zu den türen 
	if(Global.animal_move and Global.animal_move_not):
		$AnimatedSprite2D.play("run")
		$".".position.x -= 2
		await get_tree().create_timer(18.5).timeout
		$".".queue_free()
		move = false
	
	

	move_and_slide()





func _on_area_2d_body_entered(body): #Wenn spieler in die Area kommen fangen katzen an sich zu bewegen und eigentlich zu meown aber die funktion wird weggelassen
	if(body.is_in_group("Player")):
		move = true
		meow = true
		Global.animal_move = true

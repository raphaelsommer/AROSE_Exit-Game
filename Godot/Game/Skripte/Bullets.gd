extends Node2D

var directionLeft = true
var damage = 1
func _ready():
	pass
	
	
	
func _physics_process(delta): #Wenn waffe gefeuert wird soll die kugel mit der geschwindigkeit in x richtung bewegen 
	self.position.x += 20
	$AnimatedSprite2D.play("idle")
	
	
	

	
	


func _on_area_2d_body_entered(body): #Wenn die Bullets die ki treffen wird der ki ein leben abgezogen und die gukel soll danach verschwinden
	if(body.is_in_group("ki")):
		Global.robot_hp -= 1
		print(Global.robot_hp)
		queue_free()
		

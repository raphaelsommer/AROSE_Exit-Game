extends Node2D

var directionLeft = true
var damage = 1
func _ready():
	pass
	
	
	
func _physics_process(delta):
	self.position.x += 20
	$AnimatedSprite2D.play("idle")
	
	
	

	
	


func _on_area_2d_body_entered(body):
	if(body.is_in_group("ki")):
		Global.robot_hp -= 1
		print(Global.robot_hp)
		queue_free()
		

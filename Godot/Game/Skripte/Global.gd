extends Node

var door_open = false
var coins = 0
var player_hp = 1
var player_hp2 = 1
var player1_canMove = true
var gun_on = false
var robot_hp = 10


func dead():
	if(Global.robot_hp <= 0):
		$explosion.visible = true
		$explosion.play("explosion")
		await get_tree().create_timer(0.5).timeout
		$".".queue_free()



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

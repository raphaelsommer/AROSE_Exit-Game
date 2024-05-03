extends Node

var door_open = false
var coins = 0
var player_hp = 1
var player_hp2 = 1
var player1_canMove = true
var gun_on = false
var robot_hp = 10
var szenen_wechsel = false
var animals = false
var ki_destroyed = false
var sauerstoff = false
var key = false
var gravity = true
var player2_canMove = true
var timer_on = false




var timer

func _ready():
	timer = Timer.new()
	timer.wait_time = float(5 * 60)
	timer.one_shot = true
	timer.start()
	timer.autostart = true
	add_child(timer)
	
	
	
func _process(delta):
	pass
























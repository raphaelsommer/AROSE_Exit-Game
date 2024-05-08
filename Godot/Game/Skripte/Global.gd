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
var door_a5 = 1
var door_a4 = 1
var door_a3 = 1
var game_hard = false
var door_c1 = 1
var door_b4 = 1
var door_b3 = 1
var door_b2 = 1
var door_rk = 0
var door_c0 = 1
var mqtt_connect = false
var animal_move = false
var animal_move_not = true






var  timer

func _ready():
	timer = Timer.new()
	timer.wait_time = float(10 * 60)
	timer.one_shot = true
	timer.start()
	timer.autostart = true
	add_child(timer)
		
	
	
	
func _process(delta):
	pass
	

























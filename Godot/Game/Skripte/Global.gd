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

var door_a5 = 1
var door_a4 = 1
var door_a3 = 1
var game_hard = false
var door_c1 = 1
var door_c1_left = 1
var door_c1_right = 1
var door_b4 = 1
var door_b3 = 1
var door_b2 = 1
var door_rk = 0
var door_c0 = 1
var animal_move = false
var animal_move_not = true


var startMqtt = false
var mqtt_status = 0
var mqtt_connect = false
var mqtt_local = false
var mqtt_stop = false

var hasFailed = false

var timer_on = false
var timerStarted = false
var timer
var realTimerOver = false

func _ready():
	timer = Timer.new()
	timer.wait_time = float(9 * 60)
	timer.one_shot = true
	add_child(timer)
		
	
	
	
func _process(delta):
	if(timer_on and !timerStarted):
		timer.start()
		timerStarted = true
	if(timerStarted and timer.time_left <= 0 and !hasFailed):
		get_tree().change_scene_to_file("res://Szenen/Dead-Screen.tscn")
		hasFailed = true
		timer.stop()
		if mqtt_connect:
			MQTT_Client.pub("/gen/global", "stop")
	elif(timerStarted and timer.time_left > 0 and !timer.is_stopped() and hasFailed):
		get_tree().change_scene_to_file("res://Szenen/Dead-Screen.tscn")
		timer.stop()
		if mqtt_connect:
			MQTT_Client.pub("/gen/global", "stop")
	elif(realTimerOver and hasFailed):
		get_tree().change_scene_to_file("res://Szenen/Dead-Screen.tscn")
		timer.stop()
	if mqtt_stop:
		if mqtt_connect:
			MQTT_Client.pub("/gen/global", "stop")
























extends CanvasLayer


# Called when the node enters the scene tree for the first time.
func _ready():
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var elapsed = int(Global.timer.wait_time - Global.timer.time_left)
	var minutes = int(elapsed / 60)
	var seconds = elapsed % 60
	
	
	$VBoxContainer/HBoxContainer/Leben.text = str (Global.player_hp)
	$VBoxContainer/HBoxContainer3/Coins.text = str (Global.coins)
	$VBoxContainer/HBoxContainer2/Time.text = '%02d:%02d' % [minutes, seconds]
	if(Global.key):
		$VBoxContainer/HBoxContainer4.visible = true

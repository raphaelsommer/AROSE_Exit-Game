extends CanvasLayer


# Called when the node enters the scene tree for the first time.
func _ready():
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var elapsed = int(Global.timer.time_left) #Hier wird die auteilung gemacht wie die zeit dargestellt werden soll
	var minutes = int(elapsed / 60)
	var seconds = elapsed % 60
	

	
	
	$VBoxContainer/HBoxContainer/Leben.text = str (Global.player_hp) #Leben der Spieler wird angezeigt
	$VBoxContainer/HBoxContainer3/Coins.text = str (Global.coins) #Coins werden angezeigt
	$VBoxContainer/HBoxContainer2/Time.text = '%02d:%02d' % [minutes, seconds] #timer wird angezeigt
	
	if(Global.key):
		$VBoxContainer/HBoxContainer4.visible = true #Wenn schlüssel eingesammelt wird, wird angezigt dass der schlüssel im inventar ist

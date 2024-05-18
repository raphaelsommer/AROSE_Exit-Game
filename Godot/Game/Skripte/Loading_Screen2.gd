extends Node2D



func _ready():
	await get_tree().create_timer(5).timeout #wenn szene geladen wird startet ein timer von 5 sekunden und danach wechselt der screen zur nächsten szene
	get_tree().change_scene_to_file("res://Szenen/Start.tscn")


func _process(delta): #Wenn mqtt nicht connected ist kommt eine fehlermeldung
	if(!Global.mqtt_connect):
		$RichTextLabel2.visible = true

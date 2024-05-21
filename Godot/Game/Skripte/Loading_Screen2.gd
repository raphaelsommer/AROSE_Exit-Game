extends Node2D



func _ready():
	await get_tree().create_timer(5).timeout
	get_tree().change_scene_to_file("res://Szenen/Start.tscn")


func _process(delta):
	if(!Global.mqtt_connect):
		$RichTextLabel2.visible = true

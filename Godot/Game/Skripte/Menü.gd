extends Node2D


func _ready():
	await get_tree().create_timer(5).timeout
	#Global.mqtt_connect = true
	pass

func _on_start_pressed():
	get_tree().change_scene_to_file("res://Szenen/Loading_Screen2.tscn")
	


func _process(delta):
	await get_tree().create_timer(5).timeout
	$Sprite2D.position.x += 7
	$Sprite2D2.position.x -= 7
	

func _on_exit_pressed():
	get_tree().quit()
	




func _on_faq_pressed():
	$FAQ/Sprite2D.visible = true
	




func _on_rating_pressed():
	$Rating/Sprite2D.visible = true
	



func _on_exit_list_pressed():
	$Rating/Sprite2D.visible = false
	



func _on_info_pressed():
	$Info/Sprite2D.visible = true
	



func _on_exit_faq_pressed():
	$FAQ/Sprite2D.visible = false
	
	

	




func _on_settings_pressed():
	$Settings/Sprite2D3.visible = true
	
	


func _on_simple_pressed():
	Global.game_hard = false
	$Settings/Sprite2D3.visible = false


func _on_hard_pressed():
	Global.game_hard = true
	$Settings/Sprite2D3.visible = false




func _on_button_pressed():
	if(Global.mqtt_connect):
		$Sprite2D4/RichTextLabel.visible = false
		$Sprite2D4/RichTextLabel2.visible = true

extends Node2D


var sauerstoff = false


func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = true
		sauerstoff = true


func _process(delta):
	if(Input.is_action_just_pressed("Sauerstoff") and sauerstoff):
		Global.sauerstoff = true
		$pc/Area2D.queue_free()
		Global.timer.wait_time += float(9 * 60)
		$pc/RichTextLabel.visible = true
		await get_tree().create_timer(2).timeout
		$pc/RichTextLabel.queue_free()
		



func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$pc/Sprite2D.visible = false
		




func _on_gravity_body_entered(body):
	if(body.is_in_group("Player2")):
		Global.gravity = false


func _ready():
	#Global.timer = Timer.new()
	#Global.timer.wait_time = float(5 * 60)
	#Global.timer.one_shot = true
	#Global.timer.start()
	#Global.timer.autostart = true
	#add_child(Global.timer)
	pass

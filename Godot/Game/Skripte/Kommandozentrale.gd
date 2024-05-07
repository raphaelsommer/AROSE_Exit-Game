extends Node2D


func _physics_process(delta):
	await get_tree().create_timer(2).timeout
	$door.visible = false
	if(Global.animals):
		$CharacterBody2D4.visible = true
		$CharacterBody2D5.visible = true
	
	


func _ready():
	Global.animal_move_not = false


func _on_ip_body_entered(body):
	if(body.is_in_group("Player")):
		$RichTextLabel.visible = true


func _on_ip_body_exited(body):
	if(body.is_in_group("Player")):
		$RichTextLabel.visible = false

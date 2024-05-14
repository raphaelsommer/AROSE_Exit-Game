extends Node2D

var buyable = false


func _on_ready():
	$AnimatedSprite2D.play("off")
	
	

func _on_area_2d_body_entered(body):
	if(body.is_in_group("Player")):
		$AnimatedSprite2D.play("on")
		$Press.visible = true
		$I.visible = true


func _physics_process(delta):
	if(Input.is_action_just_pressed("Interagieren")):
		buyable = true
		$AudioStreamPlayer2D1.play()
		$Press.visible = false
		$I.visible = false
		$"Text Robot".visible = true
		
	if(Input.is_action_just_pressed("Abbruch")):
		$"Text Robot".visible = false
		$Press.visible = true
		$I.visible = true
		buyable = false
		
	if(Input.is_action_just_pressed("kaufen") and (Global.coins >= 5) and buyable):
		print(Global.coins)
		$AudioStreamPlayer2D2.play()
		Global.coins -= 5
		print(Global.coins)
		Global.player_hp += 1
		Global.player_hp2 += 1
		print(Global.player_hp)
		if(Global.coins < 5):
			$"Text Robot/RichTextLabel".visible = false
			$"Text Robot/Leave".visible = false
			$"Text Robot/Buy".visible = false
			$Keinecoins.visible = true
			$Continue.visible = true
	if(Input.is_action_just_pressed("Continue")):
		$"Text Robot".visible = false
		$Continue.visible = false
		$Keinecoins.visible = false
		
	
		
	
	#$Sprite2D.visible = true
	#if(Input.is_action_just_pressed("kaufen")):
	#Global.coins -= 5
	#Global.player1_hp += 1
	#if(Input.is_action_just_pressed("Abbruch")):
	#$Sprite2D.visible = false


func _on_area_2d_body_exited(body):
	if(body.is_in_group("Player")):
		$Press.visible = false
		$I.visible = false
		$AnimatedSprite2D.play("off")

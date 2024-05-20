extends Node2D


#Ich werde nicht jede türe einzel kommentieren da der Code identisch ist zu den anderen türen nur mit anderen variabeln 

func _process(delta): #Wenn Spiel erfolgreich abgeschlossen wird, sendet de mqtt broker eine nachircht und setzt den zustand der Türe auf 0
	if(Global.door_a5 == 0):
		$AnimatedSprite2D.play("Opens")
		$AudioStreamPlayer2D.play() #Sound wird gespielt
		$CharacterBody2D.collision_layer = 2
		Global.door_a5 = 1




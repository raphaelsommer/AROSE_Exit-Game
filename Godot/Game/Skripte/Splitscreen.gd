extends Node

@onready var players := {
	"1": {
		viewport = $"HBoxContainer/SubViewportContainer/SubViewport",
		camera = $"HBoxContainer/SubViewportContainer/SubViewport/Camera2D",
		player = $HBoxContainer/SubViewportContainer/SubViewport/MainGate/Player1,
	},			#Der Viewport, Kamera und Spieler wird für die Richtige seite des Bildschrimes eingestellt
	"2": {
		viewport = $"HBoxContainer/SubViewportContainer2/SubViewport",
		camera = $"HBoxContainer/SubViewportContainer2/SubViewport/Camera2D2",
		player = $HBoxContainer/SubViewportContainer/SubViewport/MainGate/Player2,
	}
}


func _ready() -> void:
	players["2"].viewport.world_2d = players["1"].viewport.world_2d
	for node in players.values():
		var remote_transform := RemoteTransform2D.new()
		remote_transform.remote_path = node.camera.get_path()
		node.player.add_child(remote_transform)
	var sprite = $HBoxContainer/SubViewportContainer2/SubViewport/Bg
		#Das was Spieler 1 sieh(die Map) soll auch SPieler 2 sehen, leider hat dass mit dem Hintergund nicht geklappt
	sprite.scale = Vector2(2, 2)


	
	


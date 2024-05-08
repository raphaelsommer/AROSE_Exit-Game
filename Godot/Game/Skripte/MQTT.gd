extends Node
#192.168.0.102 1883
# MQTT client implementation in GDScript
# Loosely based on https://github.com/pycom/pycom-libraries/blob/master/lib/mqtt/mqtt.py
# and initial work by Alex J Lennon <ajlennon@dynamicdevices.co.uk>
# but then heavily rewritten to follow https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html

# mosquitto_sub -h test.mosquitto.org -v -t "metest/#"
# mosquitto_pub -h test.mosquitto.org -t "metest/retain" -m "retained message" -r

@export var client_id = "rsMac"
@export var verbose_level = 2  # 0 quiet, 1 connections and subscriptions, 2 all messages
@export var binarymessages = false
@export var pinginterval = 30

var socket = true

const BCM_NOCONNECTION = 0
const BCM_WAITING_SOCKET_CONNECTION = 2
const BCM_FAILED_CONNECTION = 5
const BCM_WAITING_CONNMESSAGE = 10
const BCM_WAITING_CONNACK = 19
const BCM_CONNECTED = 20

var brokerconnectmode = BCM_NOCONNECTION

var regexbrokerurl = RegEx.new()

const DEFAULTBROKERPORT_TCP = 1883

const CP_PINGREQ = 0xc0
const CP_PINGRESP = 0xd0
const CP_CONNACK = 0x20
const CP_CONNECT = 0x10
const CP_PUBLISH = 0x30
const CP_SUBSCRIBE = 0x82
const CP_UNSUBSCRIBE = 0xa2
const CP_PUBREC = 0x40
const CP_SUBACK = 0x90
const CP_UNSUBACK = 0xb0

var pid = 0
var user = "rsMac"
var pswd = "rsMacArose1234!"
var keepalive = 120
var lw_topic = null
var lw_msg = null
var lw_qos = 0
var lw_retain = false

signal received_message(topic, message)
signal broker_connected()
signal broker_disconnected()
signal broker_connection_failed()
signal publish_acknowledge(pid)

var receivedbuffer : PackedByteArray = PackedByteArray()

var common_name = null

func checkConnect():
	return socket.put_data(PackedByteArray([0x00]))

func senddata(data):
	var E = 0
	if socket != null:
		E = socket.put_data(data)
	if E != 0:
		print("bad senddata packet E=", E)
	
func receiveintobuffer():
	if socket != null and socket.get_status() == StreamPeerTCP.STATUS_CONNECTED:
		socket.poll()
		var n = socket.get_available_bytes()
		if n != 0:
			var sv = socket.get_data(n)
			assert (sv[0] == 0)  # error code
			receivedbuffer.append_array(sv[1])
	
var pingticksnext0 = 0

func _process(delta):
	if brokerconnectmode == BCM_NOCONNECTION:
		pass
	
	elif brokerconnectmode == BCM_WAITING_SOCKET_CONNECTION:
		socket.poll()
		var socketstatus = socket.get_status()
		if socketstatus == StreamPeerTCP.STATUS_ERROR:
			if verbose_level:
				print("TCP socket error")
			brokerconnectmode = BCM_FAILED_CONNECTION
			emit_signal("broker_connection_failed")
		if socketstatus == StreamPeerTCP.STATUS_CONNECTED:
			brokerconnectmode = BCM_WAITING_CONNMESSAGE
	
	elif brokerconnectmode == BCM_WAITING_CONNMESSAGE:
		senddata(firstmessagetoserver())
		brokerconnectmode = BCM_WAITING_CONNACK
		
	elif brokerconnectmode == BCM_WAITING_CONNACK or brokerconnectmode == BCM_CONNECTED:
		receiveintobuffer()
		wait_msg()
		if brokerconnectmode == BCM_CONNECTED and pingticksnext0 < Time.get_ticks_msec():
			pingreq()
			pingticksnext0 = Time.get_ticks_msec() + pinginterval*1000

	elif brokerconnectmode == BCM_FAILED_CONNECTION:
		cleanupsockets()

func _ready():
	regexbrokerurl.compile('^(tcp://|wss://|ws://|ssl://)?([^:\\s]+)(:\\d+)?(/\\S*)?$')
	if client_id == "":
		randomize()
		client_id = "rr%d" % randi()

func set_last_will(stopic, smsg, retain=false, qos=0):
	assert((0 <= qos) and (qos <= 2))
	assert(stopic)
	self.lw_topic = stopic.to_ascii_buffer()
	self.lw_msg = smsg if binarymessages else smsg.to_ascii_buffer()
	self.lw_qos = qos
	self.lw_retain = retain
	if verbose_level:
		print("LASTWILL%s topic=%s msg=%s" % [ " <retain>" if retain else "", stopic, smsg])

func firstmessagetoserver():
	var clean_session = true
	var msg = PackedByteArray()
	msg.append(CP_CONNECT);
	msg.append(0x00);
	msg.append(0x00);
	msg.append(0x04);
	msg.append_array("MQTT".to_ascii_buffer());
	msg.append(0x04);
	msg.append(0x02);
	msg.append(0x00);
	msg.append(0x3C);

	msg[1] = 10 + 2 + len(self.client_id)
	msg[9] = (1<<1) if clean_session else 0
	if self.user != null:
		msg[1] += 2 + len(self.user) + 2 + len(self.pswd)
		msg[9] |= 0xC0
	if self.keepalive:
		assert(self.keepalive < 65536)
		msg[10] |= self.keepalive >> 8
		msg[11] |= self.keepalive & 0x00FF
	if self.lw_topic:
		msg[1] += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
		msg[9] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
		msg[9] |= 1<<5 if self.lw_retain else 0

	msg.append(len(self.client_id) >> 8)
	msg.append(self.client_id.length() & 0xFF)
	msg.append_array(self.client_id.to_ascii_buffer())
	if self.lw_topic:
		msg.append(len(self.lw_topic) >> 8)
		msg.append(len(self.lw_topic) & 0xFF)
		msg.append_array(self.lw_topic)
		msg.append(len(self.lw_msg) >> 8)
		msg.append(len(self.lw_msg) & 0xFF)
		msg.append_array(self.lw_msg)
	if self.user != null:
		msg.append(self.user.length() >> 8)
		msg.append(self.user.length() & 0xFF)
		msg.append_array(self.user.to_ascii_buffer())
		msg.append(self.pswd.length() >> 8)
		msg.append(self.pswd.length() & 0xFF)
		msg.append_array(self.pswd.to_ascii_buffer())
	return msg

func cleanupsockets(retval=false):
	if verbose_level:
		print("cleanupsockets")
	if socket:
		socket.disconnect_from_host()
		socket = null

	brokerconnectmode = BCM_NOCONNECTION
	return retval

func connect_to_broker(brokerurl):
	var brokerprotocol = "tcp"
	var brokerserver = brokerurl
	var brokerport = 1883
	
	socket = StreamPeerTCP.new()
	
	if verbose_level:
		print("Connecting to %s:%s" % [brokerserver, brokerport])
	var E = socket.connect_to_host(brokerserver, brokerport)
	if E != 0:
		print("ERROR: socketclient.connect_to_url Err: ", E)
		return cleanupsockets(false)
	brokerconnectmode = BCM_WAITING_SOCKET_CONNECTION
	
	return true

func disconnect_from_server():
	if brokerconnectmode == BCM_CONNECTED:
		senddata(PackedByteArray([0xE0, 0x00]))
		emit_signal("broker_disconnected")
	cleanupsockets()

func publish(stopic, smsg, retain=false, qos=0):
	var msg = smsg.to_ascii_buffer() if not binarymessages else smsg
	var topic = stopic.to_ascii_buffer()
	
	var pkt = PackedByteArray()
	pkt.append(CP_PUBLISH | (2 if qos else 0) | (1 if retain else 0));
	pkt.append(0x00);
		
	var sz = 2 + len(topic) + len(msg)
	if qos > 0:
		sz += 2
	assert(sz < 2097152)
	var i = 1
	while sz > 0x7f:
		pkt[i] = (sz & 0x7f) | 0x80
		sz >>= 7
		i += 1
		if i + 1 > len(pkt):
			pkt.append(0x00);
	pkt[i] = sz
	
	pkt.append(len(topic) >> 8)
	pkt.append(len(topic) & 0xFF)
	pkt.append_array(topic)

	if qos > 0:
		pid += 1
		pkt.append(pid >> 8)
		pkt.append(pid & 0xFF)
	pkt.append_array(msg)
	senddata(pkt)
	if verbose_level >= 2:
		print("CP_PUBLISH%s%s topic=%s msg=%s" % [ "[%d]"%pid if qos else "", " <retain>" if retain else "", stopic, smsg])
	return pid

func subscribe(stopic, qos=0):
	pid += 1
	var topic = stopic.to_ascii_buffer()
	var length = 2 + 2 + len(topic) + 1
	var msg = PackedByteArray()
	msg.append(CP_SUBSCRIBE);
	msg.append(length)
	msg.append(pid >> 8)
	msg.append(pid & 0xFF)
	msg.append(len(topic) >> 8)
	msg.append(len(topic) & 0xFF)
	msg.append_array(topic)
	msg.append(qos);
	if verbose_level:
		print("SUBSCRIBE[%d] topic=%s" % [pid, stopic])
	senddata(msg)

func pingreq():
	if verbose_level >= 2:
		print("PINGREQ")
	senddata(PackedByteArray([CP_PINGREQ, 0x00]))

func unsubscribe(stopic):
	pid += 1
	var topic = stopic.to_ascii_buffer()
	var length = 2 + 2 + len(topic)
	var msg = PackedByteArray()
	msg.append(CP_UNSUBSCRIBE);
	msg.append(length)
	msg.append(pid >> 8)
	msg.append(pid & 0xFF)
	msg.append(len(topic) >> 8)
	msg.append(len(topic) & 0xFF)
	msg.append_array(topic)
	if verbose_level:
		print("UNSUBSCRIBE[%d] topic=%s" % [pid, stopic])
	senddata(msg)

func wait_msg():
	var n = receivedbuffer.size()
	if n < 2:
		return OK
	var op = receivedbuffer[0]
	var i = 1
	var sz = receivedbuffer[i] & 0x7f
	while (receivedbuffer[i] & 0x80):
		i += 1
		if i == n:
			return 0
		sz += (receivedbuffer[i] & 0x7f) << ((i-1)*7)
	i += 1
	if n < i + sz:
		return OK
		
	var E = OK
	if op == CP_PINGRESP:
		assert (sz == 0)
		if verbose_level >= 2:
			print("PINGRESP")
			
	elif op & 0xf0 == 0x30:
		var topic_len = (receivedbuffer[i]<<8) + receivedbuffer[i+1]
		var im = i + 2
		var topic = receivedbuffer.slice(im, im + topic_len).get_string_from_ascii()
		im += topic_len
		var pid1 = 0
		if op & 6:
			pid1 = (receivedbuffer[im]<<8) + receivedbuffer[im+1]
			im += 2
		var data = receivedbuffer.slice(im, i + sz)
		var msg = data if binarymessages else data.get_string_from_ascii()
		
		if verbose_level >= 2:
			print("received topic=", topic, " msg=", msg)
			if topic == "/gen/global" and msg == "timeOver":
				Global.hasFailed = true
				Global.realTimerOver = true
				print("GAME OVER...")
			elif topic == "/b3/morse" and msg == "finished":
				Global.door_b3 = 0
				Global.door_b4 = 0
				Global.door_a4 = 0
				print("Opened B3, B4 and A4")
			elif topic == "/a3/buttons" and msg == "finished":
				Global.door_a3 = 0
				Global.door_a5 = 0
				Global.door_b2 = 0
				Global.gravity = 1
				print("Opened B2, A3, A5 and re-established Gravity")
			elif topic == "/c1/rfid" and msg == "finished":
				Global.door_c1 = 0
				print("Openend JnR")
			elif topic == "/c0/ip" and msg == "finished":
				Global.door_c0 = 0
				print("Openend C0")
			elif topic == "/rk/wire" and msg == "win":
				Global.door_rk = 1
				print("Openend RK -> GAME WON")
			elif topic == "/rk/wire" and msg == "fail":
				Global.hasFailed = true
				print("GAME OVER")
		emit_signal("received_message", topic, msg)
		
		if op & 6 == 2:
			senddata(PackedByteArray([0x40, 0x02, (pid1 >> 8), (pid1 & 0xFF)]))
		elif op & 6 == 4:
			#assert(0)
			pass

	elif op == CP_CONNACK:
		assert (sz == 2)
		var retcode = receivedbuffer[i+1]
		if verbose_level:
			print("CONNACK ret=%02x" % retcode)
		if retcode == 0x00:
			brokerconnectmode = BCM_CONNECTED
			emit_signal("broker_connected")
		else:
			if verbose_level:
				print("Bad connection retcode=", retcode) # see https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
			emit_signal("broker_connection_failed")
			E = FAILED

	elif op == CP_PUBREC:
		assert (sz == 2)
		var apid = (receivedbuffer[i]<<8) + receivedbuffer[i+1]
		if verbose_level >= 2:
			print("PUBACK[%d]" % apid)
		emit_signal("publish_acknowledge", apid)

	elif op == CP_SUBACK:
		assert (sz == 3)
		var apid = (receivedbuffer[i]<<8) + receivedbuffer[i+1]
		if verbose_level:
			print("SUBACK[%d] ret=%02x" % [apid, receivedbuffer[i+2]])
		if receivedbuffer[i+2] == 0x80:
			E = FAILED

	elif op == CP_UNSUBACK:
		assert (sz == 2)
		var apid = (receivedbuffer[i]<<8) + receivedbuffer[i+1]
		if verbose_level:
			print("UNSUBACK[%d]" % apid)

	else:
		if verbose_level:
			print("Unknown MQTT opcode op=%x" % op)

	trimreceivedbuffer(i + sz)
	return E

func trimreceivedbuffer(n):
	if n == receivedbuffer.size():
		receivedbuffer = PackedByteArray()
	else:
		assert (n <= receivedbuffer.size())
		receivedbuffer = receivedbuffer.slice(n)

#!/usr/bin/python3
from subprocess import check_output, CalledProcessError
from xmlrpc.server import SimpleXMLRPCServer

server = SimpleXMLRPCServer(("0.0.0.0", 8080))

server.register_introspection_functions()


def add_xmpp_user(username):
    try:
        print(check_output(
            ["/bin/sh", "/system-manager/scripts/" + "add_chat_user.sh", str(username).split("@")[0]], shell=False))
    except CalledProcessError as e:
        print(e)
        return False
    return True


def turn_on():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(2, True)
    return True


def turn_off():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(2, False)
    return True


server.register_function(add_xmpp_user)
server.register_function(turn_on)
server.register_function(turn_off)
server.serve_forever()

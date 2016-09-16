#!/usr/bin/python3
import os
from xmlrpc.server import SimpleXMLRPCServer

server = SimpleXMLRPCServer(("0.0.0.0", 8080))

server.register_introspection_functions()


def add_xmpp_user(username):
    user_data_file_path = "/var/lib/prosody/" + os.environ[
        'XMPP_DOMAIN_NAME'] + "%2elocal/accounts/" + username + ".dat"
    admin_roster_file_path = "/var/lib/prosody/" + os.environ['XMPP_DOMAIN_NAME'] + "%2elocal/roster/" + os.environ[
        'XMPP_HOST'] + ".dat"
    user_roster_file_path = "/var/lib/prosody/" + os.environ[
        'XMPP_DOMAIN_NAME'] + "%2elocal/roster/" + username + ".dat"
    roster_dir = "/var/lib/prosody/" + os.environ['XMPP_DOMAIN_NAME'] + "%2elocal/roster"

    if os.path.exists(user_data_file_path):
        return False
    else:
        open(user_data_file_path, 'w').write("return {\n\t[\"password\"] = \"abcd\";\n};")
        if not os.path.exists(roster_dir):
            os.makedirs(roster_dir, exist_ok=True)
        new_roster_content = "return {\n\t[false] = {\n\t\t[\"version\"] = 3;\n\t};\n};"
        if not os.path.exists(admin_roster_file_path):
            open(admin_roster_file_path, 'w').write(new_roster_content)
        open(user_roster_file_path, 'w').write(new_roster_content)

        with open(admin_roster_file_path, 'r+') as admin_roster_file:
            data = admin_roster_file.readlines()
            data = data[:-1]
            data.append("\t[\"" + username + "@" + os.environ[
                'XMPP_DOMAIN_NAME'] + ".local\"] = {\n\t\t[\"subscription\"] = \"to\";\n\t\t[\"groups\"] = {};\n\t};\n};")

            admin_roster_file.seek(0)
            admin_roster_file.writelines(data)
            admin_roster_file.truncate()

        with open(user_roster_file_path, 'r+') as user_roster_file:
            data = user_roster_file.readlines()
            data = data[:-1]
            data.append("\t[\"" + os.environ['XMPP_HOST'] + "@" + os.environ[
                'XMPP_DOMAIN_NAME'] + ".local\"] = {\n\t\t[\"subscription\"] = \"from\";\n\t\t[\"groups\"] = {};\n\t};\n};")

            user_roster_file.seek(0)
            user_roster_file.writelines(data)
            user_roster_file.truncate()

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

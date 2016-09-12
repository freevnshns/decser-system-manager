#!/usr/bin/python3
from subprocess import check_call, CalledProcessError
from xmlrpc.server import SimpleXMLRPCServer

server = SimpleXMLRPCServer(("0.0.0.0", 8080))

server.register_introspection_functions()


def add_xmpp_user(username):
    try:
        check_call(
            ["/bin/bash", "/system-manager/scripts/" + "add_chat_user.sh", str(username).split("@")[0]], " > log.txt",
            shell=True)
    except CalledProcessError as e:
        print(e.output)


server.register_function(add_xmpp_user)

server.serve_forever()

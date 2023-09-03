from hisock import *
import hisock
server = hisock.server.ThreadedHiSockServer((hisock.get_local_ip(), 6969))

@server.on("join")
def on_client_join(client: hisock.utils.ClientInfo):
    server.send_client(client, "ask_profile", "Do you like sheep?")

@server.on("client_profile")
def on_question_response(client: hisock.utils.ClientInfo, profile:dict):
    print(profile)
@server.on("move")
def handle_move(client: hisock.utils.ClientInfo, move:list):
    print(f"{client.name} did {move}")

server.start()
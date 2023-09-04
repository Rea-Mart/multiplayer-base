from hisock import *
import hisock
server = hisock.server.ThreadedHiSockServer((hisock.get_local_ip(), 6969))
min_clients = 2

@server.on("join")
def on_client_join(client: hisock.utils.ClientInfo):
    server.send_client(client, "ask_profile", "Do you like sheep?")
    client_count = len(server.get_all_clients())
    server.send_all_clients("server_msg",f"{client.name} connected ({client_count}/{min_clients})")
    if client_count >= min_clients:
        server.send_all_clients("server_msg","enough clients")
        server.send_all_clients("gamestate","play")
        print("enough players")
@server.on("client_profile")
def on_question_response(client: hisock.utils.ClientInfo, profile:dict):
    print(profile)
@server.on("move")
def handle_move(client: hisock.utils.ClientInfo, move:list):
    print(f"{client.name} did {move}")

server.start()
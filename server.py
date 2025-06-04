import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # Diccionario: socket -> nombre_usuario

def broadcast(message):
    for client in clients:
        client.send(message)
    

def menu():
    return """\n--- Menu ---
/login <nombre_usuario>   -> Login
/send <usuario> <mensaje> -> Enviar mensaje privado
/sendall <mensaje>        -> Enviar mensaje a todos
/show                     -> Mostrar usuarios conectados
/exit                     -> Salir
"""

def handle_client(client, address):
    client.send(b"Bienvenido al servidor!\n")
    nombre = None
    while True:
        try:
            client.send(menu().encode())
            message = client.recv(1024)
            if not message:
                break
            message = message.decode("utf-8").strip()
            print("mensaje: "+message)
            if message.startswith("/login"):
                parts = message.split()
                if len(parts) > 1:
                    nombre = parts[1]
                    clients[client] = nombre
                    client.send(f"Usuario iniciado: {nombre}\n".encode())
                    print(f"{nombre} inició sesión.")
                else:
                    client.send(b"Use: /login <ingrse un nombre\n")

            elif message.startswith("/send "):
                parts = message.split()
                if len(parts) >= 3:
                    user_destino = parts[1]
                    texto = ' '.join(parts[2:])
                    enviado = False
                    for c, n in clients.items():
                        if n == user_destino:
                            c.send(f"[{nombre}] te dice: {texto}\n".encode())
                            enviado = True
                            break
                    if not enviado:
                        client.send(b"Usuario no encontrado.\n")
                else:
                    client.send(b"Use: /send <usuario> <mensaje>\n")

            elif message.startswith("/sendall "):
                if nombre is None:
                    client.send(f"Primero debes iniciar sesión con /login\n")
                    continue
                texto = message[len("/sendall "):]
                broadcast(f"[{nombre}] dice a todos: {texto}\n".encode())

            elif message == "/show":
                usuarios_conectados = ', '.join(clients.values())
                client.send(f"Usuarios conectados: {usuarios_conectados}\n".encode())
                
            elif message == "/exit":
                print("entro al exit")
                client.send("chauu!\n".encode())
                
            else:
                client.send("Comando no reconocido.\n")

        except:
            break

    # Cuando sale el cliente
    if client in clients:
        print(f"{clients[client]} se desconectó.")
        del clients[client]
    client.close()

def receive():
    print("Servidor esperando conexiones...")
    while True:
        client, address = server.accept()
        print(f"Conectado con {address}")
        thread = threading.Thread(target=handle_client, args=(client, address), daemon=True)
        thread.start()

receive()

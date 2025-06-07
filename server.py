# Importación del módulo
import socket
import threading

# Dirección IP local 
HOST = '127.0.0.1'
# Puerto de la conexiones 
PORT = 12345

# Creación del socket del servidor 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlaza el socket a la dirección y puerto especificados
server.bind((HOST, PORT))
# El servidor empieza a escuchar conexiones entrantes
server.listen()

# Diccionario para almacenar los clientes conectados 
clients = {}

# Función para enviar un mensaje a todos los clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)

# Función que devuelve el menú 
def menu():
    return """\n--- Menu ---
/login <nombre_usuario>   -> Login
/send <usuario> <mensaje> -> Enviar mensaje privado
/sendall <mensaje>        -> Enviar mensaje a todos
/show                     -> Mostrar usuarios conectados
/exit                     -> Salir
"""

# Función que maneja la comunicación con un cliente específico
def handle_client(client, address):
    # Enviar mensaje de bienvenida al cliente
    client.send(b"Bienvenido al servidor!\n")
    nombre = None  

    while True:
        try:
            # Mostrar el menú de opciones al cliente
            client.send(menu().encode())

            # Esperar y recibir mensaje del cliente
            message = client.recv(1024)
            if not message:
                break  

            # Decodificar el mensaje de bytes a string y quitar espacios innecesarios
            message = message.decode("utf-8").strip()

            # Imprimir mensaje en consola del servidor 
            print("mensaje: " + message) 

            # Comando de login
            if message.startswith("/login"):
                parts = message.split()
                if len(parts) > 1:
                    nombre = parts[1]
                    clients[client] = nombre  # Guardar el usuario en el diccionario
                    client.send(f"Usuario iniciado: {nombre}\n".encode())
                    print(f"{nombre} inició sesión.")
                else:
                    client.send(b"Use: /login <ingrese un nombre>\n")

            # Comando para enviar mensaje privado a otro usuario
            elif message.startswith("/send "):
                parts = message.split()
                if len(parts) >= 3:
                    user_destino = parts[1]
                    texto = ' '.join(parts[2:]) 
                    enviado = False
                    for c, n in clients.items():
                        if n == user_destino:
                            # Enviar el mensaje al usuario destino
                            c.send(f"[{nombre}] te dice: {texto}\n".encode())
                            enviado = True
                            break
                    if not enviado:
                        client.send(b"Usuario no encontrado.\n")
                else:
                    client.send(b"Use: /send <usuario> <mensaje>\n")

            # Comando para enviar un mensaje a todos los usuarios conectados
            elif message.startswith("/sendall "):
                if nombre is None:
                    # Si el usuario no ha hecho login
                    client.send(f"Primero debes iniciar sesión con /login\n".encode())
                    continue
                texto = message[len("/sendall "):]  # Extraer solo el mensaje
                broadcast(f"[{nombre}] dice a todos: {texto}\n".encode())

            # Comando para mostrar todos los usuarios conectados
            elif message == "/show":
                usuarios_conectados = ', '.join(clients.values())
                client.send(f"Usuarios conectados: {usuarios_conectados}\n".encode())

            # Comando para salir
            elif message == "/exit":
                print("entro al exit")  # Mensaje en consola del servidor
                client.send("chauu!\n".encode())  # Mensaje de despedida al cliente

            # Comando no reconocido
            else:
                client.send("Comando no reconocido.\n".encode())

        except:
            break  # Si ocurre algún error, se termina 

    # Al salir del bucle, se elimina al cliente del diccionario y se cierra la conexión
    if client in clients:
        print(f"{clients[client]} se desconectó.")
        del clients[client]
    client.close()

# Función principal que acepta conexiones nuevas de clientes
def receive():
    print("Servidor esperando conexiones...")
    while True:
        # Esperar a que un cliente se conecte
        client, address = server.accept()
        print(f"Conectado con {address}")

        # Crear y lanzar un hilo para manejar a este cliente
        thread = threading.Thread(target=handle_client, args=(client, address), daemon=True)
        thread.start()

# Iniciar el servidor
receive()

# Importación del módulo 
import socket
import threading

# Dirección IP del servidor al que se va a conectar el cliente 
HOST = '127.0.0.1'
# Puerto de la conexión con el servidor
PORT = 12345

# Creación de un socket para el cliente usando 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión del cliente al servidor especificado por HOST y PORT
client.connect((HOST, PORT))

# Función que recibe mensajes del servidor
def receive():
    while True:
        try:
            # Intenta recibir un mensaje del servidor (máx 1024 bytes) y decodificarlo a UTF-8
            message = client.recv(1024).decode('utf-8')
            # Imprime el mensaje recibido en la consola
            print(message)
        except ConnectionResetError:
            # Se ejecuta si la conexión se interrumpe desde el lado del servidor
            print("Conexión interrumpida.")
            break
        except:
            # Si ocurre cualquier otro error, cierra la conexión del cliente y termina 
            client.close()
            break

# Función que envía mensajes al servidor
def send():
    while True:
        # Lee un mensaje escrito por el usuario en la consola
        message = input()
        if message == "/exit":
            # Si el usuario escribe "/exit", se notifica el cierre de sesión
            print("cerrando sesión")
            # Envía el mensaje "/exit" al servidor antes de cerrar
            client.send(message.encode('utf-8'))
            # Cierra la conexión del cliente
            client.close()
            break
        else:
            # Si no es "/exit", simplemente se envía el mensaje al servidor
            client.send(message.encode('utf-8'))

# Se crea un hilo independiente para recibir mensajes del servidor sin bloquear el resto del programa
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Se crea otro hilo independiente para enviar mensajes al servidor
write_thread = threading.Thread(target=send)
write_thread.start()


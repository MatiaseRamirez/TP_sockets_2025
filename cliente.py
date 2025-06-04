import socket
import threading


HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)

        except ConnectionResetError:
            print("Conexión interrumpida.")
            break
        except :
            client.close()
            break

def send():
    while True:
        message = input()
        if message=="/exit":
            print("cerrando sesion")
            client.send(message.encode('utf-8'))
            client.close()
            break
        else:
            client.send(message.encode('utf-8'))
            
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()



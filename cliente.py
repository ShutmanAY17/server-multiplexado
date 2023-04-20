import socket

HOST = '127.0.0.1'
PORT = 12345
print("Con que nombre se guarda?")
name_save = input()


with socket.socket() as socket_client:
    socket_client.connect((HOST, PORT))
    socket_client.sendall((name_save + '.mp3').encode("utf-8"))
    with open('C:\\Users\\alexc\\Downloads\\Prueba\\audio2.mp3', 'rb') as f:
        audio = f.read()

    paquetes = [audio[i:i+1024] for i in range(0, len(audio), 1024)]
    for paquete in paquetes:
        socket_client.sendall(paquete)
        confirmacion = socket_client.recv(1024)
        print(confirmacion.decode())

    socket_client.sendall(b'final del audio')
    




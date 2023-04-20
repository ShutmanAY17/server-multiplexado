import socket
import selectors
import errno

sel = selectors.DefaultSelector()
nombre = ""

def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept()  # Should be ready
    print('aceptado', sock_conn, ' de', addr)
    sock_conn.setblocking(False)
    sel.register(sock_conn, selectors.EVENT_READ, upload_music)


def upload_music(sock_c, mask):
    if mask & selectors.EVENT_READ:
        paquetes = []
        hay_nombre = False
        while True:
            try:
                datos = sock_c.recv(1024)
                if not hay_nombre:
                    print(datos)
                    nombre = datos.decode("utf-8")
                    hay_nombre = True
            except BlockingIOError as e:
                if e.errno == errno.EWOULDBLOCK:
                    print("No hay datos disponibles para leer en el socket en este momento.")
                else:
                    print("Se ha producido un error de socket:", e)
            else:
                if datos != b'final del audio':
                    sock_c.sendall(b'Paquete recibido correctamente')
                    paquetes.append(datos)
                else:
                    audio = b''.join(paquetes)
                    with open(nombre, 'wb') as f:
                        f.write(audio)
                        print("Audio escrito\n")
                    sel.unregister(sock_c)
                    sock_c.close()
                    break
        
    
with socket.socket() as sock_accept:
    sock_accept.bind(('localhost', 12345))
    sock_accept.listen(100)
    sock_accept.setblocking(False)
    sel.register(sock_accept, selectors.EVENT_READ, accept)
    while True:
        print("Esperando evento...")
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

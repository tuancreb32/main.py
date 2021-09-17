import socket
import ssl
import select
from ssl import SSLContext
import  hashlib
import threading
BUFCLIENTLEN = 2048
BUFSERVERLEN = 2048
HOST = "tuserver.com o direccion IP"
PORT = 443
SNI = "www.google.com"
LISTENPORT = 8080
def Manejador(ClienteSocket):
    ContextoSSL = SSLContext(protocol=ssl.PROTOCOL_SSLv23)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketSeguro = ContextoSSL.wrap_socket(sock, server_hostname=SNI)
    socketSeguro.connect((HOST, PORT))
    socketSeguro.do_handshake()
    der = socketSeguro.getpeercert(binary_form=True)
    pem_data = ssl.DER_cert_to_PEM_cert(der)
    print "Algoritmo de cifrado "+socketSeguro.cipher()[0]
    try:
        while True:
            socketPaleer = [ClienteSocket, socketSeguro]
            socketSel, _, _ = select.select(socketPaleer, [], [])
            if not socketSel:
                socketSeguro.close()
                ClienteSocket.close()
                print "TERMINO AL CONEXION"
                break
            for s in socketSel:
                if s is socketSeguro:
                    data = s.recv(BUFSERVERLEN)
                    ClienteSocket.send(data)
                else:
                    data = s.recv(BUFCLIENTLEN)
                    socketSeguro.send(data)

    except:
        ClienteSocket.close()
        socketSeguro.close()
        print "encontre un error"



# SET VARIABLES
print "Reemplimentacion de Tunnel SSL escrito en python crea un tunnel seguro y protege tus datos"
print "------------------------------------------"
print "-Requisitos-"
print "-Interprete python en Windows,Linux,Android etc."
print "-Diferentes arquitecturas"
print "-Disfruta de tu privacidad"
print "-------------------------------------------"
print "Creditos ph502 por la idea, Contactos TG: @wtxor, @ph502"
print "escuchando en localhost:"+str(LISTENPORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0",LISTENPORT))
sock.listen(90)
while True:
    ClientSock,direccion = sock.accept()
    ClientSock.setblocking(0)
    print  "Nueva conexion "+str(direccion)
    x = threading.Thread(target=Manejador,args=(ClientSock,))
    x.start()


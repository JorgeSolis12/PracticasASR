from ftplib import FTP
import telnetlib
from getSNMP import *
import getpass
import tftpy

comunidad = "RO"
ip = "192.168.1.1"
def conectar_FTP():
    ftp = FTP()
    ftp.connect(ip, 21, -999) 
    ftp.login('rcp', 'rcp')
    archivo = ftp.retrlines('RETR example.py') 
    print(archivo) 
    ftp.close()

def conectar_Telnet():
    
    HOST = ip
    user = input("Enter your remote account: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    
    data = '' 
    while data.find("startup-config") == -1:
        data = tn.read_very_eager()
    print(data)


def conectar_TFTP():
    client = tftpy.TftpClient(ip, 69)
    client.download('startup-config', 'startup-config')

def main():
    a = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.1.1.0')
    d = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.1.4.0')
    e = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.1.5.0')
    f = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.1.6.0')
    g = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.1.1.0') 
    
    opcion = int(input("Que desea hacer \n 1. Ver archivo\n 2. Tomar archivo 3. Agregar archivo"))
    if(opcion == 1):
        conectar_FTP()
    elif(opcion == 2):
        conectar_Telnet()
    elif(opcion == 3):
        conectar_TFTP()

if __name__ == "__main__":
    main()
from ftplib import FTP
import telnetlib
from getSNMP import *
import getpass
import tftpy
import os

comunidad = "public"
ip = "192.168.1.1"
def conectar_FTP():
    ftp = FTP()
    ftp.connect(ip, 21, -999) 
    ftp.login('rcp', 'rcp')
    archivo = ftp.retrlines('RETR startup-config') 
    print(archivo) 
    ftp.close()

def conectar_FTP_download():
    ftp = FTP()
    ftp.connect(ip, 21, -999) 
    ftp.login('rcp', 'rcp')
    listing = []
    ftp.retrlines("LIST", listing.append)

    filename = "startup-config"
    # download the file
    local_filename = os.path.join(r"C:\Users\nirfa\OneDrive\Documentos\GitHub\PracticasASR\Practica 4", filename)
    lf = open(local_filename, "wb")
    ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
    lf.close()

def conectar_FTP_upload():
    ftp = FTP()
    ftp.connect(ip, 21, -999) 
    ftp.login('rcp', 'rcp')
    listing = []
    ftp.retrlines("LIST", listing.append)

    # Ubicacion del fichero origen
    routeOrigin="C:/Users/nirfa/OneDrive/Documentos/GitHub/PracticasASR/Practica 4/3"

    filename = "startup-config"
    local_filename = os.path.join(r"C:\Users\nirfa\OneDrive\Documentos\GitHub\PracticasASR\Practica 4", filename)
    lf = open(local_filename, "rb")
    ftp.storbinary("STOR " +filename,lf, 8*1024)
   
    lf.close()

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
        print("entro")
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
    
    print("Sistema operativo: " +a)
    print("Contacto: "+d)
    print("Dispositivo: "+e)
    print("Localización: "+f)

    opcion = int(input("Que desea hacer \n 1. Ver archivo\n 2. Tomar archivo\n 3. Agregar archivo\n"))
    if(opcion == 1):
        conectar_FTP()
    elif(opcion == 2):
        conectar_FTP_download()
        #conectar_Telnet()
    elif(opcion == 3):
        conectar_FTP_upload()
        #conectar_TFTP()

if __name__ == "__main__":
    main()
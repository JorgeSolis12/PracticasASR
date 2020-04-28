import time
from getSNMP import *

comunidad = "grupo4CV5"
ip = "192.168.100.19"

def main():

    print("-------------------Menú-----------------------------------")
    
    print("¿Qué desea hacer?")
    print("1. Capas de transporte")
    print("2. Paquetes IP de red")
    print("3. Números de puerto de una aplicación")
    entrada = int(input("¿Que desea realizar?"))
    total = 0
    totalin = 0
    while True:
        if entrada == 1:
            a = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.6.10.0')
            b = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.6.11.0')
            print("TCP packets:  " +" input: " + a+" output: "+b)
            print("---------------------------------------------------------")
            totalin = totalin+int(a)
            print("Total input: "+str(totalin))
            total = total+int(b)
            print("Total output: "+str(total)+"\n")

            a = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.7.1.0')
            b = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.7.4.0')
            print("UDP datagrams:  " +" input: " + a+" output: "+b)
            print("---------------------------------------------------------")
            totalin = totalin+int(a)
            print("Total input: "+str(totalin))
            total = total+int(b)
            print("Total output: "+str(total)+"\n")
        
        elif entrada == 2:
            a = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.4.3.0')
            b = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.4.10.0')
            print(" IP packets  " +"input: " + a+" output: "+b)
            print("---------------------------------------------------------")
            totalin = totalin+int(a)
            print("Total input: "+str(totalin))
            total = total+int(b)
            print("Total output: "+str(total)+"\n")
        elif entrada ==3:
            print("Ports TCP: ")
            a = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.6.5.0')
            print("---------------------------------------------------------")
            print("Packets: "+ a)
            total = total + int(a)
            print("Total: "+str(total))
            print("Ports UDP: ")
            b = consultaSNMP(comunidad,ip, '1.3.6.1.2.1.7.2.0')
            print("---------------------------------------------------------")
            print("Packets: "+ b)

            totalin = totalin + int(b)
            print("Total: "+str(totalin))
        else:
            print("Entrada no valida")
        time.sleep(1)

if __name__ == "__main__":
    main()
import sys
import time
import os
import rrdtool
import threading
from getSNMP import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

hilos_mulicast = []
w_or_l = [1,2]

numero_agentes = 2
numero_puertos = 1
ips = ['10.100.74.60','10.100.74.133']
comunidad = "JorgeSolis4CV5"
def down_or_up(entero):
    if entero == 1:
        return "up"
    elif entero == 2:
        return "down"
    else:
        return "testing"

def inicio(agent, n_age):
    agentes = "Número de agente en monitoreo: "+ str(numero_agentes)
    print(agentes)
    if agent == 1:
        a = consultaSNMP(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.1.0')
        d = consultaSNMP(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.4.0')
        e = consultaSNMP(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.5.0')
        f = consultaSNMP(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.6.0')
        g = consultaSNMP(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.1.0') 
        # response = os.system("ping -c 1 " + ips[i]) -> este seria para Windows
        response = os.system("ping -c 1 " + ips[n_age-1] + " > /dev/null 2>&1")

        if response == 0:
            j = "up"
        else:
            j= "down"

        print(str(n_age)+". Agente: "+a)
        print("\tContacto:"+d)
        print("\tEquipo: "+e)
        print("\tLocalización: "+f)
        print("\tSO: "+g)
        print("\tEstado: "+j)
        
        numero_puertos = int(consultaSNMP(comunidad,ips[n_age-1], "1.3.6.1.2.1.2.1.0"))
        
        print("numero de puertos: "+ str(numero_puertos))
        print("\tPuertos:")

        for i in range(0,numero_puertos):
            oid = "1.3.6.1.2.1.2.2.1.2." + str(i+1)
            oid2 = "1.3.6.1.2.1.2.2.1.7."+str(i+1) 
            k = consultaSNMP(comunidad,ips[n_age-1], oid)
            k2 = down_or_up(int(consultaSNMP(comunidad,ips[n_age-1], oid2)))
            
            print("\t\t"+k+": "+k2)

    elif agent == 2:  
        response = os.system("ping -c 1 " + ips[n_age-1]) 
        #response = os.system("ping -c 1 " + ips[n_age-1] + " > /dev/null 2>&1")
        a = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.1.0')
        d = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.4.0')
        e = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.5.0')
        f = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.6.0')
        g = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.1.1.0') 
        
        if response == 0:
            j = "up"
        else:
            j= "down"

        print(str(n_age)+". Agente: "+a)
        print("\tContacto:"+d[27:])
        print("\tEquipo: "+e[24:])
        print("\tLocalización: "+f[28:])
        print("\tSO: "+g)
        print("\tEstado: "+j)

    
        aux = consultaSNMPWindows(comunidad,ips[n_age-1], '1.3.6.1.2.1.2.1.0')
        str_cut = aux[26:]
        entero = int(str_cut)
        numero_puertos = entero
        print("numero de puertos: "+ str(numero_puertos))
        print("\tPuertos:")

        for i in range(0,numero_puertos):
            oid = "1.3.6.1.2.1.2.2.1.2." + str(i+1)
            oid2 = "1.3.6.1.2.1.2.2.1.7."+str(i+1) 
            k = consultaSNMP(comunidad,ips[n_age-1], oid)
            k2 = down_or_up(int(consultaSNMP(comunidad,ips[n_age-1], oid2)))
            print("\t\t"+k+": "+k2)

    return

def eliminar_agente(entero):
    global numero_agentes
    print("entro")
    hilos_mulicast.pop(entero-1)
    ips.pop(entero-1)
    w_or_l.pop(entero-1)
    numero_agentes = numero_agentes-1
    print("agente "+ str(entero)+ " eliminado")
    return
def agregar_agente(ip_na,wl,port):
    global numero_agentes
    ips.append(ip_na)
    numero_agentes = numero_agentes +1
    w_or_l.append(wl)
    t = threading.Thread(target=multicast_package, args=(numero_agentes,numero_agentes,))
    t2 = threading.Thread(target=ipv4_package, args=(numero_agentes,numero_agentes,))
    t3 = threading.Thread(target=ICMP_package, args=(numero_agentes,numero_agentes,))
    t4 = threading.Thread(target=UDP, args=(numero_agentes,numero_agentes,))
    t5 = threading.Thread(target=segments, args=(numero_agentes,numero_agentes,))
    
    t.start()
    hilos_mulicast.append(t)

def menu():
    print("número de agentes en la arquitectura: " + str(numero_agentes))
    print ("---------------------Inicio------------------------------")
    print("1. mostrar información general")
    print("2. agregar agente")
    print("3. eliminar agente")
    print("4. Generar reporte")
    
    index = int(input())
    if index== 1:
        age = 0
        print("Es agente: \n 1. Linux \n 2. Windows")
        age = int(input())
        print("teclee el número de agente")
        ag = int(input())
        inicio(age, ag)
    if index == 2:
        print("Dame la ip a generar")
        ip_na = input()
        print("Que SO es:\n 1.Linux \n 2.Windows")
        wl = int(input())
        print("Dame el puerto")
        port = int(input())
        agregar_agente(ip_na,wl,port)
        print("agregado con exito")

    if index == 3:
        print("que agente desea eliminar?")

        for i in range(0,numero_agentes):
            if w_or_l[i]==1:
                print(str(i+1)+". Agente_Linux: "+ips[i])
            else:
                print(str(i+1)+". Agente_Windows: "+ips[i])

        hilo_supr = int(input())
        eliminar_agente(hilo_supr)
        print("exito al eliminar")

    if index == 4:
        print("Es agente: \n 1. Linux \n 2. Windows")
        age = int(input())

        for i in range(0,numero_agentes):
            if w_or_l[i]==1:
                print(str(i+1)+". Agente_Linux: "+ips[i])
            else:
                print(str(i+1)+". Agente_Windows: "+ips[i])

        print("teclee el número de agente")
        ag = int(input())
        documento(age,ag)
    menu()

def ipv4_package(na_get,agent):
    #1.3.6.1.2.1.4.9.0
    agente  = numero_agentes
    if agente == agent:
        name = "ipv4_"+str(na_get+1)+"."
        ret = rrdtool.create(name+"rrd",
                            "--start",'N', 
                            "--step",'60', 
                            "DS:inoctets:COUNTER:600:U:U",
                            "DS:outoctets:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600")

        rrdtool.dump(name+"rrd", name+"xml")
        total_input_mcast = 0

        while 1:
            if w_or_l[na_get-1] == 1:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.4.9.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.4.9.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            else:
                if agente == agent:
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.4.9.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.4.9.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            
        if ret:
            print(rrdtool.error())
    else:
        time.sleep(5)
        agente = numero_agentes
    

def multicast_package(na_get,agent):
    #1.3.6.1.2.1.2.2.1.11
    agente  = numero_agentes
    if agente == agent:
        name = "paquetes_multicast"+str(na_get+1)+"."
        ret = rrdtool.create(name+"rrd",
                            "--start",'N', 
                            "--step",'60', 
                            "DS:inoctets:COUNTER:600:U:U",
                            "DS:outoctets:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600")

        rrdtool.dump(name+"rrd", name+"xml")
        total_input_mcast = 0

        while 1:
            if w_or_l[na_get-1] == 1:
                if agente == agent:
                    n_p = int(consultaSNMP(comunidad,ips[na_get-1], "1.3.6.1.2.1.2.1.0"))
                    for i in range(0,n_p):
                        oid = "1.3.6.1.2.1.2.2.1.11."+ str(i+1)
                        total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],oid))
                        total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],oid))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            else:
                if agente == agent:
                    n_p = int(consultaSNMP(comunidad,ips[na_get-1], "1.3.6.1.2.1.2.1.0"))
                    for i in range(0,n_p):
                        oid = "1.3.6.1.2.1.2.2.1.11."+ str(i+1)
                        total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],oid))
                        total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],oid))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
        if ret:
            print(rrdtool.error())
    else:
        time.sleep(5)
        agente = numero_agentes


def ICMP_package(na_get,agent):
    #1.3.6.1.2.1.5.21.0

    agente  = numero_agentes
    if agente == agent:
        name = "ICMP_"+str(na_get+1)+"."
        ret = rrdtool.create(name+"rrd",
                            "--start",'N', 
                            "--step",'60', 
                            "DS:inoctets:COUNTER:600:U:U",
                            "DS:outoctets:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600")

        rrdtool.dump(name+"rrd", name+"xml")
        total_input_mcast = 0

        while 1:
            if w_or_l[na_get-1] == 1:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.5.21.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.5.21.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            else:
                
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.5.21.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.5.21.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
        if ret:
            print(rrdtool.error())
    else:
        time.sleep(5)
        agente = numero_agentes

def segments(na_get,agent):
    #1.3.6.1.2.1.6.10.0

    agente  = numero_agentes
    if agente == agent:
        name = "segments"+str(na_get+1)+"."
        ret = rrdtool.create(name+"rrd",
                            "--start",'N', 
                            "--step",'60', 
                            "DS:inoctets:COUNTER:600:U:U",
                            "DS:outoctets:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600")

        rrdtool.dump(name+"rrd", name+"xml")
        total_input_mcast = 0

        while 1:
            if w_or_l[na_get-1] == 1:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.6.10.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.6.10.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            else:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.6.10.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.6.10.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
        if ret:
            print(rrdtool.error())
    else:
        time.sleep(5)
        agente = numero_agentes

def UDP(na_get,agent):
    #1.3.6.1.2.1.7.1.0

    agente  = numero_agentes
    if agente == agent:
        name = "udp"+str(na_get+1)+"."
        ret = rrdtool.create(name+"rrd",
                            "--start",'N', 
                            "--step",'60', 
                            "DS:inoctets:COUNTER:600:U:U",
                            "DS:outoctets:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600")

        rrdtool.dump(name+"rrd", name+"xml")
        total_input_mcast = 0

        while 1:
            if w_or_l[na_get-1] == 1:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.7.1.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.7.1.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
            else:
                if agente == agent:  
                    total_input_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.7.1.0"))
                    total_output_mcast = total_input_mcast+ int(consultaSNMP(comunidad,ips[na_get-1],"1.3.6.1.2.1.7.1.0"))
                    
                    valor = "N:"+str(total_input_mcast)+":"+str(total_output_mcast)
                    rrdtool.update(name+"rrd", valor)
                    rrdtool.dump(name+"rrd",name+"xml")
                    time.sleep(1)
                else:
                    time.sleep(5)
                    agente = numero_agentes
        if ret:
            print(rrdtool.error())
    else:
        time.sleep(5)
        agente = numero_agentes

def documento(n_agente, na):
    #print("desde que hora deseas empezar tu entero")
    #inicio = input()
    #print("a que hora deseas terminar")
    #final = input()
    ALTO = 155/2
    ANCHO = 497/2

    na_ips = na-1
    if n_agente == 1:
        Sysname = consultaSNMP(comunidad,ips[na_ips],'1.3.6.1.2.1.1.5.0')
        SysDesc = consultaSNMP(comunidad,ips[na_ips],'1.3.6.1.2.1.1.1.0')
        a = consultaSNMP(comunidad,ips[na_ips], '1.3.6.1.2.1.1.1.0')
        b = consultaSNMP(comunidad,ips[na_ips], '1.3.6.1.2.1.1.4.0')
        f = consultaSNMP(comunidad,ips[na_ips], '1.3.6.1.2.1.1.5.0')
        d = consultaSNMP(comunidad,ips[na_ips], '1.3.6.1.2.1.1.6.0')
        e = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.1.0') 

    else:
        Sysname_aux = consultaSNMPWindows(comunidad,ips[na_ips],'1.3.6.1.2.1.1.5.0')
        Sysname = Sysname_aux[24:]
        SysDesc_aux = consultaSNMPWindows(comunidad,ips[na_ips],'1.3.6.1.2.1.1.1.0')
        SysDesc = SysDesc_aux[24:]
        a = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.1.0')
        b_aux = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.4.0')
        b = b_aux[27:]
        f_aux = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.5.0')
        c= b_aux[24:]
        d_aux = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.6.0')
        d = d_qb_aux[28:]
        e = consultaSNMPWindows(comunidad,ips[na_ips], '1.3.6.1.2.1.1.1.0') 

    w, h = A4
    x = 120
    y = h -75
    document = "Documento"+str(na)+".pdf"
    c = canvas.Canvas(document, pagesize=A4)
    #generar el texto en el pdf
    text = c.beginText(50, h - 50)
    text.setFont("Times-Roman", 12)
    text.textLine(Sysname)
    text.textLine(SysDesc)
    c.drawText(text)
    c.line(0, y, x + 600, y)
    

    text2 = c.beginText(50, h-100)
    text2.setFont("Times-Roman",8)
    text2.textLine(a)
    text2.textLine(b)
    text2.textLine(f)
    text2.textLine(d)
    text2.textLine(e)
    c.drawText(text2)
    #multicast
    name = "paquetes_multicast"+str(na)+"."
    ret = rrdtool.graph( name+"png",
                    "--start",'1582758960',
                    "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inoctets="+name+"rrd:inoctets:AVERAGE",
                    "DEF:outoctets="+name+"rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out traffic\r")


    c.drawImage(name+"png", 180, h - 300, width=ANCHO, height=ALTO)
    
    #ipv4
    name = "ipv4_"+str(na)+"."
    ret = rrdtool.graph( name+"png",
                    "--start",'1582758960',
                    "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inoctets="+name+"rrd:inoctets:AVERAGE",
                    "DEF:outoctets="+name+"rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out traffic\r")
    
    c.drawImage(name+"png", 180, h - 320-ALTO, width=ANCHO, height=ALTO)
    
    #segments
    name = "segments"+str(na)+"."
    ret = rrdtool.graph( name+"png",
                     "--start",'1582758960',
                    "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inoctets="+name+"rrd:inoctets:AVERAGE",
                    "DEF:outoctets="+name+"rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out traffic\r")
    
    c.drawImage(name+"png", 180, h - 340-(ALTO*2), width=ANCHO, height=ALTO)
    #ICMP
    
    name = "ICMP_"+str(na)+"."
    ret = rrdtool.graph( name+"png",
                     "--start",'1582758960',
                    "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inoctets="+name+"rrd:inoctets:AVERAGE",
                    "DEF:outoctets="+name+"rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out traffic\r")
    
    c.drawImage(name+"png", 180, h - 360-(ALTO*3), width=ANCHO, height=ALTO)
    
    #UDP
    name = "udp"+str(na)+"."
    ret = rrdtool.graph( name+"png",
                     "--start",'1582758960',
                    "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inoctets="+name+"rrd:inoctets:AVERAGE",
                    "DEF:outoctets="+name+"rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out traffic\r")

    c.drawImage(name+"png", 180, h - 380-(ALTO*4), width=ANCHO, height=ALTO)
    
    c.showPage()
    c.save()
    return

def multicast_monitor(entero):
    for i in range (0,entero):
        t = threading.Thread(target=multicast_package, args=(i,numero_agentes,))
        t.start()
        hilos_mulicast.append(t)

def ipv4_monitor(entero):
    for i in range (0,entero):
        t = threading.Thread(target=ipv4_package, args=(i,numero_agentes,))
        t.start()
        hilos_mulicast.append(t)

def ICMP_monitor(entero):
    for i in range (0,entero):
        t = threading.Thread(target=ICMP_package, args=(i,numero_agentes,))
        t.start()
        hilos_mulicast.append(t)

def udp_monitor(entero):
    for i in range (0,entero):
        t = threading.Thread(target=UDP, args=(i,numero_agentes,))
        t.start()
        hilos_mulicast.append(t)

def segments_monitor(entero):
    for i in range (0,entero):
        t = threading.Thread(target=segments, args=(i,numero_agentes,))
        t.start()
        hilos_mulicast.append(t)


def menu_th():
    menu()    

def main():
    menu_verify = False
    question = 0
    if(menu_verify == False):    
        t = threading.Thread(target=menu_th)
        t.start()
        multicast_monitor(numero_agentes)
        ipv4_monitor(numero_agentes)
        ICMP_monitor(numero_agentes)
        segments_monitor(numero_agentes)
        udp_monitor(numero_agentes)

        if question == 1:
            print("desea salir del programa?\n 1.Si \n 2. No")
            verify = int(input())    
            if(verify == 1):
                menu_verify == True
            elif(verify ==2):
                menu_verify == False
            else:
                print("numero invalido")
                menu_verify == False
        else:
            time.sleep(5)
            question = question+1
    else:
        t.join()
        sys.exit()
    return
    

if __name__ == "__main__":
    main()
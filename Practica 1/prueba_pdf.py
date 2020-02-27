import rrdtool
import threading
from getSNMP import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ALTO = 155/2

ANCHO = 497/2
    
Sysname = consultaSNMP('grupo4cv5',"localhost",'1.3.6.1.2.1.1.5.0')
SysDesc = consultaSNMP('grupo4cv5',"localhost",'1.3.6.1.2.1.1.1.0')
a = consultaSNMP('grupo4cv5',"localhost", '1.3.6.1.2.1.1.1.0')
b = consultaSNMP('grupo4cv5',"localhost", '1.3.6.1.2.1.1.4.0')
f = consultaSNMP('grupo4cv5',"localhost", '1.3.6.1.2.1.1.5.0')
d = consultaSNMP('grupo4cv5',"localhost", '1.3.6.1.2.1.1.6.0')
e = consultaSNMPWindows('grupo4cv5',"localhost", '1.3.6.1.2.1.1.1.0') 

w, h = A4
x = 120
y = h -75
name = "paquetes_multicast"+str(1)+"."
name1 = "ipv4_"+str(1)+"."
name2 = "segments"+str(1)+"."
name3 = "udp"+str(1)+"."
name4 = "ICMP_"+str(1)+"."

document = "Documento"+str(1)+".pdf"
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

#MULTICAST_Gráfica

c.drawImage(name+"png", 180, h - 300, width=ANCHO, height=ALTO)
#IPV4 Gráfica
c.drawImage(name1+"png", 180, h - 320-ALTO, width=ANCHO, height=ALTO)
#Segments 
c.drawImage(name2+"png", 180, h - 340-(ALTO*2), width=ANCHO, height=ALTO)
#UDP
c.drawImage(name2+"png", 180, h - 360-(ALTO*3), width=ANCHO, height=ALTO)
#ICMP
c.drawImage(name2+"png", 180, h - 380-(ALTO*4), width=ANCHO, height=ALTO)
c.showPage()
c.save()
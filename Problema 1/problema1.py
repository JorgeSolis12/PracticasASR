#!/usr/bin/env python
# -*- coding: utf-8 -*-

from path import *
from Notify import *
from getSNMP import *
from getSNMP import consultaSNMP
#from Notify import check_aberration
total_input_traffic = 0
import time
import numpy as np #Librería numérica
import rrdtool
import matplotlib.pyplot as plt # Para crear gráficos con matplotlib
#%matplotlib inline # Si quieres hacer estos gráficos dentro de un jupyter notebook

from sklearn.linear_model import LinearRegression #Regresión Lineal con scikit-learn

comunidad = "grupo4CV5"
IP = "192.168.100.19"
gh = 4.2
not_val1 = True
not_val2 =True

def notificacion(name):
    if not_val1 == True:
        send_alert_attached("CPU Al 90%",name)
        not_val1 = False

    if not_val2 == True:
        send_alert_attached("CPU al 100%",name)
        not_val2 = False

def f(x):  # función f(x) = 0.1*x + 1.25 + 0.2*Ruido_Gaussiano
    np.random.seed(42) # para poder reproducirlo
    y = 0.1*x + 1.25 + 0.2*np.random.randn(x.shape[0])
    return y
def tarea_1():
    print("Tarea1")

    carga_array = []
    y = 0

    for i in range(0,20):
        carga = float(consultaSNMP(comunidad, IP, '1.3.6.1.4.1.2021.10.1.3.1'))
        carga = (carga*100)/gh

        if carga == 90 or carga == 100:
            notificacion("gráfico")
        carga_array.append(carga) 

    x = np.array(carga_array)
    y = f(x)

    regresion_lineal = LinearRegression() 
    regresion_lineal.fit(x.reshape(-1,1), y) 
    w = regresion_lineal.coef_  
    b = regresion_lineal.intercept_
    print('w = ' + str(w) + ', b = ' + str(b))
    
    #predicción a 90
    nuevo_x = np.array([90]) 
    prediccion = regresion_lineal.predict(nuevo_x.reshape(-1,1))
    print(prediccion)
        
    #predicción a 100
    nuevo_x2 = np.array([100]) 
    prediccion2 = regresion_lineal.predict(nuevo_x2.reshape(-1,1))
    print(prediccion2)
    
    plt.scatter(x,y,label='data', color='blue')
    plt.title('Datos')
    plt.plot(nuevo_x,prediccion)
    plt.plot(nuevo_x2,prediccion2)
    plt.grid()
    plt.show()
    plt.savefig("gráfico.png")

def tarea_2():
    print("Tarea 2")
    
    #creamos la base de datos.
    ret = rrdtool.create(rrdpath+rrdname,
                     "--start",'N',
                     "--step",'60',
                     "DS:inoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:3000",
            #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                     "RRA:HWPREDICT:1000:0.1:0.0035:200:3",
              #RRA:SEASONAL:seasonal period:gamma:rra-num
                     "RRA:SEASONAL:200:0.1:2",
              #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
                     "RRA:DEVSEASONAL:200:0.1:2",
                #RRA:DEVPREDICT:rows:rra-num
                     "RRA:DEVPREDICT:1000:4",
            #RRA:FAILURES:rows:threshold:window length:rra-num
                     "RRA:FAILURES:1000:7:9:4")

    #HWPREDICT rra-num is the index of the SEASONAL RRA.
    #SEASONAL rra-num is the index of the HWPREDICT RRA.
    #DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
    #DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
    #FAILURES rra-num is the index of the DEVSEASONAL RRA.

    fname=rrdpath+rrdname
    # Generate charts for last 24 hours
    endDate = rrdtool.last(fname) #ultimo valor del XML
    begDate = endDate - 3600

    while 1:
        carga = float(consultaSNMP(comunidad, IP, '1.3.6.1.4.1.2021.10.1.3.1'))
        total_input_traffic  = (carga*100)/gh

        valor = rrdtool.lastupdate(fname)+1 + str(total_input_traffic)
        print (valor)
        ret = rrdtool.update(fname, valor)
        rrdtool.dump(fname,'pred.xml')
        time.sleep(1)


    if ret:
        print (rrdtool.error())
        time.sleep(300)

    title="Deteccion de comportamiento anomalo"
    fname=rrdpath+rrdname
    endDate = rrdtool.last(fname) #ultimo valor del XML
    begDate = endDate - 30000
    DatosAyer=begDate - 86400
    FinAyer=endDate - 86400
    #rrdtool.tune(rrdname, '--alpha', '0.1')
    ret = rrdtool.graph(pngpath+"pred.png",
                            '--start', str(begDate), '--end', str(endDate), '--title=' + title,
                            "--vertical-label=Bytes/s",
                            '--slope-mode',
                            "DEF:obs=" + fname + ":inoctets:AVERAGE",
                            "DEF:obsAyer=" + fname + ":inoctets:AVERAGE:start="+str(DatosAyer)+":end="+str(FinAyer),
                            "DEF:pred=" + fname + ":inoctets:HWPREDICT",
                            "DEF:dev=" + fname + ":inoctets:DEVPREDICT",
                            "DEF:fail=" + fname + ":inoctets:FAILURES",
                            'SHIFT:obsAyer:86400',
                        #"RRA:DEVSEASONAL:1d:0.1:2",
                        #"RRA:DEVPREDICT:5d:5",
                        #"RRA:FAILURES:1d:7:9:5""
                            "CDEF:scaledobs=obs,8,*",
                            "CDEF:scaledobsAyer=obsAyer,8,*",
                            "CDEF:upper=pred,dev,2,*,+",
                            "CDEF:lower=pred,dev,2,*,-",
                            "CDEF:scaledupper=upper,8,*",
                            "CDEF:scaledlower=lower,8,*",
                            "CDEF:scaledpred=pred,8,*",
                        "TICK:fail#FDD017:1.0: Fallas",
                        "AREA:scaledobsAyer#9C9C9C:Ayer",
                        "LINE3:scaledobs#00FF00:In traffic",
                        "LINE1:scaledpred#FF00FF:Prediccion",
                        #"LINE1:outoctets#0000FF:Out traffic",
                        "LINE1:scaledupper#ff0000:Upper Bound Average bits in",
                        "LINE1:scaledlower#0000FF:Lower Bound Average bits in")

    if carga == 90 or carga == 100:
        notificacion("fname")
    
def menu():
    n = int(input("¿Qué tarea desea observar?"))

    if n == 1:
        tarea_1()
    elif n == 2:
        tarea_2()
    else:
        print("opción no valida")
        menu()

def main():
    menu()    

if __name__ == "__main__":
    main()
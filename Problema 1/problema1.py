#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getSNMP import *
import numpy as np #Librería numérica
import rrdtool
import matplotlib.pyplot as plt # Para crear gráficos con matplotlib
#%matplotlib inline # Si quieres hacer estos gráficos dentro de un jupyter notebook

from sklearn.linear_model import LinearRegression #Regresión Lineal con scikit-learn

comunidad = "grupo4CV5"
IP = "192.168.100.19"
gh = 4.2

def f(x):  # función f(x) = 0.1*x + 1.25 + 0.2*Ruido_Gaussiano
    np.random.seed(42) # para poder reproducirlo
    y = 0.1*x + 1.25 + 0.2*np.random.randn(x.shape[0])
    return y

def main():
    print("Tarea1")

    carga_array = []
    y = 0

    for i in range(0,20):
        carga = float(consultaSNMP(comunidad, IP, '1.3.6.1.4.1.2021.10.1.3.1'))
        carga = (carga*100)/gh   
        carga_array.append(carga) 

    x = np.array(carga_array)
    y = f(x)

    regresion_lineal = LinearRegression() 
    regresion_lineal.fit(x.reshape(-1,1), y) 
    w = regresion_lineal.coef_  
    b = regresion_lineal.intercept_
    print('w = ' + str(w) + ', b = ' + str(b))
    
    nuevo_x = np.array([90]) 
    prediccion = regresion_lineal.predict(nuevo_x.reshape(-1,1))
    print(prediccion)
    
    
    plt.scatter(x,y,label='data', color='blue')
    plt.title('Datos')
    plt.plot(nuevo_x,prediccion)
    plt.grid()
    plt.show()
    plt.savefig("gráfico.png")
    
        

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
#!/usr/bin/python

import time

def anos(ano):
    dias_anos = (ano)-1995
    dias_b = (ano)%4
    dias_anos = dias_anos*365
    dias_anos = dias_anos + dias_b
    return dias_anos

def actual_year(mes,ano):
    dias_actual = 0
    i_mes = 0
    for i_mes in range(0,mes):
        if i_mes == 1:
            dias_actual = dias_actual+31
        if i_mes == 2:
            if ano%4 == 0:
                dias_actual = dias_actual+29
            else:
                dias_actual = dias_actual+28

        if i_mes == 3:
            dias_actual = dias_actual+31
        if i_mes == 4:
            dias_actual = dias_actual+30
        if i_mes == 5:
            dias_actual = dias_actual+31
        if i_mes == 6:
            dias_actual = dias_actual+30
        if i_mes == 7:
            dias_actual = dias_actual+31
        if i_mes == 8:
            dias_actual = dias_actual+31
        if i_mes == 9:
            dias_actual = dias_actual+30
        if i_mes == 10:
            dias_actual = dias_actual+31
        if i_mes == 11:
            dias_actual = dias_actual+30
        if i_mes == 12:
            dias_actual = dias_actual+31
    return dias_actual

def edad():
    ano = time.strftime("%Y")
    mes = time.strftime("%m")
    suma = anos(int(ano)-1) + actual_year(int(mes)-1,ano) + 25
    resultado = suma%3
    print("El resultado es " , resultado)

if __name__ == "__main__":
    edad()
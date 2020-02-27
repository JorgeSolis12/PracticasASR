from getSNMP import *
prueba = consultaSNMP('grupo4cv5',"10.100.64.15", '1.3.6.1.2.1.4.9.0')
str_cut = prueba[24:]

print(prueba)
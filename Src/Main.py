# -*- coding: utf-8 -*-
# Eric Mendoza, carnet 15002
# Jonnathan Juarez, carnet 15377
# 23 de Agosto del 2016
# Descripcion: Simulacion de un sistema operativo
# utilizando Sympy
#
import sys
import simpy
import random


# objeto de S.O.

class SistemaOperativo:
    def __init__(self, env, memoria, capacidad, procesador,velocidad):
        self.procesador = simpy.Resource(env,capacidad)
        self.memoria = simpy.Container(env, memoria, memoria)
        self.velocida = velocidad

class Procesos:
    def __init__(self, memAsignada, id):
        self.tamanioProceso = random.randint(1,10)
        self.cantidadDeInstrucciones = random.randint(1,10)
        self.memoriaAsignada = memAsignada
        self.identificacion = id


    def ejecutar(self):
        print ("Proeso ejecutandose")
        print ("Esperando memoria para el proceso ")
        yield self.env.timeout(1)
        yield (self.memoria)  # Solicitar memoria ram
        yield self.env.timeout(1)
        print ("Proceso '{0}' memoria alocada en: {1} "
        yield self.env.timeout(2)


def main(argv):
    so = SistemaOperativo()
    env = simpy.Environment()

    env.run()


# Funcion main
if __name__ == "__main__":
    main(sys.argv)
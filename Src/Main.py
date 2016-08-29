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

#clasle prooceso
class Proceso:
#constructtor
    def __init__(self,env,identificador):
        self.identificador = identificador
        self.env = env
        self.cantDeMemoria = self.setCantDeMemoria()
        self.cantDeInstrucciones = self.setCantDeIntrucciones()
        self.instructionsCPU = 0
        self.Terminated = False
    def setCantDeMemoria(self):
        self.cantDeMemoria = random.randint(1,10)

    def setCantDeIntrucciones(self):
        self.cantDeInstrucciones = random.randint(1,10)
    #ejecucion del proceso
    def ejecutar(self,instrucARealizar):
        self.instructionsCPU = instrucARealizar
        self.cantDeInstrucciones = self.cantDeInstrucciones - self.instructionsCPU
        if self.cantDeInstrucciones <= 0:
            return 0
        return self.cantDeInstrucciones

    def setTerminated(self,estado):
        self.Terminated = estado
        if estado == True:
            print ("Proceso %s terminado" %self.identificador)

class Computadora:
    def __init__(self, env):
        self.procesarores = simpy.Resource(env, capacity=1)
        self.ram = simpy.Container(env, init=100, capacity=100)

class SitemaOperativo:
    def __init__(self, env, recursos, proceso):
        self.resources = recursos
        self.process = proceso












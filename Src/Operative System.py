# -*- coding: cp1252 -*-
import simpy
import random
import math


# Eric Mendoza, carnet 15002
# Jonnathan Juarez, carnet 15377
# 23 de Agosto del 2016
# Descripcion: Simulacion de un sistema operativo
# utilizando Sympy
#
# Data
CapacidadRAM = 100
NumeroDeCPU = 2
random.seed(24)  # Semilla
NumProcesos = 200  # Cantidad de procesos
Interval = 1  # Intervalo de creacion de procesos
InstruccionesPorCiclo = 3  # Cuantas instrucciones realiza el CPU por unidad de tiempo
TiempoOperacionInOut = 5  # Tiempo de operacion I/O
TiemposDeProcesos = []  # Lista para almacenar tiempos


class SistemaOperativo:
    """Es el ambiente del sistema operativo, crea la RAM y los CPU"""

    def __init__(self, env):
        self.RAM = simpy.Container(env, init=CapacidadRAM, capacity=CapacidadRAM)
        self.CPU = simpy.Resource(env, capacity=NumeroDeCPU)


class Proceso:
    """La clase Proceso modela el funcionamiento de un proceso en la computadora"""

    def __init__(self, id, no, env, sistema_operativo):
        # Atributos
        self.id = id
        self.no = no
        self.instrucciones = random.randint(1, 10)
        self.memoriaRequerida = random.randint(1, 10)
        self.env = env
        self.terminated = False
        self.sistema_operativo = sistema_operativo
        self.createdTime = 0
        self.finishedTime = 0
        self.totalTime = 0
        self.proceso = env.process(self.procesar(env, sistema_operativo))

    # Metodos
    def procesar(self, env, sistema_operativo):
        inicio = env.now
        self.createdTime = inicio
        print('%s: Creado en %d' % (self.id, inicio))  # El proceso se crea en ese momento
        with sistema_operativo.RAM.get(self.memoriaRequerida) as getRam:  # Obtener RAM dependiendo de la requerida
            yield getRam

            # Inicio uso de RAM
            print('%s: Obtiene RAM en %d (Estado: Wait)' % (self.id, env.now))
            siguiente = 0  # Variable para saber que hacer despues de 'running'
            while not self.terminated:
                with sistema_operativo.CPU.request() as req:  # Pedir CPU hasta terminar
                    print('%s: Espera al CPU en %d (Estado: Wait)' % (self.id, env.now))
                    yield req

                    # Inicio uso de CPU
                    print('%s: Obtiene CPU en %d (Estado: Running)' % (self.id, env.now))
                    for i in range(InstruccionesPorCiclo):  # Realizar operaciones por ciclo
                        if self.instrucciones > 0:
                            self.instrucciones -= 1  # Si aun hay instrucciones: Operar
                            siguiente = random.randint(1, 2)  # Para definir su siguiente paso
                    yield env.timeout(1)  # Se tarda una unidad de tiempo en realizar InstruccionesPorCiclo

                    # Inicio proceso I/O
                    if siguiente == 1:
                        print('%s: Espera operacion I/O en %d (Estado: I/O)' % (self.id, env.now))
                        yield env.timeout(TiempoOperacionInOut)

                    # Fin de uso de RAM (Salir de while)
                    if self.instrucciones == 0:
                        self.terminated = True  # Si ya no hay instrucciones: Terminar

            print('%s: Terminado en %d (Estado: Terminated)' % (self.id, env.now))
            sistema_operativo.RAM.put(self.memoriaRequerida)  # Liberar RAM
        fin = env.now
        self.finishedTime = fin  # Marcar fin
        self.totalTime = int(self.finishedTime - self.createdTime)  # Obtener tiempo en computadora
        TiemposDeProcesos.insert(self.no, self.totalTime)


# Generador de procesos
def proceso_generator(env, sistema_operativo):
    for i in range(NumProcesos):
        tiempo_creacion = random.expovariate(1.0/Interval)
        Proceso('Proceso %d' % i, i, env, sistema_operativo)
        yield env.timeout(tiempo_creacion)  # Tiempo que tardara en aparecer cada uno


# Main
class Main:
    """Esta clase se encarga de crear los objetos para la simulacion"""
    def __init__(self):
        env = simpy.Environment()  # Creaar ambiente
        sistema_operativo = SistemaOperativo(env)  # Crear sistema operativo (recursos)
        env.process(proceso_generator(env, sistema_operativo))  # Crear procesos
        env.run()

        # Calcular estadisticas de tiempo
        def promedio(s): return sum(s) * 1.0 / len(s)

        tiempo_promedio_total = promedio(TiemposDeProcesos)  # Obtener Promedio
        varianza_tiempo_total = map(lambda x: (x - tiempo_promedio_total) ** 2, TiemposDeProcesos)  # Obtener Varianza
        desvest_tiempo_total = math.sqrt(promedio(varianza_tiempo_total))  # Calcular la desviacion estandar

        print "El promedio de tiempo es de: ", tiempo_promedio_total, ", y su desviacion estandar es de: ", \
            desvest_tiempo_total


Main()  # Correr

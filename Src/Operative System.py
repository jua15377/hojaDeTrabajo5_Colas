# -*- coding: cp1252 -*-
import simpy
import random
import math

# Data
CapacidadRAM = 100
NumeroDeCPU = 10
random.seed(24)
NumProcesos = 25
Interval = 5
InstruccionesPorCiclo = 3
TiempoOperacionInOut = 5
TiemposDeProcesos = []


class SistemaOperativo:
    """Es el ambiente del sistema operativo"""

    def __init__(self, env):
        self.RAM = simpy.Container(env, init=CapacidadRAM, capacity=CapacidadRAM)
        self.CPU = simpy.Resource(env, capacity=NumeroDeCPU)


class Proceso:
    """La clase Proceso modela el funcionamiento de un proceso"""

    def __init__(self, id, no, env, cpu):
        self.id = id
        self.no = no
        self.instrucciones = random.randint(1, 10)
        self.memoriaRequerida = random.randint(1, 10)
        self.env = env
        self.terminated = False
        self.cpu = cpu
        self.createdTime = 0
        self.finishedTime = 0
        self.totalTime = 0
        self.proceso = env.process(self.procesar(env, cpu))

    def procesar(self, env, cpu):
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


def proceso_generator(env, sistema_operativo):
    for i in range(NumProcesos):
        tiempoCreacion = random.expovariate(1.0/Interval)
        Proceso('Proceso %d' % i, i, env, sistema_operativo)
        yield env.timeout(tiempoCreacion)  # Tiempo que tardara en aparecer cada uno


env = simpy.Environment()
sistema_operativo = SistemaOperativo(env)
pro_generator = env.process(proceso_generator(env, sistema_operativo))
env.run()


def promedio(s): return sum(s) * 1.0 / len(s)
tiempoPromedioTotal = promedio(TiemposDeProcesos)  # Obtener Promedio
varianzaTiempoTotal = map(lambda x: (x - tiempoPromedioTotal)**2, TiemposDeProcesos)  # Obtener Varianza
desVestTiempoTotal = math.sqrt(promedio(varianzaTiempoTotal))

print "El promedio de tiempo es de: ", tiempoPromedioTotal, ", y su desviacion estandar es de: ", desVestTiempoTotal

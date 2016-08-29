<<<<<<< HEAD
import random

=======
# -*- coding: utf-8 -*-
# Eric Mendoza, carnet 15002
# Jonnathan Juarez, carnet 15377
# 23 de Agosto del 2016
# Descripcion: Simulacion de un sistema operativo
# utilizando Sympy
#
import sys
import random
>>>>>>> a0259241135236b93b3d6c9308a860c0b26c7a9c
import simpy


RANDOM_SEED = 42
<<<<<<< HEAD
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))

# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
=======
RAM = 200     # liters
THRESHOLD = 10             # Threshold for calling the tank truck (in %)
RAM_PARA_PROCESO = [5, 25]  # Min/max levels of fuel tanks (in liters)
REFUELING_SPEED = 2        # liters / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
INTERVALO = 10        # Create a proceso every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds
CANT_PROCESOS = 25



def proceso(numero, env, procesador, ram_disponible):
    """A proceso arrives at the gas station for refueling.

    It requests one of the gas station's fuel pumps and tries to get the
    desired amount of gas from it. If the stations reservoir is
    depleted, the proceso has to wait for the tank truck to arrive.

    """
    ram_para_proceso = random.randint(*RAM_PARA_PROCESO)
    print('%s PRECESO EMPEZADO A T = %d' % (numero, env.now))
    with procesador.request() as req:
        start = env.now
        # pide el procesador
        yield req
        # obtine la memoria ram
        yield ram_disponible.get(ram_para_proceso)
        # el timepo de proceso toma 3 unidades de tiempo
        yield env.timeout(3)

        print('%s TERMINO DE EJECUTARSE, LE TOMO: %d UNIDADES DE TIEMPO' %(numero, env.now - start))

def procesador_control(env, ram_disponible):
    """Periodically check the level of the *ram_disponible* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if ram_disponible.level / ram_disponible.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(tank_truck(env, ram_disponible))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, ram_disponible):
    """Arrives at the gas station after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    ammount = ram_disponible.capacity - ram_disponible.level
    print('Tank truck refuelling %.1f liters.' % ammount)
    yield ram_disponible.put(ammount)


def proceso_generator(env, procesador, ram_disponible):
    """Generate new procesos that arrive at the gas station."""
    for i in range(CANT_PROCESOS):
        yield env.timeout(random.expovariate(1.0/INTERVALO))
        env.process(proceso('proceso %d' % i, env, procesador, ram_disponible))


# Setup and start the simulation
print('PROCESO EN UN SISTEMA OPERATIVO')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
procesador = simpy.Resource(env, 1)
ram_disponible = simpy.Container(env, RAM, init=RAM)
env.process(procesador_control(env, ram_disponible))
env.process(proceso_generator(env, procesador, ram_disponible))

# Execute!
env.run(SIM_TIME)








>>>>>>> a0259241135236b93b3d6c9308a860c0b26c7a9c

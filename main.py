import threading
import random
import time
from collections import deque

from classes.airship import Airship

total_airships = 1; # Controla o numero total de naves, não deixando passar de 18
total_airships_land = 0; # numero tatal que de naves que ja apareceu no aeroporto, não ira passar de 9
total_airships_air = 0; # numero total de naves que ja apareceu no ar, não ira passar de 9

track = threading.Semaphore(1) # semaforo para controlar as naves na pista, limitando para apenas 1.
spawn_lock = threading.Semaphore(1) # semaforo limitando no nascimento de naves.
prioridade = 0 # variavel para aumentar ou diminuir prioridade de ações. diminuindo a chance de uma
# mesma ação(pouso/decolagem) acontecer em sequencia, a não ser que não va atrapalhar o resto das naves

airships_on_land = deque([]); # fila das naves em terra
airships_on_air = deque([]); # fila das naves voando
locals = ["ar", "aeroporto"]; # locais possiveis para nascimento das naves

def create_airship():
    global total_airships
    global total_airships_land
    global total_airships_air
    global airships_on_land
    global airships_on_air
    if spawn_lock._value == 1:
        spawn_lock.acquire()
        time.sleep(8)
        spawn_location = random.choice(locals)
        if spawn_location == "ar" and total_airships <= 18 and total_airships_air <= 9:
            airship = Airship(total_airships, spawn_location)
            airships_on_air.append(airship)
            total_airships_air += 1
            print(f'novo aviao {total_airships} spawnou no {spawn_location}!!,+ total de aviões no ar/aeroporto {len(airships_on_air)}/{len(airships_on_land)} time : {time.perf_counter()}\n')
            total_airships += 1
            spawn_lock.release()
        elif spawn_location == "aeroporto" and len(airships_on_land) < 3 and total_airships <= 18 and total_airships_land <= 9:
            airship = Airship(total_airships, spawn_location)
            airships_on_land.append(airship)
            total_airships_land += 1
            print(f'novo aviao {total_airships} spawnou no {spawn_location}!!, total de aviões no ar/aeroporto {len(airships_on_air)}/{len(airships_on_land)} time : {time.perf_counter()}\n')
            total_airships += 1
            spawn_lock.release()
        else:
            spawn_lock.release()

def landing():
    global prioridade
    if track._value == 1 and len(airships_on_air) > 0:
        track.acquire()
        x = airships_on_air.popleft()
        prioridade-=1
        print(f'O avião {x.id} está pousando...\n')
        landing_time = time.perf_counter()
        time.sleep(10)
        print(f'O avião {x.id} pousou com sucesso ! tempo total no ar : {landing_time - x.spawn_time}\n')
        track.release()


def take_off():
    global prioridade
    if track._value == 1 and len(airships_on_land) > 0:
        track.acquire()
        x = airships_on_land.popleft()
        prioridade+=1
        print(f'O avião {x.id} está preparando para decolar...\n')
        time.sleep(10)
        print(f'O avião {x.id} decolou com sucesso !\n')
        track.release()


while(True):
    if total_airships <= 18:
        AIRSHIP_SPAWN = threading.Thread(target=create_airship)
        AIRSHIP_SPAWN.start()

    if len(airships_on_air) > 0:
        combustivel = time.perf_counter() - airships_on_air[0].spawn_time

    if len(airships_on_land) > 1 and prioridade <= 1 and combustivel<15:
        TAKE_OFF = threading.Thread(target=take_off)
        TAKE_OFF.start()
    elif len(airships_on_air) == 0 and len(airships_on_land) > 0:
        TAKE_OFF = threading.Thread(target=take_off)
        TAKE_OFF.start()
    else:
        LANDING = threading.Thread(target=landing)
        LANDING.start()

    if total_airships >= 18 and len(airships_on_air) == 0 and len(airships_on_land) == 0 and track._value == 1 and spawn_lock._value == 1:
        print("fim do programa! se chegamos aqui, tudo ocorreu bem...")
        break;





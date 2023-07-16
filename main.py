import threading
from lcu_driver import Connector
import json
import tkinter as tk
from queue import Queue
import client

isARAM = False
wasChampSelect = False

client = client.Client()

connector = Connector()
@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')
    player = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if player.status != 200:
        print("player id err")
        return
    res = json.loads(await player.read())

    client.setSummonerId(res['summonerId'])
    print(f'Missing data from {len(client.getChampIds())-len(client.getChampData())} champions due to wiki inaccuracies')
    q.put(res['summonerId'])

@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def aramCheck(connection, event):
    await champSelect(connection)

async def champSelect(connection):
    lobby = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
    if lobby.status != 200:
        print("Err: /lol-gameflow/v1/gameflow-phase")
        return
    res = json.loads(await lobby.read())
    print(res)
    global isARAM
    global wasChampSelect
    if res == 'ChampSelect':
        gamemode = await connection.request('get', '/lol-gameflow/v1/session')
        if gamemode.status != 200:
            print("Err: /lol-gameflow/v1/session")
            return
        res = json.loads(await gamemode.read())
        if res['map']['gameMode'] == 'ARAM':
            isARAM = True
        isARAM = True #TODO REMOVE FOP PROD
        wasChampSelect = True
    else:
        if wasChampSelect:
            q.put("stop")
            wasChampSelect = False
        client.setSummonerIdx(-1)
        client.setCurrentChamp(-1)
        isARAM = False
        
@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def characterInfo(connection, event):
    if not isARAM:
        return
    await sessionInfo(connection)

async def sessionInfo(connection):
    if len(threads) < 2:
        g = threading.Thread(target=gui)
        threads.append(g)
        g.start()

    session = await connection.request('get', '/lol-champ-select/v1/session')
    if session.status != 200:
        print("Err: /lol-champ-select/v1/session")
        print(session.status)
        return
    res = json.loads(await session.read())
    team = res['myTeam']

    if client.getSummonerIdx() < 0:
        for idx, p in enumerate(team):
            if p['summonerId'] == client.getSummonerId():
                client.setSummonerIdx(idx)
    player = team[client.getSummonerIdx()]

    if player['championId'] == 0:
        return
    if client.getCurrentChamp() != player['championId']:
        client.setCurrentChamp(player['championId'])
        champName = client.getChampIds()[client.getCurrentChamp()].lower()
        try:
            data = client.getChampData()[champName]
            print(data)
            q.put(data)
        except:
            q.put("Perfectly balanced or missing from wiki lol")
            # print("Perfectly balanced or missing from wiki lol")





def driver():
    print("driver thread starting")
    connector.start()

def gui():
    window = tk.Tk()
    nameLabel = tk.Label(text="Name: ")
    nameData = tk.Label(text="")
    dealtLabel = tk.Label(text="Damage Dealt: ")
    dealtData = tk.Label(text="")
    receivedLabel = tk.Label(text="Damage Taken: ")
    receivedData = tk.Label(text="")
    effectsLabel = tk.Label(text="Other Effects: ")
    effectsData = tk.Label(text="")
    
    nameLabel.grid(row = 0, column = 0)
    nameData.grid(row = 0, column = 1)
    dealtLabel.grid(row = 1, column = 0)
    dealtData.grid(row = 1, column = 1)
    receivedLabel.grid(row = 2, column = 0)
    receivedData.grid(row = 2, column = 1)
    effectsLabel.grid(row = 3, column = 0)
    effectsData.grid(row = 4, column = 1)

    print("gui thread starting")

    def check_queue():
        try:
            res = q.get(0)
            print(res)
            if res == "stop":
                stop_gui()
            if isinstance(res, str):
                nameData.config(text="")
                dealtData.config(text = "")
                receivedData.config(text="")
                effectsData.config(text=res)
            else:
                nameData.config(text=res['name'])
                dealtData.config(text = res['damageDealt'])
                receivedData.config(text=res['damageReceived'])
                effectsData.config(text=res['otherEffects'])
        except:
            print("queue empty")
        finally:
            window.after(100, check_queue)

    def stop_gui():
        window.destroy()
        t = threads.pop()
        t.join()

    check_queue()
    window.mainloop()



threads = list()
q = Queue()

d = threading.Thread(target=driver)
threads.append(d)
d.start()

# g = threading.Thread(target=gui)
# threads.append(g)
# g.start()

for idx, thread in enumerate(threads):
    print("joining thread ", idx)
    thread.join()


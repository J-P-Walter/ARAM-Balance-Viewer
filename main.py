import threading
from lcu_driver import Connector
import json
import tkinter as tk
from queue import Queue
import client
import logging

isARAM = False
wasChampSelect = False

logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s %(message)s')

client = client.Client()

#Fires when the connection is established, ie. the client is open
#Gets the player's unique id to be used as an index later
connector = Connector()
@connector.ready
async def connect(connection):
    print("LCU API is ready to be used.")
    player = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if player.status != 200:
        logging.error(player)
        return
    res = json.loads(await player.read())

    client.setSummonerId(res['summonerId'])
    q.put(res['summonerId'])

#Fires during changes of state in the client
#Ex. None, Lobby, ChampSelect, etc.
#Only interested in ChampSelect and if the gamemode is ARAM
@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def aramCheck(connection, event):
    await champSelect(connection)

async def champSelect(connection):
    lobby = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
    if lobby.status != 200:
        logging.WARNING(lobby)
        return
    res = json.loads(await lobby.read())
    global isARAM
    global wasChampSelect
    if res == 'ChampSelect':
        gamemode = await connection.request('get', '/lol-gameflow/v1/session')
        if gamemode.status != 200:
            logging.error(gamemode)
            return
        res = json.loads(await gamemode.read())
        if res['map']['gameMode'] == 'ARAM':
            isARAM = True
        # isARAM = True #TODO REMOVE FOR PROD
        wasChampSelect = True
    else:
        #takes care of someone dodging as well as game going through
        #to add the stop command to the queue
        if wasChampSelect:
            q.put("stop")
            wasChampSelect = False
        client.setSummonerIdx(-1) #Resets variables in client
        client.setCurrentChamp(-1)
        isARAM = False

#Fires when isARAM is true
#Adds gui in its own thread, making sure to not add multiple
#Gets the current champ using data from the client
#Adds the data to the queue used by the threads
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
        logging.ERROR(session)
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
            q.put(data)
        except:
            q.put("Perfectly balanced or missing from wiki lol")

#Start the driver
def driver():
    print("Driver thread starting")
    connector.start()

#Start the gui
def gui():
    window = tk.Tk()

    window.geometry("200x350")

    nameLabel = tk.Label(text="Name: ")
    nameData = tk.Label(text="")
    dealtLabel = tk.Label(text="Damage Dealt: ")
    dealtData = tk.Label(text="")
    receivedLabel = tk.Label(text="Damage Taken: ")
    receivedData = tk.Label(text="")
    effectsLabel = tk.Label(text="Other Effects: ")
    effectsData = tk.Label(text="", wraplength=100, justify='center')
    
    nameLabel.grid(row = 0, column = 0)
    nameData.grid(row = 0, column = 1)
    dealtLabel.grid(row = 1, column = 0)
    dealtData.grid(row = 1, column = 1)
    receivedLabel.grid(row = 2, column = 0)
    receivedData.grid(row = 2, column = 1)
    effectsLabel.grid(row = 3, column = 0)
    effectsData.grid(row = 3, column = 1)

    print("Gui thread starting")

    #Checks the queue for data
    #Updates accordingly
    #Currently checks every 100ms which seems to be a reasonable amount
    def check_queue():
        try:
            res = q.get(0)
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
            pass
        finally:
            window.after(100, check_queue)

    def stop_gui():
        print("gui thread stopping")
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

for idx, thread in enumerate(threads):
    print("joining thread ", idx)
    thread.join()


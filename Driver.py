from lcu_driver import Connector
import json
import Client

isARAM = False

connector = Connector()
client = Client.Client()

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

    zoom = await connection.request('get', '/riotclient/zoom-scale')
    res = json.loads(await zoom.read())
    print("zoom", res)

@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def aramCheck(connection, event):
    await champSelect(connection)

async def champSelect(connection):
    lobby = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
    if lobby.status != 200:
        print("Err: /lol-gameflow/v1/gameflow-phase")
        return
    res = json.loads(await lobby.read())
    global isARAM
    print(res)
    if res != 'ChampSelect':
        client.setSummonerIdx(-1)
        client.setCurrentChamp(-1)
        global isARAM
        isARAM = True #TODO CHANGE FOR PROD
    else:
        gamemode = await connection.request('get', '/lol-gameflow/v1/session')
        if gamemode.status != 200:
            print("Err: /lol-gameflow/v1/session")
            return
        res = json.loads(await gamemode.read())
        if res['map']['gameMode'] == 'ARAM':
            isARAM = True
        

@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def characterInfo(connection, event):
    if not isARAM:
        return
    await sessionInfo(connection)

async def sessionInfo(connection):
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
        except:
            print("Perfectly balanced or missing from wiki lol")

def main():
    connector.start()

from lcu_driver import Connector
import json
import client

class Driver():
    isAram = False
    connector = Connector()

    def __init__():
        client = client.Client()

    @connector.ready
    async def connect(connection):
        print('LCU API is ready to be used.')
        player = await connection.request('get', '/lol-summoner/v1/current-summoner')
        if player.status != 200:
            print("player id err")
            return
        res = json.loads(await player.read())

        client.setSummonerId(res['summonerId'])
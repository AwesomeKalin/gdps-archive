import asyncio
import gd
import internetarchive
from os.path import expanduser

async def main(client):
    levelId: int = 7

    print('Starting archive from id ' + str(levelId))

    while(levelId != 0):
        await archive(levelId, client)
        levelId += 1

async def archive(level, client):
    item: internetarchive.Item = internetarchive.get_item('gdps-2.2-level-' + str(level))
    if item.exists:
        return False
    
    print('Archiving Level ' + str(level))
    try:
        lvl = await client.get_level(level_id=level)
        file = open(expanduser("~") + '/.gdpsarchive/' + str(level) + '.gd', "w")
        file.write(lvl.unprocessed_data)
    except:
        print('Level does not exist')
    
client = gd.Client()

with client.http.change(url='http://game.gdpseditor.com/server'):
    asyncio.run(main(client))
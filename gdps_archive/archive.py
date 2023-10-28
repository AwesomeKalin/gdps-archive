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
        print('Downloaded Level, starting archive')
        print(lvl.song.download_url)
        internetarchive.upload('gdps-2.2-level-' + str(level), expanduser("~") + '/.gdpsarchive/' + str(level) + '.gd', metadata={'creator': lvl.creator, 'scanner': 'GDPS Editor 2.2 Archiver', 'title': lvl.name, 'subject': 'gdps;geometry dash;2.2;gdps editor 2.2;gdps editor;level', 'description': lvl.description, 'stars': lvl.stars, 'publicdate': lvl.created_at, 'difficulty': lvl.difficulty, 'song': lvl.song.id})
    except:
        print('Level does not exist')
    
client = gd.Client()

with client.http.change(url='http://game.gdpseditor.com/server'):
    asyncio.run(main(client))
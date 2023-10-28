import asyncio
import gd
import internetarchive
from os.path import expanduser
from os import remove
import urllib.request

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
        internetarchive.upload('gdps-2.2-level-' + str(level), expanduser("~") + '/.gdpsarchive/' + str(level) + '.gd', metadata={'creator': lvl.creator.name, 'scanner': 'GDPS Editor 2.2 Archiver', 'title': lvl.name, 'subject': 'gdps;geometry dash;2.2;gdps editor 2.2;gdps editor;level', 'description': lvl.description, 'stars': str(lvl.stars), 'difficulty': str(lvl.difficulty.value), 'song': str(lvl.song.id)})
        print('Level ID ' + level + ' is archived!')
        remove(str(level), expanduser("~") + '/.gdpsarchive/' + str(level) + '.gd')

        item: internetarchive.Item = internetarchive.get_item('gdps-2.2-song-' + str(lvl.song.id))

        if lvl.song.download_url != None or 'newgrounds' in lvl.song.download_url or item.exists:
            return True
        
        print('Archiving Song ID ' + str(lvl.song.id))
        urllib.request.urlretrieve(lvl.song.download_url, expanduser("~") + '/.gdpsarchive/' + str(lvl.song.id) + '.mp3')
        print('Downloaded Song, Archiving')
        internetarchive.upload('gdps-2.2-song-' + str(lvl.song.id), expanduser("~") + '/.gdpsarchive/' + str(lvl.song.id) + '.mp3', metadata={'creator': lvl.song.artist, 'scanner': 'GDPS Editor 2.2 Archiver', 'title': lvl.song.name, 'subject': 'gdps;geometry dash;2.2;gdps editor 2.2;gdps editor;song', 'description': 'A song archive from the GDPS Editor 2.2 Reupload System. Originally archived for Level ID ' + level})
        print('Archiving successful!')

    except:
        print('Level does not exist or achiving failed')
    
client = gd.Client()

with client.http.change(url='http://game.gdpseditor.com/server'):
    asyncio.run(main(client))
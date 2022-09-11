import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    matches = ['play/', 'play_movie/', 'play_gogo/']

    if any(x in path for x in matches):
        path = f'{path}?source_select=true'

    xbmc.executebuiltin(f'PlayMedia({path})')

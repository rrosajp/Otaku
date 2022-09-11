# -*- coding: utf-8 -*-

from resources.lib.ui import control
from resources.lib.windows.base_window import BaseWindow
from resources.lib.WatchlistFlavor import WatchlistFlavor


class SourceSelect(BaseWindow):

    def __init__(self, xml_file, location, actionArgs=None, sources=None, anilist_id=None, rescrape=None, **kwargs):
        super(SourceSelect, self).__init__(xml_file, location, actionArgs=actionArgs)
        self.actionArgs = actionArgs
        self.sources = sources
        self.anilist_id = anilist_id
        self.rescrape = rescrape
        self.position = -1
        self.canceled = False
        self.anime_list_entry = {}
        self.editor_list = None
        self.flavors_list = None
        self.anime_item = None
        self.last_action = 0
        control.closeBusyDialog()

    def onInit(self):
        self.editor_list = self.getControl(2001)
        self.flavors_list = self.getControl(2000)

        if control.anilist_enabled():
            menu_item = control.menuItem(label='AniList')
            menu_item.setProperty('username', control.getSetting('anilist.username'))
            self.flavors_list.addItem(menu_item)

            self.anime_list_entry['anilist'] = WatchlistFlavor.watchlist_anime_entry_request('anilist', '235')

        if control.kitsu_enabled():
            menu_item = control.menuItem(label='Kitsu')
            menu_item.setProperty('username', control.getSetting('kitsu.username'))
            self.flavors_list.addItem(menu_item)

            self.anime_list_entry['kitsu'] = WatchlistFlavor.watchlist_anime_entry_request('kitsu', '235')

        if control.myanimelist_enabled():
            menu_item = control.menuItem(label='MyAnimeList')
            menu_item.setProperty('username', control.getSetting('mal.username'))
            self.flavors_list.addItem(menu_item)

            self.anime_list_entry['myanimelist'] = WatchlistFlavor.watchlist_anime_entry_request('mal', '235')

        selected_flavor_item = self.flavors_list.getSelectedItem()
        self.selected_flavor = (selected_flavor_item.getLabel()).lower()
        for _id, value in list(self.anime_list_entry[self.selected_flavor].items()):
            item = control.menuItem(label=f'{_id}')
            item.setProperty(_id, str(value))
            self.editor_list.addItem(item)

        self.setFocusId(2000)

    def doModal(self):
        super(SourceSelect, self).doModal()
        self.clearProperties()
        return

    def flip_flavor(self):
        self.editor_list.reset()
        selected_flavor_item = self.flavors_list.getSelectedItem()
        self.selected_flavor = (selected_flavor_item.getLabel()).lower()
        for _id, value in list(self.anime_list_entry[self.selected_flavor].items()):
            item = control.menuItem(label=f'{_id}')
            item.setProperty(_id, str(value))
            self.editor_list.addItem(item)

    def edit_anime(self):
        self.anime_item = self.editor_list.getSelectedItem()
        status = self.anime_item.getProperty('status')
        eps_watched = self.anime_item.getProperty('eps_watched')
        score = self.anime_item.getProperty('score')

        if status:
            self.flip_status(status)

        if eps_watched:
            self.edit_eps_watched()

        if score:
            self.flip_score(score)

    def flip_status(self, status):
        status_dict = {
            'anilist': {
                'Planning': 'Current',
                'Current': 'Completed',
                'Completed': 'Rewatching',
                'Rewatching': 'Paused',
                'Paused': 'Dropped',
                'Dropped': 'Planning'
            },
            'myanimelist': {
                'Plan_To_Watch': 'Watching',
                'Watching': 'Completed',
                'Completed': 'On_Hold',
                'On_Hold': 'Dropped',
                'Dropped': 'Plan_To_Watch'
            }
        }

        # if status == 'Plan to Watch':
        #     new_status = 'Watching'

        # if status == 'Watching':
        #     new_status = 'Completed'

        # if status == 'Completed':
        #     new_status = 'On-Hold'

        # if status =='On-Hold':
        #     new_status = 'Dropped'

        # if status == 'Dropped':
        #     new_status = 'Plan to Watch'

        try:
            new_status = status_dict[self.selected_flavor][status]
            self.anime_item.setProperty('status', new_status)
        except:
            pass

    def edit_eps_watched(self):
        episodes_watched = control.showDialog.numeric(0, 'Enter episodes watched')
        if not episodes_watched:
            episodes_watched = '0'
        self.anime_item.setProperty('eps_watched', str(episodes_watched))

    def flip_score(self, score):

        new_score = '1'

        if score != 'null' and 1 <= int(score) < 10:
            new_score = int(score) + 1

        if score == '10':
            new_score = '0'

        self.anime_item.setProperty('score', new_score)

    def onClick(self, controlId):

        self.handle_action(7)

    def handle_action(self, action):

        focus_id = self.getFocusId()

        if action in [4, 3, 7] and focus_id == 2000:
            # UP/ DOWN
            self.flip_flavor()

        if action in [92, 10]:
            # BACKSPACE / ESCAPE
            self.close()

        if action == 7 and focus_id == 2001:
            self.edit_anime()

    def onAction(self, action):
        action = action.getId()

        if action == 7:
            return

        self.handle_action(action)

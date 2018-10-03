#!/usr/bin/python3
import glob
import os
from datetime import datetime
import pprint
import curses
from curses.textpad import rectangle
import re
import threading
import time

fileList = {}


class Object:
    def __init__(self):
        self.objectList = ['files', 'search', 'confBox']
        self.active = 0
        self.searchString = ''

    def setActiveNext(self):
        if self.active != 2:
            self.active = (self.active + 1) % (len(self.objectList) - 1)

    def setActiveObject(self, p_search, p_files, p_confBox):
        if self.objectList[self.active] == 'files':
            p_confBox.setInactive()
            p_search.setInactive()
            p_files.setActive()
        elif self.objectList[self.active] == 'search':
            p_confBox.setInactive()
            p_files.setInactive()
            p_search.setActive()
        else:
            p_confBox.setActive()
            p_files.setInactive()
            p_search.setInactive()

    def getActive(self):
        return self.objectList[self.active]

    def processButton(self, p_buttonPressed, p_stdscr, p_fileFilst, p_confBox):
        if p_buttonPressed == ord('\t'): self.setActiveNext()
        if p_buttonPressed == 10 and self.active == 0:
            self.active = 2
        elif p_buttonPressed == 10 and self.active == 2:
            if p_confBox.selectedButton == 1:
                self.active = 0
            else:
                p_confBox.drawRunning(p_stdscr, p_fileFilst);


class fileList():
    def __init__(self, p_position, p_logDirectory):
        self.x, self.y = p_position
        t_fileList = glob.glob(p_logDirectory)
        self.fileList = {}
        self.is_active = True
        self.selectedItem = 0
        t_iterator = 0
        for t_file in t_fileList:
            self.fileList[t_iterator] = {'fileName': os.path.basename(t_file),
                                         'createTime': datetime.fromtimestamp(os.path.getmtime(t_file)).strftime(
                                             '%Y%m%d%H%M%S'),
                                         'isMarked': False,
                                         'isVisible': True,
                                         'command': 'sleep 3',
                                         'currentStatus': 'unknown',
                                         'commandStatus': 'none'}
            t_iterator += 1

    def setActive(self):
        self.is_active = True

    def setInactive(self):
        self.is_active = False

    def setCommandStatus(self, p_status, p_i):
        self.fileList[p_i].update({'commandStatus': p_status})

    def getSelectedCount(self):
        t_count = 0
        for i in range(len(self.fileList)):
            if self.fileList[i]['isMarked']: t_count += 1
        return t_count

    def draw(self, p_stdscr):
        t_pos = 0
        for i in range(len(self.fileList)):
            if self.fileList[i]['isVisible']:
                t_markString = "[X] " if self.fileList[i]['isMarked'] else "[ ] "
                t_selectColor = curses.color_pair(
                    2) if i == self.selectedItem and self.is_active else curses.color_pair(1)
                p_stdscr.addstr(self.y + t_pos, self.x, "{} {} ".format(t_markString, self.fileList[i]['fileName']),
                                t_selectColor)
                t_pos += 1

    def processButton(self, p_buttonPressed):
        if self.is_active:
            if p_buttonPressed == curses.KEY_DOWN:
                t_currentPos = self.selectedItem
                while True:
                    t_currentPos += 1
                    if t_currentPos >= len(self.fileList) or self.fileList[t_currentPos]['isVisible']: break
                if t_currentPos < len(self.fileList): self.selectedItem = t_currentPos

            elif p_buttonPressed == curses.KEY_UP:
                t_currentPos = self.selectedItem
                while True:
                    t_currentPos -= 1
                    if t_currentPos < 0 or self.fileList[t_currentPos]['isVisible']: break
                if t_currentPos >= 0: self.selectedItem = t_currentPos
            if p_buttonPressed == ord(' '):
                self.fileList[self.selectedItem]['isMarked'] = True if self.fileList[self.selectedItem][
                                                                           'isMarked'] == False else False

    def setVisible(self, o_searchString):
        for i in range(len(self.fileList)):
            if re.search(r'(?i)' + o_searchString, self.fileList[i]['fileName']) or not len(o_searchString):
                self.fileList[i]['isVisible'] = True
            else:
                self.fileList[i]['isVisible'] = False


class searchField():
    def __init__(self, p_position):
        self.x, self.y = p_position
        self.is_activ = False
        self.searchString = ''

    def setActive(self):
        self.is_active = True

    def setInactive(self):
        self.is_active = False

    def draw(self, p_stdscr):
        t_selectColor = curses.color_pair(2) if self.is_active else curses.color_pair(1)
        p_stdscr.addstr(self.y, self.x, "Search: ", t_selectColor)
        p_stdscr.addstr(self.searchString, curses.color_pair(1))

    def processButton(self, p_buttonPressed):
        if self.is_active:
            if ((p_buttonPressed >= 97 and p_buttonPressed <= 122) or (
                    p_buttonPressed >= 48 and p_buttonPressed <= 57)): self.searchString += chr(p_buttonPressed)
            if p_buttonPressed == 263: self.searchString = self.searchString[:-1]


class confirmationBox():
    def __init__(self, p_position):
        self.x, self.y = p_position
        self.selectedButton = 1
        self.is_active = False

    def setActive(self):
        self.is_active = True
        self.firstActivation = True

    def setInactive(self):
        self.is_active = False

    def processButtion(self, p_buttonPressed, p_objectList):
        if self.is_active:
            if p_buttonPressed == ord('\t') or p_buttonPressed == 260 or p_buttonPressed == 261:
                self.selectedButton = (self.selectedButton + 1) % 2

    def draw(self, p_stdscr, p_fileList):
        if self.is_active:
            t_selCount = p_fileList.getSelectedCount()
            t_pos = 0
            self.win = curses.newwin(3 + t_selCount, 25, self.y + 1, self.x + 1)
            rectangle(p_stdscr, self.y, self.x, self.y + 4 + t_selCount, self.x + 31)
            for i in range(len(p_fileList.fileList)):
                if p_fileList.fileList[i]['isMarked']:
                    self.win.addstr(1 + t_pos, 1, p_fileList.fileList[i]['fileName'])
                    self.win.addstr(1 + t_pos, 15, 'PENDING', curses.color_pair(3))
                    t_pos += 1
            self.win.addstr(1 + t_selCount, 1, ' YES ', curses.color_pair(2 - self.selectedButton))
            self.win.addstr(1 + t_selCount, 8, ' NO ', curses.color_pair(self.selectedButton + 1))

    def drawRunning(self, p_stdscr, p_fileList):
        if self.is_active:
            t_selCount = p_fileList.getSelectedCount()
            t_toProcess = t_selCount
            t_pos = 0
            t_threads = []
            self.win = curses.newwin(3 + t_selCount, 25, self.y + 1, self.x + 1)
            rectangle(p_stdscr, self.y, self.x, self.y + 4 + t_selCount, self.x + 31)
            for i in range(len(p_fileList.fileList)):
                if p_fileList.fileList[i]['isMarked']:
                    t = threading.Thread(target=worker, args=(p_fileList, i))
                    t_threads.append(t)
                    t.start()

            while t_toProcess > 0:
                t_pos = 0
                for i in range(len(p_fileList.fileList)):
                    if p_fileList.fileList[i]['isMarked']:
                        self.win.addstr(1 + t_pos, 1, p_fileList.fileList[i]['fileName'])
                        if p_fileList.fileList[i]['commandStatus'] == 'RUNNING':
                            self.win.addstr(1 + t_pos, 15, 'RUNNING       ', curses.color_pair(6))
                        elif p_fileList.fileList[i]['commandStatus'] == 'SUCCESS (warn)':
                            self.win.addstr(1 + t_pos, 15, 'SUCCESS (warn)', curses.color_pair(3))
                        elif p_fileList.fileList[i]['commandStatus'] == 'ERROR':
                            self.win.addstr(1 + t_pos, 15, 'ERROR         ', curses.color_pair(4))
                        elif p_fileList.fileList[i]['commandStatus'] == 'SUCCESS':
                            self.win.addstr(1 + t_pos, 15, 'SUCCESS       ', curses.color_pair(5))
                        t_pos += 1
                t_toProcess - 1
                self.win.refresh()
                time.sleep(1)

    def refresh(self):
        if self.is_active:
            self.win.refresh()


def worker(p_fileList, p_i):
    p_fileList.setCommandStatus('RUNNING', p_i)
    time.sleep(p_i)
    p_fileList.setCommandStatus('ERROR', p_i)


def drawWorkArea(stdscr):
    l_buttonPressed = 0
    l_selectedItem = 0
    l_currentSearchString = ''

    o_files = fileList([4, 4], 'log/PZG*')
    o_search = searchField([2, 2])
    o_confBox = confirmationBox([6, 6])
    o_objectList = Object()

    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        if (l_buttonPressed == ord('q')): break  # and o_objectList.getActive() != 'search'): break
        stdscr.clear()

        o_objectList.processButton(l_buttonPressed, stdscr, o_files, o_confBox)
        o_objectList.setActiveObject(o_search, o_files, o_confBox)
        o_search.processButton(l_buttonPressed)
        o_files.processButton(l_buttonPressed)
        o_confBox.processButtion(l_buttonPressed, o_objectList)
        o_files.setVisible(o_search.searchString)
        o_search.draw(stdscr)
        o_files.draw(stdscr)
        o_confBox.draw(stdscr, o_files)

        # begin_x = 40; begin_y =39
        # height = 5; width = 40
        # win = curses.newwin(height, width, begin_y, begin_x)
        # rectangle(stdscr, 0,0, begin_y+2, begin_x+2)
        # win.addstr("test")

        debug = "button: {}, Active: {}, Search: {} , tmp: {}".format(l_buttonPressed, o_objectList.getActive(),
                                                                      o_objectList.searchString, o_confBox.is_active)
        stdscr.addstr(0, 0, debug, curses.color_pair(2))
        stdscr.refresh()
        o_confBox.refresh()
        l_buttonPressed = stdscr.getch()


def main():
    curses.wrapper(drawWorkArea)


if __name__ == "__main__":
    main()

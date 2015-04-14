#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

from widgets import Canvas


class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.maximize()
        self.set_title('Aprende python!')

        self.box = Canvas()
        self.add(self.box)

        self.connect('destroy', Gtk.main_quit)

        self.show_all()


if __name__ == '__main__':
    Window()
    Gtk.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject
from gi.repository import GdkPixbuf

_file = open(os.path.join(os.path.dirname(__file__), 'data/data.json'))
DATA = json.load(_file)
_file.close()


class LateralPanel(Gtk.VBox):

    __gsignals__ = {
        'show-file': (GObject.SIGNAL_RUN_FIRST, None, [str, str]),
    }

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.set_size_request(100, -1)

        self.titles = {}

        self.entry = Gtk.SearchEntry()
        self.pack_start(self.entry, False, False, 5)

        scrolled = Gtk.ScrolledWindow()
        self.listbox = Gtk.ListBox()
        self.listbox.connect('row-selected', self.row_selected)
        scrolled.add(self.listbox)
        self.pack_start(scrolled, True, True, 0)

        self.make_titles()
        self.show_all()

    def row_selected(self, listbox, row):
        if not row:
            return

        if not row.path:
            return

        self.emit('show-file', row.name, row.path)

    def make_row(self, name, path, bold=False):
        row = Gtk.ListBoxRow()
        row.name = name
        row.path = os.path.join(os.path.dirname(__file__), 'data', path) if path else None
        hbox = Gtk.HBox()
        label = Gtk.Label()
        text = ('<b>%s</b>' % name) if bold else '     ' + name
        label.set_markup(text)

        self.titles[name] = path

        hbox.pack_start(label, False, False, 0)
        row.add(hbox)
        self.listbox.add(row)

    def make_titles(self):
        titles = DATA['Orden']
        for title in titles:
            if type(DATA[title]) == str:
                self.make_row(title, DATA[title], bold=True)

            elif type(DATA[title]) == dict:
                _dict = DATA[title]
                subtitles = _dict['Orden']
                self.make_row(title, None, bold=True)
                for subtitle in subtitles:
                    self.make_row(subtitle, _dict[subtitle])


class Viewer(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.box = Gtk.VBox()
        self.box.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65535, 65535, 65535))
        self.add(self.box)
        self.show_all()

    def set_data(self, name, path):
        while self.box.get_children():
            self.box.remove(self.box.get_children()[0])

        label_title = Gtk.Label(name)
        label_title.set_selectable(True)
        label_title.modify_font(Pango.FontDescription('Bold 25'))
        self.box.pack_start(label_title, False, False, 20)

        text = open(path).read()
        #text = text.replace('SUBTITLE', 'SPLITSUBTITLE')
        #text = text.replace('CODE', 'SPLITCODE')
        #lines = text.split('SPLIT')
        lines = text.splitlines()

        view = Gtk.TextView()
        view.set_wrap_mode(Gtk.WrapMode.WORD)
        view.set_editable(False)
        view.set_cursor_visible(False)
        view.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65535, 65535, 65535))
        view.modify_bg(Gtk.StateType.SELECTED, Gdk.Color(6682, 32896, 46774))

        buffer = view.get_buffer()
        buffer.create_tag('code', background='#121B21', foreground='#B8D0E0', font='15')
        buffer.create_tag('subtitle', font='Bold 20')
        buffer.create_tag('default', font='15')

        for line in lines:
            iter = buffer.get_end_iter()
            line = line.strip()
            if line.startswith('CODE'):
                line = line[4:].strip() + '\n'
                buffer.insert_with_tags_by_name(iter, line, 'code')

            elif line.startswith('SUBTITLE'):
                line = line[8:].strip() + '\n'
                buffer.insert_with_tags_by_name(iter, line, 'subtitle')

            elif line.startswith('IMAGE'):
                line = line[5:].strip()
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(line)
                buffer.insert_pixbuf(iter, pixbuf)

            else:
                buffer.insert_with_tags_by_name(iter, line + '\n', 'default')

            #label_data.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(4626, 6939, 8481))

        self.box.pack_start(view, False, False, 0)
        self.show_all()


class Canvas(Gtk.HBox):

    def __init__(self):
        Gtk.HBox.__init__(self)

        self.lateral_panel = LateralPanel()
        self.lateral_panel.connect('show-file', self.show_file)
        self.pack_start(self.lateral_panel, False, False, 2)

        self.viewer = Viewer()
        self.pack_start(self.viewer, True, True, 0)

        self.show_all()

    def show_file(self, lateral_panel, name, path):
        self.viewer.set_data(name, path)

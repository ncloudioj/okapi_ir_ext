#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from okapi import OkapiBss

ID_BTN_EXIT         = 0x01
ID_BTN_SEARCH       = 0x02
ID_COM_DATABASE     = 0x03
ID_TXT_QUERIES      = 0x04
ID_TXT_RECORD       = 0x05
ID_LIST_RECORD      = 0x06
ID_BTN_INFILE       = 0x07

wildcard = "Text file (*.txt)|*.txt|" \
           "All files (*.*)|*.*"

class OkapiApp(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))
        panel = wx.Panel(self, -1)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, -1, 'Database')
        st1.SetFont(font)
        hbox1.Add(st1, 0, wx.RIGHT | wx.CENTER, 8)
        self.com1 = wx.ComboBox(panel, ID_COM_DATABASE, size=(120,-1),
                style=wx.CB_DROPDOWN | wx.CB_READONLY)
        hbox1.Add(self.com1, 1)
        st2 = wx.StaticText(panel, -1, 'Queries')
        st2.SetFont(font)
        hbox1.Add(st2, 0, wx.RIGHT | wx.CENTER, 8)
        self.tc1 = wx.TextCtrl(panel, ID_TXT_QUERIES)
        hbox1.Add(self.tc1, 1)
        btn1 = wx.Button(panel, ID_BTN_SEARCH, 'Search', size=(70, 30))
        btn3 = wx.Button(panel, ID_BTN_INFILE, 'Import', size=(70, 30))
        hbox1.Add(btn3, 0)
        hbox1.Add(btn1, 0)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, -1, 'Retrieved Documents')
        st2.SetFont(font)
        hbox2.Add(st2, 0)
        vbox.Add(hbox2, 0, wx.LEFT | wx.TOP, 10)
        vbox.Add((-1, 10))
        self.lb1 = wx.ListBox(panel, ID_LIST_RECORD,
                              style=wx.LB_SINGLE|wx.LB_NEEDED_SB)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc2 = wx.TextCtrl(panel, ID_TXT_RECORD, style=wx.TE_MULTILINE)
        hbox3.Add(self.lb1, 1, wx.EXPAND, border=10)
        hbox3.Add(self.tc2, 1, wx.EXPAND)
        vbox.Add(hbox3, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        vbox.Add((-1, 25))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, -1, 'Posting')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, -1, 'Weight')
        cb2.SetFont(font)
        hbox4.Add(cb2, 0, wx.LEFT, 10)
        cb3 = wx.CheckBox(panel, -1, 'Document')
        cb3.SetFont(font)
        hbox4.Add(cb3, 0, wx.LEFT, 10)
        vbox.Add(hbox4, 0, wx.LEFT, 10)
        vbox.Add((-1, 25))
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn2 = wx.Button(panel, ID_BTN_EXIT, 'Exit', size=(70, 30))
        hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
        panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

        # Event Register
        self.Bind(wx.EVT_BUTTON, self.OnSearch, id=ID_BTN_SEARCH)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_BTN_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=ID_LIST_RECORD)
        self.Bind(wx.EVT_BUTTON, self.OnImport, id=ID_BTN_INFILE)

        # init okapi
        self.okapi = OkapiBss()
        for database in self.okapi.show_database():
            self.com1.Append(database['name'])

    def OnClose(self, event):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()

    def OnSearch(self, event):
        dbname = self.com1.GetStringSelection()
        if dbname == "":
            self.NotifyIssus("Please select the database.")
            return
        queries = self.tc1.GetValue()
        #import pdb; pdb.set_trace()
        if queries == "":
            self.NotifyIssus("Please input the queries.")
            return

        result = []
        self.okapi.use(dbname)
        (nset, nposting) = self.okapi.search(queries.split(" "))
        #import pdb; pdb.set_trace()
        self.records = {}
        for record in self.okapi.show(nset, 0, nposting):
            posting = "Posting: %s, Weight: %.3f" % (record["posting"],
                    record["weight"])
            self.records[posting] = record["text"]
            result.append( posting )

        self.tc2.Clear()
        self.lb1.Clear()
        self.lb1.InsertItems(result, 0)


    def OnSelect(self, event):
        posting = event.GetString()
        self.tc2.SetValue(self.records[posting])


    def NotifyIssus(self, msg):
        dial = wx.MessageDialog(None, msg, 'Question', wx.OK |
                wx.ICON_INFORMATION)
        dial.ShowModal()

    def OnImport(self, event):
        dlg = wx.FileDialog(
                            self, message="Choose a file",
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.OPEN | wx.CHANGE_DIR
                            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.queries = []
            with open(path, 'r') as f:
                for line in f:
                    [ self.queries.append(word) for word in
                            line.rstrip('\n').split(' ') ]
            self.tc1.SetValue(" ".join(self.queries))

def main():

    ex = wx.App()
    OkapiApp(None, -1, 'Okapi System')
    ex.MainLoop()


if __name__ == '__main__':
    main()

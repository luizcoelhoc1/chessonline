# -*- coding: utf-8 -*-

import PySimpleGUI as sg

from main import Tabuleiro, Casa

sg.ChangeLookAndFeel('Dark')
sg.SetOptions(element_padding=(0,0))

t = Tabuleiro()

layout = []

for i in range(0,8):
    layout.append([])
    for j in range(0,8):
        layout[i].append(t.tabuleiro[i][j].btn)
    
    
# Create the Window
window = sg.Window('Chess online', layout, background_color="#000000")
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
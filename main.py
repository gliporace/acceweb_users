#####################
#
# acceweb_new_user
# Crea un utente Acceweb utilizzando Google Chrome per compilare la maschera di
# creazione utenti di Hitech Acceweb
# utilizza il driver ChromeDriver per "pilotare" Google Chrome scaricabile da https://chromedriver.chromium.org
# scaricare la versione compatibile con quella di Chrome installato
# che deve essere posizionato in c:\Python38
# o in una cartella in PATH
#
# (c) 2020 Gianfranco Liporace
######################

import os, sys
import wx
from ui import MainWindow


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow().Show()
    app.MainLoop()

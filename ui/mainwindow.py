# gridEvents.py
import wx
import wx.grid as grid
import acceweb_user as au
from selenium.common.exceptions import SessionNotCreatedException

########################################################################
class BaseGrid(grid.Grid):

    def __init__(self, parent):
        """Constructor"""
        grid.Grid.__init__(self, parent)
        self.CreateGrid(1, 6)
        # set column headers       
        self.SetColLabelValue(0, "Username")
        self.SetColLabelValue(1, "Cognome")
        self.SetColLabelValue(2, "Nome")
        self.SetColLabelValue(3, "Profilo")
        self.SetColLabelValue(4, "Password")
        self.SetColLabelValue(5, "Sede")

        # bind Key "KEY_DOWN" to add a new row
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, evt):
        kc = evt.GetKeyCode()
        # print("Tasto: %s, Posizione riga: %d, Numero righe: %d" % (kc, self.GetGridCursorRow(), self.GetNumberRows()))
        if kc == wx.WXK_DOWN:
            if self.GetGridCursorRow() == self.GetNumberRows() - 1:
                self.AppendRows()
                self.ForceRefresh()
        evt.Skip()
        

########################################################################
class MainWindow(wx.Frame):

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Utenti Acceweb")
        panel = wx.Panel(self)
        
        self.base_grid = BaseGrid(panel)
        crea_utenti_acceweb_btn = wx.Button(panel, wx.ID_ANY, "Crea utenti Acceweb")
        crea_utenti_acceweb_btn.Bind(wx.EVT_BUTTON, self.creaUtentiAcceweb)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.base_grid, 1, wx.EXPAND | wx.ALL)
        sizer.Add(crea_utenti_acceweb_btn, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        self.SetClientSize(panel.GetSize() + (10, 150))
        
    def creaUtentiAcceweb(self, evt):
        try:
            utente = au.AccewebUser()
        except SessionNotCreatedException as e:
            wx.MessageDialog(None, 'Attenzione: problema creazione sessione verso Chrome\n%s' % (str(e),), 'Errore', wx.OK | wx.ICON_ERROR).ShowModal()
            exit(0)
        utente.login('LIPGIA', 'VERCELLI')
        for row in range(0, self.base_grid.GetNumberRows()):
            u = []
            for col in range(0, self.base_grid.GetNumberCols()):
                u.append(self.base_grid.GetCellValue(row, col))
            utente.create_user(*u[:-2])
            utente.save_user()
            print("Sede: " + u[5])
            print("Profilo: " + u[3])
            if (u[5] =='VC'):
                utente.load_profiles(u[3], au.ELENCO_REPARTI_VC)
            elif (u[5] == 'BS'):
                utente.load_profiles(u[3], au.ELENCO_REPARTI_BS)
            elif (u[5] == None): # crea l'utenza senza profilazione
                pass
            elif (u[5] == 'ALL'):
                utente.load_profiles(u[3], au.ELENCO_REPARTI_VC)
                utente.load_profiles(u[3], au.ELENCO_REPARTI_BS)
            else:
                utente.load_profiles(u[3], u[5])
            utente.save_profiles()
            utente.clear_fields()
        utente.logout()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from time import sleep

DEFAULT_PASSWORD = "vercelli"

ELENCO_REPARTI_VC = ['301',
 #                   '9601',
                     '102',
                     '0205',
                     '0201',
                     '302',
                     '6702',
                     '6701',
                     '307',
                     '101',
                     '309',
                     '502',
                     '203',
                     '105',
                     '204',
                     '6601',
                     '3061',
                     '202',
                     '201',
                     '103',
                     '104',
                     '312',
                     '313',
                     '501',
                     '205',
                     '503',
                     '504',
                     '505',
#                    '506',
                     '507', # pneumologia covid19
                     '508' # covid vercelli
]

ELENCO_REPARTI_BS = ['3011',
                     '9602',
                     '1022',
                     '0502',
                     '0202',
                     '6704',
                     '6703',
                     '1011',
                     '1051',
                     '2022',
                     '2011',
                     '1031',
                     '1041',
                     '2051',
                     '2061',
                     '1061',
                     '4061',
                     '1071']


class AccewebUser():
    def __init__(self):
        options = Options()
        # lancia il browser Chrome in headless mode, ovvero non viene visualizzata la finestra del browser
        options.add_argument("--headless")
        # disattiva la gpu, opzione necessaria sotto windows
        options.add_argument("--disable-gpu")
        # self.browser = webdriver.Chrome(chrome_options=options)
        self.browser = webdriver.Chrome()
        # Apre Hitech - Acceweb
        self.browser.get("http://172.16.171.10/xpe/index.do")

    def load_profiles(self, profilo, elenco):
        for e in elenco:
            self.insert_profile(e, profilo)
    
    def change_frame(self, frame):
        """ Cambia il frame attivo di Acceweb

        Args:
            frame (str): frame da attivare ("menu" per il menu a sinistra, "main" per il frame centrale)
        """
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(frame)

    def login(self, username, password):
        uname = self.browser.find_element_by_name("username")
        pw = self.browser.find_element_by_name("password")
        uname.send_keys(username)
        pw.send_keys(password)
        self.browser.find_element_by_class_name("pulsante").click()

    def logout(self):
        self.change_frame("menu")
        self.browser.find_element_by_link_text("Logout").click()
        self.browser.close()

    def create_user(self, matricola, cognome, nome, password=None):
        """ Crea un nuovo utente; se viene specificata una password allora viene effettuato un cambio password
            di un utente esistente

        Args:
            matricola: matricola del dipendente; viene utilizzata per impostare il nome utente
            cognome, nome: cognome e nome del dipendente
            password: se viene specificato, viene effettuato un cambio password di utente già esistente, 
                      altrimenti viene utilizzata la password di default
        """
        self.change_frame("menu")
        try:
            self.browser.find_element_by_link_text("Gestione Utenti e Profili").click()
        except NoSuchElementException:
            self.browser.find_element_by_link_text("Gestione Utenti").click()
            WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Gestione Utenti e Profili"))
            )
            self.browser.find_element_by_link_text("Gestione Utenti e Profili").click()
        self.change_frame("main")
        self.browser.find_element_by_id("cognome").send_keys(cognome)
        self.browser.find_element_by_id("nome").send_keys(nome)
        self.browser.find_element_by_id("codice").send_keys(matricola)
        if (password != None and self.browser.find_element_by_id("buttonModifica").is_enabled()):
            self.browser.find_elements_by_id("buttonModifica").click()
        else:
            password = DEFAULT_PASSWORD
        self.browser.find_element_by_id("password").clear()
        self.browser.find_element_by_id("password").send_keys(password)    

    def insert_profile(self, reparto, profilo):
        ac = ActionChains(self.browser)
        self.browser.find_element_by_id("buttonHelpReparto").click()
        WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "bloccoHelp"))
        )
        sleep(0.5)
        rep = self.browser.find_element_by_id("helpsearchpattern%s" % (reparto, ))
        print("Reparto: " + reparto)
        print("Profilo: " + profilo)
        ac.double_click(rep).perform()
        prof = Select(self.browser.find_element_by_id('profilo'))
        prof.select_by_value(profilo)
        self.browser.find_element_by_id('buttonAddProfilo').click()

    def save_user(self):
        self.browser.find_element_by_id("buttonInserisci").click()
        # fa un pausa dopo il click altrimenti l'alert non viene intercettato
        sleep(1)
        try:
            # controlla se esce fuori il pop-up "nuovo utente registrato"
            # se non viene fuori vuol dire che l'utenza è già presente
            if EC.alert_is_present():
                alert = self.browser.switch_to.alert
                alert.dismiss()
        except:
            pass

    def save_profiles(self):
        self.browser.find_element_by_id("buttonSalvaProfili").click()
        # fa un pausa dopo il click altrimenti l'alert non viene intercettato
        sleep(1)
        try:
            # controlla se esce fuori il pop-up "profili salvati"
            if EC.alert_is_present():            
                alert = self.browser.switch_to.alert
                alert.dismiss()
        except:
            pass

    def clear_fields(self):
        self.browser.find_element_by_id("buttonPulisci").click()


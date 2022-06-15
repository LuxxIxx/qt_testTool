# coding=gbk
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from UI.share import SI
from UI.Main import main
from UI import data
import requests

class Win_Login:

    def __init__(self):
        self.ui = QUiLoader().load('login.ui')
        self.ui.btn_login.clicked.connect(self.onLogin)
        self.ui.edt_password.returnPressed.connect(self.onLogin)
        self.ui.box_url.addItems(['千帆t1', '千帆t2', '千帆线上', '神啦考研t1', '神啦考研线上', '中英考研t1', '中英考研腾讯云', '中英考研线上', '师来考编t1', '师来考编线上'])




    def onLogin(self):
        username = self.ui.edt_username.text().strip()
        password = self.ui.edt_password.text().strip()
        url = data.login_url[self.ui.box_url.currentText()]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        }
        Data = {}
        if self.ui.box_url.currentText() == '千帆t1' or self.ui.box_url.currentText() == '千帆t2' or self.ui.box_url.currentText() == '千帆线上':
            Data.update(phone=username, smscode=password)
        else:
            Data.update(username=username, password=password)
        r = requests.post(url, headers=headers, data=Data)


        if str(r.json()['code']) == '0':
            access_token = str(r.json()['data']['access_token'])
            SI.token = access_token
            SI.className = self.ui.box_url.currentText()
            SI.mainWin = main.Win_Main()
            SI.mainWin.ui.show()
            self.ui.edt_password.setText('')
            self.ui.close()

        else:
            QMessageBox.warning(
                self.ui,
                '登陆失败',
                str(r.json()['message'])
            )

app = QApplication([])
SI.loginWin = Win_Login()
SI.loginWin.ui.show()
app.exec_()
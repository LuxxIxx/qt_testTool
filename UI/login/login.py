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
        self.ui.box_url.addItems(['ǧ��t1', 'ǧ��t2', 'ǧ������', '��������t1', '������������', '��Ӣ����t1', '��Ӣ������Ѷ��', '��Ӣ��������', 'ʦ������t1', 'ʦ����������'])




    def onLogin(self):
        username = self.ui.edt_username.text().strip()
        password = self.ui.edt_password.text().strip()
        url = data.login_url[self.ui.box_url.currentText()]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        }
        Data = {}
        if self.ui.box_url.currentText() == 'ǧ��t1' or self.ui.box_url.currentText() == 'ǧ��t2' or self.ui.box_url.currentText() == 'ǧ������':
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
                '��½ʧ��',
                str(r.json()['message'])
            )

app = QApplication([])
SI.loginWin = Win_Login()
SI.loginWin.ui.show()
app.exec_()
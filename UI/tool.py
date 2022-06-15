from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from UI.share import SI
from UI.Main import main
import requests

class Stats:

    def __init__(self):
        # ���ļ��м���UI����

        # �� UI �����ж�̬ ����һ����Ӧ�Ĵ��ڶ���
        # ע�⣺����Ŀؼ�����Ҳ��Ϊ���ڶ����������
        # ���� self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('main.ui')

        self.ui.button.clicked.connect(self.handleCalc)

app = QApplication([])
SI.loginWin = Win_Login()
SI.loginWin.ui.show()
app.exec_()
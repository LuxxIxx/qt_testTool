# coding=gbk
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QTableWidgetItem
from UI.share import SI
import requests
from UI import data
import datetime

class Win_Main:
    def __init__(self):
        # ��Ӷ�����ʼ��
        self.ui = QUiLoader().load('../Main/main.ui')

        if SI.className == 'ǧ������' or SI.className == '������������' or SI.className == '��Ӣ��������' or SI.className == 'ʦ����������':
            self.ui.box_isAudit.addItems(['��'])
        else:
            self.ui.box_isAudit.addItems(['��', '��'])
        if SI.className == 'ǧ��t1' or SI.className == 'ǧ��t2' or SI.className == 'ǧ������':
            self.ui.box_store.addItems(['��ʦ����', '���;�ѧ', '�۲�ѧ��', '������ʦ', '��ʦ����', '�����е�', '��ѧ����', '��ѧ��', '�۲�ľ��', '����ʦͨ', '���½���'])
        else:
            self.ui.box_store.addItems([SI.className])
        self.ui.btn_sub.clicked.connect(self.addOrder)
        self.ui.lab_name.setText(SI.className)
        self.ui.btn_addOrder_clear.clicked.connect(self.addOrder_clear)

        # ��ѯ�༶��ʼ��
        self.ui.table_class.setRowCount(10)
        self.ui.table_class.setColumnWidth(0, 130)
        self.ui.table_class.setColumnWidth(1, 65)
        self.ui.table_class.setColumnWidth(2, 150)
        self.ui.table_class.setColumnWidth(3, 140)
        self.ui.table_class.setColumnWidth(4, 140)
        self.ui.btn_suchClassByOrder.clicked.connect(self.suchClass)
        self.ui.btn_lastPage.clicked.connect(self.suchClassLastPage)
        self.ui.btn_nextPage.clicked.connect(self.suchClassNextPage)
        self.ui.btn_clear.clicked.connect(self.suchClassClear)

        # push������ʼ��
        self.ui.btn_push.clicked.connect(self.pushOrder)

        # �˳���¼
        self.ui.btn_logout.clicked.connect(self.logout)

        # ���˵���ʼ��
        self.ui.btn_addOrder.clicked.connect(self.showAddOrder)
        self.ui.btn_addClass.clicked.connect(self.showAddClass)
        self.ui.btn_pushOrder.clicked.connect(self.showPushOrder)
        self.ui.btn_suchClass.clicked.connect(self.showSuchClass)

        # ��Ӱ༶��ʼ��
        self.ui.btn_addClass_push.clicked.connect(self.addClass)
        if SI.className == 'ǧ��t1' or SI.className == 'ǧ��t2' or SI.className == 'ǧ������':
            self.ui.box_addClass_store.addItems(['��ʦ����', '���;�ѧ', '�۲�ѧ��', '������ʦ', '��ʦ����', '�����е�', '��ѧ����', '��ѧ��', '�۲�ľ��', '����ʦͨ', '���½���', 'ȫƽ̨'])
        else:
            self.ui.box_addClass_store.addItems([SI.className])

    def addOrder(self):
        phonenum = self.ui.edit_phone.text().strip()
        ordernum = self.ui.edit_num.text().strip()
        url = data.addOrder_url[SI.className]
        headers = {
            'authorization': 'Bearer ' + SI.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }

        if SI.className == 'ǧ��t1' or SI.className == 'ǧ��t2' or SI.className == 'ǧ������':
            changeData = {
                'companyId': data.qf_companyId[self.ui.box_store.currentText()],
            }
            rCd = requests.post('https://t1-jsapi.gzjushiwang.com/base/current/user/changeCompany', headers=headers, data=changeData)

        Data = {
            'productSkuId': self.ui.edit_classId.text(),
            'couponId':'',
            'phone': phonenum,
            'receiverName': '������Ա',
            'isSubtract': '1',
            'receiverPhone': phonenum,
            'receiverProvinceCode': '110000',
            'receiverProvinceName': '������',
            'receiverCityCode': '110100',
            'receiverCityName': '������',
            'receiverRegionCode': '110105',
            'receiverRegionName': '������',
            'receiverDetailAddress': '���Ե�ַ',
            'thirdPartOrderNo':'',
            'thirdPartConfigId':''
        }

        for item in range(0, int(ordernum)):
            r = requests.post(url, headers=headers, data=Data)
            self.ui.edit_log.appendPlainText('������������� ' + r.json()['message'])
            # print(r.json())
            orderid = r.json()['data']['orderId']
            url2 = data.auditOrder_url[SI.className]
            Data2 = {
                'orderId': orderid,
                'name': phonenum,
                'url': 'public / voucher / TNAZJQKrdA.jpg',
                'payTypeFin': 'XXZZ'
            }
            r2 = requests.post(url2, headers=headers, data=Data2)
            self.ui.edit_log.appendPlainText('�ϴ�ƾ֤����� ' + r2.json()['message'])
            # print(r2.json())

            if self.ui.box_isAudit.currentText() == '��':
                url3 = data.remitOrder_url[SI.className]
                Data3 = {
                    'orderId': orderid,
                    'payTimeStr': datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'),
                    'auditStatus': '2',
                    'platMerchantId': '23'
                }
                r3 = requests.post(url3, headers=headers, data=Data3)
                print(r3.json())
                self.ui.edit_log.appendPlainText('��˽���� ' + r3.json()['message'])

                self.ui.edit_log.appendPlainText('��ӽ���� ' + r3.json()['message'] + '        ������Ϊ��' + r.json()['data']['orderNumber'])

    def addOrder_clear(self):
        self.ui.edit_log.setPlainText('')
        self.ui.edit_num.setText('')
        self.ui.edit_classId.setText('')
        self.ui.edit_phone.setText('')

    def showAddOrder(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showAddClass(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def showPushOrder(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def showSuchClass(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def logout(self):
        headers = {
            'authorization': 'Bearer ' + SI.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        }
        url = data.logout_url[SI.className]
        Data3 = {
            'token': SI.token
        }
        r = requests.post(url, headers=headers, data=Data3)
        SI.mainWin = None
        SI.loginWin.ui.show()
        self.ui.close()

    def pushOrder(self):
        url = 'https://api.kpjushi.cn/order/order/adm/order/pushOrderToAnalyse'
        params = {
            'orderId': self.ui.edit_orderId.text().strip()
        }
        headers = {
            'authorization': 'Bearer ' + SI.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        }
        r = requests.get(url, params=params, headers=headers)
        self.ui.edit_pushLog.setText('���ͽ���� ' + r.json()['message'])
        print(r.json())

    def suchClass(self):
        url = data.such_class_url[SI.className]
        params = {
            'page': '1',
            'limit': '10',
            'publishFlag': '0',
            'favourFlag': '0',
            'showFlag': '0',
            'categoryId': '',
            'expressType': '0',
            'skuName': self.ui.edit_suchClass_OrderId.text().strip(),
            'specs': '',
            'authStatus': '',
            'spuStatus': ''
        }
        headers = {
            'authorization': 'Bearer ' + SI.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        if SI.className == 'ǧ��t1' or SI.className == 'ǧ��t2' or SI.className == 'ǧ������':

            changeData = {
                'companyId': '1'
            }
            rCd = requests.post('https://t1-jsapi.gzjushiwang.com/base/current/user/changeCompany', headers=headers,data=changeData)

        r = requests.get(url, params=params, headers=headers)

        SI.suchClass_page_now = 1
        SI.suchClass_page = r.json()['data']['pages']

        self.ui.text_page.setText(str(SI.suchClass_page_now) + "/" + SI.suchClass_page)

        self.ui.table_class.clearContents()
        count = 0
        for i in r.json()['data']['records']:
            item1 = QTableWidgetItem()
            item1.setText(str(i['skuName']))
            self.ui.table_class.setItem(count, 0, item1)

            try:
                item2 = QTableWidgetItem()
                item2.setText(str(i['priceSale']))
                self.ui.table_class.setItem(count, 1, item2)
            except:
                pass

            item3 = QTableWidgetItem()
            item3.setText(str(i['insertDate']))
            self.ui.table_class.setItem(count, 2, item3)

            item4 = QTableWidgetItem()
            item4.setText(str(i['id']))
            self.ui.table_class.setItem(count, 3, item4)

            item5 = QTableWidgetItem()
            item5.setText(str(i['spuId']))
            self.ui.table_class.setItem(count, 4, item5)
            count += 1

    def suchClassLastPage(self):
        if SI.suchClass_page is None or SI.suchClass_page == 0:
            pass
        else:
            if SI.suchClass_page_now > 1:
                url = data.such_class_url[SI.className]
                page = SI.suchClass_page_now - 1
                params = {
                    'page': page,
                    'limit': '10',
                    'publishFlag': '0',
                    'favourFlag': '0',
                    'showFlag': '0',
                    'categoryId': '',
                    'expressType': '0',
                    'skuName': self.ui.edit_suchClass_OrderId.text().strip(),
                    'specs': '',
                    'authStatus': '',
                    'spuStatus': ''
                }
                headers = {
                    'authorization': 'Bearer ' + SI.token,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
                }

                r = requests.get(url, params=params, headers=headers)
                self.ui.edit_pushLog.setText('��ѯ����� ' + r.json()['message'])

                SI.suchClass_page_now = page
                SI.suchClass_page = r.json()['data']['pages']

                self.ui.text_page.setText(str(SI.suchClass_page_now) + "/" + SI.suchClass_page)

                self.ui.table_class.clearContents()
                count = 0
                for i in r.json()['data']['records']:
                    item1 = QTableWidgetItem()
                    item1.setText(str(i['skuName']))
                    self.ui.table_class.setItem(count, 0, item1)

                    try:
                        item2 = QTableWidgetItem()
                        item2.setText(str(i['priceSale']))
                        self.ui.table_class.setItem(count, 1, item2)
                    except:
                        pass

                    item3 = QTableWidgetItem()
                    item3.setText(str(i['insertDate']))
                    self.ui.table_class.setItem(count, 2, item3)

                    item4 = QTableWidgetItem()
                    item4.setText(str(i['id']))
                    self.ui.table_class.setItem(count, 3, item4)

                    item5 = QTableWidgetItem()
                    item5.setText(str(i['spuId']))
                    self.ui.table_class.setItem(count, 4, item5)
                    count += 1
            else:
                pass

    def suchClassNextPage(self):
        if not SI.suchClass_page or SI.suchClass_page == 0:
            pass
        else:
            if SI.suchClass_page_now < int(SI.suchClass_page):
                url = data.such_class_url[SI.className]
                page = SI.suchClass_page_now + 1
                params = {
                    'page': page,
                    'limit': '10',
                    'publishFlag': '0',
                    'favourFlag': '0',
                    'showFlag': '0',
                    'categoryId': '',
                    'expressType': '0',
                    'skuName': self.ui.edit_suchClass_OrderId.text().strip(),
                    'specs': '',
                    'authStatus': '',
                    'spuStatus': ''
                }
                headers = {
                    'authorization': 'Bearer ' + SI.token,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
                }

                r = requests.get(url, params=params, headers=headers)
                self.ui.edit_pushLog.setText('��ѯ����� ' + r.json()['message'])

                SI.suchClass_page_now = page
                SI.suchClass_page = r.json()['data']['pages']

                self.ui.text_page.setText(str(SI.suchClass_page_now) + "/" + SI.suchClass_page)

                self.ui.table_class.clearContents()
                count = 0
                for i in r.json()['data']['records']:
                    item1 = QTableWidgetItem()
                    item1.setText(str(i['skuName']))
                    self.ui.table_class.setItem(count, 0, item1)

                    try:
                        item2 = QTableWidgetItem()
                        item2.setText(str(i['priceSale']))
                        self.ui.table_class.setItem(count, 1, item2)
                    except:
                        pass

                    item3 = QTableWidgetItem()
                    item3.setText(str(i['insertDate']))
                    self.ui.table_class.setItem(count, 2, item3)

                    item4 = QTableWidgetItem()
                    item4.setText(str(i['id']))
                    self.ui.table_class.setItem(count, 3, item4)

                    item5 = QTableWidgetItem()
                    item5.setText(str(i['spuId']))
                    self.ui.table_class.setItem(count, 4, item5)
                    count += 1
            else:
                pass

    def suchClassClear(self):
        self.ui.table_class.clearContents()
        self.ui.edit_suchClass_OrderId.setText('')

    def addClass(self):
        skuId = self.ui.edit_addClass_skuId.text().strip()
        phoneNum = self.ui.edit_addClass_phoneNum.text().strip()
        store = self.ui.box_addClass_store.currentText()
        stuId_list = []
        stuId = ''

        headers = {
            'authorization': 'Bearer ' + SI.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }

        url0 = data.such_student_url[SI.className]
        stuIdParams = {
            'page': '1',
            'limit': '20',
            'userType': '1',
            'phone': phoneNum
        }
        r0 = requests.get(url0, params=stuIdParams, headers=headers)

        if store == 'ȫƽ̨':
            pass
        else:
            for i in r0.json()['data']['records']:
                if i['companyName'] == store:
                    stuId = i['id']

        url = data.addClass_url[SI.className]
        datas = {
            'userId': stuId,
            'skuId': skuId,
            'spuType': '1',
            'getMode': '5',
            'delFlag': '1',
            'feedbackSource': '����',
            'reason': '6',
            'remarks': '����',
            'phone': phoneNum,
            'skuName': '',
            'spuName': ''
        }
        if SI.className == 'ǧ��t1' or SI.className == 'ǧ��t2' or SI.className == 'ǧ������':
            changeData = {
                'companyId': '1'
            }
            rCd = requests.post('https://t1-jsapi.gzjushiwang.com/base/current/user/changeCompany', headers=headers,data=changeData)

        r = requests.post(url, data=datas, headers=headers)
        self.ui.edit_addClass_log.setText('��Ӱ༶����� ' + r.json()['message'])
















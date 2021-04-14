from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import MySQLdb
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

db = MySQLdb.connect(host='localhost', user='root', password='toor', db='myapp')
cur = db.cursor()

FORM_CLASS,_ = loadUiType("ui/admin panel.ui")

class Admin_Panel(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(Admin_Panel, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Main()

    def Main(self):
        self.tabWidget.tabBar().setVisible(False)
        self.All_Buttons()
        self.tabWidget.setCurrentIndex(0)
        self.Show_Products()
        self.Show_Employees()
        self.dialogs = list()

    def All_Buttons(self):
        self.actionProducts.triggered.connect(self.Products_Tab)
        self.actionWorkers.triggered.connect(self.Workers_Tab)
        self.actionCashier.triggered.connect(self.Cashier_Tab)
        self.actionStore_Data.triggered.connect(self.Store_Data_Tab)
        self.actionUsers.triggered.connect(self.Users_Tab)
        self.actiondashboard.triggered.connect(self.Dashboard_Tab)
        self.actionCategory.triggered.connect(self.Category_Tab)
        self.actionHistory.triggered.connect(self.History_Tab)
        self.tableWidget.clicked.connect(self.Click_Products_Table)
        self.pushButton_4.clicked.connect(self.Clear)
        self.pushButton.clicked.connect(self.Add_Product)
        self.pushButton_3.clicked.connect(self.Delete_Product)
        self.pushButton_2.clicked.connect(self.Edit_Product)
        self.pushButton_6.clicked.connect(self.Clear)
        self.pushButton_8.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Edit_Employee)
        self.pushButton_7.clicked.connect(self.Delete_Employee)
        self.tableWidget_2.clicked.connect(self.Click_Employee_Table)
        self.actionReset.triggered.connect(self.Reset)

    def Products_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Workers_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Dashboard_Tab(self):
        self.tabWidget.setCurrentIndex(5)

    def History_Tab(self):
        self.tabWidget.setCurrentIndex(7)

    def Users_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    def Cashier_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    
    def Store_Data_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Category_Tab(self):
        self.tabWidget.setCurrentIndex(6)

    def Show_Products(self):
        try:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            cur.execute('''
                    SELECT PROname , PROcode , PROprice , PROquantity , PROdate_added , PROcategory FROM product
                ''')
            products = cur.fetchall()
            for row, form in enumerate(products):
                for col, item in enumerate(form):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                rows = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rows)
        except Exception as e:
            print(e)
    
    def Show_Employees(self):
        rowPosition = self.tableWidget_2.rowCount()
        self.tableWidget_2.insertRow(rowPosition)
        cur.execute('''
            SELECT WORname , WORid , WORsalary ,Worage, WORphone , WORjob FROM worker
        ''')
        products = cur.fetchall()
        for row, form in enumerate(products):
            for col, item in enumerate(form):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            rows = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(rows)

    def Click_Products_Table(self,row):
        try:
            items = []
            for item in range(0, 6):
                item2 = self.tableWidget.item(row.row(), item).text()
                items.append(item2)

            self.lineEdit.setText(items[0])
            self.lineEdit_2.setText(items[1])
            self.lineEdit_3.setText(items[3])
            self.lineEdit_4.setText(items[4])
            self.lineEdit_5.setText(items[2])
            self.comboBox.setCurrentText(items[5])
            items = []
        except Exception as e:
            QMessageBox.information(self, "Error", "Do not click on an empty row")

    def Click_Employee_Table(self,row):
        try:
            items = []
            for item in range(0, 6):
                item2 = self.tableWidget_2.item(row.row(), item).text()
                items.append(item2)

            self.lineEdit_6.setText(items[0])
            self.lineEdit_7.setText(items[3])
            self.lineEdit_8.setText(items[4])
            self.lineEdit_9.setText(items[1])
            self.lineEdit_10.setText(items[2])
            self.lineEdit_11.setText(items[5])
            items = []
        except Exception as e:
            QMessageBox.information(self, "Error", "Do not click on an empty row")

    def Add_Product(self):
        name = self.lineEdit.text()
        price = self.lineEdit_5.text()
        date_added = self.lineEdit_4.text()
        quantity = self.lineEdit_3.text()
        code = self.lineEdit_2.text()
        category = self.comboBox.currentText()
        cur.execute('''
            INSERT INTO product(PROname , PROcode , PROprice , PROquantity , PROdate_added , PROcategory)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (name, code, price, quantity, date_added, category))
        db.commit()
        cur.execute('''
            INSERT INTO cashier(name , quantity , price , code)
            VALUES (%s , %s , %s , %s)
        ''', (name, quantity, price, code))
        db.commit()
        self.Reset()

    def Add_Employee(self):
        name = self.lineEdit_6.text()
        age = self.lineEdit_7.text()
        phone = self.lineEdit_8.text()
        wid = self.lineEdit_9.text()
        salary = self.lineEdit_10.text()
        job = self.lineEdit_11.text()
        cur.execute('''
            INSERT INTO worker(WORname , WORid , WORsalary , WORage , WORphone , WORjob)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (name, wid, salary, age , phone, job))
        db.commit()
        self.Reset()

    def Delete_Product(self):
        code = self.lineEdit_2.text()
        cur.execute('''
            DELETE FROM product WHERE PROcode = %s
        ''',[(code)])
        db.commit()
        cur.execute('''
            DELETE FROM cashier WHERE code = %s
        ''', [(code)])
        db.commit()
        self.Reset()

    def Delete_Employee(self):
        ID = self.lineEdit_9.text()
        cur.execute('''
            DELETE FROM worker WHERE WORid = %s
        ''', [(ID)])
        db.commit()
        self.Reset()

    def Edit_Product(self):
        name = self.lineEdit.text()
        price = self.lineEdit_5.text()
        date_added = self.lineEdit_4.text()
        quantity = self.lineEdit_3.text()
        code = self.lineEdit_2.text()
        category = self.comboBox.currentText()
        cur.execute('''
            UPDATE product SET PROname = %s , PROprice = %s , PROdate_added = %s , PROquantity = %s , PROcategory = %s WHERE PROcode = %s
        ''',(name , price , date_added , quantity , category , code))
        db.commit()
        self.Reset()

    def Edit_Employee(self):
        name = self.lineEdit_6.text()
        age = self.lineEdit_7.text()
        phone = self.lineEdit_8.text()
        wid = self.lineEdit_9.text()
        salary = self.lineEdit_10.text()
        job = self.lineEdit_11.text()
        cur.execute('''
            UPDATE worker SET WORname = %s , WORsalary = %s , WORage = %s , WORjob = %s , WORphone = %s WHERE WORid = %s
        ''', (name , salary , age , job , phone , wid))
        db.commit()
        self.Reset()

    def Clear(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')

    def Reset(self):
        curent_tabWidget = self.tabWidget.currentIndex()
        last_geometry = self.geometry()
        dialog = Admin_Panel(self)
        self.dialogs.append(dialog)
        dialog.setGeometry(last_geometry)
        dialog.tabWidget.setCurrentIndex(int(curent_tabWidget))
        dialog.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Admin_Panel()
    window.show()
    app.exec_()
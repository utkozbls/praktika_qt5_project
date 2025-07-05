from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
import sys
from library import Grup, Person

app = QtWidgets.QApplication(sys.argv)
win = uic.loadUi("student.ui")
Gr = Grup()

try:
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    pass

def load_table():
    win.tableWidget.setRowCount(Gr.count)
    for row, person in Gr.A.items():
        for col, value in enumerate(person.getPerson_forTable()):
            win.tableWidget.setItem(row, col, QTableWidgetItem(value))

def add_person():
    dlg: QDialog = uic.loadUi("Append_Студента.ui")
    dlg.buttonBox.accepted.connect(dlg.accept)
    dlg.buttonBox.rejected.connect(dlg.reject)
    if dlg.exec() == QDialog.Accepted:
        data = [
            dlg.lineEdit_4.text(),
            dlg.lineEdit_5.text(),
            dlg.lineEdit_6.text(),
            dlg.lineEdit_7.text(),
            dlg.lineEdit_8.text(),
            dlg.lineEdit_9.text(),
            dlg.lineEdit_10.text()
        ]
        Gr.appendPerson(data)
        Gr.write_data_to_file("text.txt")
        load_table()

def edit_person():
    selected = win.tableWidget.currentRow()
    if selected < 0 or selected >= Gr.count:
        QtWidgets.QMessageBox.warning(win, "Ошибка", "Сначала выберите строку для редактирования.")
        return

    person = Gr.A.get(selected)
    if not person:
        return

    dlg: QDialog = uic.loadUi("Append_Студента.ui")
    dlg.lineEdit_4.setText(person.fam)
    dlg.lineEdit_5.setText(person.name)
    dlg.lineEdit_6.setText(person.otchestvo)
    dlg.lineEdit_7.setText(person.year)
    dlg.lineEdit_8.setText(person.city)
    dlg.lineEdit_9.setText(person.sb_inf)
    dlg.lineEdit_10.setText(person.sb_math)
    dlg.buttonBox.accepted.connect(dlg.accept)
    dlg.buttonBox.rejected.connect(dlg.reject)

    if dlg.exec() == QDialog.Accepted:
        data = [
            dlg.lineEdit_4.text(),
            dlg.lineEdit_5.text(),
            dlg.lineEdit_6.text(),
            dlg.lineEdit_7.text(),
            dlg.lineEdit_8.text(),
            dlg.lineEdit_9.text(),
            dlg.lineEdit_10.text()
        ]
        Gr.editPerson(selected, data)
        Gr.write_data_to_file("text.txt")
        load_table()

def delete_person():
    dlg: QDialog = uic.loadUi("delition.ui")
    dlg.buttonBox.accepted.connect(dlg.accept)
    dlg.buttonBox.rejected.connect(dlg.reject)

    def find_row():
        query = dlg.lineEdit_4.text().strip()
        target = -1

        if not query:
            dlg.textBrowser.setText("Введите номер строки или id товара.")
            dlg.buttonBox.button(dlg.buttonBox.Ok).setEnabled(False)
            return

        if query.isdigit():
            num = int(query)
            if 1 <= num <= Gr.count:
                target = num - 1
            elif 0 <= num < Gr.count:
                target = num
        else:
            for idx, person in Gr.A.items():
                if person.sb_math == query:
                    target = idx
                    break

        if target == -1:
            dlg.textBrowser.setText("Строка не найдена…")
            dlg.buttonBox.button(dlg.buttonBox.Ok).setEnabled(False)
        else:
            row_data = " | ".join(Gr.A[target].getPerson_forTable())
            dlg.textBrowser.setText(row_data)
            dlg.lineEdit_4.setProperty("target_row", target)
            dlg.buttonBox.button(dlg.buttonBox.Ok).setEnabled(True)

    dlg.pushButton.clicked.connect(find_row)
    dlg.buttonBox.button(dlg.buttonBox.Ok).setEnabled(False)

    if dlg.exec() == QDialog.Accepted:
        target = dlg.lineEdit_4.property("target_row")
        if target is None:
            return

        del Gr.A[target]
        Gr.A = {i: p for i, (_, p) in enumerate(sorted(Gr.A.items()))}
        Gr.count = len(Gr.A)
        Gr.write_data_to_file("text.txt")
        load_table()

def sort_by_price():
    try:
        sorted_items = sorted(Gr.A.items(), key=lambda item: float(item[1].getPerson_forTable()[4]))
    except ValueError:
        QtWidgets.QMessageBox.warning(win, "Ошибка", "В столбце 'цена' есть нечисловые значения.")
        return

    Gr.A = {i: p for i, (_, p) in enumerate(sorted_items)}
    Gr.count = len(Gr.A)
    load_table()

def search_person():
    dlg: QDialog = uic.loadUi("poisk.ui")

    def find_rows():
        query = dlg.lineEdit_4.text().strip().lower()
        dlg.tableWidget.setRowCount(0)

        if not query:
            return

        key = None
        value = query
        if "=" in query:
            key, value = (x.strip().lower() for x in query.split("=", 1))

        col_map = {
            "товар": 0, "fam": 0,
            "страна": 1, "name": 1,
            "город": 2, "otchestvo": 2,
            "завод": 3, "year": 3,
            "цена": 4, "city": 4,
            "кол-во": 5, "sb_inf": 5,
            "id": 6, "id товара": 6, "sb_math": 6,
        }

        matches = []
        for person in Gr.A.values():
            fields = person.getPerson_forTable()
            if key:
                idx = col_map.get(key)
                if idx is not None and value in fields[idx].lower():
                    matches.append(fields)
            else:
                if any(value in f.lower() for f in fields):
                    matches.append(fields)

        dlg.tableWidget.setRowCount(len(matches))
        for r, row in enumerate(matches):
            for c, text in enumerate(row):
                dlg.tableWidget.setItem(r, c, QTableWidgetItem(text))

    dlg.pushButton.clicked.connect(find_rows)
    dlg.exec()

Gr.read_data_from_file("text.txt")
load_table()

win.pushButton.clicked.connect(load_table)
win.pushButton_3.clicked.connect(add_person)
win.pushButton_4.clicked.connect(edit_person)
win.pushButton_5.clicked.connect(search_person)
win.pushButton_6.clicked.connect(sort_by_price)
win.pushButton_7.clicked.connect(delete_person)

win.show()
sys.exit(app.exec())







import numpy as np
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget, QMessageBox,QComboBox
)
import pandas as pd
import sys
import json
import os



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ana Menü')
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()


        self.course_operations_button = QtWidgets.QPushButton("Ders İşlemleri")
        self.course_operations_button.clicked.connect(self.open_course_operations)
        main_layout.addWidget(self.course_operations_button)

        self.not_upload_button = QtWidgets.QPushButton("Not Yükle")
        self.not_upload_button.clicked.connect(self.open_not_yukle)
        main_layout.addWidget(self.not_upload_button)

        self.table4ve5_button = QtWidgets.QPushButton("Tablo 4 ve 5 Oluştur")
        self.table4ve5_button.clicked.connect(self.open_table4ve5)
        main_layout.addWidget(self.table4ve5_button)



        self.setLayout(main_layout)

    def open_course_operations(self):
        self.course_operations_window = CourseOperationsWindow()
        self.course_operations_window.show()

    def open_not_yukle(self):
        self.not_yukle_window = NotYukleWindow()
        self.not_yukle_window.show()

    def open_table4ve5(self):
        self.table4ve5_window = Table4ve5()
        self.table4ve5_window.show()


class CourseOperationsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle('Ders ve Program Çıktı Yönetimi')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()


        self.course_input = QtWidgets.QLineEdit()
        self.add_course_button = QtWidgets.QPushButton("Ders Ekle")
        self.add_course_button.clicked.connect(self.add_course)

        self.course_selector = QtWidgets.QComboBox()
        self.course_selector.currentIndexChanged.connect(self.load_columns_for_course)


        self.column_input = QtWidgets.QLineEdit()
        self.weight_input = QtWidgets.QLineEdit()
        self.add_column_button = QtWidgets.QPushButton("Kriter ve Ağırlık Ekle")
        self.add_column_button.clicked.connect(self.add_column)

        self.edit_columns_button = QtWidgets.QPushButton("Ders Kriteri ve Ağırlıkları Düzenle")
        self.edit_columns_button.clicked.connect(self.edit_columns)


        self.columns_view = QtWidgets.QListWidget()


        self.generate_table_button = QtWidgets.QPushButton("Tablo 2 Oluştur")
        self.generate_table_button.clicked.connect(self.generate_table)
        self.table2_widget = QtWidgets.QTableWidget()


        self.create_table3_button = QtWidgets.QPushButton("Ağırlıklı Tablo Oluştur")
        self.create_table3_button.clicked.connect(self.create_weighted_table)


        self.delete_course_button = QtWidgets.QPushButton("Ders Sil")
        self.delete_course_button.clicked.connect(self.delete_course)

        self.save_table2_button = QtWidgets.QPushButton("Tablo 2'yi Kaydet")
        self.save_table2_button.clicked.connect(self.save_table2)


        self.log_area = QtWidgets.QTextEdit()
        self.log_area.setReadOnly(True)


        form_layout.addRow("Yeni Ders Adı:", self.course_input)
        form_layout.addRow("", self.add_course_button)
        form_layout.addRow("", self.delete_course_button)
        form_layout.addRow("Ders Seçimi:", self.course_selector)
        form_layout.addRow("Kriter Adı:", self.column_input)
        form_layout.addRow("Ağırlık (%):", self.weight_input)
        form_layout.addRow("", self.add_column_button)
        form_layout.addRow("", self.edit_columns_button)
        form_layout.addRow("Kriterler ve Ağırlıklar:", self.columns_view)
        form_layout.addRow("", self.generate_table_button)
        form_layout.addRow("", self.save_table2_button)
        form_layout.addRow("Tablo 2 (Ders Çıktı İlişkileri):", self.table2_widget)
        form_layout.addRow("", self.create_table3_button)
        form_layout.addRow("İşlem Logları:", self.log_area)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)


        self.data_file = "course_data.json"
        self.courses = {}
        self.current_course = None

    def save_data(self):
        """Save course data to a JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.courses, file, ensure_ascii=False, indent=4)

    def load_data(self):
        """Load course data from a JSON file."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.courses = json.load(file)
                self.course_selector.addItems(self.courses.keys())
        except (FileNotFoundError, json.JSONDecodeError):
            self.courses = {}

    def add_course(self):
        course_name = self.course_input.text().strip()
        if course_name and course_name not in self.courses:
            self.courses[course_name] = {}
            self.course_selector.addItem(course_name)
            self.log_area.append(f"Ders eklendi: {course_name}")
            self.save_data()
        self.course_input.clear()

    def load_columns_for_course(self):
        course_name = self.course_selector.currentText()
        self.current_course = course_name
        self.columns_view.clear()
        self.columns_and_weights = {}
        if course_name and course_name in self.courses:
            for column, weight in self.courses[course_name].items():
                self.columns_view.addItem(f"{column} - {weight}%")
                self.columns_and_weights[column] = weight

    def add_column(self):
        column_name = self.column_input.text().strip()
        weight = self.weight_input.text().strip()

        if self.current_course and column_name and weight.isdigit():
            weight = float(weight)

            current_total_weight = sum(self.courses[self.current_course].values())
            if current_total_weight + weight > 100:
                self.log_area.append("Hata: Ağırlıkların toplamı %100'ü geçemez!")
                return

            # Yeni kriteri ekle
            self.courses[self.current_course][column_name] = weight
            self.columns_view.addItem(f"{column_name} - {weight}%")
            self.log_area.append(f"Kriter ve ağırlık eklendi: {column_name} ({weight}%)")
            self.save_data()
        else:
            self.log_area.append("Geçerli bir kriter adı ve ağırlık girin.")
        self.column_input.clear()
        self.weight_input.clear()

    def delete_course(self):
        selected_course = self.course_selector.currentText()
        if selected_course:
            confirmation = QtWidgets.QMessageBox.question(
                self, "Ders Silme", f"{selected_course} dersini silmek istediğinize emin misiniz?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirmation == QtWidgets.QMessageBox.Yes:
                del self.courses[selected_course]
                self.course_selector.removeItem(self.course_selector.currentIndex())
                self.log_area.append(f"Ders silindi: {selected_course}")
                self.save_data()

    def edit_columns(self):
        course_name = self.course_selector.currentText()
        if not course_name:
            self.log_area.append("Lütfen bir ders seçin.")
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"{course_name} Kriter ve Ağırlıkları Düzenle")
        dialog.setGeometry(200, 200, 400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        table = QtWidgets.QTableWidget(len(self.courses[course_name]), 2)
        table.setHorizontalHeaderLabels(["Kriter", "Ağırlık (%)"])
        table.horizontalHeader().setStretchLastSection(True)

        for row, (column, weight) in enumerate(self.courses[course_name].items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(column))
            weight_item = QtWidgets.QTableWidgetItem(str(weight))
            weight_item.setFlags(weight_item.flags() | QtCore.Qt.ItemIsEditable)
            table.setItem(row, 1, weight_item)

        layout.addWidget(table)


        button_layout = QtWidgets.QHBoxLayout()
        save_button = QtWidgets.QPushButton("Kaydet")
        cancel_button = QtWidgets.QPushButton("İptal")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)


        def save_changes():
            total_weight = 0
            new_columns = {}
            for row in range(table.rowCount()):
                column = table.item(row, 0).text().strip()
                try:
                    weight = float(table.item(row, 1).text().strip())
                except ValueError:
                    self.log_area.append(f"Hata: {column} kriteri için geçerli bir ağırlık girin.")
                    return

                if weight < 0:
                    self.log_area.append(f"Hata: {column} kriteri için negatif ağırlık giremezsiniz.")
                    return

                total_weight += weight
                new_columns[column] = weight

            if total_weight > 100:
                self.log_area.append(f"Hata: Toplam ağırlık %100'ü geçemez (Şu anda: {total_weight}%).")
                return


            self.courses[course_name] = new_columns
            self.save_data()
            self.load_columns_for_course()
            self.log_area.append(f"{course_name} kriterleri başarıyla güncellendi.")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    def generate_table(self):
        try:

            selected_course = self.course_selector.currentText()
            criteria = self.courses.get(selected_course, {})
            if not criteria:
                QtWidgets.QMessageBox.warning(self, "Uyarı", "Seçilen dersin kriterleri bulunamadı.")
                return


            num_criteria = len(criteria)
            num_rows = 5
            self.table2_widget.setRowCount(num_rows)
            self.table2_widget.setColumnCount(num_criteria)
            self.table2_widget.setHorizontalHeaderLabels(list(criteria.keys()))

            for row in range(num_rows):
                for col in range(num_criteria):
                    self.table2_widget.setItem(row, col, QtWidgets.QTableWidgetItem("0"))

            self.log_area.append("Tablo 2 başarıyla oluşturuldu. Tüm hücreler 0 ile dolduruldu.")
        except Exception as e:
            error_message = f"Hata oluştu: {str(e)}"
            self.log_area.append(error_message)
            QtWidgets.QMessageBox.critical(self, "Hata", error_message)

    def save_table2(self):
        try:

            num_rows = self.table2_widget.rowCount()
            num_cols = self.table2_widget.columnCount()

            data = []
            for row in range(num_rows):
                row_data = []
                for col in range(num_cols):
                    item = self.table2_widget.item(row, col)
                    value = int(item.text()) if item and item.text().isdigit() else 0
                    row_data.append(value)
                data.append(row_data)


            table2_df = pd.DataFrame(data, columns=[self.table2_widget.horizontalHeaderItem(col).text() for col in
                                                    range(num_cols)])
            selected_course = self.course_selector.currentText()
            table2_file = f"{selected_course}_Tablo2.xlsx"
            table2_df.to_excel(table2_file, index=False, sheet_name="Tablo 2")

            self.log_area.append(f"Tablo2 '{table2_file}' dosyasına kaydedildi.")
            QtWidgets.QMessageBox.information(self, "Başarılı",
                                              f"Tablo2 başarıyla '{table2_file}' dosyasına kaydedildi.")
        except Exception as e:
            self.log_area.append(f"Hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", f"Tablo2 kaydedilirken hata oluştu: {str(e)}")

    def create_weighted_table(self):
        try:

            num_rows = self.table2_widget.rowCount()
            num_cols = self.table2_widget.columnCount()

            if not self.columns_and_weights:
                self.log_area.append("Hata: Kriter ve ağırlık bilgileri bulunamadı.")
                return

            data = []
            for row in range(num_rows):
                row_data = []
                for col in range(num_cols):
                    item = self.table2_widget.item(row, col)
                    value = int(item.text()) if item and item.text().isdigit() else 0
                    row_data.append(value)
                data.append(row_data)


            column_names = list(self.columns_and_weights.keys())
            if len(column_names) != num_cols:
                self.log_area.append("Hata: Tablo sütun sayısı ile kriter sayısı eşleşmiyor.")
                return


            table2_df = pd.DataFrame(data, columns=column_names)


            weighted_data = {}
            for column_name, weight in self.columns_and_weights.items():
                weighted_data[column_name] = table2_df[column_name] * weight / 100

            weighted_df = pd.DataFrame(weighted_data)
            weighted_df['TOPLAM'] = weighted_df.sum(axis=1)


            self.log_area.append("Ağırlıklı değerlendirme tablosu oluşturuldu:")
            self.log_area.append(str(weighted_df.round(1)))


            selected_course = self.course_selector.currentText()
            output_file = f"{selected_course}_AğırlıklıDeğerlendirmeTablosu.xlsx"
            weighted_df.to_excel(output_file, index=False, sheet_name="Ağırlıklı Tablo")
            self.log_area.append(f"Tablo '{output_file}' dosyasına kaydedildi.")

        except Exception as e:
            self.log_area.append(f"Hata oluştu: {str(e)}")


class NotYukleWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_courses()

    def initUI(self):
        self.setWindowTitle('Not Yükle')
        self.setGeometry(100, 100, 800, 600)


        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()


        self.course_selector = QtWidgets.QComboBox()
        form_layout.addRow("Ders Seçimi:", self.course_selector)


        self.load_student_list_button = QtWidgets.QPushButton("Öğrenci Listesi Yükle")
        self.load_student_list_button.clicked.connect(self.load_student_list)
        form_layout.addRow("", self.load_student_list_button)


        self.table_widget = QtWidgets.QTableWidget()
        form_layout.addRow("Not Tablosu:", self.table_widget)

        self.save_button = QtWidgets.QPushButton("Not Listesini Kaydet")
        self.save_button.clicked.connect(self.save_notes)
        form_layout.addRow("", self.save_button)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)


        self.data_file = "course_data.json"
        self.courses = {}
        self.student_list = None

    def load_courses(self):
        """Load courses from the JSON file."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.courses = json.load(file)
                self.course_selector.addItems(self.courses.keys())
        except (FileNotFoundError, json.JSONDecodeError):
            self.courses = {}

    def load_student_list(self):
        """Load student list and generate the table."""
        selected_course = self.course_selector.currentText()
        if not selected_course:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir ders seçin.")
            return


        file_dialog = QtWidgets.QFileDialog.getOpenFileName(self, "Öğrenci Listesi Yükle", "", "Excel Dosyaları (*.xlsx)")
        file_path = file_dialog[0]

        if file_path:
            try:
                self.student_list = pd.read_excel(file_path)
                if "Ogrenci_No" not in self.student_list.columns:
                    raise ValueError("Excel dosyasında 'Ogrenci_No' sütunu bulunamadı.")

                self.generate_table(selected_course)
                QtWidgets.QMessageBox.information(self, "Başarılı", "Öğrenci listesi yüklendi.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Hata", f"Öğrenci listesi yüklenirken hata oluştu: {e}")

    def generate_table(self, selected_course):
        """Generate the table based on students and course criteria."""
        criteria = self.courses.get(selected_course, {})
        if not criteria:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Seçilen dersin kriterleri yok.")
            return


        self.table_widget.setRowCount(len(self.student_list))
        self.table_widget.setColumnCount(len(criteria) + 1)


        headers = ["Ogrenci_No"] + list(criteria.keys())
        self.table_widget.setHorizontalHeaderLabels(headers)


        for row, ogrenci_no in enumerate(self.student_list["Ogrenci_No"]):
            item = QtWidgets.QTableWidgetItem(str(ogrenci_no))
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Öğrenci No düzenlenemez
            self.table_widget.setItem(row, 0, item)


        for row in range(self.table_widget.rowCount()):
            for col in range(1, self.table_widget.columnCount()):
                self.table_widget.setItem(row, col, QtWidgets.QTableWidgetItem("0"))

    def save_notes(self):
        """Save the notes to an Excel file with averages."""
        selected_course = self.course_selector.currentText()
        if not selected_course:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir ders seçin.")
            return

        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen önce tabloyu oluşturun.")
            return

        try:

            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    value = item.text() if item else ""
                    row_data.append(value)
                data.append(row_data)


            headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                       range(self.table_widget.columnCount())]
            df = pd.DataFrame(data, columns=headers)


            numeric_columns = headers[1:]
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce',
                                                            axis=1)


            df["Ortalama"] = df[numeric_columns].mean(axis=1)


            output_file = f"{selected_course}_NotListesi.xlsx"
            df.to_excel(output_file, index=False)
            QtWidgets.QMessageBox.information(self, "Başarılı", f"Not listesi '{output_file}' olarak kaydedildi.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Not listesi kaydedilirken hata oluştu: {e}")


class Table4ve5(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data_file = "course_data.json"
        self.courses = {}
        self.load_courses()

    def init_ui(self):
        self.setWindowTitle("Ders Değerlendirme")
        self.setGeometry(200, 200, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label_ders = QLabel("Ders Seçimi:")
        layout.addWidget(self.label_ders)

        self.course_selector = QComboBox()
        layout.addWidget(self.course_selector)

        self.label_path = QLabel("Çalışma Dizin: Proje Dizini")
        layout.addWidget(self.label_path)

        self.button_process = QPushButton("Dosyaları İşle ve Çıktıları Kaydet")
        self.button_process.clicked.connect(self.process_files)
        layout.addWidget(self.button_process)

        central_widget.setLayout(layout)

    def load_courses(self):
        """Load courses from the JSON file."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.courses = json.load(file)
                self.course_selector.addItems(self.courses.keys())
        except (FileNotFoundError, json.JSONDecodeError):
            self.courses = {}

    def process_files(self):
        selected_course = self.course_selector.currentText()
        if not selected_course:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen bir ders seçin.")
            return

        try:
            project_directory = os.getcwd()

            input_file1 = "Tablo1.xlsx"
            input_file2 = f"{project_directory}/{selected_course}_Tablo2.xlsx"
            input_file3 = f"{project_directory}/{selected_course}_NotListesi.xlsx"
            weighted_file = f"{project_directory}/{selected_course}_AğırlıklıDeğerlendirmeTablosu.xlsx"
            output_file = f"{project_directory}/{selected_course}_Tablo4ve5.xlsx"

            self.run_processing(input_file1, input_file2, input_file3, weighted_file, output_file)

            QMessageBox.information(
                self,
                "Başarılı",
                f"İşlem tamamlandı. Çıktılar kaydedildi:\n{weighted_file}\n{output_file}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")

    def run_processing(self, input_file1, input_file2, input_file3, weighted_file, output_file):
        try:

            excel_data_tab1 = pd.ExcelFile(input_file1)
            sheet1_data = excel_data_tab1.parse(header=1)

            excel_data_tab2 = pd.ExcelFile(input_file2)
            sheet2_data = excel_data_tab2.parse()

            excel_data_tab3 = pd.ExcelFile(input_file3)
            tablo_not_data = excel_data_tab3.parse()

            relation_column_name = "İlişki Değ."


            weights_raw = sheet2_data.iloc[0, 1:6]
            weights = pd.to_numeric(weights_raw.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0).astype(
                float)

            grades = sheet2_data.iloc[2:, 1:6].apply(pd.to_numeric, errors='coerce').fillna(0)
            weighted_grades = grades * weights.values / 100
            weighted_grades['Ağırlıklı Toplam'] = weighted_grades.sum(axis=1)


            column_headers = list(sheet2_data.columns[1:6])
            weighted_table = weighted_grades.copy()
            weighted_table.columns = column_headers + ['Ağırlıklı Toplam']
            weighted_table = weighted_table.round(1)


            weighted_table.to_excel(weighted_file, index=False, sheet_name="Ağırlıklı Tablo")


            student_data = tablo_not_data.iloc[:, 1:6].apply(pd.to_numeric, errors='coerce').fillna(0)
            weights_data = weighted_table.iloc[:, :-1]
            students = [f"Öğrenci {i + 1}" for i in range(len(tablo_not_data))]

            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

                pd.DataFrame({'Placeholder': [0]}).to_excel(writer, sheet_name="Placeholder")

                for i, student in enumerate(students):
                    student_grades = student_data.iloc[i].values
                    weighted_grades = weights_data.values * student_grades
                    weighted_grades_sum = weighted_grades.sum(axis=1)
                    max_values = weights_data.sum(axis=1).values * 100
                    success_percentage = (weighted_grades_sum / max_values) * 100


                    student_result = pd.DataFrame(weighted_grades, columns=column_headers)
                    student_result['TOPLAM'] = weighted_grades_sum
                    student_result['MAX'] = max_values
                    student_result['% Başarı'] = success_percentage
                    student_result = student_result.round(1)
                    student_result.to_excel(writer, sheet_name=f"{student}_Tablo4", index=False)


                    relationship_values = sheet1_data[relation_column_name].apply(pd.to_numeric,
                                                                                  errors='coerce').fillna(1)
                    program_outcomes = sheet1_data.iloc[:, 0]
                    success_percentages = student_result['% Başarı'].values

                    tablo5_rows = []
                    tablo5_values = []

                    for j in range(len(program_outcomes)):
                        related_outcomes = sheet1_data.iloc[j, 1:6].apply(pd.to_numeric, errors='coerce').fillna(0)
                        related_success = success_percentages * related_outcomes
                        tablo5_rows.append(related_success.round(1).tolist())

                        num_outcomes = sheet1_data.shape[1] - 2
                        mean_success = related_success.sum() / num_outcomes if num_outcomes > 0 else 0
                        success_rate = mean_success / relationship_values[j] if relationship_values[j] != 0 else 0
                        tablo5_values.append(success_rate)

                    tablo5_df = pd.DataFrame(tablo5_rows, columns=[f"Ders Çıktısı {k + 1}" for k in range(5)])
                    tablo5_df['Başarı Oranı'] = tablo5_values
                    tablo5_df.index = program_outcomes
                    tablo5_df = tablo5_df.round(1)

                    tablo5_df.to_excel(writer, sheet_name=f"{student}_Tablo5", index=True)


                del writer.sheets["Placeholder"]

        except Exception as e:

            print("grades.shape:", grades.shape)
            print("weights.values.shape:", weights.values.shape)

            print("weights_data.values.shape:", weights_data.values.shape)
            print("student_grades.shape:", student_grades.shape)

            print(f"Hata: {e}")
            raise


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
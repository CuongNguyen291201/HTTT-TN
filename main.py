import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt

from fuzzy import FuzzySystem

class FuzzyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tạo các nhãn và các ô nhập liệu cho các thông số đầu vào
        self.r_label = QLabel('Tỷ suất lợi nhuận (%)')
        self.r_edit = QLineEdit()
        self.p_label = QLabel('Thời gian hoàn vốn (năm)')
        self.p_edit = QLineEdit()
        self.s_label = QLabel('Tỷ lệ rủi ro (%)')
        self.s_edit = QLineEdit()

        # Tạo một nút để tính chỉ số hiệu quả đầu tư
        self.calc_button = QPushButton('Tính chỉ số hiệu quả đầu tư')
        self.calc_button.clicked.connect(self.calculate)

        # Tạo một nhãn để hiển thị kết quả
        self.result_label = QLabel('Chỉ số hiệu quả đầu tư:')

        # Sắp xếp các thành phần trên giao diện theo lưới
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.r_label, 1, 0)
        grid.addWidget(self.r_edit, 1, 1)
        grid.addWidget(self.p_label, 2, 0)
        grid.addWidget(self.p_edit, 2, 1)
        grid.addWidget(self.s_label, 3, 0)
        grid.addWidget(self.s_edit, 3, 1)
        grid.addWidget(self.calc_button, 4, 1)
        grid.addWidget(self.result_label, 5, 1)

        self.setLayout(grid)

        # Đặt tiêu đề và kích thước cửa sổ
        self.setWindowTitle('Hệ thống đánh giá chỉ số hiệu quả đầu tư của một dự án kinh tế sử dụng hệ mờ')
        self.resize(400, 200)
        self.show()

    # def calculate(self):
    #     # Lấy giá trị của các thông số đầu vào từ các ô nhập liệu
    #     try:
    #         r = float(self.r_edit.text())
    #         p = float(self.p_edit.text())
    #         s = float(self.s_edit.text())

    #         print(r, s, p)

    #         # Tạo một đối tượng FuzzySystem với các thông số đầu vào
    #         fs = FuzzySystem(r, p, s)
    #         # Tính giá trị của chỉ số hiệu quả đầu tư bằng phương pháp centroid

    #         print(fs)

    #         e = fs.centroid()

    #         print(e)

    #         # Hiển thị kết quả trên nhãn
    #         self.result_label.setText(f'Chỉ số hiệu quả đầu tư: {e:.2f}')
    #     except ValueError:
    #         # Nếu có lỗi nhập liệu thì hiển thị thông báo lỗi
    #         QMessageBox.critical(self, 'Lỗi nhập liệu', 'Vui lòng nhập các giá trị số thực cho các thông số đầu vào')

    def calculate(self):
        # Lấy giá trị của các thông số đầu vào từ các ô nhập liệu
        try:
            r = float(self.r_edit.text())
            p = float(self.p_edit.text())
            s = float(self.s_edit.text())

            # Kiểm tra các giá trị đầu vào xem có nằm trong phạm vi hợp lệ không
            if 0 <= r <= 100 and p >= 0 and 0 <= s <= 100:
                # Tạo một đối tượng FuzzySystem với các thông số đầu vào
                fs = FuzzySystem(r, p, s)
                # Tính giá trị của chỉ số hiệu quả đầu tư bằng phương pháp centroid
                e = fs.centroid()
                if e is not None:  # Kiểm tra nếu giá trị e khác None
                    # Hiển thị kết quả trên nhãn
                    self.result_label.setText(f'Chỉ số hiệu quả đầu tư: {e:.2f}')
                else:
                    # Hiển thị thông báo lỗi nếu có lỗi trong quá trình tính toán
                    QMessageBox.critical(self, 'Lỗi tính toán', 'Có lỗi xảy ra trong quá trình tính toán.')
            else:
                QMessageBox.critical(self, 'Lỗi nhập liệu', 'Vui lòng nhập các giá trị hợp lệ cho các thông số đầu vào.')
        except ValueError:
            # Nếu có lỗi nhập liệu thì hiển thị thông báo lỗi

            print('ValueError', ValueError)

            QMessageBox.critical(self, 'Lỗi nhập liệu', 'Vui lòng nhập các giá trị số thực cho các thông số đầu vào')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FuzzyApp()
    sys.exit(app.exec_())

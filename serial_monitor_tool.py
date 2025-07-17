import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QPushButton, QTextEdit, QLabel, QLineEdit)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

class SerialThread(QThread):
    received = pyqtSignal(str)
    connection_status = pyqtSignal(bool)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.is_running = True

    def run(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                self.connection_status.emit(True)
                while self.is_running:
                    if ser.in_waiting:
                        data = ser.readline().decode('utf-8').strip()
                        self.received.emit(data)
        except serial.SerialException:
            self.connection_status.emit(False)

    def stop(self):
        self.is_running = False

class SerialMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Monitor")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.serial_thread = None
        self.setup_ui()

    def setup_ui(self):
        # Port selection
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_ports)
        port_layout.addWidget(QLabel("Port:"))
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_button)
        self.layout.addLayout(port_layout)

        # Baudrate selection
        baud_layout = QHBoxLayout()
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        baud_layout.addWidget(QLabel("Baudrate:"))
        baud_layout.addWidget(self.baud_combo)
        self.layout.addLayout(baud_layout)

        # Connect/Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        self.layout.addWidget(self.connect_button)

        # Status indicator
        self.status_label = QLabel("Status: Disconnected")
        self.layout.addWidget(self.status_label)

        # Data display
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.layout.addWidget(self.data_display)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_display)
        self.layout.addWidget(self.clear_button)

        # Data input
        self.data_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_data)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.data_input)
        input_layout.addWidget(self.send_button)
        self.layout.addLayout(input_layout)

        self.refresh_ports()

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        if self.serial_thread is None:
            port = self.port_combo.currentText()
            baudrate = int(self.baud_combo.currentText())
            self.serial_thread = SerialThread(port, baudrate)
            self.serial_thread.received.connect(self.update_display)
            self.serial_thread.connection_status.connect(self.update_connection_status)
            self.serial_thread.start()
            self.connect_button.setText("Disconnect")
        else:
            self.serial_thread.stop()
            self.serial_thread.wait()
            self.serial_thread = None
            self.connect_button.setText("Connect")
            self.update_connection_status(False)

    @pyqtSlot(bool)
    def update_connection_status(self, connected):
        if connected:
            self.status_label.setText("Status: Connected")
            self.status_label.setStyleSheet("color: green")
        else:
            self.status_label.setText("Status: Disconnected")
            self.status_label.setStyleSheet("color: red")

    @pyqtSlot(str)
    def update_display(self, data):
        self.data_display.append(data)

    def send_data(self):
        if self.serial_thread and self.serial_thread.isRunning():
            data = self.data_input.text() + '\n'
            try:
                with serial.Serial(self.serial_thread.port, self.serial_thread.baudrate) as ser:
                    ser.write(data.encode('utf-8'))
                self.data_input.clear()
            except serial.SerialException:
                self.update_connection_status(False)

    def clear_display(self):
        self.data_display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialMonitor()
    window.show()
    sys.exit(app.exec())

# Serial Monitor Tool (PyQt6)

A simple serial monitor GUI built with PyQt6 for communicating with serial (COM) ports. It allows you to connect to serial devices, read incoming data, send messages, and view the communication log in real time.

## Features

- Select and connect to available COM ports
- Choose standard baud rates (9600 to 115200)
- View live serial data in a scrollable text box
- Send messages to the connected serial device
- Clear display buffer
- Connection status indicator
- Threaded serial communication for non-blocking GUI

## Requirements

- Python 3.7+
- [PyQt6](https://pypi.org/project/PyQt6/)
- [pyserial](https://pypi.org/project/pyserial/)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pyqt6-serial-monitor.git
cd pyqt6-serial-monitor

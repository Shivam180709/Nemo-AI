from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette
import sys

class VoiceChatUI(QWidget):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.setWindowTitle("Voice Chat with Nemo")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: white;")  # Default background

        # Chat Logs Section
        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)
        self.chat_log.setPlaceholderText("Chat Logs will appear here...")
        self.chat_log.setStyleSheet("font-size: 14px; padding: 5px;")

        # Activate Button
        self.activate_button = QPushButton("Activate", self)
        self.activate_button.setFixedSize(100, 100)  # Making it a square
        self.activate_button.setStyleSheet("""
            QPushButton {
                border-radius: 50px;  /* Circular shape */
                background-color: #3498db; /* Default Blue */
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.activate_button.clicked.connect(self.toggle_activation)

        # Layouts
        layout = QHBoxLayout()
        layout.addWidget(self.activate_button)
        layout.addWidget(self.chat_log)

        self.setLayout(layout)

        # Timer for Animation
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.animate_button)
        self.color_index = 0
        self.colors = ["#e74c3c", "#f39c12", "#2ecc71", "#9b59b6", "#1abc9c"]  # Red, Orange, Green, Purple, Teal
        self.is_active = False

    def toggle_activation(self):
        if not self.is_active:
            self.is_active = True
            self.activate_button.setText("Deactivate")
            self.activate_button.setStyleSheet("""
                QPushButton {
                    border-radius: 50px;
                    background-color: #e74c3c;  /* Red */
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.setStyleSheet("background-color: #ecf0f1;")  # Change background color
            self.color_timer.start(500)  # Start animation every 500ms
        else:
            self.is_active = False
            self.activate_button.setText("Activate")
            self.activate_button.setStyleSheet("""
                QPushButton {
                    border-radius: 50px;
                    background-color: #3498db; /* Default Blue */
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.setStyleSheet("background-color: white;")  # Reset background color
            self.color_timer.stop()  # Stop animation

    def animate_button(self):
        if self.is_active:
            new_color = self.colors[self.color_index]
            self.activate_button.setStyleSheet(f"""
                QPushButton {{
                    border-radius: 50px;
                    background-color: {new_color};
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }}
            """)
            self.color_index = (self.color_index + 1) % len(self.colors)  # Cycle through colors

# Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceChatUI()
    window.show()
    sys.exit(app.exec_())

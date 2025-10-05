from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextBrowser, QDialog, QDialogButtonBox,
    QLineEdit, QLabel, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import sys


class EditDialog(QDialog):
    def __init__(self, title, current_text, multiline=False):
        super().__init__()
        self.setWindowTitle(f"Edit {title}")
        self.setFixedSize(400, 250)
        # Dark theme stylesheet
        STYLE_SHEET = """
            QWidget {
                background-color: #1f222b;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QTextBrowser {
                background-color: #2a2d3e;
                border: 1px solid #3c3f52;
                border-radius: 8px;
                padding: 8px;
            }

            QLineEdit, QTextEdit {
                background-color: #2a2d3e;
                border: 1px solid #4d4f63;
                border-radius: 6px;
                padding: 6px;
                color: #ffffff;
            }

            QPushButton {
                background-color: #f0a500;
                border: none;
                padding: 6px 14px;
                color: black;
                font-weight: bold;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #f8bb38;
            }

            QDialog {
                background-color: #1f222b;
            }

            QDialog QLabel {
                font-weight: bold;
                margin-bottom: 6px;
            }

            QDialogButtonBox QPushButton {
                background-color: #f0a500;
                color: black;
                padding: 5px 15px;
                border-radius: 5px;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #f8bb38;
            }
        """

        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{title}:"))

        if multiline:
            self.input = QTextEdit()
            self.input.setText(current_text)
        else:
            self.input = QLineEdit()
            self.input.setText(current_text)

        layout.addWidget(self.input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def getText(self):
        return self.input.toPlainText() if isinstance(self.input, QTextEdit) else self.input.text()

class ProfileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nemo AI Profile")
        self.setFixedSize(650, 400)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        # Name Section
        name_layout = QHBoxLayout()
        self.name_browser = QTextBrowser()
        self.name_browser.setText("Shivam Pathak")
        name_layout.addWidget(QLabel("👤 Name:"))
        name_layout.addWidget(self.name_browser)
        name_edit_btn = QPushButton("✏️")
        name_edit_btn.clicked.connect(self.editName)
        name_layout.addWidget(name_edit_btn)
        layout.addLayout(name_layout)

        # Spacer
        layout.addSpacing(20)

        # Brief Introduction Section
        brief_layout = QHBoxLayout()
        self.brief_browser = QTextBrowser()
        self.brief_browser.setText(
            "I’m Shivam Pathak, a 16-year-old Indian citizen with a deep passion for AI..."
        )
        brief_layout.addWidget(QLabel("🧠 Brief Intro:"))
        brief_layout.addWidget(self.brief_browser)
        brief_edit_btn = QPushButton("✏️")
        brief_edit_btn.clicked.connect(self.editBrief)
        brief_layout.addWidget(brief_edit_btn)
        layout.addLayout(brief_layout)

        self.setLayout(layout)

    def editName(self):
        dialog = EditDialog("Name", self.name_browser.toPlainText(), multiline=False)
        if dialog.exec_() == QDialog.Accepted:
            self.name_browser.setHtml(f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li
</style></head><body style=" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt; font-weight:600;">Name:</span><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt;"> 
{dialog.getText()}</span></p></body></html>""")

    def editBrief(self):
        dialog = EditDialog("Brief Introduction", self.brief_browser.toPlainText(), multiline=True)
        if dialog.exec_() == QDialog.Accepted:
            self.brief_browser.setText(dialog.getText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = ProfileWindow()
    window.show()
    sys.exit(app.exec_())

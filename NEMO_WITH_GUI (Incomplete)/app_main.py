import json
import sys
import subprocess
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QListWidgetItem, QListView, \
    QStyledItemDelegate, QStyle, QWidget, QHBoxLayout, QLineEdit, QAction, QSpacerItem, QSizePolicy, QAbstractItemView, \
    QGridLayout, QLabel, QFrame, QVBoxLayout, QItemDelegate, QDialogButtonBox
from PyQt5.QtCore import pyqtSlot, QSize, QStringListModel, QPoint
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QTextEdit, QDialogButtonBox)
from PyQt5.QtCore import Qt
from sidebar_ui import Ui_MainWindow
from home_window import HomeWindow
from chat_window import ChatWindow
from connect_db import ConnectDB
import PyQt5
import chatbot
import webbrowser
from PyQt5.QtCore import QThread, pyqtSignal
import time
#from widgets.chat_window_ui import Ui_Form as Chat_Form


class MemoryInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How It Works?")
        self.setFixedSize(450, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #1f222b;
                color: white;
                font-family: 'Segoe UI';
                font-size: 16px;
            }

            QLabel {
                color: #e0e0e0;
                font-size: 15px;
                line-height: 1.4;
            }

            QPushButton {
                background-color: #f0a500;
                color: black;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
                min-width: 240px;
            }

            QPushButton:hover {
                background-color: #f8bb38;
            }
        """)

        layout = QVBoxLayout()

        info_label = QLabel(
            "🧠 How Nemo Remembers You:\n\n"
            "You can teach Nemo new things by saving custom info to its memory.\n"
            "Whatever you want Nemo to remember gets added to a special memory file (a JSON file).\n"
            "This way, Nemo becomes smarter and more personal over time.\n\n"
            "🔧 To add something to memory:\n"
            "1. Click the 'Remember This' button or use a memory input section.\n"
            "2. Type what you want Nemo to remember (e.g., 'My birthday is Jan 1').\n"
            "3. It will be saved, and Nemo will use it in future replies.\n\n"
            "📌 Note: You can always update or clear memory as needed."
        )

        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addSpacing(20)

        #yt_button = QPushButton("📺 Watch Tutorial on YouTube")
        #yt_button.clicked.connect(self.open_youtube)
        #layout.addWidget(yt_button)

        self.setLayout(layout)

    #def open_youtube(self):
        # Replace with your real video URL
        #webbrowser.open("https://youtu.be/mQtyZ91QkGU")  

class ApiInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini API Info")
        self.setFixedSize(450, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #1f222b;
                color: white;
                font-family: 'Segoe UI';
                font-size: 16px;
            }

            QLabel {
                color: #e0e0e0;
                font-size: 15px;
                line-height: 1.4;
            }

            QPushButton {
                background-color: #f0a500;
                color: black;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
                min-width: 240px;
            }

            QPushButton:hover {
                background-color: #f8bb38;
            }
        """)

        layout = QVBoxLayout()

        info_label = QLabel(
            "To use Gemini AI, you need a Gemini API Key from Google AI Studio.\n\n"
            "1. Visit: https://aistudio.google.com/\n"
            "2. Sign in with your Google Account\n"
            "3. Go to 'API Keys' section\n"
            "4. Click 'Create API Key'\n"
            "5. Copy and paste it in the field provided in Nemo"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addSpacing(20)

        yt_button = QPushButton("📺 Watch Tutorial on YouTube")
        yt_button.clicked.connect(self.open_youtube)
        layout.addWidget(yt_button)

        self.setLayout(layout)

    def open_youtube(self):
        # Replace with your real video URL
        webbrowser.open("https://youtu.be/mQtyZ91QkGU")  

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
        l = QLabel(f"{title}:")
        l.setMaximumHeight(40)
        layout.addWidget(l)

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

class CustomWidget(QWidget):
    """
    create chat in chats list
    """

    def __init__(self, text, show_btn_flag, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        # Create layout for chat title
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)

        # create icon widget of chat title
        chat_icon = QIcon("static/icon/chat-left.svg")
        chat_icon_btn = QPushButton(self)
        chat_icon_btn.setIcon(chat_icon)

        # Create title widget to show title
        chat_title = QLineEdit(self)
        chat_title.setText(text)
        chat_title.setReadOnly(True)

        # Create delete and edit button for chat title
        delete_btn = QPushButton(self)
        delete_btn.setIcon(QIcon("static/icon/delete.svg"))

        edit_btn = QPushButton(self)
        edit_btn.setIcon(QIcon("static/icon/edit.svg"))

        # StyleSheet for QPushButton in chat title
        style_str = """
            QPushButton {
                border: none;
                max-width: 20px;
                max-height: 20px;
                background:transparent;
            }
        """
        # StyleSheet for QLineEdit in chat title
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: none;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """
        chat_title.setStyleSheet(chat_title_style)
        chat_icon_btn.setStyleSheet(style_str)
        edit_btn.setStyleSheet(style_str)
        delete_btn.setStyleSheet(style_str)

        if not show_btn_flag:
            # If not be selected, hide delete and edit button in chat title list
            delete_btn.hide()
            edit_btn.hide()

        # Add all the widgets of the chat title.
        layout.addWidget(chat_icon_btn)
        layout.addWidget(chat_title)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)


class ChatbotThread(QThread):
    def __init__(self):
        super().__init__()
        self._running = True
        import subprocess

    # Start the inner program
    def start_inner(self):
        global proc
        proc = subprocess.Popen(["python", "Nemo_Main_File.py"])
        print("Inner program started.")


    # Stop the inner program
    def stop_inner(self):
        proc.terminate()  # or proc.kill()
        print("Inner program stopped.")

    def run(self):
        print("Chatbot thread started")
        self.start_inner()


    def stop(self):
        print("Stopping chatbot thread")
        self.stop_inner()
        self.quit()
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize of the main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Instantiate the database object
        self.connect_db = ConnectDB()
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        # Get objects from main window
        self.message_input = self.ui.input_textEdit
        self.input_frame = self.ui.input_frame
        self.new_chat_btn = self.ui.new_chat_btn
        self.send_message_btn = self.ui.send_btn
        self.main_scrollArea = self.ui.scrollArea
        #self.robot_combo_box = self.ui.comboBox
        self.clear_conversations_btn = self.ui.pushButton_2
        #self.logout_btn = self.ui.pushButton_6
        self.addtomemory_btn = self.ui.addtomemory_btn
        self.openjsonfile_btn = self.ui.openjsonfile_btn
        self.clearmemory_btn = self.ui.clearmemory_btn
        self.memory_textEdit = self.ui.memory_textEdit
        self.profile_btn = self.ui.profile_btn
        self.voicechat_btn = self.ui.voicechat_btn
        self.textchat_btn = self.ui.textchat_btn
        self.Troubleshoot_btn = self.ui.Troubleshoot_btn
        self.name_textbrowser_btn = self.ui.name_textbrowser_btn
        self.name_textbrowser = self.ui.name_textbrowser
        self.briefintro_textbrowser = self.ui.briefintro_textbrowser
        self.briefintro_textbrowser_btn = self.ui.briefintro_textbrowser_btn
        self.system_instruction_textbrowser = self.ui.system_instruction_textbrowser
        self.system_instruction_textbrowser_btn = self.ui.system_instruction_textbrowser_btn
        self.apikey_label = self.ui.apikey_label
        self.api_edit_btn = self.ui.api_edit_btn
        self.api_info_btn = self.ui.api_info_btn
        self.activate_btn  = self.ui.activate_btn
        self.howitworks_btn = self.ui.howitworks_btn
        self.label_8 = self.ui.label_8
        self.voice_chatlog_text_browser = self.ui.voice_chatlog_text_browser
        self.voicechat_gif = self.ui.voicechat_gif
        # Hide scrollbar of scroll area
        self.main_scrollArea.setVerticalScrollBarPolicy(1)

        # Resize input frame and textEdit
        self.message_input.setFixedHeight(24)
        self.input_frame.setFixedHeight(42)

        # Set data for main chat and chat list when start app
        self.show_chat_list()
        self.show_home_window()

        # Set signal and slot
        self.howitworks_btn.clicked.connect(self.show_howitworks_btn)
        self.activate_btn.clicked.connect(self.toggle_voice_assistant)
        self.api_info_btn.clicked.connect(self.show_api_info)
        self.api_edit_btn.clicked.connect(self.editAPIkey)
        self.system_instruction_textbrowser_btn.clicked.connect(self.editSysteminfo)
        self.briefintro_textbrowser_btn.clicked.connect(self.editBrief)
        self.name_textbrowser_btn.clicked.connect(self.editName)
        self.Troubleshoot_btn.clicked.connect(self.troubleshoot_btn_ds)
        self.textchat_btn.clicked.connect(self.textchat_ds)
        self.voicechat_btn.clicked.connect(self.voicechat_ds)
        self.profile_btn.clicked.connect(self.profile_ds)
        self.clearmemory_btn.clicked.connect(self.clearjson)
        self.openjsonfile_btn.clicked.connect(self.openjson)
        self.addtomemory_btn.clicked.connect(self.extract_and_clear_text)

        self.send_message_btn.clicked.connect(self.get_response)
        self.new_chat_btn.clicked.connect(self.create_new_chat)
        self.clear_conversations_btn.clicked.connect(self.clear_conversations)

        self.gif_starter()

        

    ## Functions
    def gif_starter(self):
         
        l1= PyQt5.QtGui.QMovie(":/images/images/gif3.gif")
        self.voicechat_gif.setMovie(l1) 
        l1.start()
            

    def toggle_voice_assistant(self):
        if self.ui.activate_btn.text()=="Activate":
            print("Voice_Chat_Activated..")
            self.ui.activate_btn.setText("Deactivate")
            self.chatbot_thread = ChatbotThread()
            self.chatbot_thread.start()
        else:
            print("Voice_Chat_Deactivated..")
            self.ui.activate_btn.setText("Activate")
            if self.chatbot_thread:
                self.chatbot_thread.stop()
                self.chatbot_thread = None
        
    def append_to_json_file(self,file_path, new_data):
        try:
            # Step 1: Open and read the existing data from the JSON file
            with open(file_path, 'r') as file:
                try:
                    # Load the current content of the file into a list
                    data = json.load(file)
                    if not isinstance(data, list):
                        raise ValueError("The JSON file must contain a list at the top level.")
                except json.JSONDecodeError:
                    # If the file is empty or the content is not a valid JSON, we start with an empty list
                    data = []

            # Step 2: Append the new data to the list
            if isinstance(new_data, list):
                data.extend(new_data)  # Append if new_data is a list
            else:
                data.append(new_data)  # Append if new_data is a single object

            # Step 3: Write the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)

            print(f"Data successfully appended to {file_path}.")

        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_and_clear_text(self):
        text = self.memory_textEdit.toPlainText().strip()  # Get text and remove extra spaces

        if not text:  # Check if text is empty
            QSound.play(r"sounds\warning.wav")
            msg = QMessageBox()
            msg.setWindowTitle("Warning ⚠️")  # Icon beside title
            msg.setText("TextEdit is empty! Nothing to extract.")
            msg.setIcon(QMessageBox.Warning)  # Warning icon
            icon16 = QtGui.QIcon()
            icon16.addPixmap(QtGui.QPixmap(":/icon/icon/bot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            msg.setWindowIcon(QIcon(icon16))
            msg.exec_()
            return  # Stop further execution
        response_list = chatbot.get_response(text)
        print("Extracted Text:", text)  # Process the extracted text
        user_data = {
            "role": "user",
            "parts": [f"{text}"]
            }
        model_data = {
            "role": "model",
            "parts": [f"Ok I will remember it."]
            }
        self.append_to_json_file(r'datas/permanent_memory.json', user_data)  
        self.append_to_json_file(r'datas/permanent_memory.json', model_data)  
        self.memory_textEdit.clear()  # Clear QTextEdit

        # Success Message with sound and icon
        QSound.play(r"sounds\notification.wav")
        msg = QMessageBox()
        msg.setWindowTitle("Success ✅")  # Icon beside title
        msg.setText("Text extracted and cleared!")
        msg.setIcon(QMessageBox.Information)  # Information icon+
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icon/icon/bot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowIcon(QIcon(icon16))
        msg.exec_()

    def show_message_box(self):
        QSound.play(r"sounds\notification.wav")
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText("Are you sure.?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icon/icon/bot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg_box.setWindowIcon(QIcon(icon16))
       
        result = msg_box.exec_()
        
        if result == QMessageBox.Yes:
            with open(r"datas\permanent_memory.json", "w") as file:
                file.write("[]")  # Clears the file by writing an empty list
        else:
            print("User clicked No")

    def clearjson(self):
        
        self.show_message_box()
    
    def openjson(self):
        QSound.play(r"sounds\notification.wav")
        json_file = r"datas\permanent_memory.json"  # Change this to your JSON file path
        subprocess.Popen(["notepad.exe", json_file])
  
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    #Edit Button Functions

    def editName(self):
        dialog = EditDialog("Name", self.name_textbrowser.toPlainText().replace("Name:",""), multiline=False)
        if dialog.exec_() == QDialog.Accepted:
            self.name_textbrowser.setHtml(f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li
</style></head><body style=" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt; font-weight:600;">Name:</span><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt;"> 
{dialog.getText()}</span></p></body></html>""")
            
    def editBrief(self):
        dialog = EditDialog("Brief Introduction", self.briefintro_textbrowser.toPlainText().replace("Brief Introduction:",""), multiline=True)
        if dialog.exec_() == QDialog.Accepted:
            self.briefintro_textbrowser.setHtml(f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li
</style></head><body style=" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt; font-weight:600;">Brief Introduction:</span><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt;"> 
{dialog.getText()}</span></p></body></html>""")
            
    def editSysteminfo(self):
        dialog = EditDialog("System Instruction", self.system_instruction_textbrowser.toPlainText().replace("System Instruction:",""), multiline=True)
        if dialog.exec_() == QDialog.Accepted:
            self.system_instruction_textbrowser.setHtml(f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li
</style></head><body style=" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt; font-weight:600;">System Instruction:</span><span style=" font-family:'MS Shell Dlg 2'; font-size:11pt;"> 
{dialog.getText()}</span></p></body></html>""")
                  
    def editAPIkey(self):
        dialog = EditDialog("Enter You Gemini API key", self.apikey_label.text(), multiline=True)
        if dialog.exec_() == QDialog.Accepted:
            self.apikey_label.setText(dialog.getText())
    
    
    def show_api_info(self):
        dialog = ApiInfoDialog()
        dialog.exec_()

    def show_howitworks_btn(self):
        dialog = MemoryInfoDialog()
        dialog.exec_()

    def start_voice_assistant(self):
        if not self.voice_thread.isRunning():
            self.voice_thread.start()



    ## Function for changing page to user page
    def textchat_ds(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def troubleshoot_btn_ds(self): 
        pass

    def voicechat_ds(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def profile_ds(self):
        self.ui.stackedWidget.setCurrentIndex(6)
    
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashborad_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_dashborad_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_orders_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_orders_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_products_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_products_btn_2_toggled(self, ):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_customers_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_customers_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    ## Functions for main window //////////////////////
    # Create a new chat
    def create_new_chat(self):
        self.show_home_window()
        self.show_chat_list(selected_index=None)

    # Delete all the chats from chat list
    def clear_conversations(self):
        self.connect_db.delete_all_data()
        self.show_home_window()
        self.show_chat_list()


    # Adjust input height by text height
    def on_input_textEdit_textChanged(self):
        document = self.message_input.document()
        self.message_input.setFixedHeight(int(document.size().height()))
        self.input_frame.setFixedHeight(int(document.size().height() + 18))

    ## Functions for chat list ///////////////////////////////
    # Delete a chat form chat list
    def delete_chat_data(self):
        # Get current selected chat index
        selected_chat_index = self.ui.chat_list.currentIndex()
        index = selected_chat_index.row()

        # Delete the chat from database
        self.connect_db.delete_chat_data(index)

        # Reload window
        self.show_home_window()
        self.show_chat_list()

    # Function for clearing all the widgets in chat window when reload chat window
    def clear_main_scroll_area(self):
        # Get QGridLayout object from scroll area
        grid_layout = self.main_scrollArea.findChild(QGridLayout)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Get all the objects in main chat window
        children_list = grid_layout.children()
        remove_widget_list = [QLabel, QPushButton, QFrame]
        for remove_widget in remove_widget_list:
            children_list += self.main_scrollArea.findChildren(remove_widget)

        # Delete all the found object
        for child in children_list:
            child.deleteLater()

        # Remove all the spacer items from the grid layout
        for row in range(grid_layout.rowCount()):
            for column in range(grid_layout.columnCount()):
                item = grid_layout.itemAtPosition(row, column)
                if item:
                    grid_layout.removeItem(item)

        return grid_layout

    # Signal and slot function for chat list(QListView)
    def on_chat_list_clicked(self):
        chat_list = []

        # Clear input when change chat
        self.message_input.clear()
        # Get select row
        current_index = self.ui.chat_list.currentIndex()
        select_row = current_index.row()

        # Get the count of chat list
        chat_models = self.ui.chat_list.model()
        chat_count = chat_models.rowCount()

        # Traverse chat list in window
        for i in range(chat_count):
            row_index = chat_models.index(i, 0)
            current_chat = self.ui.chat_list.indexWidget(row_index)
            chat_title = current_chat.findChild(QLineEdit)
            if chat_title:
                # Check if the chat state is waiting to delete
                if i == select_row and chat_title.text().startswith("Delete \""):
                    chat_list.append(chat_title.text().split('"')[1])
                else:
                    chat_list.append(chat_title.text())
            else:
                chat_list.append("")

        # Reload chat list
        for row, chat in enumerate(chat_list):
            index = chat_models.index(row, 0)
            # Check if the chat title is selected?
            if row == select_row:
                show_btn_flag = True
            else:
                show_btn_flag = False

            # Create chat title widget
            widget = CustomWidget(chat, show_btn_flag)

            # Set and show chat title in chat list(QListView)
            self.ui.chat_list.setIndexWidget(index, widget)

            # Get QPushButton object in  chat title widget
            operation_btn = widget.findChildren(QPushButton)

            # Connect signal and slot for buttons
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)

            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)

        # Get the selected chat data and show it in main chat content window
        chat_db = self.connect_db.get_chat_data()
        chat_data = chat_db[select_row]
        self.show_chat_window(chat_data)

    @pyqtSlot()
    def edit_chat(self):
        current_index = self.ui.chat_list.currentIndex()
        current_chat = self.ui.chat_list.indexWidget(current_index)

        chat_title = current_chat.findChild(QLineEdit)

        # Get original chat title
        pre_chat_title = chat_title.text()

        chat_title.setReadOnly(False)
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: 1px solid #2563eb;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """

        chat_title.setStyleSheet(chat_title_style)

        operation_btns = current_chat.findChildren(QPushButton)
        confirm_btn = operation_btns[2]
        cancel_btn = operation_btns[1]

        confirm_btn.setIcon(QIcon("static/icon/check-lg.svg"))
        cancel_btn.setIcon(QIcon("static/icon/x-lg.svg"))

        confirm_btn.clicked.disconnect()
        cancel_btn.clicked.disconnect()

        confirm_btn.clicked.connect(lambda: self.confirm_edit(chat_title))
        cancel_btn.clicked.connect(lambda: self.cancel_edit(pre_chat_title, chat_title))

    @pyqtSlot()
    def confirm_edit(self, chat_title):
        current_index = self.ui.chat_list.currentIndex().row()

        chat_db = self.connect_db.get_chat_data()
        chat_db[current_index]["title"] = chat_title.text()

        self.connect_db.save_chat_data(chat_db)
        self.on_chat_list_clicked()

    @pyqtSlot()
    def cancel_edit(self, pre_chat_title, chat_title):
        chat_title.setText(pre_chat_title)
        self.on_chat_list_clicked()

    @pyqtSlot()
    def delete_chat(self):
        current_index = self.ui.chat_list.currentIndex()
        current_chat = self.ui.chat_list.indexWidget(current_index)

        chat_title = current_chat.findChild(QLineEdit)
        chat_title.setReadOnly(True)
        chat_title_text = chat_title.text()
        chat_title.setText(f'Delete "{chat_title_text}"?')
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: none;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """

        chat_title.setStyleSheet(chat_title_style)

        operation_btns = current_chat.findChildren(QPushButton)
        chat_icon_btn = operation_btns[0]
        confirm_btn = operation_btns[2]
        cancel_btn = operation_btns[1]

        chat_icon_btn.setIcon(QIcon("static/icon/delete.svg"))
        confirm_btn.setIcon(QIcon("static/icon/check-lg.svg"))
        cancel_btn.setIcon(QIcon("static/icon/x-lg.svg"))

        confirm_btn.clicked.disconnect()
        cancel_btn.clicked.disconnect()

        confirm_btn.clicked.connect(self.confirm_delete)
        cancel_btn.clicked.connect(self.cancel_delete)

    @pyqtSlot()
    def confirm_delete(self):
        current_index = self.ui.chat_list.currentIndex()
        index = current_index.row()
        chat_db = self.connect_db.get_chat_data()
        chat_db.pop(index)

        self.connect_db.save_chat_data(chat_db)
        self.show_home_window()
        self.show_chat_list()

    @pyqtSlot()
    def cancel_delete(self):
        self.on_chat_list_clicked()

    # Show a default window if there is no chat is selected
    def show_home_window(self):
        grid_layout = self.clear_main_scroll_area()
        # show new message
        home_window = HomeWindow()
        grid_layout.addWidget(home_window)

    # Show one chat data in main chat content window
    def show_chat_window(self, chat_data):
        grid_layout = self.clear_main_scroll_area()
        # show new message
        chat_window = ChatWindow(chat_object=self.message_input, chat_data=chat_data)
        grid_layout.addWidget(chat_window)

    # Show chat title list in chat list window
    def show_chat_list(self, selected_index=None):
        # Create QStandardItemModel for show chat title list
        model = QStandardItemModel()
        self.ui.chat_list.setModel(model)
        # Get chat title list from database
        chat_list = self.connect_db.get_chat_title_list()

        for chat in chat_list:
            item = QStandardItem()
            model.appendRow(item)

            index = item.index()
            index_text = index.row()

            if index_text == selected_index:
                show_btn_flag = True
                # Set current item selected
                self.ui.chat_list.setCurrentIndex(index)
            else:
                show_btn_flag = False

            # Create chat title widget
            widget = CustomWidget(chat, show_btn_flag)

            # Set and show chat title in chat list(QListView)
            self.ui.chat_list.setIndexWidget(index, widget)

            # Get QPushButton object in  chat title widget
            operation_btn = widget.findChildren(QPushButton)

            # Connect signal and slot for buttons
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)

            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)

    # Get response and show it from ChatGPT
    def get_response(self):
        message_input = self.message_input.toPlainText().strip()

        chat_db = self.connect_db.get_chat_data()

        if message_input:
            response_list = chatbot.get_response(message_input)
            response_str = response_list
            # response_str = "Example"

            # Check if open a chat
            if self.ui.chat_list.selectedIndexes():
                # Get current selected chat index
                current_index = self.ui.chat_list.currentIndex()
                select_row = current_index.row()

                chat_db[select_row]["chat_list"] += [{"input_str": message_input, "out_str": response_str}]
                chat_data = chat_db[select_row]

                self.connect_db.save_chat_data(chat_db)
                self.show_chat_window(chat_data)

            else:
                # Create new chat and save it into database
                chat_data = {
                    "title": message_input,
                    "chat_list": [
                        {
                            "input_str": message_input,
                            "out_str": response_str
                        }
                    ]
                }
                chat_db.insert(0, chat_data)
                self.connect_db.save_chat_data(chat_db)

                # Reload window
                self.show_chat_window(chat_data)
                self.show_chat_list(selected_index=0)

            ## Clear input after get response
            self.message_input.clear()

        else:
            # msg_box = QMessageBox()
            # msg_box.setStyleSheet("QPushButton{text-align: center;}")
            # msg_box.information(self, "Note", "Please input content first.")
            return

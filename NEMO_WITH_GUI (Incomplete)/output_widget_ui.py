import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from widgets.out_widget_ui import Ui_Form  # Import the generated UI class
import pyttsx3


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1])
engine.setProperty('rate', 165)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
engine.setProperty('voice', voices[0].id)  


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Create a new class that extends QWidget to use the generated UI
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Connect the speak button to a function
        self.ui.speak_btn.clicked.connect(self.handle_speak_button)

    def handle_speak_button(self):
        """
        Slot to handle the speak button click.
        Runs the speak_text function in a separate thread.
        """
        text = self.ui.label_4.text()  # Get the text from the label
        if text.strip():  # Ensure there is text to speak
            thread = threading.Thread(target=speak, args=(text,), daemon=True)
            thread.start()


# Main application execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

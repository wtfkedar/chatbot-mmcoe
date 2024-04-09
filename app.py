from tkinter import *
import json
from difflib import SequenceMatcher

BG_GRAY = "#ABB289"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.data = self.load_data_from_json('intents.json')

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # Head label
        self.head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                                text="Welcome", font=FONT_BOLD, pady=10)
        self.head_label.place(relwidth=1)

        # Divider
        self.line = Label(self.window, width=450, bg=BG_GRAY)
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Scrollbar
        self.scrollbar = Scrollbar(self.text_widget)
        self.scrollbar.place(relheight=1, relx=0.974)
        self.scrollbar.configure(command=self.text_widget.yview)

        # Bottom label
        self.bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        self.bottom_label.place(relwidth=1, rely=0.825)

        # Message entry box
        self.msg_entry = Entry(self.bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Send button
        self.send_button = Button(self.bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                  command=lambda: self._on_enter_pressed(None))
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def load_data_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['intents']

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_response_from_json(self, question):
        max_similarity = 0
        response = None
        for item in self.data:
            for pattern in item['patterns']:
                similarity = self.similar(question.lower(), pattern.lower())
                if similarity > max_similarity:
                    max_similarity = similarity
                    response = item['responses'][0]  # We assume the first response in the list
        return response if max_similarity > 0.6 else None

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        self.msg_entry.delete(0, END)  # Clear the entry box after sending the message

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, f"{sender}: {msg}\n\n")
        self.text_widget.configure(state=DISABLED)

        # Get response and display it
        response = self.get_response_from_json(msg)
        if response:
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, f"Bot: {response}\n\n")
            self.text_widget.configure(state=DISABLED)
        else:
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, "Bot: Sorry, I don't understand.\n\n")
            self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ChatApplication()
    app.run()

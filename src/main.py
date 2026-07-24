import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

from main import load_signatures, scan_directory
from project import PROJECT

class MinerRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.status_label = Label(text="Ready", size_hint=(1, 0.1))
        self.add_widget(self.status_label)

        self.results_label = Label(text="", size_hint_y=None)
        self.results_label.bind(texture_size=self.results_label.setter("size"))

        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.results_label)
        self.add_widget(scroll)

        scan_button = Button(text="Choose folder and scan", size_hint=(1, 0.2))
        scan_button.bind(on_press=self.open_file_chooser)
        self.add_widget(scan_button)

    def open_file_chooser(self, instance):
        chooser = FileChooserIconView(path=os.path.expanduser("~"), dirselect=True)
        popup = Popup(title="Select folder", content=chooser, size_hint=(0.9, 0.9))

        def on_selection(instance, selection):
            if selection:
                popup.dismiss()
                self.run_scan(selection[0])

        chooser.bind(selection=on_selection)
        popup.open()

    def run_scan(self, path):
        self.status_label.text = f"Scanning {path}..."
        signatures = load_signatures()
        results = scan_directory(path, signatures)

        if results:
            self.status_label.text = f"Found {len(results)} threat(s)"
            self.results_label.text = "\n".join(
                f"[!] {r['path']}\n    {r['threat']} ({r['hash'][:12]}...)"
                for r in results
            )
        else:
            self.status_label.text = "No threats found"
            self.results_label.text = ""

class MinerApp(App):
    def build(self):
        self.title = PROJECT["name"]
        return MinerRoot()

if __name__ == "__main__":
    MinerApp().run()

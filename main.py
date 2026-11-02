from kivy.app import App
from kivy.uix.button import Button

class TalypApp(App):
    def build(self):
        return Button(
            text="Talyp dolandyryş ulgamy",
            font_size=24
        )

TalypApp().run()

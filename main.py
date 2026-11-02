
import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class TalypApp(App):

    def build(self):
        self.students = []
        self.file = os.path.join(
            self.user_data_dir, "students.json"
        )

        self.load_data()

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        root.add_widget(Label(
            text="TALYP DOLANDYRYŞ ULGAMY",
            font_size=23,
            size_hint_y=None,
            height=55
        ))

        self.name = TextInput(
            hint_text="Talyp ady",
            multiline=False,
            size_hint_y=None,
            height=48
        )

        self.age = TextInput(
            hint_text="Ýaşy",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=48
        )

        self.grade = TextInput(
            hint_text="Synpy",
            multiline=False,
            size_hint_y=None,
            height=48
        )

        root.add_widget(self.name)
        root.add_widget(self.age)
        root.add_widget(self.grade)

        self.status = Label(
            text="Taýýar",
            size_hint_y=None,
            height=35
        )
        root.add_widget(self.status)

        buttons = GridLayout(
            cols=2,
            spacing=6,
            size_hint_y=None,
            height=110
        )

        actions = [
            ("Talyp goş", self.add_student),
            ("Talyplary görkez", self.show_students),
            ("Talyp gözle", self.search_student),
            ("Talyp poz", self.delete_student)
        ]

        for title, action in actions:
            btn = Button(text=title)
            btn.bind(on_press=action)
            buttons.add_widget(btn)

        root.add_widget(buttons)

        scroll = ScrollView()

        self.student_list = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.student_list.bind(
            minimum_height=self.student_list.setter(
                "height"
            )
        )

        scroll.add_widget(self.student_list)
        root.add_widget(scroll)

        self.show_students()
        return root

    def load_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    self.students = json.load(f)
            except:
                self.students = []

    def save_data(self):
        with open(self.file, "w") as f:
            json.dump(self.students, f)

    def add_student(self, instance):
        name = self.name.text.strip()
        age = self.age.text.strip()
        grade = self.grade.text.strip()

        if not name or not age or not grade:
            self.status.text = "Ähli maglumatlary doldur!"
            return

        student = {
            "name": name,
            "age": age,
            "grade": grade
        }

        self.students.append(student)
        self.save_data()

        self.name.text = ""
        self.age.text = ""
        self.grade.text = ""

        self.status.text = "Talyp goşuldy!"
        self.show_students()

    def show_students(self, instance=None):
        self.student_list.clear_widgets()

        if not self.students:
            self.student_list.add_widget(
                Label(text="Talyp ýok", size_hint_y=None,
                      height=45)
            )
            return

        for i, s in enumerate(self.students, 1):
            self.student_list.add_widget(
                Label(
                    text=f"{i}. {s['name']} | "
                         f"{s['age']} ýaş | {s['grade']}",
                    size_hint_y=None,
                    height=45
                )
            )

    def search_student(self, instance):
        search = self.name.text.strip().lower()

        self.student_list.clear_widgets()
        found = [
            s for s in self.students
            if s["name"].lower() == search
        ]

        if not found:
            self.status.text = "Talyp tapylmady!"
            return

        for s in found:
            self.student_list.add_widget(
                Label(
                    text=f"{s['name']} | {s['age']} | {s['grade']}",
                    size_hint_y=None,
                    height=45
                )
            )

        self.status.text = "Talyp tapyldy!"

    def delete_student(self, instance):
        name = self.name.text.strip().lower()

        for s in self.students:
            if s["name"].lower() == name:
                self.students.remove(s)
                self.save_data()
                self.status.text = "Talyp pozuldy!"
                self.show_students()
                return

        self.status.text = "Talyp tapylmady!"


TalypApp().run()

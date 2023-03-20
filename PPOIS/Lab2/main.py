from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window

from Lab2.src.DAO.PetDAO import PetDAO
from Lab2.src.checkers.Checker import Checker
from Lab2.src.erorrs.DateIsNotValid import DateIsNotValid
from Lab2.src.models.pet import Pet

SIZE = {'width': 1100, 'height': 550}

Window.size = (SIZE.get('width'), SIZE.get('height'))


class ErrorPopup(Popup):

    def open(self, text, *_args, **kwargs):
        label = Label(size_hint=(1, 0.9))
        label.text = text
        bl = BoxLayout(orientation='vertical', size=(SIZE.get('width'), SIZE.get('height')))
        self.add_widget(bl)
        bl.add_widget(label)
        bl.add_widget(Button(text="cancel", size_hint=(1, 0.1), on_press=self.dismiss))
        super().open(*_args, **kwargs)


class MyWidget(GridLayout):

    def __init__(self, parent_popup: Popup, label: Label, **kwargs):
        self.popup = parent_popup
        super().__init__(**kwargs)
        self.label = label

    def selected(self, filename):
        try:
            petDAO.path = filename[0]
            for pet in petDAO.get_first_page():
                self.label.text = self.label.text + str(pet)+"\n"
            self.popup.dismiss()
        except:
            pass


class MyApp(App):
    __page_counter = 0

    def print_info(self):
        self.label.text = ''
        if petDAO.path != '':
            for pet in petDAO.get_page(self.__page_counter):
                self.label.text = self.label.text + "\n " + str(pet)

    def first_page(self, instance):
        petDAO.get_first_page()
        self.__page_counter = 0
        self.print_info()

    def prev_page(self, instance):
        if self.__page_counter>0:
            self.__page_counter -= 1
            self.print_info()

    def next_page(self, instance):
        if self.__page_counter < int((len(petDAO.read()) - 1) / petDAO.SIZE):
            self.__page_counter += 1
            self.print_info()

    def last_page(self, instance):
        self.__page_counter = int((len(petDAO.read())-1)/petDAO.SIZE)
        self.print_info()

    def delete(self, instance):
        popup = Popup(size=(SIZE.get('width') / 10, SIZE.get('height') / 10), title='delete')

        bl = BoxLayout(orientation='vertical')
        bl.add_widget(Label(text='variants of delete'))

        bl.add_widget(
            Button(text='pets name and birth date', on_press=partial(self.delete_popup, ['name', 'birth date'], popup)))

        bl.add_widget(Button(text='date of last admission and veterinarians name',
                             on_press=partial(self.delete_popup, ['date of last admission', 'veterinarians name'], popup)))

        bl.add_widget(Button(text='diagnosis', on_press=partial(self.delete_popup, ['diagnosis'], popup)))

        bl.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.add_widget(bl)
        popup.open()

    def delete_popup(self, lst: list, parent_popup: Popup, instance):
        popup = Popup(size=(SIZE.get('width'), SIZE.get('height')), title='delete pet')
        bl = BoxLayout(orientation='vertical')
        popup.add_widget(bl)
        tis = []
        if len(lst) == 2:
            ti_1 = TextInput(text='', hint_text=lst[0])
            bl.add_widget(ti_1)
            ti_2 = TextInput(text='', hint_text=lst[1])
            bl.add_widget(ti_2)
            tis = [ti_1, ti_2]

        if len(lst) == 1:
            ti_0 = TextInput(text='', hint_text=lst[0])
            bl.add_widget(ti_0)
            tis = [ti_0]

        bl.add_widget(Button(text='delete', on_press=partial(self.try_delete, lst, tis, parent_popup, popup)))
        bl.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.open()

    def try_delete(self, lst: list, tis: list, parent_popup: Popup, popup: Popup, instance):
        if lst[0] == 'name':
            petDAO.delete_by_name_and_birth_date(tis[0].text, tis[1].text)
        if lst[0] == 'date of last admission':
            petDAO.delete_by_veterinarians_name_and_date_of_last_admission(tis[0].text, tis[1].text)
        if len(lst) == 1:
            petDAO.delete_by_part_of_diagnosis(tis[0].text)
        self.__page_counter = 0
        self.print_info()
        popup.dismiss()
        parent_popup.dismiss()

    def search(self, instance):
        popup = Popup(size=(SIZE.get('width')/10, SIZE.get('height')/10), title='search')

        bl = BoxLayout(orientation='vertical')
        bl.add_widget(Label(text='variants of search'))

        bl.add_widget(Button(text='pets name and birth date', on_press=partial(self.search_popup, ['name', 'birth date'])))

        bl.add_widget(Button(text='date of last admission and veterinarians name', on_press=partial(self.search_popup, ['date of last admission', 'veterinarians name'])))

        bl.add_widget(Button(text='diagnosis', on_press=partial(self.search_popup, ['diagnosis'])))

        bl.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.add_widget(bl)
        popup.open()

    def search_popup(self, lst: list, instance):
        popup = Popup(size=(SIZE.get('width'), SIZE.get('height')), title='search pet')
        bl = BoxLayout(orientation='vertical')
        popup.add_widget(bl)
        tis = []
        if len(lst) == 2:
            ti_1 = TextInput(text='', hint_text=lst[0])
            bl.add_widget(ti_1)
            ti_2 = TextInput(text='', hint_text=lst[1])
            bl.add_widget(ti_2)
            tis = [ti_1, ti_2]

        if len(lst) == 1:
            ti_0 = TextInput(text='', hint_text=lst[0])
            bl.add_widget(ti_0)
            tis = [ti_0]

        bl.add_widget(Button(text='search', on_press=partial(self.try_search, lst, tis)))
        bl.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.open()

    def try_search(self, lst: list, tis: list, instance):
        try:
            if lst[0] == 'name':
                self.open_result(petDAO.combining(petDAO.find_by_name(tis[0].text), petDAO.find_by_birth_date(tis[1].text)))
            if lst[0] == 'date of last admission':
                self.open_result(petDAO.combining(petDAO.find_by_veterinarians_name(tis[1]), petDAO.find_by_date_of_last_admission(tis[0].text)))
            if len(lst) == 1:
                self.open_result(petDAO.find_by_part_or_diagnosis(tis[0].text))
        except DateIsNotValid as e:
             ErrorPopup().open(str(e))

    def open_result(self, lst):
        popup = Popup(title='result', size=(SIZE.get('width'), SIZE.get('height')))
        bl = BoxLayout(orientation='vertical')
        label = Label(text='')
        print(len(lst))
        for pet in lst:
            label.text = label.text+"\n"+str(pet)

        bl.add_widget(label)
        bl.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.add_widget(bl)
        popup.open()

    def add(self, instance):
        popup = Popup(size=(SIZE.get('width'), SIZE.get('height')), title='add pet')

        add_popup = BoxLayout(orientation='vertical')

        ti_name = TextInput(text='', hint_text='name')
        add_popup.add_widget(ti_name)

        ti_birth_date = TextInput(text='', hint_text='birth date')
        add_popup.add_widget(ti_birth_date)

        ti_date_of_last_admission = TextInput(text='', hint_text='date of last admission')
        add_popup.add_widget(ti_date_of_last_admission)

        ti_veterinarians_name = TextInput(text='', hint_text='veterinarians name')
        add_popup.add_widget(ti_veterinarians_name)

        ti_diagnosis = TextInput(text='', hint_text='diagnosis')
        add_popup.add_widget(ti_diagnosis)

        add_popup.add_widget(Button(text='save', on_press=partial(self.add_pet, popup, add_popup)))
        add_popup.add_widget(Button(text='cancel', on_press=popup.dismiss))
        popup.add_widget(add_popup)
        popup.open()

    def add_pet(self,  popup, add_popup: BoxLayout, instance):
        pet = Pet()
        pet.name = add_popup.children[6].text
        pet.birth_date = add_popup.children[5].text
        pet.date_of_last_admission = add_popup.children[4].text
        pet.veterinarians_name = add_popup.children[3].text
        pet.diagnosis = add_popup.children[2].text
        if not Checker.date_is_valid(pet.birth_date) or not Checker.date_is_valid(pet.date_of_last_admission):
            ErrorPopup().open("invalid date")
        else:
                petDAO.add(pet)
                self.__page_counter = 0
                self.print_info()
                popup.dismiss()

    def open_file(self, instance):
        popup = Popup(title='choose file')
        bl = BoxLayout(orientation='vertical')
        file_chooser = MyWidget(parent_popup=popup, label=self.label, size_hint=(1, .9))
        bl.add_widget(file_chooser)
        bl.add_widget(Button(text='cancel', on_press=popup.dismiss, size_hint=(1, .1)))
        popup.add_widget(bl)
        popup.open()

    def build(self):
        self.label = Label()
        self.print_info()
        popup = Popup(title='Pets info', content=self.label, size_hint=(1, 0.9))
        main_layout = BoxLayout(orientation='horizontal')
        bl = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
        bl.add_widget(popup)
        buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10, padding=10)
        buttons.add_widget(Button(text='<<', on_press=self.first_page))
        buttons.add_widget(Button(text="<", on_press=self.prev_page))
        buttons.add_widget(Button(text='>', on_press=self.next_page))
        buttons.add_widget(Button(text='>>', on_press=self.last_page))
        bl.add_widget(buttons)
        main_buttons = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=10, padding=10)
        main_buttons.add_widget(Button(text='search', on_press=self.search))
        main_buttons.add_widget(Button(text='delete', on_press=self.delete))
        main_buttons.add_widget(Button(text='add', on_press=self.add))
        main_buttons.add_widget(Button(text='open', on_press=self.open_file))
        main_buttons.add_widget(Widget())
        main_buttons.add_widget(Widget())
        main_layout.add_widget(bl)
        main_layout.add_widget(main_buttons)
        return main_layout


if __name__ == "__main__":
    petDAO = PetDAO()
    MyApp().run()

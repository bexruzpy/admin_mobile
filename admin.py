from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import requests
import pickle
import requests  # So'rov yuborish uchun kerak

# from kivy.core.text import LabelBase
# LabelBase.register(name='NotoSans', fn_regular='fonts/NotoSans-Regular.ttf')


token = ""
try:
    with open("data.db", "rb") as file:
        token = pickle.load(file)
except:
    with open("data.db", "wb") as file:
        pickle.dump(token, file)

def refresh():
    with open("data.db", "wb") as file:
        pickle.dump(token, file)

# Asosiy menyu ekrani
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')  # Vertikal tartibda joylashtirish
        btn1 = Button(text="Hisob", on_press=self.switch_to_first, size_hint_y=0.7)
        btn2 = Button(text="Payment", on_press=self.switch_to_second)
        btn3 = Button(text="About user", on_press=self.switch_to_third)
        btn4 = Button(text="chiqish", on_press=self.quit, size_hint_y=0.7)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)
        self.add_widget(layout)

    def switch_to_first(self, instance):
        self.manager.current = 'first'

    def switch_to_second(self, instance):
        self.manager.current = 'second'

    def switch_to_third(self, instance):
        self.manager.current = 'third'
    def quit(self, instance):
    	app.stop()
# 1-oyna (Birinchi ekran)
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        
        # Vertikal joylashtirish
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        btn = Button(text="Asosiy menyuga qaytish", on_press=self.switch_to_main_menu)
        layout.add_widget(btn)
        try:
            res = requests.get(f"https://api.projectsplatform.uz/admin/about_admin?token={token}")
            self.fullname_label = Label(text=f'F.I.SH: {res.json()["full_name"]}', halign="left")
            layout.add_widget(self.fullname_label)
            self.username_label = Label(text=f'Username: {res.json()["username"]}', halign="left")
            layout.add_widget(self.username_label)
        except Exception as e:
            print(e)
            self.fullname_label = Label(text='F.I.SH: -', halign="left")
            layout.add_widget(self.fullname_label)
            self.username_label = Label(text='Username: -', halign="left")
            layout.add_widget(self.username_label)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        layout.add_widget(self.username_input)
        
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        layout.add_widget(self.password_input)
        
        send_code_btn = Button(text="Send Code", on_press=self.send_code)
        layout.add_widget(send_code_btn)

        self.code_input = TextInput(hint_text="Code", multiline=False)
        layout.add_widget(self.code_input)
        
        login_btn = Button(text="LOGIN", on_press=self.login)
        layout.add_widget(login_btn)
        self.lab = Label(text='', halign="left", size_hint_y=7)
        layout.add_widget(self.lab)
        self.add_widget(layout)
    
    def send_code(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        res = requests.post(f"https://api.projectsplatform.uz/admin/login", json={"username": username, "password": password})
        print(res.json())

    def login(self, instance):
        global token
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        code = self.code_input.text.strip()
        try:
            res = requests.post(f"https://api.projectsplatform.uz/admin/check-login", json={"username": username, "password": password, "code": int(code)})
            token = res.json()["token"]
            print(token)
            refresh()
            res = requests.get(f"https://api.projectsplatform.uz/admin/about_admin?token={token}")
            self.fullname_label.text = f'F.I.SH: {res.json()["full_name"]}'
            self.username_label.text = f'Username: {res.json()["username"]}'
        except Exception as e:
            print(e)

    def switch_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

# 2-oyna (Ikkinchi ekran)
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        btn = Button(text="Asosiy menyuga qaytish", on_press=self.switch_to_main_menu)
        layout.add_widget(btn)

        self.tg_id_input = TextInput(hint_text="Telegram ID", multiline=False)
        layout.add_widget(self.tg_id_input)

        self.summ_input = TextInput(hint_text="So'm", multiline=False)
        layout.add_widget(self.summ_input)

        # Fayl yorlig'i va tugmasini joylashtirish uchun horizontal BoxLayout
        file_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=1, height=40)
        self.file_label = Label(text='Kvitansiya:')
        self.open_btn = Button(text='||', size_hint=(0.3, 1))
        self.open_btn.bind(on_press=self.open_filechooser)

        # Label va Buttonni horizontal BoxLayout ichiga qo'shamiz
        file_layout.add_widget(self.file_label)
        file_layout.add_widget(self.open_btn)
        layout.add_widget(file_layout)
        
        self.bio_input = TextInput(hint_text="To'lov habari uchun izoh", multiline=False, text = 'Bizga ishonch bildirganingizdan mamnunmiz!', size_hint_y=5)
        layout.add_widget(self.bio_input)


        self.mall = Label(text="", halign="left")
        layout.add_widget(self.mall)


        login_btn = Button(text="O'tkazish", on_press=self.pay, size_hint_y=2)
        layout.add_widget(login_btn)
        self.lab = Label(text='', halign="left", size_hint_y=10)
        layout.add_widget(self.lab)
        self.selected_file = None  # Tanlangan faylni saqlash uchun

        self.add_widget(layout)

    def open_filechooser(self, instance):
        # Fayl tanlash uchun FileChooserIconView ni yaratamiz
        filechooser = FileChooserIconView()

        # FileChooserIconView va Button ni BoxLayout ichiga joylashtiramiz
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)

        # Faylni tanlash tugmasi
        select_btn = Button(text='Tanlash', size_hint=(1, 0.2))
        select_btn.bind(on_press=lambda x: self.load_file(filechooser.selection))
        layout.add_widget(select_btn)

        # Popup yaratib, BoxLayout ni kontent sifatida qo'shamiz
        self.popup = Popup(title='Faylni tanlang', content=layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_file(self, selection):
        if selection:
            self.selected_file = selection[0]  # Fayl nomini saqlash
            self.file_label.text = f'Tanlangan fayl: {self.selected_file}'
            print(f"Yuklangan fayl: {self.selected_file}")
        self.popup.dismiss()

    def pay(self, instance):
        tg_id = self.tg_id_input.text
        summa = self.summ_input.text
        bio = self.bio_input.text

        # Admin tokenni kiriting
        admin_token = token  # Bu joyda admin tokeningizni kiriting

        # Kerakli ma'lumotlarni tekshirish
        if not tg_id.strip().isdigit() or not summa.strip().isdigit():
            self.show_success_message("Xatolik","Telegram ID va to'lov summasi faqat raqamlar bo'lishi kerak!")
            return

        if not self.selected_file:
            self.show_success_message("Yetishmaslik","Iltimos, kvitansiya uchun screenshot tanlang!")
            return

        # So'rov yuborish
        url = "https://api.projectsplatform.uz/admin/payment"  # API'ning haqiqiy manzilini kiriting
        headers = {"Authorization": f"Bearer {admin_token}"}

        # So'rov ma'lumotlari
        data = {
            "admin_token": admin_token,
            "tg_id": int(tg_id),
            "tulov_summasi": int(summa),
            "bio": "bio",
        }

        # Faylni ochish va yuborish
        with open(self.selected_file, "rb") as file:
            files = {"payment_chek_img": file}
            response = requests.post(url, headers=headers, data=data, files=files)

        # Javobni qayta ishlash
        print(response.text)
        if response.status_code == 200:
            print("To'lov muvaffaqiyatli amalga oshirildi!")
            self.mall.text = f"Username: {tg_id}\nO'tkazildi: {int(summa):,} so'm"
            self.show_success_message("./ - To'lov muvaffaqiyatli\namalga oshirildi!", f"Username: {tg_id}\nO'tkazildi: {int(summa):,} so'm")  # Muvaffaqiyatli xabar
        else:
            print(f"Xatolik yuz berdi: {response.status_code} - {response.text}")
            self.show_success_message(f"x - To'lov amalga oshirilmadi!",f"{response.json()['detail']}" )  # Muvaffaqiyatli xabar
    def show_success_message(self, title, message):
        # Popup yaratamiz
	    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
	    msg_label = Label(text=message, size_hint=(1, None), text_size=(None, None), valign='center')  # wrap_text noto'g'ri, text_size ishlatamiz
	    label = Label(text="", size_hint=(1, 1), text_size=(None, None), valign='center')
	    msg_label.bind(size=msg_label.setter('text_size'))  # Matnni o'rab olish uchun text_size ni ulab qo'yamiz
	    ok_button = Button(text='Yopish', size_hint=(1, None))
	    if title != "Yetishmaslik":
	        ok_button.bind(on_press=self.clear_inputs_and_close)
	    else:
	    	ok_button.bind(on_press=self.close_message)
	
	    content.add_widget(msg_label)
	    content.add_widget(label)
	    content.add_widget(ok_button)
	
	    self.success_popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
	    self.success_popup.open()

    def clear_inputs_and_close(self, instance):
        # Inputlarni tozalash
        self.tg_id_input.text = ""
        self.summ_input.text = ""
        self.file_label.text = 'Kvitansiya:'
        self.selected_file = None

        # Popup ni yopish
        self.success_popup.dismiss()
    def close_message(self, instance):
        self.success_popup.dismiss()
    def switch_to_main_menu(self, instance):
        self.manager.current = 'main_menu'


# 3-oyna (About ekran)
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        btn = Button(text="Asosiy menyuga qaytish", on_press=self.switch_to_main_menu, size_hint_y=0.5)
        layout.add_widget(btn)
        self.mall = Label(text="Username: bexruzdeveloper\nBalance: 1,000,000 so'm", halign="left")
        layout.add_widget(self.mall)

        login_btn = Button(text="Ko'rish", on_press=self.get_user)
        layout.add_widget(login_btn)

        self.add_widget(layout)
        
    def switch_to_main_menu(self, instance):
        self.manager.current = 'main_menu'
    def get_user(self, instance):
        try:
            res = requests.get(f"https://api.projectsplatform.uz/admin/get-pckundalikcom?token={token}")
            res2 = requests.get(f"https://api.projectsplatform.uz/admin/get_all_telegram_ids?token={token}")
            self.mall.text = f"Jami: {len(res2.json()['all_telegram_ids'])-1:,} foydalanuvchilar\nFoydalanyapti: {len(res.json()['pckundalikcom'])-1:,} foydalanuvchilar"
        except:
            pass
# Ilova
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(AboutScreen(name='third'))
        return sm

if __name__ == '__main__':
    app = MyApp()
    app.run()

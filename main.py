__version__ = "1.0"
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from dbobject import DbObject
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar


# Window.size = (375, 750)
Window.size = (375, 600)


class HomeScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class MainApp(MDApp):

    def on_start(self):
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primaru_hue = '500'
        self.theme_cls.theme_style = 'Light'
        self.db = DbObject('myappdb.db')
        self.curr_user_id = -1
        self.curr_user_name = ""
        self.curr_user_email = ""

    def change_screen(self, screen_name, direction, mode):
        screen_manager = self.root.ids.screen_manager
        if direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return
        screen_manager.transition = CardTransition(
            direction=direction, mode=mode)
        screen_manager.current = screen_name

    def opensidebarmenu(self, action):
        self.root.ids.nav_drawer.set_state(action)

    def chk_user(self, uname, upswd):
        screen_manager = self.root.ids.screen_manager
        chk_authorized = self.db.chk_login_pwd(uname, upswd)

        return_str = self.db.get_user_name(3)
        print(return_str)

        if(chk_authorized == 1):
            print("Authorized access!!")
            self.change_screen("scr_home", direction='right', mode='push')
            self.curr_user_id = self.db.get_user_id(uname)
            self.curr_user_name = self.db.get_user_name(self.curr_user_id)
            self.curr_user_email = self.db.get_user_email(self.curr_user_id)
            self.root.ids['navsidebar_user_name'].text = self.curr_user_name
            self.root.ids['navsidebar_user_email'].text = self.curr_user_email
            self.db.upd_curr_user(self.curr_user_id)
        else:
            screen_manager.get_screen(
                'scr_login').ids.txt_login_info.text = "[color=ff0000]Invalid Username or Password. Try again![/color]"
            print("UNauthorized access!!")
        print("hello! Ur name : {}, id : {}, password : {}?".format(
            uname, self.curr_user_id, upswd))

    def register_user(self, login, username, email, psswd, adm_psswd):
        screen_manager = self.root.ids.screen_manager
        if(self.db.chk_exist_user(login) == 1):
            screen_manager.get_screen(
                'scr_register').ids.txt_info_register.text = "[color=ff0000]Login name already taken. Choose another one.[/color]"
        else:
            isadmin = self.db.chk_login_pwd('admin', adm_psswd)
            if(isadmin == 1):
                self.db.ins_tbl_users(login, username, email, psswd, 1)
                self.change_screen("scr_login", direction='left', mode='push')
                Snackbar(text="New User Registered!").open()
            else:
                screen_manager.get_screen(
                    'scr_register').ids.txt_info_register.text = "[color=ff0000]Invalid Administrator password. Contact Admin for further assitance.[/color]"

    def leftmenucallback(self, x):
        screen_manager = self.root.ids.screen_manager
        self.change_screen("scr_settings", direction='left', mode='push')
        #Snackbar(text="Under Construction..").open()

    def save_settings(self, old_pwd, new_pwd):
        screen_manager = self.root.ids.screen_manager
        curr_pwd = self.db.get_user_pswd(self.curr_user_id)
        if(curr_pwd == old_pwd):
            self.db.upd_user_passwd(self.curr_user_id, new_pwd)
            self.change_screen("scr_login", direction='right', mode='push')
            Snackbar(text="New Password Updated!").open()
        else:
            screen_manager.get_screen(
                'scr_settings').ids.txt_info_settings.text = "[color=ff0000]Wrong old password.[/color]"


MainApp().run()

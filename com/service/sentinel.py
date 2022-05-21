from copy import deepcopy
from playsound import playsound
from pynput import keyboard

from com.config.config_handler import ConfigHandler
from com.model.config import Config
from com.service.keyboard_guard import KeyboardGuard
from com.service.mouse_guard import MouseGuard
from com.service.task_manager_guard import TaskManagerGuard
from definitions import MEDIA_PATH

SYSTEM_SOUND_ONLINE = 'coinwin.wav'
SYSTEM_SOUND_OFFLINE = 'bassdrop.mp3'

class Sentinel:

    def __init__(self):
        self.__config: Config = ConfigHandler.instance().get()
        self.__online = False
        self.__password = self.__config.sentinel.password
        self.__hash_seq = [{p: False} for p in self.__password]
        self.__original_hash_seq = [{p: False} for p in self.__password]

        self.__mouse_guard = MouseGuard()
        self.__keyboard_guard = KeyboardGuard()
        self.__task_manager_guard = TaskManagerGuard()

        listener = keyboard.Listener(on_press=self.__on_press)
        listener.start()  # start to listen on a separate thread
        listener.join()  # remove if main thread is polling self.keys

    def __on_press(self, key):
#        if key == keyboard.Key.esc:
#            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        self.__update_seq(k)
        is_correct  = self.__check_password()

        if is_correct:
            if not self.__online:
                print('system online')
                self.__mouse_guard.start()
                self.__keyboard_guard.start()
                self.__task_manager_guard.start()
                playsound(f'{MEDIA_PATH}{SYSTEM_SOUND_ONLINE}')
            else:
                print('system off')
                self.__mouse_guard.stop()
                self.__keyboard_guard.stop()
                self.__task_manager_guard.stop()
                playsound(f'{MEDIA_PATH}{SYSTEM_SOUND_OFFLINE}')
            self.__online = not self.__online
            self.__reset_password()
        else:
            print(k)

    def __update_seq(self, k: str):
        for comination in self.__hash_seq:
            key = list(comination.keys())[0]
            value = comination.get(key)
            if value:
                continue

            if value == False and key == k:
                comination[key] = True
            else:
                self.__reset_password()
            break

    def __check_password(self) -> bool:
        for comination in self.__hash_seq:
            key = list(comination.keys())[0]
            value = comination.get(key)
            if value == False:
                return False
        return True

    def __reset_password(self):
        self.__hash_seq = deepcopy(self.__original_hash_seq)

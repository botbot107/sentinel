from copy import deepcopy
from pynput import keyboard

from com.config.config_handler import ConfigHandler
from com.model.config import KeyboardGuardConfig


class KeyboardGuard:

    def __init__(self):
        self.__config : KeyboardGuardConfig = ConfigHandler.instance().get().keyboard_guard_config
        self.__success_index = []
        for bad_combo in self.__config.bad_combos:
            self.__success_index.append(set())

    def start(self):
        self.__keyboard_listener = keyboard.Listener(on_press=self.__on_press)
        self.__keyboard_listener.setDaemon(True)
        self.__keyboard_listener.start()


    def stop(self):
        print('shout down keyboard guard')
        self.__keyboard_listener.stop()

    def __on_press(self, key):
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        self.__update_success_index(k)

        if self.__check_success_index():
            print('inValid Comb detected')
        print(f"keyboard guard {k}")

    def __update_success_index(self, k: str):
        for idx, bad_combo in enumerate(self.__config.bad_combos):
            if k in bad_combo.combo and k not in self.__success_index[idx]:
                self.__success_index[idx].add(k)
            else:
                self.__reset_success_index_element(idx)

    def __check_success_index(self) -> bool:
        for idx, bad_combo in enumerate(self.__config.bad_combos):
            if len(bad_combo.combo) == len(self.__success_index[idx]):
                self.__reset_success_index_element(idx)
                return True
        return False

    def __reset_success_index_element(self, idx):
        self.__success_index[idx] = set()

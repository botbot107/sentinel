from threading import Thread
import psutil
from time import sleep

from com.config.config_handler import ConfigHandler
from com.model.config import TaskManagerGuardConfig


class TaskManagerGuard():

    def __init__(self):
        self.__config : TaskManagerGuardConfig = ConfigHandler.instance().get().task_manager_guard_config
        self.__is_on = False

    def start(self):
        self.__is_on = True
        self.__first_run = True
        T = Thread(target=self.__task_listener)
        T.setDaemon(True)
        T.start()


    def stop(self):
        print('shout down TaskManagerGuard')
        self.__is_on = False

    def __task_listener(self):
        while True:
            # close listener
            if self.__is_on == False:
                print('TaskManagerGuard down')
                exit()

            # save snapshot tasks
            if self.__first_run:
                self.__task_snapshot = set()
                for task in psutil.process_iter():
                    self.__task_snapshot.add(task.name())
                self.__first_run = False

            if self.__config.shut_down_any_new_task:
                for task in psutil.process_iter():
                    if task.name() not in self.__task_snapshot:
                        print(f"new task {task.name()}")



            for task in psutil.process_iter():
                if task.name() in self.__config.exit_task:
                    print(f'shut Down task: {task.name()}')
                    task.terminate()
            sleep(1.5)
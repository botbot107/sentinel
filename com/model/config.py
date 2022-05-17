# create json -> object
# https://freecodegenerators.com/code-converters/json-to-python
from typing import List, Set
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Sentinel:
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'Sentinel':
        _password = str(obj.get("password"))
        return Sentinel(_password)

@dataclass
class BadCombo:
    combo: Set[str]

    @staticmethod
    def from_dict(obj: Any) -> 'BadCombo':
        _combo = set(str(y) for y in obj.get("combo"))
        return BadCombo(_combo)

@dataclass
class KeyboardGuardConfig:
    bad_combos: List[BadCombo]

    @staticmethod
    def from_dict(obj: Any) -> 'KeyboardGuardConfig':
        _bad_combos = [BadCombo.from_dict(y) for y in obj.get("bad_combos")]
        return KeyboardGuardConfig(_bad_combos)

@dataclass
class TaskManagerGuardConfig:
    exit_task: Set[str]
    shut_down_any_new_task: bool

    @staticmethod
    def from_dict(obj: Any) -> 'TaskManagerGuardConfig':
        _exit_task = set(str(y) for y in obj.get("exit_task"))
        _shut_down_any_new_task = bool(obj.get("shut_down_any_new_task"))
        return TaskManagerGuardConfig(_exit_task, _shut_down_any_new_task)

@dataclass
class Config:
    sentinel: Sentinel
    keyboard_guard_config: KeyboardGuardConfig
    task_manager_guard_config: TaskManagerGuardConfig

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        _sentinel = Sentinel.from_dict(obj.get("sentinel"))
        _keyboard_guard_config = KeyboardGuardConfig.from_dict(obj.get("keyboard_guard_config"))
        _task_manager_guard_config = TaskManagerGuardConfig.from_dict(obj.get("task_manager_guard_config"))
        return Config(_sentinel, _keyboard_guard_config, _task_manager_guard_config)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)

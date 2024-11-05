from abc import ABC, abstractmethod
import pandas as pd


class PyStataCommand(ABC):
    """
    PyStataCommand 基类，每个命令都应该继承该类并实现 `execute` 方法。
    """

    @abstractmethod
    def execute(self, data_manager, tokens, *args):
        """
        执行命令的主要逻辑，接受 DataManager 和参数。
        """
        pass

    @classmethod
    @abstractmethod
    def register(cls):
        """
        注册命令，返回命令的名字字符串。
        """
        pass

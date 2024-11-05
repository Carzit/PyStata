import pandas as pd
import os
from typing import List
from .base import PyStataCommand

class ClearCommand(PyStataCommand):
    def __init__(self):
        super().__init__()

    def execute(self, data_manager, tokens):
        # 解析命令选项
        if len(tokens["body"]) == 1:
            data_manager.clear()
            return ""

    @staticmethod
    def register():
        return "clear"
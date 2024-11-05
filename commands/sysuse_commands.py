import pandas as pd
import os
from typing import List
from .base import PyStataCommand

_SYSUSE_DIR = r"D:\PythonProjects\PyStata\sysuse"

class SysuseCommand(PyStataCommand):
    def __init__(self):
        super().__init__()

    def execute(self, data_manager, tokens):
        # 解析命令选项
        dir_path = _SYSUSE_DIR
        print(tokens)
        if tokens["body"][1] == "dir":
            _all = "all" in tokens["options"]
            data_file_names = self._list_datasets(dir_path=dir_path, _all=_all)
            print(self._generate_html_table(data_file_names))
            return self._generate_html_table(data_file_names)
            
        else:
            file_name = tokens["body"][1].removeprefix("\"").removesuffix("\"").removesuffix(".dta")    
            _clear = "clear" in tokens["options"]
            if self._check_dataset(dir_path, file_name):
                self._load_dataset(data_manager, file_name, _clear)
                return f"({data_manager.metadata.file_label})"
            else:
                return "invalid file specification"
            
    def _generate_html_table(self, strings, columns=6):
        """
        将字符串列表按指定列数生成 HTML 表格，不包含表头。
        
        :param strings: 字符串列表
        :param columns: 每行的列数，默认为6
        :return: 格式化的 HTML 表格字符串
        """
        # 将字符串列表按列数分组
        rows = [strings[i:i + columns] for i in range(0, len(strings), columns)]
        
        # 开始生成 HTML 表格
        table = '<table>\n'
        
        for row in rows:
            padded_row = row + [''] * (columns - len(row))  # 填充空列
            table += '  <tr>\n'
            for cell in padded_row:
                table += f'    <td>{cell}</td>\n'
            table += '  </tr>\n'
        
        table += '</table>\n'
        return table         

    def _check_dataset(self, dir_path, file_name):
        file_names = os.listdir(dir_path)
        data_file_names = [file_name.removesuffix(".dta") for file_name in file_names if file_name.endswith(".dta")]
        return file_name in data_file_names    
    
    def _load_dataset(self, data_manager, file_name, _clear):
        if _clear:
            data_manager.clear()
        data_manager.read(os.path.join(_SYSUSE_DIR, f"{file_name}.dta"))
            
    def _list_datasets(self, dir_path, _all):
        file_names = os.listdir(dir_path)
        data_file_names = [file_name.removesuffix(".dta") for file_name in file_names if file_name.endswith(".dta")]
        if not _all:
            data_file_names = [file_name for file_name in data_file_names if not file_name.startswith("__")]
        return data_file_names

    @staticmethod
    def register():
        return "sysuse"
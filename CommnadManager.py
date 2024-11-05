import importlib
import json
from commands.base import PyStataCommand

class CommandManager:
    def __init__(self, data_manager, config_file="commands/config.json"):
        self.data_manager = data_manager
        self.commands = {}
        self.load_commands(config_file)

    def load_commands(self, config_file):
        """
        从配置文件中读取命令类，并动态加载和注册。
        """
        with open(config_file, "r") as file:
            config = json.load(file)

        for command_info in config:
            module_name = command_info["module"]
            class_name = command_info["class"]
            
            # 动态加载模块和类
            module = importlib.import_module(module_name)
            command_class = getattr(module, class_name)
            
            # 确保类是 PyStataCommand 的子类
            if issubclass(command_class, PyStataCommand):
                command_name = command_class.register()
                self.commands[command_name] = command_class()
            else:
                print(f"{class_name} is not a subclass of PyStataCommand")

    def parse_command(self, command_line:str):
        """
        执行用户输入的命令。
        """
        comma_index = command_line.find(",")
        if comma_index == -1:
            body = command_line[:].strip()
            options = ""
        else:
            body = command_line[:comma_index].strip()
            options = command_line[comma_index:].removeprefix(",").strip()
        tokens = {"body": body.split(), "options": options.split()}
        return tokens
    
    def execute_command(self, command_line:str):
        tokens = self.parse_command(command_line)
        if not tokens["body"]:
            return "."
        command_name = tokens["body"][0].lower()
        if command_name in self.commands:
            command = self.commands[command_name]
            return command.execute(self.data_manager, tokens)
        else:
            return f"Unknown command: {command_name}"
        
    
# webui_manager.py
import gradio as gr
import pandas as pd
from typing import List, Tuple, Optional, Literal, Dict


from DataManager import DataManager
from CommnadManager import CommandManager



class WebUIManager:
    def __init__(self, data_manager, command_manager):
        self.data_manager:DataManager = data_manager
        self.command_manager = command_manager

        self.command_history_window: gr.Dataframe
        self.output_window: gr.Textbox

        self.history:List[Tuple[str, str]] = []
        self.command_history = []
        self.variable_overview = pd.DataFrame({"name": [], "dtype": [], "label": []})
        self.variable_attribute = pd.DataFrame({"name":["label", "dtype", "format", "value lable"], "":["", "", "", ""]})
        self.data_attribute = pd.DataFrame({"file name":["label", "notes", "variables", "observations", "size", "memory", "sorted by"], "":["", "", "", "", "", "", ""]})

    def create_interface(self):
        with gr.Blocks(title="PyStata", fill_width=True) as interface:
            with gr.Row():
                # 左侧 10%：命令历史窗口
                with gr.Column(scale=1):
                    with gr.Accordion(label="History", open=True):
                        self.command_history_window = gr.Dataframe(interactive=True, 
                                                                        headers=["commands"],
                                                                        type="array", 
                                                                        col_count=1)
                    
                # 中间 70%：输出和命令输入
                with gr.Column(scale=7):
                    with gr.Group():
                        with gr.Row():
                            # 输出窗口占 90%
                            self.output_window = gr.Markdown(label="Output", show_label=True, min_height=600, max_height=600, line_breaks=True)
                        
                        with gr.Row():
                            # 命令输入窗口占 10%
                            self.input_window = gr.Textbox(label="Command Input", placeholder="Type your command here...")
                
                # 右侧 20%：变量预览窗口
                with gr.Column(scale=2):
                    with gr.Group():
                        with gr.Row():
                            with gr.Accordion(label="Variable Overview",  open=True):
                                self.variable_overview_window = gr.Dataframe(
                                                                        interactive=True, 
                                                                        headers=["name", "dtype", "label"],
                                                                        datatype=["str", "str", "str"],
                                                                        col_count=(3, "fixed"))
                        with gr.Row():
                            with gr.Row():
                                with gr.Accordion(label="Variable Attribute", open=True):
                                    self.variable_attribute_window = gr.Dataframe(value=self.variable_attribute,
                                                                            interactive=False, 
                                                                            datatype=["str", "str"],
                                                                            col_count=(2, "fixed"))
                            with gr.Row():
                                with gr.Accordion(label="Data Attribute", open=True):
                                    self.data_attribute_window = gr.Dataframe(value=self.data_attribute,
                                                                            interactive=False, 
                                                                            datatype=["str", "str"],
                                                                            col_count=(2, "fixed"))

                        
            # 绑定命令提交
            self.input_window.submit(fn=self.run_command, 
                                 inputs=self.input_window, 
                                 outputs=[self.output_window, self.input_window, self.variable_overview_window, self.command_history_window])
            self.command_history_window.select(fn=self.command_history_window_select, 
                                               inputs=self.command_history_window, 
                                               outputs=self.input_window)
            self.variable_overview_window.select(fn=self.variable_overview_window_select,
                                                 inputs=self.variable_overview_window,
                                                 outputs=[self.variable_attribute_window, self.data_attribute_window],
                                                 scroll_to_output=True)

        return interface

    def run_command(self, command):
        self.command_history.append(command)
        result = self.command_manager.execute_command(command)
        self.history.append((command, result))
        return self.render_output(), "", self.update_variable_overview(), self.update_command_history_display()
    
    def render_output(self):
        cells:List[str] = []
        for command, result in self.history:
            if "\n" in command:
                command = "  \n&ensp;".join(command.split("\n"))
            formatted_command = f"**> {command}**  "
            formatted_result = f"{result}"
            cells.append("<br/>\n".join([formatted_command, formatted_result]))
        return "\n\n".join(cells)

    def update_variable_overview(self):
        if self.data_manager.df is None:
            self.variable_overview = pd.DataFrame({"name": [],
                                                   "dtype": [],
                                                   "label": []})
        else:
            if self.data_manager.metadata is None:
                self.variable_overview = pd.DataFrame({"name": self.data_manager.df.columns,
                                                       "dtype": self.data_manager.df.dtypes, 
                                                       "label": [""]*len(self.data_manager.df.columns)})
            else:
                self.variable_overview = pd.DataFrame({"name": self.data_manager.metadata.column_names,
                                                       "dtype": self.data_manager.df.dtypes, 
                                                       "label": self.data_manager.metadata.column_labels})
        return self.variable_overview

    def update_command_history_display(self):
        history_df = pd.DataFrame(self.command_history, columns=["Command"])
        return history_df
    
    def command_history_window_select(self, value, evt: gr.SelectData):
        return evt.value

    def variable_overview_window_select(self, value, evt: gr.SelectData):
        var_index = evt.index[0]
        var_name = self.variable_overview.iloc[var_index, 0]
        if self.data_manager.metadata:
            var_label = self.data_manager.metadata.column_names_to_labels[var_name]
            var_type = self.data_manager.metadata.readstat_variable_types[var_name]
            var_format = self.data_manager.metadata.original_variable_types[var_name]
            if var_name in self.data_manager.metadata.variable_value_labels:
                value_label = self.data_manager.metadata.variable_to_label[var_name]
            else:
                value_label = ""
            self.variable_attribute = pd.DataFrame({"name":["label", "type", "format", "value lable"], var_name:[var_label, var_type, var_format, value_label]})
            self.data_attribute = pd.DataFrame({"file name":["label", 
                                                             "notes", 
                                                             "variables", 
                                                             "observations", 
                                                             "size", 
                                                             "memory", 
                                                             "sorted by"], 
                                                self.data_manager.data_path:[self.data_manager.metadata.file_label, 
                                                                             self.data_manager.metadata.notes, 
                                                                             self.data_manager.metadata.number_columns, 
                                                                             self.data_manager.metadata.number_rows, 
                                                                             self.data_manager.file_size, 
                                                                             self.data_manager.memory_usage,
                                                                             None]})
        else:
            self.variable_attribute = pd.DataFrame({"name":["label", "dtype", "format", "value lable"], var_name:["", self.data_manager.df.dtypes[var_index], "", ""]})
            self.data_attribute = pd.DataFrame({"file name":["label", 
                                                             "notes", 
                                                             "variables", 
                                                             "observations", 
                                                             "size", 
                                                             "memory", 
                                                             "sorted by"], 
                                                self.data_manager.data_path:[self.data_manager.metadata.file_label, 
                                                                             self.data_manager.metadata.notes, 
                                                                             self.data_manager.metadata.number_columns, 
                                                                             self.data_manager.metadata.number_rows, 
                                                                             self.data_manager.file_size, 
                                                                             self.data_manager.memory_usage]})
            
        return self.variable_attribute, self.data_attribute
        

    
# main.py
if __name__ == "__main__":

    data_manager = DataManager()
    command_manager = CommandManager(data_manager)
    web_ui_manager = WebUIManager(data_manager, command_manager)

    web_ui_manager.create_interface().launch(inbrowser=True)

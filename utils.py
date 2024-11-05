from dataclasses import dataclass
from typing import List, Dict, Optional, Union

__logo = '''
  ___   _   _   ___  ____  ____  ____  ____
 /__/   |_ /   /__    /   ____/   /   ____/ 
/       __/   ___/   /   /___/   /   /___/  

'''


@dataclass
class MetaData:
    notes: str
    creation_time: str
    modification_time: str
    column_names: List[str]
    column_labels: List[str]
    column_names_to_labels: Dict[str, str]
    file_encoding: str
    number_columns: int
    number_rows: int
    variable_value_labels: Dict[str, Dict[Union[int, float, str], str]]
    value_labels: Dict[str, Dict[Union[int, float, str], str]]
    variable_to_label: Dict[str, str]
    original_variable_types: Dict[str, str]
    readstat_variable_types: Dict[str, str]
    table_name: str
    file_label: str
    missing_ranges: Dict[str, List[Dict[str, Union[int, float, str]]]]
    missing_user_values: Dict[str, List[Union[int, float, str]]]
    variable_alignment: Dict[str, str]
    variable_storage_width: Dict[str, int]
    variable_display_width: Dict[str, int]
    variable_measure: Dict[str, str]

    @classmethod
    def wrap(cls, unknown):
        return cls(
            notes=unknown.notes,
            creation_time=unknown.creation_time,
            modification_time=unknown.modification_time,
            column_names=unknown.column_names,
            column_labels=unknown.column_labels,
            column_names_to_labels=unknown.column_names_to_labels,
            file_encoding=unknown.file_encoding,
            number_columns=unknown.number_columns,
            number_rows=unknown.number_rows,
            variable_value_labels=unknown.variable_value_labels,
            value_labels=unknown.value_labels,
            variable_to_label=unknown.variable_to_label,
            original_variable_types=unknown.original_variable_types,
            readstat_variable_types=unknown.readstat_variable_types,
            table_name=unknown.table_name,
            file_label=unknown.file_label,
            missing_ranges=unknown.missing_ranges,
            missing_user_values=unknown.missing_user_values,
            variable_alignment=unknown.variable_alignment,
            variable_storage_width=unknown.variable_storage_width,
            variable_display_width=unknown.variable_display_width,
            variable_measure=unknown.variable_measure
        )
    
    def __repr__(self):
        return (f"Metadata(notes={self.notes}, "
                f"creation_time={self.creation_time}, "
                f"modification_time={self.modification_time}, "
                f"column_names={self.column_names}, "
                f"column_labels={self.column_labels}, "
                f"column_names_to_labels={self.column_names_to_labels}, "
                f"file_encoding={self.file_encoding}, "
                f"number_columns={self.number_columns}, "
                f"number_rows={self.number_rows}, "
                f"variable_value_labels={self.variable_value_labels}, "
                f"value_labels={self.value_labels}, "
                f"variable_to_label={self.variable_to_label}, "
                f"original_variable_types={self.original_variable_types}, "
                f"readstat_variable_types={self.readstat_variable_types}, "
                f"table_name={self.table_name}, "
                f"file_label={self.file_label}, "
                f"missing_ranges={self.missing_ranges}, "
                f"missing_user_values={self.missing_user_values}, "
                f"variable_alignment={self.variable_alignment}, "
                f"variable_storage_width={self.variable_storage_width}, "
                f"variable_display_width={self.variable_display_width}, "
                f"variable_measure={self.variable_measure})")
    



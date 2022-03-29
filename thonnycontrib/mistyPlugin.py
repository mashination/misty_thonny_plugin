from thonny import get_workbench
from tkinter.messagebox import showinfo

from thonny import get_shell
from thonny.editors import get_saved_current_script_filename
from thonny.editors import extract_target_path, is_local_path

PATH_MISTY = "misty/Misty.py "

def run():
    filename = get_saved_current_script_filename()
    if  is_local_path(filename):
        target_path = filename
    else:
        target_path = extract_target_path(filename)
    get_shell().submit_magic_command("%Run " + PATH_MISTY +  "\"" + target_path + "\"")

def load_plugin():
    get_workbench().add_command(command_id="misty",
                                menu_name="run",
                                command_label="Misty Run",
                                handler=run)

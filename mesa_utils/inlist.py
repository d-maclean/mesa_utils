import os
import glob
from collections import OrderedDict

# open file, get list of lines
# strip lines,
#   iterate over list and remove whitespace and blank lines
# 

def get_lines(file_path) -> list:
    """Load an inlist file at `file_path` and split it into lines."""
    with open(file_path, "r") as file:
        return file.read().splitlines()


def format_inlist(settings: OrderedDict) -> str:
    """Rewrite an OrderedDict of settings as a string (which should be a valid inlist)"""

    if not isinstance(settings, OrderedDict):
        print(f"Warning! {settings} is not an OrderedDict. Order will not be preserved.") 

    text = ""

    for key, value in settings.items():

        if key.startswith("delim_"):
            text += f"\n{value}\n"
        else:
            text += f"{key} = {value}\n"
    
    return text


def treat_lines(lines: list) -> OrderedDict:
    """Takes a list of lines and produces an OrderedDict of stripped settings and values."""
    settings = OrderedDict()
    delim_ct = 0

    for l in lines:
        l: str = l.strip()

        if (not l.startswith(("!"))) and len(l) > 0:

            if not l.startswith(("/", "&")):
                
                l = l.split("!", 1)[0] # remove trailing comments and internal whitespace
            
                if l.find("=") != -1:
                    key, value = l.split("=",1)
                    key = key.strip()
                    value = value.strip()
                    
                    # ordered dict method to make sure the bottom setting always "wins"
                    settings[key] = value
            
            else:
                l = l.strip()
                settings[f"delim_{delim_ct}"] = l
                delim_ct += 1
                    
    return settings
    

def strip_duplicate_lines(settings: OrderedDict,
                          reference: OrderedDict) -> OrderedDict:
    """
    Takes two Dicts, 'settings' and 'reference.'
    Scans each key in 'settings,' and if the setting is the same in `reference,` removes it.
    """
    pruned_settings = OrderedDict()
    n_pruned_lines: int = 0

    for key, value in settings.items():
        if key.startswith("delim_"):
            pruned_settings[key] = value

        else:

            if (key not in reference.keys()):
                pruned_settings[key] = value
            elif (key in reference.keys()):
                if reference[key] != value:
                    pruned_settings[key] = value
            else:
                n_pruned_lines += 1
    
    print(f"Pruned {n_pruned_lines} settings.")
    return pruned_settings


def get_common_lines(settings1: OrderedDict,
                    settings2: OrderedDict) -> OrderedDict:
    """
    Takes two dicts, `settings1` and `settings2`, and scans each setting.
    Returns a dict with each setting that is identical in each inlist.
    """
    common_settings = OrderedDict()
    n_skipped_lines: int = 0

    for key, value in settings1.items():
        if key.startswith("delim_"):
            common_settings[key] = value

        if key in settings2.keys():
            if value == settings2[key]:
                common_settings[key] = value
            else:
                n_skipped_lines += 1
    
    print(f"Skipped {n_skipped_lines} settings.")
    return common_settings


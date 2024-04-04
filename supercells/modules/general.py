import json
from pathlib import Path
from typing import Optional
import logging
from supercells.config import CUTOFFS_DICT


def read_and_check_cutoff_dict(cutoff_dict_path: str) -> Optional[dict]:
    if not cutoff_dict_path:
        logging.warning(f"cutoff_dict_path was not passed, using default params")
        return CUTOFFS_DICT

    try:
        cutoff_dict_path = Path(cutoff_dict_path)
        logging.info(f"Reading cutoff_dict from '{cutoff_dict_path}'")
        with cutoff_dict_path.open("r") as f:
            cutoff_dict = json.load(f)
            if extra_keys := set(cutoff_dict.keys()) - set(CUTOFFS_DICT.keys()):
                logging.error(f"cutoff_dict read from '{cutoff_dict_path}', contains extra keys: {extra_keys}")
                raise Exception
            else:
                return cutoff_dict

    except (TypeError, FileNotFoundError, PermissionError):
        logging.error(f"Could not read '{cutoff_dict_path}', using default cutoff params.")
        return CUTOFFS_DICT

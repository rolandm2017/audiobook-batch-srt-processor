
import subprocess
import os
import traceback

from typing import List, Tuple, Optional, Dict, TypedDict


from .colorsPrinter import colored_print, wrap_text_in_color, colored_print_info_type


class CommandRunner:
    def __init__(self) -> None:
        pass

    @staticmethod  # in CommandRunner
    def run_command(cmd: List[str], description: str = "", capture_output: bool = False) -> bool:
        """
        Run a command and handle errors consistently.

        ** You probably DON'T want capture_output = True, as it suppresses WhisperX output
        
        Args:
            cmd: Command as list of arguments
            description: Description of what the command does
            capture_output: Whether to capture output
        
        Returns:
            Tuple of (success: bool, output: str or None)
        """
        colored_print_info_type("Running: ", 2, f"{description}")
        colored_print_info_type("Command: ", 2, f"{' '.join(cmd)}")
        
        try:
            if capture_output:
                result = subprocess.run(cmd, check=True, text=True, capture_output=capture_output)
                if result.stdout:
                    print(f"Output: {result.stdout}")
                return True
            else:
                result = subprocess.run(cmd, check=True, text=True)
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                colored_print_info_type(f"[Error output] ", 3, f"{e.stderr}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        
    
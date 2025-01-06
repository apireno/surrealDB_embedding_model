
from datetime import datetime
import json
import ast
import re
import os

class Helpers:
    @staticmethod
    async def logError(
        objectThatFailed,objectName,error,out_folder
    ):
        
        os.makedirs(out_folder, exist_ok=True)  
        fileToWrite = out_folder + "/" + objectName + "_errors.txt"
        with open(fileToWrite, "a") as f:
            f.write("""
            ---------------------------""")
            f.write(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            f.write("""-----------------------
            """)
            f.write(str(objectThatFailed))
            f.write("""
            -------------------------------------------------------------
            """)
            f.write(str(error))
            f.write("""
            -------------------------------------------------------------
            """)


    @staticmethod
    def fix_json_quotes(input_string):
        #this is for swapping out misaligned quotes coming from AST calls

        try:
            return ast.literal_eval(input_string)
        except:
            pattern = r"(?<!\\)'(.*?)(?<!\\)'"  
            ret_val = input_string.replace("\"", '|')
            ret_val = re.sub(pattern, r'"\1"', ret_val)
            try:
                return json.loads(ret_val.replace("|","'"))
            except:
                return ["ERR"]
            


    @staticmethod
    def time_str_to_seconds(time_str):
        """Converts a string representing time with various units to seconds.

        Args:
            time_str: A string with time and unit (e.g., '50.677µs', '10ms', '2min', '1h').
                    Supported units: µs (microseconds), ms (milliseconds), 
                    s (seconds), min (minutes), h (hours).

        Returns:
            The time in seconds as a float.
        """
        try:
            # Extract the numeric part and unit from the string
            value_str = ""
            unit = ""
            for char in time_str:
                if char.isdigit() or char == ".":
                    value_str += char
                else:
                    unit += char
            value = float(value_str)

            # Define conversion factors for each unit
            unit_factors = {
                'µs': 1e-6,
                'ms': 1e-3,
                's': 1,
                'min': 60,
                'h': 3600
            }

            # Convert to seconds using the appropriate factor
            if unit in unit_factors:
                return value * unit_factors[unit]
            else:
                print(f"------------------------")
                print(f"Unsupported unit: {unit}  time_str {time_str}")
                print(f"------------------------")
                return 0

        except (ValueError, IndexError) as e:
            print(f"Invalid input format. Provide a string like '50.677µs', '10ms', etc. Error: {e}")
            return None

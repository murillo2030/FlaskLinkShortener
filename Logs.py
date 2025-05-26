from datetime import datetime
import os
import time



class Log():
    def __init__(self):
        self.__log_name: str = None 

        if not os.path.exists("./logs"):
            os.mkdir("./logs")
    
    def __update_log_name__(self, operation: str):
        self.__update_prefix__()
        self.__update_suffix__()
        self.__log_name = "./logs/" + self.__log_prefix + self.__log_suffix + (f'_{ operation }' if operation else '') + '.txt'
        
    def create_log(self, message: str, operation: str = None) -> bool:
        try:
            self.__update_log_name__(operation)
            with open(self.__log_name, 'x') as fp:
                fp.write(message)
            return True
        except FileNotFoundError as e:
            print(f"FileNotFoundError ({ e }): couldn't create log file.")
            return False
        except Exception as e:
            print(f"Error ({ e }): error when creating log file")
            return False

    def __update_suffix__(self):
        self.__log_suffix = datetime.now().strftime("%Y%m%d_%H%M%s")
        self.__log_suffix = f'{ self.__log_suffix }'
    
    def __update_prefix__(self):
        self.__update_timestamp__()
        self.__log_prefix = f'logfile_{ self.__timestamp }_'

    
    def __update_timestamp__(self):
        self.__timestamp = int(time.time())

from typing import Any, Dict, Iterator
from os.path import exists
import json

class JsonFile:
    """ Helper class for dealing with json files """

    def __init__(self, file_name: str, default_value: Dict[str, Any]) -> None:
        self._path = f"{file_name}.json"
        self._readFile(self._path, default_value)

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __getattr__(self, name: str) -> Any:
        return getattr(self._data, name)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def _readFile(self, path: str, default_value: Dict[str, Any]) -> None:
        if not exists(path):
            self._saveFile(path, default_value)

        with open(path, "r", encoding="utf-8") as file:
            self._data = json.load(file)

    def _saveFile(self, path: str, data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, default=str)

    def reset(self):
        self._saveFile(self._path, {})

    def save(self) -> None:
        """ Saves the internal (modified?) data into the file path that were passed to the __init__. """
        self._saveFile(self._path, self._data)



        
DEFAULT_CONFIG = {
    "bot_token": "",
    "api_id": "",
    "api_hash": "",
    "broadcast_Channel_id": "",
    "main_channel_id": "",
    "show_users_command": "/show_users",
    "ban_all_users_command": "/ban_all",
    "ban_user_command": "/ban_user",
    }
        
Config = JsonFile("config", DEFAULT_CONFIG)
        
def get_group(groupId: str):
        
    if not groupId.isnumeric():
      return groupId
    
    if len(groupId) == 10:
      return int(f"-100{groupId}")
    
    if len(groupId) == 9:
      return int(f"-{groupId}")
    
    return int(groupId)
    
    
def get_config():
    return Config






        
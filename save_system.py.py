import json
import zlib
from pathlib import Path

class SaveSystem:
    def __init__(self):
        self.SAVE_DIR = "saves"
        Path(self.SAVE_DIR).mkdir(exist_ok=True)
    
    def save_game(self, data):
        data["checksum"] = self._calculate_checksum(data)
        with open(f"{self.SAVE_DIR}/game_save.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def load_game(self):
        try:
            with open(f"{self.SAVE_DIR}/game_save.json", "r") as f:
                data = json.load(f)
            if data["checksum"] == self._calculate_checksum(data):
                return data
        except:
            return None
    
    def _calculate_checksum(self, data):
        return zlib.crc32(json.dumps(data, sort_keys=True).encode())
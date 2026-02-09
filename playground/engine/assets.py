import yaml
import json

from typing import Dict
from pathlib import Path

from playground.engine.rendering import Sprite

class AssetManager:
    asset_root: Path
    asset_map: Dict[str, Sprite | dict | str]

    def __init__(self, root: Path):
        self.asset_root = root
        self.asset_map = dict()

    def load_sprite(self, asset_name: str, asset_path: str) -> Sprite:
        loaded_asset = Sprite(self.asset_root / asset_path)
        self.asset_map[asset_name] = loaded_asset
        return loaded_asset
    
    def load_config(self, asset_name: str, asset_path: str) -> dict:
        full_path = self.__get_full_path(asset_path)
        ext = full_path.suffix.lower()

        if ext == ".json":
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif ext in (".yml", ".yaml"):
            with open(full_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {ext}")

        self.asset_map[asset_name] = data
        return data
    
    def load_text(self, asset_name: str, asset_path: str) -> str:
        full_path = self.asset_root / asset_path
        
        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.asset_map[asset_name] = text
        return text

    def unload_asset(self, asset_name: str) -> None:
        self.asset_map.pop(asset_name, None)

    def get_asset(self, asset_name: str) -> Sprite | dict | str:
        asset = self.asset_map.get(asset_name)
        
        if asset is None:
            print(f"[WARNING]: Asset with key \"{asset_name}\" does not exist.")
        
        return asset
    
    def __get_full_path(self, asset_path: str) -> Path:
        full_path = self.asset_root / asset_path

        if not full_path.exists():
            raise FileNotFoundError(full_path)
        
        return full_path
from typing import Dict
from pathlib import Path

from playground.engine.rendering import Sprite

class AssetManager:
    asset_root: Path
    asset_map: Dict[str, Sprite]

    def __init__(self, root: Path):
        self.asset_root = root
        self.asset_map = dict()

    def load_asset(self, asset_name: str, asset_path: str) -> Sprite:
        loaded_asset = Sprite(self.asset_root / asset_path)
        self.asset_map[asset_name] = loaded_asset
        return loaded_asset

    def unload_asset(self, asset_name: str) -> None:
        self.asset_map.pop(asset_name, None)

    def get_asset(self, asset_name: str) -> Sprite:
        asset = self.asset_map.get(asset_name)
        
        if asset is None:
            print(f"[WARNING]: Asset with key \"{asset_name}\" does not exist.")
        
        return asset
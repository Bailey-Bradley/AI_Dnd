from pathlib import Path

class ResourceManager:

    root: Path = ""

    SOUND: Path = None
    TEXTURES: Path = None
    SAVEDATA: Path = None

    def init(program_root: Path):
        ResourceManager.root = program_root.joinpath("data")
        
        if not ResourceManager.root.exists():
            raise Exception("ERROR: Couldn't find data folder")

        ResourceManager.SOUND = ResourceManager.root.joinpath("audio")
        ResourceManager.TEXTURES = ResourceManager.root.joinpath("textures")
        ResourceManager.SAVEDATA = ResourceManager.root.joinpath("savedata")

        if not ResourceManager.SOUND.exists():
            raise Exception("ERROR: Couldn't find data/audio folder")

        if not ResourceManager.TEXTURES.exists():
            raise Exception("ERROR: Couldn't find data/textures folder")

        ResourceManager.SAVEDATA.mkdir(exist_ok=True)
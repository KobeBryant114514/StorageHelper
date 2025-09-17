from rapidnbt import nbtio
from leveldb import LevelDB
from pathlib import Path
import sys, os, msvcrt


def make_path(path) -> str:
    return os.path.join(os.path.dirname(sys.executable), path)
    # return os.path.join(os.path.dirname(__file__), path)


def export_data():
    try:
        db = LevelDB(make_path("db"))
        os.makedirs(make_path("export/player_data"), exist_ok=True)
        os.makedirs(make_path("export/player_entry"), exist_ok=True)
        os.makedirs(make_path("export/scoreboard"), exist_ok=True)

        for key, val in db.items():
            try:
                name = key.decode()
                if key.startswith(b"player_"):
                    data = nbtio.loads(val)
                    if key.startswith(b"player_server_"):
                        print(f"[INFO] Exporting player data: {name}")
                        nbtio.dump(data, make_path(f"export/player_data/{name}.nbt"))
                    else:
                        print(f"[INFO] Exporting player entry: {name}")
                        nbtio.dump(data, make_path(f"export/player_entry/{name}.nbt"))

                elif key == b"scoreboard":
                    print(f"[INFO] Exporting scoreboard")
                    nbtio.dump(
                        nbtio.loads(val), make_path("export/scoreboard/scoreboard.nbt")
                    )
            except:
                pass

        print("[INFO] Exporting storage data finished.")
    except Exception as e:
        print(f"\033[31m[ERROR] {e}\033[0m")


def import_data():
    try:
        import_path = make_path("import")
        if not os.path.exists(import_path):
            return print(
                f"\033[31m[ERROR] Couldn't find import path: {import_path}\033[0m"
            )

        db = LevelDB(make_path("db"))
        batch = {}

        for root, _, files in os.walk(import_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                stem_name = Path(file_name).stem

                key = stem_name.encode("utf-8")
                data = nbtio.load(make_path(file_path))

                if stem_name == "scoreboard":
                    print(f"[INFO] Importing scoreboard")
                    old_data = nbtio.loads(db.get(b"scoreboard"))
                    data.merge(old_data, True)
                    batch[key] = data.to_binary_nbt()

                elif stem_name.startswith("player_server_"):
                    print(f"[INFO] Importing player data: {stem_name}")
                    batch[key] = data.to_binary_nbt()

                elif stem_name.startswith("player_"):
                    print(f"[INFO] Importing player entry: {stem_name}")
                    if key in db:
                        old_entry = nbtio.loads(db.get(key))
                        old_sid = old_entry.get_string("ServerId")
                        db.delete(old_sid.encode("utf-8"))
                    batch[key] = data.to_binary_nbt()

        db.putBatch(batch)
        print("[INFO] Importing storage data finished.")
    except Exception as e:
        print(f"\033[31m {e}\033[0m")


def main():
    print("")
    print("Please choose a mode (export/import):")
    type = input("> ")
    if type == "export":
        export_data()
    elif type == "import":
        import_data()
    else:
        print(f"\033[31m[ERROR] Unsupported mode: {type}\033[0m")
        main()


if __name__ == "__main__":
    print("***********************************************************************")
    print("** Storage Helper v2.1.0")
    print("** Copyright © 2025 KobeBryant114514. All rights reserved.")
    print("***********************************************************************")
    try:
        main()
        print("Press any key to exit...")
        msvcrt.getch()
    except:
        pass

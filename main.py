from rapidnbt import nbtio
from leveldb import LevelDB
import os, msvcrt


def Info(output: str):
    print(f"\033[0m[INFO] {output}\033[0m")


def Error(output: str):
    print(f"\033[31m[ERROR] {output}\033[0m")


def export_data():
    try:
        db = LevelDB("db")
        os.makedirs("export/player_data", exist_ok=True)
        os.makedirs("export/player_entry", exist_ok=True)
        os.makedirs("export/scoreboard", exist_ok=True)

        for key, val in db.items():
            try:
                name = key.decode()
                if key.startswith(b"player_"):
                    data = nbtio.loads(val)
                    if key.startswith(b"player_server_"):
                        Info(f"Exporting player data: {name}")
                        nbtio.dump(data, f"export/player_data/{name}.nbt")
                    else:
                        Info(f"Exporting player entry: {name}")
                        nbtio.dump(data, f"export/player_entry/{name}.nbt")

                elif key == b"scoreboard":
                    Info(f"Exporting scoreboard")
                    nbtio.dump(nbtio.loads(val), "export/scoreboard/scoreboard.nbt")

            except:
                pass

        Info("Exporting storage data finished.")

    except Exception as e:
        Error(f"{e}")


def import_data():
    try:
        if not os.path.exists("import"):
            return Error(f"Couldn't find import path: {"import"}")

        db = LevelDB("db")
        batch = {}

        for root, _, files in os.walk("import"):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                name = os.path.splitext(os.path.basename(file_path))[0]

                key = name.encode()
                data = nbtio.load(file_path)

                if name == "scoreboard":
                    Info(f"Importing scoreboard")
                    old_data = nbtio.loads(db.get(b"scoreboard"))
                    data.merge(old_data, True)
                    batch[key] = data.to_binary_nbt()

                elif name.startswith("player_server_"):
                    Info(f"Importing player data: {name}")
                    batch[key] = data.to_binary_nbt()

                elif name.startswith("player_"):
                    Info(f"Importing player entry: {name}")
                    if key in db:
                        old_entry = nbtio.loads(db.get(key))
                        old_sid = old_entry.get_string("ServerId")
                        db.delete(old_sid.encode())
                    batch[key] = data.to_binary_nbt()

        db.putBatch(batch)
        Info("Importing storage data finished.")

    except Exception as e:
        Error(f"{e}")


def main():
    print("")
    print("Please choose a mode (export/import):")
    type = input("> ")
    if type == "export":
        export_data()
    elif type == "import":
        import_data()
    else:
        print(f"Unsupported mode: {type}")
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

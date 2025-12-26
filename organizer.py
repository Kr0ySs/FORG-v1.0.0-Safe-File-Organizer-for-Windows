import os
import shutil

def organize_folder(path):
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        if not os.path.isfile(full_path):
            continue

        name, ext = os.path.splitext(filename)
        folder_name = ext.replace(".", "").upper() or "OUTROS"

        target_dir = os.path.join(path, folder_name)
        os.makedirs(target_dir, exist_ok=True)

        target_path = os.path.join(target_dir, filename)

        # Evita sobrescrever arquivos com mesmo nome
        if os.path.exists(target_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(target_path):
                target_path = os.path.join(
                    target_dir, f"{base}_{counter}{ext}"
                )
                counter += 1

        shutil.move(full_path, target_path)
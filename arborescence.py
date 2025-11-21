import random
import string
import lorem
from pathlib import Path

def random_folder_name(length=8):
    """Génère un nom de dossier aléatoire."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_file_name(length=8):
    """Génère un nom de fichier aléatoire."""
    return ''.join(random.choices(string.ascii_lowercase, k=length)) + ".txt"

def create_random_tree(
    root,
    max_depth=3,
    max_subfolders=4,
    max_files=20,
    lorem_min=1,
    lorem_max=10
):
    """
    Génère récursivement une arborescence de dossiers et fichiers :
    - max_depth : profondeur maximale d'imbrication
    - max_subfolders : nombre max de sous-dossiers par dossier
    - max_files : nombre max de fichiers par dossier
    - lorem_min/lorem_max : nombre de paragraphes lorem ipsum aléatoires par fichier
    """

    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    num_files = random.randint(0, max_files)
    for _ in range(num_files):
        file_path = root / random_file_name()
        with open(file_path, "w", encoding="utf-8") as f:
            paragraphs = random.randint(lorem_min, lorem_max)
            content = "\n\n".join(lorem.paragraph() for _ in range(paragraphs))
            f.write(content)

    if max_depth <= 0:
        return

    num_subfolders = random.randint(0, max_subfolders)
    for _ in range(num_subfolders):
        subfolder = root / random_folder_name()
        create_random_tree(
            subfolder,
            max_depth=max_depth - 1,
            max_subfolders=max_subfolders,
            max_files=max_files,
            lorem_min=lorem_min,
            lorem_max=lorem_max
        )

if __name__ == "__main__":
    base_directory = "test_arbo"

    max_depth = 6
    max_subfolders = 5
    max_files = 50
    lorem_min = 1
    lorem_max = 3

    print("Génération de l'arborescence en cours...")
    
    create_random_tree(
        root=base_directory,
        max_depth=max_depth,
        max_subfolders=max_subfolders,
        max_files=max_files,
        lorem_min=lorem_min,
        lorem_max=lorem_max
    )

    print(f"Arborescence générée dans le dossier : '{base_directory}'")

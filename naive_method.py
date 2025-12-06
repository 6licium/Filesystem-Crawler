import os
import time

start_dir = "test_arbo/"
found_paths = []

start_timer = time.time()

def count_paragraphs(file_path):
    """Compte les paragraphes séparés par au moins une ligne vide."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # On sépare sur une ou plusieurs lignes vides
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    return len(paragraphs)

for root, dirs, files in os.walk(start_dir):
    for file in files:
        full_path = os.path.join(root, file)

        # On ne traite que les .txt
        if file.lower().endswith(".txt"):
            try:
                if count_paragraphs(full_path) == 3:
                    found_paths.append(full_path)
            except Exception as e:
                print(f"[ERREUR] Impossible de lire {full_path} : {e}")

# Résultats
print("\n--------------------------------------")
if found_paths:
    print(f"--> {len(found_paths)} fichier(s) avec exactement 3 paragraphes :")
    for p in found_paths:
        print(" -", p)
else:
    print("Aucun fichier avec exactement 3 paragraphes trouvé.")

end_time = time.time() - start_timer
print(f"\nTemps d'exécution : {end_time:.4f} secondes")

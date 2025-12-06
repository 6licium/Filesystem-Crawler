import os 
import time 
start_dir = "test_arbo/" 
target_name = "tqsbbxvn.txt" 
found_paths = [] 
start_timer = time.time() 
for root, dirs, files in os.walk(start_dir): 
    if target_name in files: 
        full_path = os.path.join(root, target_name) 
        found_paths.append(full_path) 
        print(f"[FLAG] Fichier trouvé : {full_path}") # Résultat final après la boucle 
    if found_paths: 
        print(f"\n--> Fichier trouvé {len(found_paths)} fois :") 
        for p in found_paths: 
            print(" -", p) 
            end_time = time.time() - start_timer 
            print(f"\nTemps d'exécution : {end_time:.4f} secondes") 
    else:
        print(f"\nFichier '{target_name}' non trouvé dans '{start_dir}'.")
        end_time = time.time() - start_timer 
        print(f"\nTemps d'exécution : {end_time:.4f} secondes")
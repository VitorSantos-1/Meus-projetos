import os
import glob
import shutil
import subprocess

def run_git_mv(src, dest):
    # Executa o git mv nativamente
    result = subprocess.run(["git", "mv", src, dest], capture_output=True, text=True)
    if result.returncode != 0:
        # Se falhar porque o arquivo nunca foi commitado, usa o fallback em shutil
        if "not under version control" in result.stderr or "bad source" in result.stderr:
            print(f"[{src}] Untracked. Movendo e adicionando manualmente...")
            shutil.move(src, dest)
            subprocess.run(["git", "add", os.path.join(dest, os.path.basename(src))])
        else:
            print(f"Erro no Git MV ao mover {src}: {result.stderr}")
    else:
        print(f"Sucesso (git mv): {src} -> {dest}")

def main():
    print("Iniciando a reestruturaçao do repositorio baseado no salvar.md...\n")
    
    dirs = [
        "src/R_exemplos",
        "src/pesquisa_preco",
        "scripts/python_geral",
        "data/utilitarios",
        "docs",
        "config/pesquisa_preco",
        "tests"
    ]
    
    print("Criando os repositórios base estruturais...")
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        gitkeep = os.path.join(d, ".gitkeep")
        with open(gitkeep, "w") as f:
            pass
        subprocess.run(["git", "add", gitkeep])

    # Mapeamento do que mover e para onde (Origem Expressao Regular, Destino Pasta)
    moves = [
        ("Alguns exemplo com R/*.R", "src/R_exemplos/"),
        ("Alguns exemplo com R/*.r", "src/R_exemplos/"),
        ("Alguns exemplo com R/*.csv", "data/"),
        ("Alguns exemplo com R/*.png", "data/"),
        ("Alguns exemplo com R/.RData", "data/"),
        ("Alguns exemplo com R/.Rhistory", "data/"),
        
        ("Projeto_Pesquisa_Preco/*.py", "src/pesquisa_preco/"),
        ("Projeto_Pesquisa_Preco/reqs*.txt", "config/pesquisa_preco/"),
        ("Projeto_Pesquisa_Preco/.env*", "config/pesquisa_preco/"),
        
        ("Python/*.py", "scripts/python_geral/"),
        
        ("Documentos_e_Utilitarios/*.md", "docs/"),
        ("Documentos_e_Utilitarios/*.zip", "data/utilitarios/"),
        ("Documentos_e_Utilitarios/*.log", "data/utilitarios/")
    ]

    print("\nMapeando arquivos e realizando git mv inteligente:")
    for pattern, dest in moves:
        for filepath in glob.glob(pattern):
            if os.path.isfile(filepath):
                run_git_mv(filepath, dest)
                
    print("\n[!] Reorganização concluída com sucesso!")
    print("[!] Você ja pode conferir e dar os commits.")

if __name__ == "__main__":
    main()

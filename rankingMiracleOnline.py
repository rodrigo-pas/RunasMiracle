import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from threading import Thread
from datetime import datetime, timedelta
import json
from time import sleep # Importado para pausar requisições

# Dicionário de skills para criar os botões
SKILLS = {
    'experience': 'Level / Exp',
    'sword': 'Sword',
    'axe': 'Axe',
    'club': 'Club',
    'dist': 'Distance',
    'maglevel': 'Magic Level',
    'shielding': 'Shielding',
    'fishing': 'Fishing',
    'mage_skill': 'Mage Combat Skills', # Adicionado para a nova função
}

# ===============================================
# CONFIGURAÇÃO GERAL
# ===============================================

class GuildAnalyzerApp:
    
    # --- CONSTANTE DE CLASSE ---
    MAX_PAGES = 10 # Busca nas 10 páginas do ranking (Top 1000)
    
    def __init__(self, root):
        self.root = root
        self.root.title("Inimigos do Analyzer - Gerador de Ranking JSON")
        self.root.geometry("600x450") 

        self.style = self.get_style()
        self.root.configure(bg=self.style['bg_color'])

        # --- VARIÁVEIS DE CONTROLE ---
        self.guild_url_var = tk.StringVar(value="https://miracle74.com/?subtopic=guilds&action=show&guild=600")
        self.guild_names = []
        self.status_var = tk.StringVar(value="Pronto")
        
        # Variáveis de Inativos e URL base
        self.inatividade_dias = tk.IntVar(value=14)
        self.url_base = tk.StringVar(value="https://miracle74.com/?subtopic=characters")
        
        self.create_widgets()
        
        # Carrega os nomes da guild assim que o programa inicia
        self.start_load_names_thread() 
        

    def get_style(self):
        return {
            'font': ('Segoe UI', 10),
            'title_font': ('Segoe UI', 12, 'bold'),
            'bg_color': '#f8f9fa',
            'frame_bg': '#ffffff',
            'generate_bg': '#dc3545', # Cor vermelha para o botão principal
            'generate_fg': 'white',
            'clear_button_bg': '#6c757d', # Cinza para o Limpar
            'status_bg': '#ced4da'
        }

    # ===============================================
    # CONSTRUÇÃO DA INTERFACE (TKINTER)
    # ===============================================

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg=self.style['bg_color'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Rótulo e Entrada da URL
        tk.Label(main_frame, text="Link da Guild:", bg=self.style['bg_color']).pack(anchor=tk.W, pady=(0, 5))
        tk.Entry(main_frame, textvariable=self.guild_url_var, width=80).pack(fill=tk.X, pady=(0, 10))

        # --- Botões de Ação Principal ---
        action_frame = tk.Frame(main_frame, bg=self.style['bg_color'])
        action_frame.pack(fill=tk.X, pady=(0, 10))

        # O BOTÃO VERMELHO QUE GERA TUDO
        self.generate_button = tk.Button(
            action_frame, 
            text="GERAR TODOS OS RANKINGS (JSON)", 
            command=self.start_all_ranking_generation,
            padx=10, pady=5, 
            bg=self.style['generate_bg'], fg=self.style['generate_fg']
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Botão Limpar
        tk.Button(
            action_frame, 
            text="Limpar", 
            command=self.clear_fields,
            bg=self.style['clear_button_bg'], fg='white', padx=10
        ).pack(side=tk.LEFT, padx=5)


        # Área de Resultados (ScrolledText)
        tk.Label(main_frame, text="Status de Geração:", bg=self.style['bg_color']).pack(anchor=tk.W, pady=(5, 0))
        self.results_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD, bg=self.style['frame_bg'])
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Barra de Status
        self.status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.style['status_bg'])
        self.status_label.pack(fill=tk.X)

    # Não precisamos mais do create_ranking_buttons pois é um botão só.

    # ===============================================
    # LÓGICA DE CARREGAMENTO DE NOMES (Guilda)
    # ===============================================
    
    def start_load_names_thread(self):
        """Inicia a thread para carregar os nomes ao iniciar o app."""
        self.status_var.set("Carregando lista de membros...")
        
        if hasattr(self, 'generate_button'): 
            self.generate_button.config(state=tk.DISABLED)
            
        Thread(target=self.load_guild_names).start()

    def load_guild_names(self):
        """Função que executa o web scraping em segundo plano."""
        guild_url = self.guild_url_var.get().strip()
        nomes = self._get_names_from_guild_url(guild_url)
        self.guild_names = nomes
        
        num_nomes = len(nomes)
        
        # Atualiza a interface 
        if num_nomes > 0:
            self.root.after(0, lambda: self.status_var.set(f"Pronto. {num_nomes} membros encontrados. Pronto para gerar JSON."))
            self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))
        else:
            self.root.after(0, lambda: self.status_var.set("ERRO: 0 membros encontrados. Verifique a URL."))
            self.root.after(0, lambda: self.generate_button.config(state=tk.DISABLED))


    def _get_names_from_guild_url(self, url):
        """Busca nomes na tabela principal de membros (MÉTODO CORRIGIDO E FUNCIONAL)."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resposta = requests.get(url, headers=headers, timeout=15)
            resposta.raise_for_status()

            soup = BeautifulSoup(resposta.content, "html.parser")
            
            guild_table = soup.find("table", class_="TableContent") 
            nomes = []

            if guild_table:
                rows = guild_table.find_all("tr", recursive=False)[1:]
                
                for row in rows:
                    tds = row.find_all("td")
                    
                    if len(tds) > 1:
                        name_cell = tds[1] 
                        link = name_cell.find("a", href=lambda href: href and "subtopic=characters" in href)
                        
                        if link and link.text.strip():
                            nome = link.text.strip()
                            if nome and "guild" not in nome.lower(): 
                                nomes.append(nome)
                                
            return list(set(nomes)) # Retorna nomes únicos

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão/requisição ao buscar nomes da guild: {e}") 
            return []
        except Exception as e:
            print(f"Erro desconhecido ao processar página da guild: {e}")
            return []

    # ===============================================
    # LÓGICA DE GERAÇÃO DE RANKING EM JSON (SEQUENCIAL)
    # ===============================================

    def start_all_ranking_generation(self):
        """Inicia a thread para gerar todos os rankings."""
        if not self.guild_names:
            messagebox.showerror("Erro", "A lista de membros está vazia. Não é possível gerar rankings.")
            return

        self.results_text.delete(1.0, tk.END)
        self.generate_button.config(state=tk.DISABLED)
        
        Thread(target=self.generate_all_skills_sequentially).start()

    def generate_all_skills_sequentially(self):
        """Itera sobre todas as skills e chama a função de ranking SEQUENCIALMENTE."""
        
        all_skills_keys = list(SKILLS.keys())
        total_skills = len(all_skills_keys)
        
        for i, skill_key in enumerate(all_skills_keys):
            skill_name = SKILLS[skill_key]
            
            self.root.after(0, lambda s=skill_name: self.results_text.insert(tk.END, f"Iniciando {s}...\n"))
            
            # --- LÓGICA DE CHAMADA DIFERENTE PARA O MAGE SKILL ---
            if skill_key == 'mage_skill':
                self.rankear_mage_skills() # Chama a função que faz a agregação de 60 páginas
            else:
                # Chama a função padrão para skills individuais
                self.rankear_guild_por_skill(skill_key) 
            
            self.root.after(0, lambda s=skill_name: self.results_text.insert(tk.END, f"-> {s} Concluído. ({i+1}/{total_skills})\n"))
            
            # Adiciona um pequeno delay para evitar que o servidor bloqueie por excesso de requests rápidos
            sleep(0.5) 

        self.root.after(0, lambda: self.status_var.set("Geração de todos os rankings concluída."))
        self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))


    def rankear_guild_por_skill(self, skill):
        """Busca as 10 páginas do ranking, filtra e SALVA como JSON (Para skills individuais)."""
        
        MAX_PAGES = self.MAX_PAGES 
        all_highscores = []
        
        # --- DEFINIÇÃO DOS ÍNDICES DE EXTRAÇÃO ---
        NAME_INDEX = 2
        
        if skill == 'experience':
            VALUE_INDEX = 4       # Level (para exibição)
            ORDER_INDEX = 5       # Experience Total (para ordenação)
            VALUE_NAME = "Level"
        else:
            # SKILLs: Skill Value em tds[5] (para exibição e ordenação)
            VALUE_INDEX = 5       # Skill Value
            ORDER_INDEX = 5       # Skill Value (ordenacao)
            VALUE_NAME = "Skill"
        
        # --- 1. COLETA DOS DADOS (Páginas 1 a 10) ---
        for page in range(1, MAX_PAGES + 1):
            url = f"https://miracle74.com/?subtopic=highscores&list={skill}&page={page}&vocation="
            try:
                self.root.after(0, lambda p=page: self.status_var.set(f"Coletando {SKILLS[skill]} - Pág. {p}/{MAX_PAGES}..."))
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # A tabela de Highscores é a SEGUNDA 'TableContent' (índice 1)
                tables = soup.find_all("table", class_="TableContent")
                if len(tables) < 2: break
                table = tables[1] 

                # Extrai os dados da página
                for tr in table.find_all("tr", bgcolor=True):
                    tds = tr.find_all("td")
                    
                    if len(tds) > ORDER_INDEX: 
                        
                        nome_tag = tds[NAME_INDEX].find("a")
                        
                        if nome_tag:
                            nome = nome_tag.text.strip()
                            
                            value_to_display = tds[VALUE_INDEX].text.strip()
                            value_to_order = tds[ORDER_INDEX].text.strip()
                            
                            all_highscores.append({
                                "nome": nome, 
                                "display_value": value_to_display, 
                                "order_value": value_to_order
                            })

            except requests.exceptions.RequestException as e:
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"Erro ao acessar ranking na página {page}: {e}\n"))
                break
        
        # --- 2. FILTRAGEM, ORDENAÇÃO E SALVAMENTO ---
        guild_names_lower = {name.lower() for name in self.guild_names} 
        nomes_em_comum = []
        
        for entry in all_highscores:
            if entry["nome"].lower() in guild_names_lower:
                nomes_em_comum.append(entry)

        # Ordenação
        def sort_key(entry):
            cleaned_value = entry['order_value'].replace(',', '').replace('.', '').replace(' ', '')
            try:
                return int(cleaned_value)
            except ValueError:
                return 0 
            
        try:
            nomes_em_comum.sort(key=sort_key, reverse=True) 
        except Exception as e:
             self.root.after(0, lambda: self.results_text.insert(tk.END, f"Erro ao ordenar: {e}\n"))
             pass 
        
        # --- 3. SALVAR EM JSON ---
        json_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "skill_name": SKILLS[skill],
            "value_type": VALUE_NAME,
            "ranking": []
        }
        
        if nomes_em_comum:
            for rank_na_guild, entry in enumerate(nomes_em_comum, start=1):
                json_data["ranking"].append({
                    "rank_guild": rank_na_guild,
                    "nome": entry['nome'],
                    "valor": entry['display_value'],
                })

        try:
            file_name = f"ranking_{skill}.json"
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"  -> JSON '{file_name}' salvo com {len(nomes_em_comum)} membros.\n"))
            
        except Exception as e:
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"ERRO FATAL ao salvar {skill} JSON: {e}\n"))


    # ===============================================
    # NOVO: LÓGICA DE AGREGAÇÃO PARA MAGE SKILLS (60 Páginas)
    # ===============================================
    def rankear_mage_skills(self):
        """Busca 60 páginas (3 weapons x 2 vocations x 10 pages) e agrega o melhor skill. (NOVO)"""
        
        mage_data = {} # Armazena o melhor skill encontrado para cada mage
        
        weapons = ['sword', 'club', 'axe']
        # 1: Sorcerer/MS, 2: Druid/ED
        vocations = {1: 'Sorcerer', 2: 'Druid'} 

        # 1. Loop Principal: Combinação de Armas e Vocações
        for weapon in weapons:
            for vocation_id, vocation_name in vocations.items():
                
                # 2. Loop de Páginas (1 a 10)
                for page in range(1, self.MAX_PAGES + 1):
                    
                    url = f"https://miracle74.com/?subtopic=highscores&list={weapon}&page={page}&vocation={vocation_id}"
                    
                    try:
                        self.root.after(0, lambda p=page: self.status_var.set(f"Coletando {vocation_name} {weapon.capitalize()} Pág {p}..."))
                        
                        # --- PAUSA AQUI (1 SEGUNDO) PARA EVITAR BLOQUEIO 429 ---
                        sleep(1) 

                        response = requests.get(url, timeout=15)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # A tabela de Highscores é a SEGUNDA 'TableContent' (índice 1)
                        tables = soup.find_all("table", class_="TableContent")
                        if len(tables) < 2: 
                            continue 
                            
                        table = tables[1] 
                        
                        # Indices da Tabela: 2 (Nome), 5 (Skill Value)
                        NAME_INDEX = 2
                        SKILL_VALUE_INDEX = 5 
                        
                        # 4. Processamento de Linhas
                        for row in table.find_all('tr', bgcolor=True):
                            cells = row.find_all('td')
                            if len(cells) <= SKILL_VALUE_INDEX: continue 
                            
                            name_tag = cells[NAME_INDEX].find('a')
                            if not name_tag: continue
                            
                            name = name_tag.text.strip()
                            
                            # Limpa o valor da skill para comparação numérica
                            skill_value_str = cells[SKILL_VALUE_INDEX].text.strip().replace(',', '').replace('.', '').replace(' ', '')
                            try:
                                skill_value = int(skill_value_str) 
                            except ValueError:
                                continue # Ignora se o valor não for numérico
                            
                            # 5. Lógica de Agregação (Unificar o melhor skill)
                            if name not in mage_data:
                                # Primeira vez que o jogador aparece
                                mage_data[name] = {
                                    'name': name,
                                    'best_skill_value': skill_value,
                                    'best_skill_name': weapon.capitalize(),
                                    'rank_value': skill_value 
                                }
                            else:
                                # Jogador já existe, checa se a skill atual é melhor
                                current_best = mage_data[name]['best_skill_value']
                                if skill_value > current_best:
                                    mage_data[name]['best_skill_value'] = skill_value
                                    mage_data[name]['best_skill_name'] = weapon.capitalize()
                                    mage_data[name]['rank_value'] = skill_value
                        
                        self.root.after(0, lambda: self.status_var.set(f"Coletando {vocation_name} {weapon.capitalize()} Pág {page}..."))


                    except requests.exceptions.RequestException as e:
                        self.root.after(0, lambda: self.results_text.insert(tk.END, f"ERRO 429/CONEXÃO: {url}\n"))
                        continue

        # 6. Ordenação e Filtragem Final
        guild_names_lower = {name.lower() for name in self.guild_names} 
        nomes_em_comum = []
        
        for name, data in mage_data.items():
            if name.lower() in guild_names_lower:
                nomes_em_comum.append({
                    "nome": data['name'],
                    "valor_exibir": f"{data['best_skill_value']} ({data['best_skill_name']})", # Valor + Arma
                    "valor_ordenar": data['best_skill_value'] # Skill pura para ordenar
                })

        # Ordenação
        def sort_key(entry):
            return entry['valor_ordenar']
            
        nomes_em_comum.sort(key=sort_key, reverse=True) 

        # 7. Salvar JSON
        json_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "skill_name": SKILLS['mage_skill'],
            "value_type": "Skill",
            "ranking": []
        }
        
        if nomes_em_comum:
            for rank_na_guild, entry in enumerate(nomes_em_comum, start=1):
                json_data["ranking"].append({
                    "rank_guild": rank_na_guild,
                    "nome": entry['nome'],
                    "valor": entry['valor_exibir'], # Salva o valor com a arma (ex: 50 (Sword))
                })

        try:
            file_name = "ranking_mage_skill.json"
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"  -> JSON '{file_name}' salvo com {len(nomes_em_comum)} membros.\n"))
            
        except Exception as e:
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"ERRO FATAL ao salvar MAGE SKILL JSON: {e}\n"))
        
    # ===============================================
    # FUNÇÕES DE UI E AUXILIARES
    # ===============================================
    
    def clear_fields(self):
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Campos limpos")

    def disable_all_buttons(self):
        if hasattr(self, 'generate_button'):
            self.generate_button.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        if hasattr(self, 'generate_button'):
            self.generate_button.config(state=tk.NORMAL)
            
    # --- Funções Placeholder ---
    def start_search_thread(self): messagebox.showinfo("Aviso", "Função desativada.")
    def display_guild_members(self): messagebox.showinfo("Aviso", "Função desativada.")
    def save_results(self): messagebox.showinfo("Aviso", "Função desativada.")
                

def buscar_informacoes_personagem(nome_personagem, url):
    return {"Name": nome_personagem, "Vocation": "N/A", "Level": "N/A", "Last Login": "N/A"}


if __name__ == "__main__":
    root = tk.Tk()
    app = GuildAnalyzerApp(root)
    root.mainloop()
import aiohttp
import asyncio
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
import threading

# Evento global para sinalizar parada
stop_event = None

async def verificar_link(session, url, timeout=10):
    try:
        async with session.get(url, timeout=timeout, ssl=False) as response:
            return response.status
    except asyncio.TimeoutError:
        return None
    except aiohttp.ClientError:
        return None

def contar_programas_tv(arquivo_entrada, encoding='utf-8'):
    with open(arquivo_entrada, 'r', encoding=encoding) as entrada:
        linhas = entrada.readlines()
    total_programas = sum(1 for linha in linhas if linha.startswith('#EXTINF'))
    return total_programas

async def processar_arquivo_m3u(arquivo_entrada, pasta_saida_funcionais, pasta_saida_nao_funcionais, total_programas, codigo_status_desejado, update_progress):
    global stop_event
    os.makedirs(pasta_saida_funcionais, exist_ok=True)
    os.makedirs(pasta_saida_nao_funcionais, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        with open(arquivo_entrada, 'r', encoding='utf-8') as entrada:
            linhas = entrada.readlines()

        valid_links = []
        invalid_links = []
        urls_repetidas = []
        urls_repetidas_dict = {}
        programas_processados = 0
        urls_processadas = {}

        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if linha.startswith('#EXTINF'):
                if i + 1 < len(linhas):
                    url = linhas[i + 1].strip()
                    if url.startswith(('http://', 'https://')):
                        if url in urls_processadas:
                            status_repetido = urls_processadas[url]
                            urls_repetidas_dict[url] = status_repetido
                            urls_repetidas.append(url)
                            status_text.insert(tk.END, f"[{status_repetido}] (REPETIDO) {url}\n", ("orange",))
                            status_text.tag_config("orange", foreground="orange")
                            status_text.see(tk.END)
                            continue

                        status = await verificar_link(session, url)
                        status_code = status if status else 'INVALID'
                        urls_processadas[url] = status_code

                        color = "green" if status == codigo_status_desejado else "red"
                        status_text.insert(tk.END, f"[{status_code}] {url}\n", (color,))
                        status_text.tag_config(color, foreground=color)
                        status_text.see(tk.END)

                        if status == codigo_status_desejado:
                            valid_links.append((status_code, linha, url))
                        else:
                            invalid_links.append((status_code, linha, url))

                        programas_processados += 1
                        progresso = (programas_processados / total_programas) * 100
                        update_progress(progresso)

            if stop_event.is_set():
                break

        if valid_links:
            arquivo_saida_funcionais = os.path.join(pasta_saida_funcionais, 'canais_validos.m3u')
            with open(arquivo_saida_funcionais, 'w', encoding='utf-8') as saida_funcionais:
                for status, linha, url in valid_links:
                    saida_funcionais.write(f"{linha}\n{url}\n")

            arquivo_saida_validos_txt = os.path.join(pasta_saida_funcionais, 'canais_validos.txt')
            with open(arquivo_saida_validos_txt, 'w', encoding='utf-8') as saida_validos_txt:
                for status, linha, url in valid_links:
                    saida_validos_txt.write(f"[{status}] {url}\n")
                saida_validos_txt.write(f"\nTotal de URLs analisadas: {len(valid_links)}\n")

        if invalid_links:
            arquivo_saida_nao_funcionais = os.path.join(pasta_saida_nao_funcionais, 'canais_invalidos.m3u')
            with open(arquivo_saida_nao_funcionais, 'w', encoding='utf-8') as saida_nao_funcionais:
                for status, linha, url in invalid_links:
                    saida_nao_funcionais.write(f"#EXTINF:-1, INVALID\n{linha}\n{url}\n")

            arquivo_saida_invalidos_txt = os.path.join(pasta_saida_nao_funcionais, 'canais_invalidos.txt')
            with open(arquivo_saida_invalidos_txt, 'w', encoding='utf-8') as saida_invalidos_txt:
                for status, linha, url in invalid_links:
                    saida_invalidos_txt.write(f"[{status}] {url}\n")
                saida_invalidos_txt.write(f"\nTotal de URLs analisadas: {len(invalid_links)}\n")

        # Salvar URLs repetidas em um arquivo na pasta canais_validos
        # Salvar URLs repetidas em um arquivo na pasta canais_validos
        if urls_repetidas_dict:  # Verifique se o dicionário contém entradas
            pasta_saida_repetidas = os.path.join(pasta_saida_funcionais)
            os.makedirs(pasta_saida_repetidas, exist_ok=True)
            arquivo_urls_repetidas = os.path.join(pasta_saida_repetidas, 'urls_repetidas.txt')
            with open(arquivo_urls_repetidas, 'w', encoding='utf-8') as saida_repetidas:
                for url in urls_repetidas:  # Alterado para iterar sobre urls_repetidas
                    status = urls_repetidas_dict[url]
                    saida_repetidas.write(f"[{status}] {url}\n")
                saida_repetidas.write(f"\nTotal de URLs repetidas: {len(urls_repetidas)}\n")




        update_progress(100)
        iniciar_button.config(state=tk.NORMAL)  # Reabilitar o botão "Iniciar"
        codigo_status_entry.config(state=tk.NORMAL)
        selecionar_arquivo_button.config(state=tk.NORMAL)
        parar_button.config(state=tk.DISABLED)


def run_asyncio(loop, *args):
    asyncio.run(processar_arquivo_m3u(*args))

def validar_arquivo():
    arquivo_entrada = input_arquivo.get().strip()
    if not arquivo_entrada:
        pasta_original = os.path.join(os.path.dirname(__file__), 'original')
        if not os.path.exists(pasta_original):
            os.makedirs(pasta_original)
        arquivos_m3u = [f for f in os.listdir(pasta_original) if f.endswith(('.m3u', '.m3u8'))]
        if arquivos_m3u:
            arquivo_entrada = os.path.join(pasta_original, arquivos_m3u[0])
            input_arquivo.config(state=tk.NORMAL)  # Habilitar somente para exibir
            input_arquivo.delete(0, tk.END)
            input_arquivo.insert(0, arquivo_entrada)
            input_arquivo.config(state='readonly')  # Tornar não editável
        else:
            return None
    return arquivo_entrada

def iniciar_processamento():
    global stop_event
    arquivo_entrada = validar_arquivo()
    
    if not arquivo_entrada:
        # Se não houver arquivo, exiba um aviso e retorne
        messagebox.showwarning("Aviso", "Nenhum arquivo M3U encontrado ou selecionado. Selecione um arquivo.")
        return

    stop_event = asyncio.Event()
    iniciar_button.config(state=tk.DISABLED)
    parar_button.config(state=tk.NORMAL)
    input_arquivo.config(state='readonly')  # Tornar não editável
    codigo_status_entry.config(state=tk.DISABLED)
    selecionar_arquivo_button.config(state=tk.DISABLED)

    codigo_status_desejado = int(codigo_status_entry.get()) if codigo_status_entry.get().isdigit() else 200
    total_programas = contar_programas_tv(arquivo_entrada)

    progresso_var.set(0)
    progress_bar['value'] = 0

    loop = asyncio.new_event_loop()
    threading.Thread(target=run_asyncio, args=(loop, arquivo_entrada, 'canais_validos', 'canais_invalidos', total_programas, codigo_status_desejado, update_progress)).start()

def update_progress(value):
    progresso_var.set(value)
    progress_bar['value'] = value

def selecionar_arquivo():
    arquivo_entrada = filedialog.askopenfilename(filetypes=[("M3U files", "*.m3u;*.m3u8")])
    if arquivo_entrada:
        input_arquivo.config(state=tk.NORMAL)  # Habilitar para mostrar o caminho
        input_arquivo.delete(0, tk.END)
        input_arquivo.insert(0, arquivo_entrada)
        input_arquivo.config(state='readonly')  # Tornar não editável

def parar_operacao():
    global stop_event
    stop_event.set()

def limpar_feedback():
    status_text.delete(1.0, tk.END)

def ajustar_responsividade(event):
    status_text.config(width=event.width // 10, height=event.height // 30)

root = tk.Tk()
root.title("Verificador de Links M3U")
root.geometry("700x500")
root.config(bg="#1C1C1C")
root.bind("<Configure>", ajustar_responsividade)

# Estilo do botão
def estilo_botao(botao):
    botao.config(bg="#ADD8E6", fg="black", borderwidth=2, relief="groove", activebackground="#87CEEB", activeforeground="black", font=("Arial", 10, "bold"), padx=5, pady=5)

frame_top = tk.Frame(root, bg="#1C1C1C")
frame_top.pack(pady=10)

tk.Label(frame_top, text="Arquivo selecionado:", bg="#1C1C1C", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky='e')
input_arquivo = tk.Entry(frame_top, width=60, fg="black", bg="#363636", insertbackground="white")
input_arquivo.grid(row=0, column=1, padx=5, pady=5)
input_arquivo.config(state='readonly')  # Tornar não editável inicialmente

selecionar_arquivo_button = tk.Button(frame_top, text="Selecionar Arquivo", command=selecionar_arquivo)
estilo_botao(selecionar_arquivo_button)
selecionar_arquivo_button.grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame_top, text="Código HTTP desejado:", bg="#1C1C1C", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky='e')
codigo_status_entry = tk.Entry(frame_top, width=10, bg="#363636", fg="white", insertbackground="white")
codigo_status_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
codigo_status_entry.insert(0, '200')

iniciar_button = tk.Button(frame_top, text="Iniciar", command=iniciar_processamento)
estilo_botao(iniciar_button)
iniciar_button.grid(row=2, column=1, padx=5, pady=10, sticky='w')

parar_button = tk.Button(frame_top, text="Parar", command=parar_operacao)
estilo_botao(parar_button)
parar_button.grid(row=2, column=2, padx=5, pady=10)
parar_button.config(state=tk.DISABLED)

frame_progress = tk.Frame(root, bg="#1C1C1C")
frame_progress.pack(pady=10)

style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", background="#ADD8E6", troughcolor="#363636")  # Customize as cores

progresso_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, variable=progresso_var, maximum=100, length=500, style="TProgressbar")
progress_bar.pack(pady=5)

frame_feedback = tk.Frame(root, bg="#1C1C1C")
frame_feedback.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
status_text = scrolledtext.ScrolledText(frame_feedback, wrap=tk.WORD, width=70, height=20, bg="#2E2E2E", fg="white", insertbackground="white")
status_text.pack(fill=tk.BOTH, expand=True)

limpar_button = tk.Button(root, text="Limpar Feedback", command=limpar_feedback)
estilo_botao(limpar_button)
limpar_button.pack(pady=5)

try:
    root.iconbitmap('i.ico')
except Exception:
    pass

root.mainloop()

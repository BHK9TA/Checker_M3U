import aiohttp
import asyncio
import os

async def verificar_link(session, url, timeout=10):
    try:
        async with session.get(url, timeout=timeout, ssl=False) as response:
            return response.status
    except asyncio.TimeoutError:
        return None
    except aiohttp.ClientError:
        return None

def contar_programas_tv(arquivo_entrada, encoding='utf-8'):
    """ Conta quantas entradas de programas de TV (linhas começando com #EXTINF) existem no arquivo M3U. """
    with open(arquivo_entrada, 'r', encoding=encoding) as entrada:
        linhas = entrada.readlines()
    total_linhas = len(linhas)
    total_programas = sum(1 for linha in linhas if linha.startswith('#EXTINF'))
    return total_programas, total_linhas

async def processar_arquivo_m3u(arquivo_entrada, pasta_saida_funcionais, pasta_saida_nao_funcionais, total_programas, total_linhas, encoding='utf-8'):
    os.makedirs(pasta_saida_funcionais, exist_ok=True)
    os.makedirs(pasta_saida_nao_funcionais, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        with open(arquivo_entrada, 'r', encoding=encoding) as entrada:
            linhas = entrada.readlines()

        valid_links = []
        invalid_links = []
        programas_processados = 0
        progresso_programas = 0

        i = 0
        while i < len(linhas):
            linha = linhas[i].strip()
            if linha.startswith('#EXTINF'):
                if i + 1 < len(linhas):
                    url = linhas[i + 1].strip()
                    if url.startswith(('http://', 'https://')):
                        status = await verificar_link(session, url)
                        if status in (200, 204, 301, 302, 304, 406):
                            valid_links.append((linha, url, status))
                            print(f"Link válido: {url} (status: {status})")
                        else:
                            invalid_links.append((linha, url, status))
                            print(f"Link inválido: {url} (status: {status})")
                    programas_processados += 1
                    progresso_programas = (programas_processados / total_programas) * 100

                i += 2
            else:
                i += 1

            progresso_linhas = (i / total_linhas) * 100
            print(f"Programas ao vivo: {programas_processados}/{total_programas} ({progresso_programas:.2f}%) | Linhas: {i}/{total_linhas} ({progresso_linhas:.2f}%)", end='\r', flush=True)

        # Salva os links válidos
        arquivo_saida_funcionais = os.path.join(pasta_saida_funcionais, 'canais_validos.m3u')
        with open(arquivo_saida_funcionais, 'w', encoding=encoding) as saida_funcionais:
            for linha, url, status in valid_links:
                saida_funcionais.write(f"{linha}\n{url}\n")
        
        # Salva os links inválidos
        arquivo_saida_nao_funcionais = os.path.join(pasta_saida_nao_funcionais, 'canais_invalidos.m3u')
        with open(arquivo_saida_nao_funcionais, 'w', encoding=encoding) as saida_nao_funcionais:
            for linha, url, status in invalid_links:
                saida_nao_funcionais.write(f"#EXTINF:-1, INVALID\n{linha}\n{url}\n")
        
        # Salva o status dos links válidos em .txt
        arquivo_saida_validos_txt = os.path.join(pasta_saida_funcionais, 'canais_validos.txt')
        with open(arquivo_saida_validos_txt, 'w', encoding=encoding) as saida_validos_txt:
            for linha, url, status in valid_links:
                saida_validos_txt.write(f"status {status} {url}\n")

        # Salva o status dos links inválidos em .txt
        arquivo_saida_invalidos_txt = os.path.join(pasta_saida_nao_funcionais, 'canais_invalidos.txt')
        with open(arquivo_saida_invalidos_txt, 'w', encoding=encoding) as saida_invalidos_txt:
            for linha, url, status in invalid_links:
                if status:
                    saida_invalidos_txt.write(f"status {status} {url}\n")
                else:
                    saida_invalidos_txt.write(f"INVALID {url}\n")

async def processar_pasta(pasta_entrada, encoding='utf-8'):
    pasta_saida_funcionais = 'canais_validos'
    pasta_saida_nao_funcionais = 'canais_invalidos'
    
    for raiz, _, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.endswith(('.m3u', '.m3u8')):
                caminho_arquivo = os.path.join(raiz, arquivo)
                print(f"Processando arquivo: {caminho_arquivo}")
                total_programas, total_linhas = contar_programas_tv(caminho_arquivo, encoding)
                print(f"Total de programas ao vivo: {total_programas}, Total de linhas: {total_linhas}")
                await processar_arquivo_m3u(caminho_arquivo, pasta_saida_funcionais, pasta_saida_nao_funcionais, total_programas, total_linhas, encoding)

def main(pasta_entrada, encoding='utf-8'):
    asyncio.run(processar_pasta(pasta_entrada, encoding))

pasta_entrada = 'original'  # Nome da pasta onde os arquivos estão
main(pasta_entrada, encoding='utf-8')

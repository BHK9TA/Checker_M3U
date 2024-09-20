📺 Checker_M3U: Script para Verificação de Links M3U
Este script em Python permite separar links de transmissão ao vivo de arquivos M3U, automatizando a verificação de links funcionais e não funcionais.

📁 O que o script faz:
1. Carrega o arquivo .m3u
O arquivo deve ser colocado em uma pasta chamada "origem".
2. Conta os programas ao vivo
O script lê entradas que começam com #EXTINF e conta quantos programas ao vivo existem.
3. Verifica os links
Utiliza requisições HTTP assíncronas (com aiohttp) para acessar os URLs.
O script considera um link funcional se retornar um dos códigos de resposta HTTP definidos.
🔍 Critério de Validação
O script verifica os seguintes códigos como válidos: 200, 204, 301, 302, 304, 406.
Você pode modificar esses critérios no código, impactando a eficiência e precisão da análise:
Por exemplo, incluir 403 como válido pode marcar links bloqueados como funcionais.
A precisão pode variar entre 90% e 100% dependendo dos critérios escolhidos.
📤 Gera os arquivos de saída:
canais_validos.m3u: Contém os links válidos.
canais_invalidos.m3u: Contém os links inválidos.
canais_validos.txt e canais_invalidos.txt: Listam os status dos links.
📂 Estrutura das pastas:
Pasta de entrada: Coloque o arquivo .m3u na pasta "origem".
Pastas de saída: O script criará as pastas canais_validos e canais_invalidos automaticamente.
🔧 Instalação das bibliotecas:
Para rodar o script, instale as bibliotecas necessárias com o seguinte comando:

bash
Copiar código
pip install aiohttp asyncio
🚀 Passos para executar:
Coloque o arquivo Checker_M3U.py em uma pasta.
Crie uma pasta chamada "origem" e adicione o arquivo .m3u nela.
No terminal (Linux/macOS) ou CMD (Windows), navegue até o diretório do script e execute:
bash
Copiar código
python Checker_M3U.py
🛠️ Personalização dos códigos de resposta:
Para modificar quais códigos HTTP são considerados válidos, altere a seguinte linha no código:

python
Copiar código
if status in (200, 204, 301, 302, 304, 406):
Para incluir o código 403, você poderia alterar para:

python
Copiar código
if status in (200, 204, 301, 302, 304, 403, 406):
🔑 Funções principais:
verificar_link: Faz a verificação do link e retorna o código de status HTTP.
contar_programas_tv: Conta quantas entradas de programas ao vivo existem no arquivo M3U.
processar_arquivo_m3u: Processa cada link, verificando sua funcionalidade e gerando os arquivos de saída.
processar_pasta: Itera sobre todos os arquivos .m3u na pasta de entrada e aplica a verificação de links.
✅ Conclusão:
Este script automatiza a verificação de listas de IPTV, separando de forma eficiente os links funcionais dos quebrados. Modificar os critérios de validação pode impactar a precisão, que geralmente fica entre 90% e 100%, dependendo das regras definidas.

Segue um outro repositório sobre como colocar o catálogo de transmissão ao vivo do jellyfin em modo lista https://github.com/BHK9TA/LiveTv-in-Jellyfin-list-mode

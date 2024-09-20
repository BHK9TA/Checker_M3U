Aqui está uma versão formatada em Markdown que você pode usar no GitHub. O Markdown é a linguagem padrão para formatação de README em repositórios GitHub, e ela permite títulos, negritos, listas e códigos formatados de maneira clara.

Exemplo de README.md:
markdown
Copiar código
# Checker_M3U

Este script em Python processa arquivos `.m3u` (listas de links de IPTV) e separa automaticamente links de transmissão ao vivo funcionais de links não funcionais. Ele gera arquivos de saída com links válidos e inválidos, além de relatórios com o status HTTP de cada link.

## Funcionalidades

- **Processa listas `.m3u`**: Separa links funcionais de não funcionais.
- **Códigos HTTP personalizáveis**: Defina os códigos de resposta que você considera válidos (ex: 200, 204, 301, etc.).
- **Gera arquivos `.m3u` e `.txt`**: Com links válidos e inválidos, e relatórios de status.
- **Alta precisão (90%-100%)**: Dependendo dos critérios de validação que você escolher.

---

## 📦 Instalação

1. **Instale o Python**:
   - O script foi testado na versão **Python 3.12.6**. Certifique-se de estar usando esta versão ou uma similar.
   
2. **Instale as bibliotecas necessárias**:
   Execute o seguinte comando no terminal para instalar as dependências:

   ```bash
   pip install aiohttp asyncio
🚀 Como Usar
Preparar o ambiente:

Coloque o arquivo Checker_M3U.py em uma pasta.
Crie uma pasta ao lado chamada origem e adicione seu arquivo .m3u dentro dessa pasta.
Executar o script:

Abra o terminal (ou o CMD no Windows) e navegue até a pasta onde o arquivo Checker_M3U.py está localizado.

Execute o comando:

bash
Copiar código
python Checker_M3U.py
Resultado:

O script separará automaticamente os links e criará duas pastas:
canais_validos: Links que passaram no teste de funcionalidade.
canais_invalidos: Links que não passaram no teste.
🔧 Configuração Personalizada
Códigos de Resposta HTTP
Por padrão, o script considera os seguintes códigos HTTP como válidos: 200, 204, 301, 302, 304, 406.
Você pode alterar esses critérios modificando esta linha do código:

python
Copiar código
if status in (200, 204, 301, 302, 304, 406):
Se, por exemplo, você quiser incluir o código 403 (proibido) nos links válidos, altere para:

python
Copiar código
if status in (200, 204, 301, 302, 304, 403, 406):
⚠️ Importante: Alterar esses critérios afeta a precisão da análise. Dependendo dos códigos de resposta escolhidos, a precisão da separação de links pode variar entre 90% e 100%.

📂 Estrutura das Pastas
Entrada: Coloque o arquivo .m3u dentro da pasta origem.
Saída:
canais_validos/: Arquivo .m3u com links funcionais e um relatório .txt.
canais_invalidos/: Arquivo .m3u com links inválidos e um relatório .txt.
📝 Explicação do Código
Funções Principais:
verificar_link(session, url, timeout=10): Faz a verificação de um link de transmissão e retorna o código de status HTTP.

contar_programas_tv(arquivo_entrada): Conta quantos programas ao vivo (entradas com #EXTINF) existem no arquivo .m3u.

processar_arquivo_m3u(arquivo_entrada, pasta_saida_funcionais, pasta_saida_nao_funcionais): Processa cada link, verifica se é funcional e salva os resultados.

processar_pasta(pasta_entrada): Processa todos os arquivos .m3u encontrados na pasta de entrada.

Personalização da Precisão
Ao ajustar os códigos de resposta HTTP que são considerados "válidos", você pode ter maior controle sobre a eficiência e precisão do script. Por exemplo:

Incluir 403 (proibido) nos códigos válidos pode adicionar links que funcionam apenas em certas regiões ou requerem autenticação.
Excluir 204 (sem conteúdo) pode eliminar links que estão funcionando, mas não possuem conteúdo visível no momento da verificação.
A precisão da análise, então, pode variar entre 90% e 100%, dependendo dos códigos que você considera como "válidos".

🛠️ Dependências
Python 3.12.6 (ou semelhante)
Bibliotecas Python: aiohttp, asyncio
Exemplo de Execução
bash
Copiar código
$ python Checker_M3U.py
Processando arquivo: origem/lista_exemplo.m3u
Total de programas ao vivo: 150, Total de linhas: 450
Link válido: http://exemplo.com/stream (status: 200)
Link inválido: http://exemplo.com/fail (status: 404)
...
Programas ao vivo: 150/150 (100.00%) | Linhas: 450/450 (100.00%)
Após a execução, você encontrará os arquivos separados em canais_validos e canais_invalidos, com relatórios em .txt mostrando o status de cada link.

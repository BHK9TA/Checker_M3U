# 📊 Análise Detalhada da ultima versão do Verificador de Links Checker_M3U_1.02

## 📝 Descrição
O script é um verificador de links em arquivos M3U que utiliza a biblioteca `Tkinter` para criar uma interface gráfica. Ele permite selecionar um arquivo M3U, verificar a validade dos links contidos nele e exibir os resultados na interface. O programa faz mesclagem de links idênticos, salvando apenas uma cópia única deles nos arquivos M3U de saída. Os links repetidos são registrados no arquivo `urls_repetidas.txt`, que contém uma cópia dos links com suas ocorrências.

![Capturar](https://github.com/user-attachments/assets/25c2cc8c-78d3-4678-a5b6-9f9b9a8d6175)


## 📦 Dependências
Para executar o script, você precisa instalar as seguintes bibliotecas:

1. **aiohttp**: Usada para realizar requisições assíncronas HTTP.
2. **asyncio**: Parte da biblioteca padrão do Python, utilizada para programação assíncrona.
3. **tkinter**: Biblioteca padrão para criar interfaces gráficas em Python (já incluída na maioria das distribuições Python).

### 📥 Instalação das Dependências

#### 🪟 Windows
1. **Instalar Python**:
   - Baixe o instalador do Python em [python.org](https://www.python.org/downloads/).
   - python --version => Python 3.12.6
   - Durante a instalação, marque a opção "Add Python to PATH".

2. **Instalar as bibliotecas**:
   - Abra o Prompt de Comando e execute:
     ```bash
     pip install aiohttp
     pip install asyncio
     pip install tk
     ```

#### 🐧 Linux
1. **Instalar Python** (se não estiver instalado):
   - Para distribuições Debian/Ubuntu:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-tk
     ```
   - Para distribuições Fedora:
     ```bash
     sudo dnf install python3 python3-pip python3-tkinter
     ```

2. **Instalar as bibliotecas**:
   - Abra o terminal e execute:
     ```bash
     pip3 install aiohttp
     pip3 install asyncio
     ```

## 🚀 Como Usar

### 🏁 Executando o Script
1. **Salve o código em um arquivo**: Crie um arquivo chamado `Checker_M3U.py` e cole o código do script nele.

2. **Prepare o arquivo M3U**: Uma opção interessante que adicionei é a possibilidade de criar uma pasta chamada 'original' ao lado do script. Dentro dessa pasta, você pode colocar seu arquivo M3U ou M3U8 com qualquer nome e iniciar a análise no programa sem precisar procurar o diretório. No entanto, isso fica a seu critério: se preferir buscar o arquivo em um local específico, basta clicar no botão 'Selecionar Arquivo'.

3. **Execute o script**:
   - No Windows, abra o Prompt de Comando na pasta onde o script está e execute:
     ```bash
     python Checker_M3U.py
     ```
   - No Linux, abra o terminal navegue até a pasta onde o script está e execute:
     ```bash
     python3 Checker_M3U.py
     ```

### 🖥️ Interface do Usuário
- **Selecionar Arquivo**: Clique no botão "Selecionar Arquivo" para escolher um arquivo M3U. O caminho do arquivo selecionado aparecerá no campo de entrada, ou deixe vazio caso já tenha colocado o arquivo M3U dentro da pasta 'original'.
- **Código HTTP Desejado**: Insira o código HTTP que deseja verificar (por padrão, é 200). O programa sugerirá outros códigos como 204, 403, etc.
- **Iniciar Processamento**: Clique no botão "Iniciar" para começar a verificação dos links.
- **Parar Operação**: Se necessário, clique no botão "Parar" para interromper o processo em andamento. O programa não será fechado, permitindo que você execute novas verificações.
- **Limpar Feedback**: O botão "Limpar Feedback" apaga o texto exibido na área de status.

### 📋 Resultados
Os links válidos e inválidos são salvos em arquivos:
- **canais_validos.m3u** e **canais_invalidos.m3u**: Contêm os links válidos e inválidos, respectivamente.
- **canais_validos.txt** e **canais_invalidos.txt**: Contêm a lista de links válidos e inválidos com seus códigos de status.
- **urls_repetidas.txt**: Contém cópias dos links que apareceram mais de uma vez.

## ⚠️ Considerações Finais
- **Interface Responsiva**: O programa ajusta automaticamente a interface ao redimensionar a janela.
- **Compatibilidade**: O script é compatível tanto com Windows quanto com Linux, desde que as dependências estejam corretamente instaladas.

Siga esses passos para configurar e usar o verificador de links M3U de forma eficaz!

Aqui está um outro repositório meu sobre o Jellyfin: https://github.com/BHK9TA/LiveTv-in-Jellyfin-list-mode

Download: [Checker_M3U_0.02.zip]([https://github.com/user-attachments/files/17091561/Checker_M3U_0.02.zip](https://github.com/user-attachments/files/17091549/Checker_M3U_0.02.zip))

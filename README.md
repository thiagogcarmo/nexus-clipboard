NEXUS // CLIPBOARD_MANAGER
Um gerenciador de área de transferência de alta performance e ultra-baixa latência, construído em Python com uma estética Cyberpunk/Sci-Fi HUD. Desenvolvido para superar as limitações do histórico nativo do Windows 11, o Nexus permite armazenar modelos infinitos de texto, organizados por abas e salvos permanentemente em um banco de dados local.

🚀 Recursos Principais
Organização por Assuntos (Abas): Crie, renomeie e exclua categorias facilmente para separar modelos de trabalho, códigos, links ou textos frequentes.

Cópia em um Clique: Textos ficam prontos para uso. Um clique no bloco de texto envia o conteúdo instantaneamente para a área de transferência do sistema operacional.

Armazenamento Persistente: Integração nativa com SQLite (nexus_data.db). Seus dados não são perdidos ao fechar o programa e o consumo de memória RAM permanece mínimo.

Exclusão de Precisão: Botões de exclusão inline para remover textos específicos sem interferir na visualização da lista.

Interface Cyberpunk Customizada: UI estilizada via QSS (PyQt6) com tema escuro, bordas neon e fontes monoespaçadas de terminais clássicos.

Suporte a Teclado: Adicione abas e textos rapidamente pressionando Enter, sem depender exclusivamente de cliques do mouse.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.x

Interface Gráfica: PyQt6 (via QWidget, QTabWidget e customização QSS avançada)

Banco de Dados: SQLite3 (Embutido)

Manipulação de SO: QClipboard para integração direta com a área de transferência do Windows.

⚙️ Instalação e Execução
Certifique-se de ter o Python instalado na sua máquina (recomendado Python 3.8 ou superior).

Clone este repositório ou faça o download do arquivo cyber_clipboard.py.

Abra o terminal (CMD, PowerShell ou VS Code) na pasta do projeto e instale a dependência gráfica:

Bash
pip install PyQt6
Execute o programa:

Bash
python cyber_clipboard.py
📖 Como Usar
Criar uma Aba: Digite o nome do assunto na barra superior (ex: PROJETOS_IOT ou RESPOSTAS_RAPIDAS) e pressione Enter ou clique em [ CRIAR ABA ].

Adicionar Texto: Selecione a aba desejada, digite ou cole seu modelo de texto na barra inferior e pressione Enter ou clique em [ ADD TEXTO ].

Copiar para Uso: Clique em qualquer texto da lista. A barra de título exibirá NEXUS // COPIADO:... indicando que o texto já pode ser colado (Ctrl + V) em qualquer outro aplicativo.

Excluir Conteúdo:

Para excluir um texto individual, clique no pequeno botão vermelho [ X ] alinhado à direita.

Para excluir uma categoria inteira (e todos os textos nela), clique no ícone de fechar na própria aba superior.

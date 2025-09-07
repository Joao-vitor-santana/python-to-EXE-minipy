# 🐍 miniPy

O **miniPy** é um ambiente gráfico simplificado para Python que automatiza o fluxo de trabalho de desenvolvedores e estudantes.  
Com ele, é possível **executar scripts Python, instalar automaticamente as bibliotecas necessárias e gerar executáveis `.exe` com apenas um clique** — tudo dentro de uma interface intuitiva feita em **Tkinter**.  

É como ter um **mini PyCharm automatizado**, leve e direto ao ponto.

---

## ✨ Funcionalidades

- 📁 **Abrir e salvar arquivos `.py`** diretamente na interface.  
- 🚀 **Executar códigos Python** em apenas um clique.  
- 📦 **Instalação automática de dependências**: bibliotecas importadas no código são detectadas e instaladas sem necessidade de comandos no terminal.  
- 🔧 **Geração de executáveis `.exe`** com PyInstaller integrado.  
- ⚙️ **Instalação automática do PyInstaller**, caso não esteja disponível.  
- 🖥️ **Console embutido** para visualizar saída, erros e logs em tempo real.  
- 📝 **Editor de código integrado**, com destaque e suporte para múltiplas linhas.  
- 🔄 **Criação e exclusão automática de arquivos temporários** durante a execução.  
- 📂 **Abertura rápida da pasta de saída** onde os `.exe` são gerados.  
- 🔍 **Verificação de dependências** já instaladas no ambiente.  
---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**  
- **Tkinter** (interface gráfica)  
- **Subprocess** (execução de scripts e comandos)  
- **AST** (detecção de imports no código)  
- **Threading** (execução sem travar a interface)  
- **PyInstaller** (geração de `.exe`)  

---

##  Como Usar

1. Clone o repositório:  
   ```bash
   git clone https://github.com/seuusuario/minipy.git
   cd minipy
   ```

2. Execute o programa:  
   ```bash
   python minipy.py
   ```

3. Abra ou escreva seu código no editor integrado.  

4. Clique em:  
   - **🚀 Executar** → roda o código e instala dependências.  
   - **🔧 Gerar EXE** → cria um executável pronto para distribuição.  

---

## 📂 Estrutura de Saída

Ao gerar um `.exe`, o miniPy cria automaticamente a pasta:  

```
/seu_projeto/
   ├── seu_script.py
   └── exe_output/
        └── seu_script_executable.exe
```

---

## ⚖️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE).  
Você pode usar, modificar e distribuir livremente, mantendo os créditos do autor.  

---

## 💡 Ideias Futuras

- 🎨 Editor com destaque de sintaxe aprimorado.  
- 🔍 Pesquisa e substituição no editor.  
- 📊 Monitoramento de uso de memória e CPU durante execução.  
- 🌐 Suporte multiplataforma com geração de binários para Linux e macOS.  

---

## 🤝 Contribuições

Contribuições são bem-vindas!  
Abra uma **issue** ou envie um **pull request** para ajudar a melhorar o miniPy.  

---

### ✍️ Autor

Criado por **JOÃO VITOR DOS SANTOS SANTANA**  
Se gostou do projeto, deixe uma ⭐ no repositório para apoiar! 🚀  

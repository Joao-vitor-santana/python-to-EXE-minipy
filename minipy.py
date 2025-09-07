import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import re
import ast
import threading
import importlib.util
from pathlib import Path
import tempfile

class PythonExecutor:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCharm Avançado - Executador Python Inteligente")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")
        
        # Instalar dependências necessárias do próprio programa
        self.install_self_dependencies()
        
        # Variáveis
        self.current_file = None
        self.code_changed = False
        self.exe_output_folder = None
        self.temp_file_counter = 0
        
        self.setup_ui()
        
    def install_self_dependencies(self):
        """Instala as dependências necessárias para o próprio programa funcionar"""
        required_packages = ['subprocess', 'ast', 'importlib', 'pathlib']
        # Estas são bibliotecas padrão do Python, mas podemos adicionar outras se necessário
        
        try:
            # Exemplo: se precisássemos de bibliotecas externas
            # import requests
            pass
        except ImportError as e:
            print(f"Instalando dependências do programa: {e}")
            
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de ferramentas
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Primeira linha de botões
        toolbar1 = ttk.Frame(toolbar)
        toolbar1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar1, text="📁 Abrir Arquivo", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar1, text="💾 Salvar", command=self.save_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar1, text="💾 Salvar Como", command=self.save_as_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar1, text="🚀 Executar", command=self.run_code, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar1, text="📦 Verificar Dependências", command=self.check_dependencies).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar1, text="🔄 Limpar Console", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        
        # Segunda linha de botões
        toolbar2 = ttk.Frame(toolbar)
        toolbar2.pack(fill=tk.X)
        
        ttk.Button(toolbar2, text="🔧 Gerar EXE", command=self.generate_exe, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar2, text="📂 Abrir Pasta EXE", command=self.open_exe_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar2, text="⚙️ Instalar PyInstaller", command=self.install_pyinstaller).pack(side=tk.LEFT, padx=5)
        
        # Frame para editor e console
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Editor de código
        editor_frame = ttk.LabelFrame(content_frame, text="Editor de Código", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))
        
        self.code_editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE, 
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            selectbackground='#264f78'
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        self.code_editor.bind('<KeyRelease>', self.on_code_change)
        
        # Console de saída
        console_frame = ttk.LabelFrame(content_frame, text="Console de Saída", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=(5, 0))
        
        self.console_output = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#000000',
            fg='#00ff00',
            state=tk.DISABLED
        )
        self.console_output.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status
        self.status_bar = ttk.Label(main_frame, text="Pronto", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Código de exemplo
        example_code = '''# Exemplo de código Python
# Este executor instalará automaticamente as bibliotecas necessárias!

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def exemplo_funcao():
    print("Olá! Este é um exemplo de código.")
    print("O executor instalará automaticamente:")
    print("- requests")
    print("- pandas") 
    print("- matplotlib")
    print("- numpy")
    
    # Exemplo de uso
    data = np.array([1, 2, 3, 4, 5])
    print(f"Array NumPy: {data}")
    
    return "Código executado com sucesso!"

if __name__ == "__main__":
    resultado = exemplo_funcao()
    print(resultado)
'''
        self.code_editor.insert(tk.END, example_code)
        
    def on_code_change(self, event=None):
        """Marca que o código foi alterado"""
        self.code_changed = True
        if self.current_file:
            title = f"PyCharm Avançado - {os.path.basename(self.current_file)} *"
        else:
            title = "PyCharm Avançado - Novo Arquivo *"
        self.root.title(title)
        
    def open_file(self):
        """Abre um arquivo Python"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_editor.delete(1.0, tk.END)
                    self.code_editor.insert(1.0, content)
                    self.current_file = file_path
                    self.code_changed = False
                    self.root.title(f"PyCharm Avançado - {os.path.basename(file_path)}")
                    self.update_status(f"Arquivo carregado: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir arquivo: {str(e)}")
                
    def save_file(self):
        """Salva o arquivo atual"""
        if self.current_file:
            try:
                content = self.code_editor.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.code_changed = False
                self.root.title(f"PyCharm Avançado - {os.path.basename(self.current_file)}")
                self.update_status(f"Arquivo salvo: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        """Salva o arquivo com um novo nome"""
        file_path = filedialog.asksaveasfilename(
            title="Salvar arquivo Python",
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                content = self.code_editor.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = file_path
                self.code_changed = False
                self.root.title(f"PyCharm Avançado - {os.path.basename(file_path)}")
                self.update_status(f"Arquivo salvo: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")

    def create_temp_file(self, code):
        """Cria arquivo temporário para códigos grandes"""
        # Incrementar contador para nomes únicos
        self.temp_file_counter += 1
        
        # Criar arquivo temporário
        temp_dir = tempfile.gettempdir()
        temp_filename = f"temp_code_{self.temp_file_counter}.py"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(code)
            return temp_path
        except Exception as e:
            self.log_to_console(f"❌ Erro ao criar arquivo temporário: {e}")
            return None

    def extract_imports(self, code):
        """Extrai todas as bibliotecas importadas do código"""
        imports = set()
        
        try:
            # Parse do código usando AST
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # Pega apenas o nome base da biblioteca
                        lib_name = alias.name.split('.')[0]
                        imports.add(lib_name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        # Pega apenas o nome base da biblioteca
                        lib_name = node.module.split('.')[0]
                        imports.add(lib_name)
                        
        except SyntaxError as e:
            self.log_to_console(f"Erro de sintaxe no código: {e}")
            return set()
            
        # Filtrar bibliotecas padrão do Python
        standard_libs = {
            'os', 'sys', 'json', 'datetime', 'time', 'random', 'math', 'collections',
            'itertools', 'functools', 'operator', 're', 'string', 'io', 'pathlib',
            'urllib', 'http', 'email', 'html', 'xml', 'csv', 'configparser',
            'logging', 'threading', 'multiprocessing', 'subprocess', 'shutil',
            'tempfile', 'glob', 'pickle', 'copy', 'pprint', 'textwrap',
            'unicodedata', 'stringprep', 'readline', 'rlcompleter', 'struct',
            'codecs', 'tokenize', 'keyword', 'token', 'ast', 'symtable',
            'py_compile', 'compileall', 'dis', 'pickletools', 'platform',
            'errno', 'ctypes', 'array', 'weakref', 'types', 'gc', 'inspect',
            'site', '__future__', 'importlib', 'pkgutil', 'modulefinder',
            'runpy', 'argparse', 'getopt', 'getpass', 'curses', 'locale',
            'calendar', 'mailcap', 'mailbox', 'mimetypes', 'base64', 'binhex',
            'binascii', 'quopri', 'uu', 'hashlib', 'hmac', 'secrets', 'ssl',
            'socket', 'selectors', 'signal', 'mmap', 'contextlib', 'abc',
            'atexit', 'traceback', 'warnings', 'dataclasses', 'graphlib'
        }
        
        # Retorna apenas bibliotecas que não são padrão
        external_imports = imports - standard_libs
        return external_imports
        
    def check_and_install_packages(self, packages):
        """Verifica e instala pacotes necessários"""
        if not packages:
            self.log_to_console("✅ Nenhuma dependência externa encontrada.")
            return True
            
        self.log_to_console(f"🔍 Verificando dependências: {', '.join(packages)}")
        
        missing_packages = []
        
        # Verifica quais pacotes estão faltando
        for package in packages:
            try:
                spec = importlib.util.find_spec(package)
                if spec is None:
                    missing_packages.append(package)
                else:
                    self.log_to_console(f"✅ {package} já está instalado")
            except (ImportError, ModuleNotFoundError):
                missing_packages.append(package)
                
        if not missing_packages:
            self.log_to_console("✅ Todas as dependências já estão instaladas!")
            return True
            
        # Instala pacotes faltando
        self.log_to_console(f"📦 Instalando pacotes: {', '.join(missing_packages)}")
        
        for package in missing_packages:
            try:
                self.log_to_console(f"⬇️ Instalando {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                self.log_to_console(f"✅ {package} instalado com sucesso!")
                
            except subprocess.CalledProcessError as e:
                self.log_to_console(f"❌ Erro ao instalar {package}: {e}")
                self.log_to_console(f"Saída do erro: {e.stderr}")
                return False
                
        return True
        
    def check_dependencies(self):
        """Verifica as dependências do código atual"""
        code = self.code_editor.get(1.0, tk.END)
        imports = self.extract_imports(code)
        
        self.log_to_console("=" * 50)
        self.log_to_console("🔍 VERIFICAÇÃO DE DEPENDÊNCIAS")
        self.log_to_console("=" * 50)
        
        if imports:
            self.log_to_console(f"📋 Bibliotecas encontradas: {', '.join(imports)}")
            self.check_and_install_packages(imports)
        else:
            self.log_to_console("✅ Nenhuma dependência externa encontrada.")

    def run_code(self):
        """Executa o código Python - VERSÃO ATUALIZADA para códigos grandes"""
        code = self.code_editor.get(1.0, tk.END).strip()
        
        if not code:
            messagebox.showwarning("Aviso", "Não há código para executar!")
            return
            
        # Executar em thread separada para não travar a interface
        def execute():
            self.update_status("Verificando dependências...")
            self.log_to_console("=" * 50)
            self.log_to_console("🚀 INICIANDO EXECUÇÃO")
            self.log_to_console("=" * 50)
            
            # Extrair e instalar dependências
            imports = self.extract_imports(code)
            if imports:
                if not self.check_and_install_packages(imports):
                    self.log_to_console("❌ Falha na instalação de dependências. Abortando execução.")
                    self.update_status("Erro na instalação de dependências")
                    return
                    
            self.log_to_console("-" * 50)
            self.log_to_console("▶️ EXECUTANDO CÓDIGO:")
            self.log_to_console("-" * 50)
            
            # Executar o código
            temp_file = None
            try:
                if self.current_file and os.path.exists(self.current_file):
                    # Se há um arquivo salvo, executa o arquivo
                    self.log_to_console(f"📁 Executando arquivo: {self.current_file}")
                    result = subprocess.run(
                        [sys.executable, self.current_file],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(self.current_file),
                        timeout=300  # Timeout de 5 minutos
                    )
                else:
                    # Para códigos grandes, sempre criar arquivo temporário
                    self.log_to_console("📝 Criando arquivo temporário para execução...")
                    temp_file = self.create_temp_file(code)
                    
                    if not temp_file:
                        self.log_to_console("❌ Falha ao criar arquivo temporário!")
                        return
                    
                    self.log_to_console(f"📁 Executando arquivo temporário: {temp_file}")
                    result = subprocess.run(
                        [sys.executable, temp_file],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(temp_file),
                        timeout=300  # Timeout de 5 minutos
                    )
                    
                if result.stdout:
                    self.log_to_console("📤 SAÍDA:")
                    self.log_to_console(result.stdout)
                    
                if result.stderr:
                    self.log_to_console("❌ ERROS:")
                    self.log_to_console(result.stderr)
                    
                if result.returncode == 0:
                    self.log_to_console("✅ Código executado com sucesso!")
                    self.update_status("Execução concluída com sucesso")
                else:
                    self.log_to_console(f"❌ Código terminou com erro (código: {result.returncode})")
                    self.update_status("Execução terminou com erro")
                    
            except subprocess.TimeoutExpired:
                self.log_to_console("⏰ Timeout: Execução cancelada após 5 minutos")
                self.update_status("Execução cancelada por timeout")
            except Exception as e:
                self.log_to_console(f"❌ Erro durante a execução: {str(e)}")
                self.update_status("Erro durante a execução")
            finally:
                # Limpar arquivo temporário
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                        self.log_to_console("🗑️ Arquivo temporário removido")
                    except:
                        pass
                
        # Executar em thread separada
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()

    def install_pyinstaller(self):
        """Instala o PyInstaller"""
        def install():
            self.log_to_console("=" * 50)
            self.log_to_console("⚙️ INSTALANDO PYINSTALLER")
            self.log_to_console("=" * 50)
            self.update_status("Instalando PyInstaller...")
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pyinstaller"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                self.log_to_console("✅ PyInstaller instalado com sucesso!")
                self.log_to_console("Agora você pode gerar arquivos EXE!")
                self.update_status("PyInstaller instalado com sucesso")
                
            except subprocess.CalledProcessError as e:
                self.log_to_console(f"❌ Erro ao instalar PyInstaller: {e}")
                self.log_to_console(f"Saída do erro: {e.stderr}")
                self.update_status("Erro na instalação do PyInstaller")
        
        # Executar em thread separada
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()
    
    def generate_exe(self):
        """Gera arquivo EXE do código atual"""
        code = self.code_editor.get(1.0, tk.END).strip()
        
        if not code:
            messagebox.showwarning("Aviso", "Não há código para converter em EXE!")
            return
        
        # Verificar se há arquivo salvo
        if not self.current_file:
            response = messagebox.askyesno(
                "Salvar Arquivo", 
                "Para gerar EXE, o código precisa estar salvo. Deseja salvar agora?"
            )
            if response:
                self.save_as_file()
                if not self.current_file:  # Se cancelou o salvamento
                    return
            else:
                return
        
        # Executar geração em thread separada
        def generate():
            self.log_to_console("=" * 50)
            self.log_to_console("🔧 GERANDO ARQUIVO EXE")
            self.log_to_console("=" * 50)
            self.update_status("Gerando arquivo EXE...")
            
            try:
                # Verificar se PyInstaller está instalado
                try:
                    import PyInstaller
                except ImportError:
                    self.log_to_console("❌ PyInstaller não encontrado! Instalando...")
                    install_result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "pyinstaller"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    self.log_to_console("✅ PyInstaller instalado!")
                
                # Instalar dependências do código antes de gerar EXE
                imports = self.extract_imports(code)
                if imports:
                    self.log_to_console("📦 Instalando dependências necessárias...")
                    self.check_and_install_packages(imports)
                
                # Preparar comando PyInstaller
                file_dir = os.path.dirname(self.current_file)
                file_name = os.path.splitext(os.path.basename(self.current_file))[0]
                
                # Criar pasta de output se não existir
                exe_dir = os.path.join(file_dir, "exe_output")
                os.makedirs(exe_dir, exist_ok=True)
                self.exe_output_folder = exe_dir
                
                self.log_to_console(f"📁 Pasta de saída: {exe_dir}")
                self.log_to_console("🔨 Executando PyInstaller...")
                
                # Comando PyInstaller
                cmd = [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile",  # Arquivo único
                    "--distpath", exe_dir,  # Pasta de destino
                    "--workpath", os.path.join(exe_dir, "build"),  # Pasta de trabalho
                    "--specpath", exe_dir,  # Pasta do spec
                    "--name", f"{file_name}_executable",  # Nome do EXE
                    self.current_file
                ]
                
                # Executar PyInstaller
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=file_dir,
                    timeout=300  # Timeout de 5 minutos
                )
                
                if result.stdout:
                    self.log_to_console("📋 Saída do PyInstaller:")
                    # Mostrar apenas as linhas mais importantes
                    for line in result.stdout.split('\n'):
                        if any(keyword in line.lower() for keyword in ['building', 'completed', 'warning', 'error']):
                            self.log_to_console(line.strip())
                
                if result.stderr:
                    self.log_to_console("⚠️ Avisos/Erros:")
                    self.log_to_console(result.stderr)
                
                if result.returncode == 0:
                    exe_path = os.path.join(exe_dir, f"{file_name}_executable.exe")
                    if os.path.exists(exe_path):
                        self.log_to_console("✅ ARQUIVO EXE GERADO COM SUCESSO!")
                        self.log_to_console(f"📍 Localização: {exe_path}")
                        
                        # Mostrar informações do arquivo
                        file_size = os.path.getsize(exe_path)
                        size_mb = file_size / (1024 * 1024)
                        self.log_to_console(f"📊 Tamanho: {size_mb:.2f} MB")
                        
                        self.update_status("EXE gerado com sucesso!")
                        
                        # Perguntar se quer abrir a pasta
                        self.root.after(1000, lambda: messagebox.showinfo(
                            "Sucesso!", 
                            f"EXE gerado com sucesso!\n\nLocalização:\n{exe_path}\n\nTamanho: {size_mb:.2f} MB"
                        ))
                    else:
                        self.log_to_console("❌ Arquivo EXE não encontrado após a geração!")
                        self.update_status("Erro: EXE não encontrado")
                else:
                    self.log_to_console(f"❌ PyInstaller falhou (código: {result.returncode})")
                    self.update_status("Falha na geração do EXE")
                    
            except subprocess.TimeoutExpired:
                self.log_to_console("⏰ Timeout: Geração de EXE cancelada após 5 minutos")
                self.update_status("Geração cancelada por timeout")
            except Exception as e:
                self.log_to_console(f"❌ Erro durante a geração: {str(e)}")
                self.update_status("Erro na geração do EXE")
        
        # Executar em thread separada
        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()
    
    def open_exe_folder(self):
        """Abre a pasta onde os EXEs são gerados"""
        if self.exe_output_folder and os.path.exists(self.exe_output_folder):
            try:
                if sys.platform == "win32":
                    os.startfile(self.exe_output_folder)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", self.exe_output_folder])
                else:  # Linux
                    subprocess.run(["xdg-open", self.exe_output_folder])
                self.log_to_console(f"📂 Pasta aberta: {self.exe_output_folder}")
            except Exception as e:
                self.log_to_console(f"❌ Erro ao abrir pasta: {e}")
        else:
            if not self.current_file:
                messagebox.showwarning("Aviso", "Nenhum arquivo foi salvo ainda!")
            else:
                file_dir = os.path.dirname(self.current_file)
                exe_dir = os.path.join(file_dir, "exe_output")
                messagebox.showinfo("Pasta EXE", f"Pasta onde os EXEs serão gerados:\n{exe_dir}")

    def log_to_console(self, message):
        """Adiciona mensagem ao console"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)
        self.root.update()
        
    def clear_console(self):
        """Limpa o console"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state=tk.DISABLED)
        
    def update_status(self, message):
        """Atualiza a barra de status"""
        self.status_bar.config(text=message)
        self.root.update()

def main():
    """Função principal"""
    root = tk.Tk()
    app = PythonExecutor(root)
    
    # Configurar fechamento da aplicação
    def on_closing():
        if app.code_changed:
            if messagebox.askokcancel("Sair", "Há alterações não salvas. Deseja sair mesmo assim?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
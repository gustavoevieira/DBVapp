import sqlite3
import tkinter as tk
from tkinter import messagebox

# Banco de dados
conn = sqlite3.connect('desbravadores.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS desbravadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT,
        funcao TEXT,
        unidade TEXT,
        telefone TEXT,
        email TEXT,
        data_ingresso TEXT
    )
''')
conn.commit()

# Funções para cada botão (iremos completar depois)
def cadastrar_desbravador():
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastrar Novo Desbravador")
    cadastro_window.geometry("400x450")
    cadastro_window.configure(bg="#E0F7FA")
    
    # Labels e Entradas
    labels = ["Nome Completo", "Data de Nascimento (AAAA-MM-DD)", "Função no Clube", "Unidade", "Telefone", "E-mail", "Data de Ingresso (AAAA-MM-DD)"]
    entries = []
    
    for i, label_text in enumerate(labels):
        label = tk.Label(cadastro_window, text=label_text, bg="#E0F7FA")
        label.pack(pady=(10 if i == 0 else 5, 0))
        entry = tk.Entry(cadastro_window, width=40)
        entry.pack()
        entries.append(entry)
    
    def salvar():
        dados = [e.get() for e in entries]
        
        if not dados[0]:  # Nome é obrigatório
            messagebox.showerror("Erro", "O nome completo é obrigatório.")
            return
        
        cursor.execute('''
            INSERT INTO desbravadores (nome, data_nascimento, funcao, unidade, telefone, email, data_ingresso)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', dados)
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Desbravador cadastrado com sucesso!")
        cadastro_window.destroy()
    
    btn_salvar = tk.Button(cadastro_window, text="Salvar", width=20, command=salvar)
    btn_salvar.pack(pady=20)


def listar_desbravadores():
    listar_window = tk.Toplevel(root)
    listar_window.title("Lista de Desbravadores")
    listar_window.geometry("500x500")
    listar_window.configure(bg="#E0F7FA")

    titulo = tk.Label(listar_window, text="Desbravadores Cadastrados", font=("Arial", 16, "bold"), bg="#E0F7FA")
    titulo.pack(pady=10)

    # Área de texto para mostrar a lista
    text_area = tk.Text(listar_window, width=60, height=20)
    text_area.pack(pady=10)

    cursor.execute("SELECT id, nome, unidade, funcao FROM desbravadores")
    desbravadores = cursor.fetchall()

    if desbravadores:
        for desbravador in desbravadores:
            id_, nome, unidade, funcao = desbravador
            text_area.insert(tk.END, f"ID: {id_} | Nome: {nome} | Unidade: {unidade} | Função: {funcao}\n")
    else:
        text_area.insert(tk.END, "Nenhum desbravador cadastrado ainda.")

    # Deixar a área de texto apenas leitura
    text_area.config(state=tk.DISABLED)


def buscar_desbravador():
    buscar_window = tk.Toplevel(root)
    buscar_window.title("Buscar Desbravador")
    buscar_window.geometry("500x500")
    buscar_window.configure(bg="#E0F7FA")

    titulo = tk.Label(buscar_window, text="Buscar por Nome", font=("Arial", 16, "bold"), bg="#E0F7FA")
    titulo.pack(pady=10)

    # Campo de entrada para nome
    lbl_nome = tk.Label(buscar_window, text="Digite o nome ou parte do nome:", bg="#E0F7FA")
    lbl_nome.pack(pady=5)

    entry_nome = tk.Entry(buscar_window, width=40)
    entry_nome.pack(pady=5)

    # Área de texto para mostrar os resultados
    text_area = tk.Text(buscar_window, width=60, height=20)
    text_area.pack(pady=10)

    def buscar():
        nome_busca = entry_nome.get()

        if not nome_busca:
            messagebox.showwarning("Atenção", "Por favor, digite um nome para buscar.")
            return

        cursor.execute("SELECT id, nome, unidade, funcao FROM desbravadores WHERE nome LIKE ?", ('%' + nome_busca + '%',))
        resultados = cursor.fetchall()

        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END)

        if resultados:
            for desbravador in resultados:
                id_, nome, unidade, funcao = desbravador
                text_area.insert(tk.END, f"ID: {id_} | Nome: {nome} | Unidade: {unidade} | Função: {funcao}\n")
        else:
            text_area.insert(tk.END, "Nenhum desbravador encontrado com esse nome.")

        text_area.config(state=tk.DISABLED)

    btn_buscar = tk.Button(buscar_window, text="Buscar", width=20, command=buscar)
    btn_buscar.pack(pady=5)


def atualizar_desbravador():
    atualizar_window = tk.Toplevel(root)
    atualizar_window.title("Atualizar Desbravador")
    atualizar_window.geometry("500x500")
    atualizar_window.configure(bg="#E0F7FA")

    titulo = tk.Label(atualizar_window, text="Atualizar Cadastro", font=("Arial", 16, "bold"), bg="#E0F7FA")
    titulo.pack(pady=10)

    # Campo de entrada para nome ou ID
    lbl_nome = tk.Label(atualizar_window, text="Digite o ID ou parte do Nome:", bg="#E0F7FA")
    lbl_nome.pack(pady=5)

    entry_busca = tk.Entry(atualizar_window, width=40)
    entry_busca.pack(pady=5)

    text_area = tk.Text(atualizar_window, width=60, height=15)
    text_area.pack(pady=10)

    def buscar_para_editar():
        termo = entry_busca.get()

        if not termo:
            messagebox.showwarning("Atenção", "Por favor, digite um ID ou Nome para buscar.")
            return

        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END)

        if termo.isdigit():
            cursor.execute("SELECT * FROM desbravadores WHERE id = ?", (termo,))
        else:
            cursor.execute("SELECT * FROM desbravadores WHERE nome LIKE ?", ('%' + termo + '%',))

        resultados = cursor.fetchall()

        if resultados:
            for desbravador in resultados:
                id_, nome, data_nascimento, funcao, unidade, telefone, email, data_ingresso = desbravador
                text_area.insert(tk.END, f"ID: {id_} | Nome: {nome} | Função: {funcao} | Unidade: {unidade}\n")
        else:
            text_area.insert(tk.END, "Nenhum desbravador encontrado.")
        
        text_area.config(state=tk.DISABLED)

    def editar_id():
        id_editar = entry_busca.get()

        if not id_editar.isdigit():
            messagebox.showerror("Erro", "Informe um ID válido para editar.")
            return

        cursor.execute("SELECT * FROM desbravadores WHERE id = ?", (id_editar,))
        desbravador = cursor.fetchone()

        if not desbravador:
            messagebox.showerror("Erro", "Desbravador não encontrado.")
            return

        editar_window = tk.Toplevel(atualizar_window)
        editar_window.title("Editar Desbravador")
        editar_window.geometry("400x500")
        editar_window.configure(bg="#E0F7FA")

        campos = ["Nome", "Data de Nascimento", "Função", "Unidade", "Telefone", "E-mail", "Data de Ingresso"]
        entries = []

        for i, campo in enumerate(campos):
            label = tk.Label(editar_window, text=campo, bg="#E0F7FA")
            label.pack(pady=(10 if i == 0 else 5, 0))
            entry = tk.Entry(editar_window, width=40)
            entry.pack()
            entry.insert(0, desbravador[i+1])  # Pulando o ID (posição 0)
            entries.append(entry)

        def salvar_edicao():
            novos_dados = [e.get() for e in entries]

            cursor.execute('''
                UPDATE desbravadores
                SET nome = ?, data_nascimento = ?, funcao = ?, unidade = ?, telefone = ?, email = ?, data_ingresso = ?
                WHERE id = ?
            ''', (*novos_dados, id_editar))
            conn.commit()

            messagebox.showinfo("Sucesso", "Cadastro atualizado com sucesso!")
            editar_window.destroy()
            atualizar_window.destroy()

        btn_salvar = tk.Button(editar_window, text="Salvar Alterações", width=20, command=salvar_edicao)
        btn_salvar.pack(pady=20)

    btn_buscar = tk.Button(atualizar_window, text="Buscar", width=20, command=buscar_para_editar)
    btn_buscar.pack(pady=5)

    btn_editar = tk.Button(atualizar_window, text="Editar pelo ID", width=20, command=editar_id)
    btn_editar.pack(pady=5)


def excluir_desbravador():
    messagebox.showinfo("Excluir", "Função de excluir (em construção)")

# Criar a janela principal
root = tk.Tk()
root.title("Clube de Desbravadores - Guardiões Dourados")
root.geometry("400x400")  # Largura x Altura
root.configure(bg="#E0F7FA")  # Cor de fundo

# Título
titulo = tk.Label(root, text="Sistema de Cadastro", font=("Arial", 18, "bold"), bg="#E0F7FA")
titulo.pack(pady=20)

# Botões
btn_cadastrar = tk.Button(root, text="Cadastrar Novo", width=25, command=cadastrar_desbravador)
btn_listar = tk.Button(root, text="Listar Todos", width=25, command=listar_desbravadores)
btn_buscar = tk.Button(root, text="Buscar por Nome", width=25, command=buscar_desbravador)
btn_atualizar = tk.Button(root, text="Atualizar Desbravador", width=25, command=atualizar_desbravador)
btn_excluir = tk.Button(root, text="Excluir Desbravador", width=25, command=excluir_desbravador)
btn_sair = tk.Button(root, text="Sair", width=25, command=root.destroy)

# Colocar os botões na tela
btn_cadastrar.pack(pady=5)
btn_listar.pack(pady=5)
btn_buscar.pack(pady=5)
btn_atualizar.pack(pady=5)
btn_excluir.pack(pady=5)
btn_sair.pack(pady=20)

# Rodar a aplicação
root.mainloop()

# Fechar conexão ao terminar
conn.close()

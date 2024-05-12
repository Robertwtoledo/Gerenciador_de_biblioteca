import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para inserir um livro no banco de dados
def inserir_livro():
    titulo = titulo_entry.get()
    autor = autor_entry.get()
    ano_publicacao = ano_entry.get()
    if titulo and autor and ano_publicacao:
        cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (?, ?, ?)',
                       (titulo, autor, ano_publicacao))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        listar_livros()
        titulo_entry.delete(0, tk.END)
        autor_entry.delete(0, tk.END)
        ano_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

# Função para listar todos os livros do banco de dados
def listar_livros():
    # Limpa a treeview antes de atualizá-la
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    for livro in livros:
        tree.insert("", "end", values=livro)

# Função para remover um livro
def remover_livro():
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            id_livro = tree.item(item, "values")[0]
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            conn.commit()
        messagebox.showinfo("Sucesso", "Livro(s) removido(s) com sucesso!")
        listar_livros()
    else:
        messagebox.showerror("Erro", "Selecione um livro para remover.")

# Função para editar um livro
def editar_livro():
    selected_item = tree.selection()
    if selected_item:
        id_livro = tree.item(selected_item, "values")[0]
        # Busca os detalhes do livro no banco de dados usando o ID
        cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
        livro = cursor.fetchone()
        # Cria uma nova janela para edição
        edit_window = tk.Toplevel(root)
        edit_window.title("Editar Livro")

        # Rótulos e campos de entrada para edição
        titulo_label = ttk.Label(edit_window, text="Título:", font=("Arial", 12))
        titulo_label.grid(row=0, column=0, sticky="e")
        titulo_entry = ttk.Entry(edit_window, font=("Arial", 12))
        titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        titulo_entry.insert(tk.END, livro[1])  # Insere o título atual no campo de entrada

        autor_label = ttk.Label(edit_window, text="Autor:", font=("Arial", 12))
        autor_label.grid(row=1, column=0, sticky="e")
        autor_entry = ttk.Entry(edit_window, font=("Arial", 12))
        autor_entry.grid(row=1, column=1, padx=5, pady=5)
        autor_entry.insert(tk.END, livro[2])  # Insere o autor atual no campo de entrada

        ano_label = ttk.Label(edit_window, text="Ano de Publicação:", font=("Arial", 12))
        ano_label.grid(row=2, column=0, sticky="e")
        ano_entry = ttk.Entry(edit_window, font=("Arial", 12))
        ano_entry.grid(row=2, column=1, padx=5, pady=5)
        ano_entry.insert(tk.END, livro[3])  # Insere o ano atual no campo de entrada

        # Função para atualizar os detalhes do livro
        def atualizar_livro():
            novo_titulo = titulo_entry.get()
            novo_autor = autor_entry.get()
            novo_ano = ano_entry.get()
            cursor.execute('UPDATE livros SET titulo=?, autor=?, ano_publicacao=? WHERE id=?',
                           (novo_titulo, novo_autor, novo_ano, id_livro))
            conn.commit()
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            edit_window.destroy()
            listar_livros()

        # Botão para atualizar os detalhes do livro
        update_button = ttk.Button(edit_window, text="Atualizar", command=atualizar_livro)
        update_button.grid(row=3, columnspan=2, pady=10)

    else:
        messagebox.showerror("Erro", "Selecione um livro para editar.")

# Função para emprestar um livro
def emprestar_livro():
    emprestimo_window = tk.Toplevel(root)
    emprestimo_window.title("Empréstimo de Livro")

    livro_label = ttk.Label(emprestimo_window, text="ID do Livro:", font=("Arial", 12))
    livro_label.grid(row=0, column=0, sticky="e")
    livro_entry = ttk.Entry(emprestimo_window, font=("Arial", 12))
    livro_entry.grid(row=0, column=1, padx=5, pady=5)

    emprestador_label = ttk.Label(emprestimo_window, text="Nome do Emprestador:", font=("Arial", 12))
    emprestador_label.grid(row=1, column=0, sticky="e")
    emprestador_entry = ttk.Entry(emprestimo_window, font=("Arial", 12))
    emprestador_entry.grid(row=1, column=1, padx=5, pady=5)

    data_emprestimo_label = ttk.Label(emprestimo_window, text="Data de Empréstimo:", font=("Arial", 12))
    data_emprestimo_label.grid(row=2, column=0, sticky="e")
    data_emprestimo_entry = ttk.Entry(emprestimo_window, font=("Arial", 12))
    data_emprestimo_entry.grid(row=2, column=1, padx=5, pady=5)

    data_devolucao_label = ttk.Label(emprestimo_window, text="Data de Devolução:", font=("Arial", 12))
    data_devolucao_label.grid(row=3, column=0, sticky="e")
    data_devolucao_entry = ttk.Entry(emprestimo_window, font=("Arial", 12))
    data_devolucao_entry.grid(row=3, column=1, padx=5, pady=5)

    # Função para realizar o empréstimo
    def realizar_emprestimo():
        id_livro = livro_entry.get()
        nome_emprestador = emprestador_entry.get()
        data_emprestimo = data_emprestimo_entry.get()
        data_devolucao = data_devolucao_entry.get()

        if id_livro and nome_emprestador and data_emprestimo and data_devolucao:
            cursor.execute('INSERT INTO emprestimos (id_livro, nome_emprestador, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)',
                           (id_livro, nome_emprestador, data_emprestimo, data_devolucao))
            conn.commit()
            messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
            emprestimo_window.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    emprestar_button = ttk.Button(emprestimo_window, text="Realizar Empréstimo", command=realizar_emprestimo)
    emprestar_button.grid(row=4, columnspan=2, pady=10)

# Função para listar todos os empréstimos do banco de dados
def listar_emprestimos():
    emprestimos_window = tk.Toplevel(root)
    emprestimos_window.title("Livros Emprestados")

    tree_frame = ttk.Frame(emprestimos_window)
    tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("ID", "ID do Livro", "Nome do Emprestador", "Data de Empréstimo", "Data de Devolução"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("ID do Livro", text="ID do Livro")
    tree.heading("Nome do Emprestador", text="Nome do Emprestador")
    tree.heading("Data de Empréstimo", text="Data de Empréstimo")
    tree.heading("Data de Devolução", text="Data de Devolução")
    tree.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    cursor.execute('SELECT * FROM emprestimos')
    emprestimos = cursor.fetchall()
    for emprestimo in emprestimos:
        tree.insert("", "end", values=emprestimo)

    # Botão para devolver livro
    def devolver_livro():
        selected_item = tree.selection()
        if selected_item:
            for item in selected_item:
                id_emprestimo = tree.item(item, "values")[0]
                cursor.execute('DELETE FROM emprestimos WHERE id = ?', (id_emprestimo,))
                conn.commit()
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
            listar_emprestimos()
        else:
            messagebox.showerror("Erro", "Selecione um livro para devolver.")

    devolver_button = ttk.Button(emprestimos_window, text="Devolver Livro", command=devolver_livro)
    devolver_button.pack(padx=10, pady=5, fill="x", expand=True)

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('livros.db')
cursor = conn.cursor()

# Cria a tabela de livros se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL
    )
''')

# Cria a tabela de emprestimos se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY,
        id_livro INTEGER NOT NULL,
        nome_emprestador TEXT NOT NULL,
        data_emprestimo TEXT NOT NULL,
        data_devolucao TEXT NOT NULL,
        FOREIGN KEY (id_livro) REFERENCES livros(id)
    )
''')

conn.commit()

# Cria a janela principal
root = tk.Tk()
root.title("Gerenciador de Livros")

# Frame para os campos de entrada
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Rótulos e campos de entrada
titulo_label = ttk.Label(frame, text="Título:", font=("Arial", 12))
titulo_label.grid(row=0, column=0, sticky="e")
titulo_entry = ttk.Entry(frame, font=("Arial", 12))
titulo_entry.grid(row=0, column=1, padx=5, pady=5)

autor_label = ttk.Label(frame, text="Autor:", font=("Arial", 12))
autor_label.grid(row=1, column=0, sticky="e")
autor_entry = ttk.Entry(frame, font=("Arial", 12))
autor_entry.grid(row=1, column=1, padx=5, pady=5)

ano_label = ttk.Label(frame, text="Ano de Publicação:", font=("Arial", 12))
ano_label.grid(row=2, column=0, sticky="e")
ano_entry = ttk.Entry(frame, font=("Arial", 12))
ano_entry.grid(row=2, column=1, padx=5, pady=5)

# Botão para adicionar livro
add_button = ttk.Button(frame, text="Adicionar Livro", command=inserir_livro)
add_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

# Treeview para exibir os livros
tree_frame = ttk.Frame(root)
tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=("ID", "Título", "Autor", "Ano de Publicação"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Título", text="Título")
tree.heading("Autor", text="Autor")
tree.heading("Ano de Publicação", text="Ano de Publicação")
tree.pack(fill="both", expand=True)

vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
tree.configure(yscrollcommand=vsb.set)

# Preenche a treeview com os dados
listar_livros()

# Botão para remover livro
remove_button = ttk.Button(root, text="Remover Livro", command=remover_livro)
remove_button.pack(padx=10, pady=5, fill="x", expand=True)

# Botão para editar livro
edit_button = ttk.Button(root, text="Editar Livro", command=editar_livro)
edit_button.pack(padx=10, pady=5, fill="x", expand=True)

# Botão para emprestar livro
emprestar_button = ttk.Button(root, text="Emprestar Livro", command=emprestar_livro)
emprestar_button.pack(padx=10, pady=5, fill="x", expand=True)

# Botão para listar empréstimos
listar_emprestimos_button = ttk.Button(root, text="Livros Emprestados", command=listar_emprestimos)
listar_emprestimos_button.pack(padx=10, pady=5, fill="x", expand=True)

# Configura a janela para ser responsiva
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()

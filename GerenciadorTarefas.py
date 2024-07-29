import sqlite3
from os import system

# Funções de adicionar tarefas
def adicionar_tarefa(conn):
    descricao = input("Digite a descrição da tarefa: ")
    with conn:
        conn.execute("INSERT INTO tarefas (descricao, concluida) VALUES (?, ?)", (descricao, False))
    print("Tarefa adicionada com sucesso!")

#Função visualisar lista de tarefas
def visualizar_tarefas(conn):
    cursor = conn.execute("SELECT id, descricao, concluida FROM tarefas ORDER BY id")
    tarefas = cursor.fetchall()
    if not tarefas:
        print("Nenhuma tarefa adicionada.")
        return
    for idx, (id_, descricao, concluida) in enumerate(tarefas, 1):
        status = "Concluída" if concluida else "Pendente"
        print(f"{id_}. {descricao} - {status}")

#Função alterar estado da tarefa
def marcar_tarefa_concluida(conn):
    visualizar_tarefas(conn)
    id_tarefa = int(input("Digite o número da tarefa que deseja marcar como concluída: "))
    with conn:
        conn.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (True, id_tarefa))
    print("Tarefa marcada como concluída!")

#Função remover tarefa existente
def remover_tarefa(conn):
    visualizar_tarefas(conn)
    id_tarefa = int(input("Digite o número da tarefa que deseja remover: "))
    with conn:
        conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    if not verificar_tarefas_existem(conn):
        resetar_autoincremento(conn)
    print("Tarefa removida com sucesso!")

#Função tarefa ja existe
def verificar_tarefas_existem(conn):
    cursor = conn.execute("SELECT COUNT(*) FROM tarefas")
    count = cursor.fetchone()[0]
    return count > 0

#Função para resetar indx tabela vazia
def resetar_autoincremento(conn):
    with conn:
        conn.execute("DELETE FROM sqlite_sequence WHERE name='tarefas'")
    print("Índice de AUTOINCREMENT resetado!")

# Função para configurar o banco de dados
def inicializar_db(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            concluida BOOLEAN NOT NULL
        )
        """)

# Função principal para o Menu de Opções
def menu():
    conn = sqlite3.connect(fr'DestravaDev\tarefas.db')
    inicializar_db(conn)
    
    while True:
        print("\nMenu de Opções:")
        print("1. Adicionar Tarefa")
        print("2. Visualizar Tarefas")
        print("3. Marcar Tarefa como Concluída")
        print("4. Remover Tarefa")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        system('cls')

        if opcao == '1':
            adicionar_tarefa(conn)
        elif opcao == '2':
            visualizar_tarefas(conn)
        elif opcao == '3':
            marcar_tarefa_concluida(conn)
        elif opcao == '4':
            remover_tarefa(conn)
        elif opcao == '5':
            conn.close()
            break
        else:
            print("Opção inválida, por favor tente novamente.")

if __name__ == "__main__":
    menu()

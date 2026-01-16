import json
import os

class GerenciadorLogistica:
    def __init__(self, arquivo_dados='dados_logistica.json'):
        self.arquivo_dados = arquivo_dados
        self.tarefas = self._carregar_dados()

    def _carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _salvar_dados(self):
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.tarefas, f, indent=4, ensure_ascii=False)

    def criar_tarefa(self, titulo, prioridade="Normal", prazo="N/A"):
        if not titulo:
            return {"sucesso": False, "mensagem": "O título é obrigatório."}
        
        nova_tarefa = {
            "id": len(self.tarefas) + 1,
            "titulo": titulo,
            "prioridade": prioridade,
            "prazo": prazo,
            "status": "A Fazer"
        }
        self.tarefas.append(nova_tarefa)
        self._salvar_dados()
        return {"sucesso": True, "tarefa": nova_tarefa}

    def listar_tarefas(self):
        return self.tarefas

    def atualizar_status(self, id_tarefa, novo_status):
        for tarefa in self.tarefas:
            if tarefa["id"] == id_tarefa:
                tarefa["status"] = novo_status
                self._salvar_dados()
                return True
        return False

    def excluir_tarefa(self, id_tarefa):
        tamanho_original = len(self.tarefas)
        self.tarefas = [t for t in self.tarefas if t["id"] != id_tarefa]
        if len(self.tarefas) < tamanho_original:
            self._salvar_dados()
            return True
        return False

# Bloco Interativo para o Console
if __name__ == "__main__":
    sistema = GerenciadorLogistica()

    while True:
        print("\n" + "="*30)
        print("      SISTEMA LOGITASK      ")
        print("="*30)
        print("1. Criar Tarefa de Entrega")
        print("2. Listar Todas as Entregas")
        print("3. Atualizar Status (Kanban)")
        print("4. Excluir Tarefa (Remover do Sistema)")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            titulo = input("Título da entrega: ")
            prioridade = input("Prioridade (Alta/Normal/Baixa): ")
            prazo = input("Prazo (DD/MM/AAAA): ")
            res = sistema.criar_tarefa(titulo, prioridade, prazo)
            print(f"\n>> {res['mensagem'] if not res['sucesso'] else 'Sucesso: Tarefa cadastrada!'}")

        elif opcao == "2":
            tarefas = sistema.listar_tarefas()
            if not tarefas:
                print("\nNenhuma tarefa encontrada.")
            for t in tarefas:
                print(f"ID: {t['id']} | {t['titulo']} | Status: {t['status']} | Prioridade: {t['priority'] if 'priority' in t else t['prioridade']}")

        elif opcao == "3":
            try:
                id_sel = int(input("ID da tarefa para atualizar: "))
                novo_st = input("Novo status (Em Progresso / Concluído): ")
                if sistema.atualizar_status(id_sel, novo_st):
                    print("\n>> Status atualizado!")
                else:
                    print("\n>> Erro: ID não encontrado.")
            except ValueError:
                print("\n>> Erve: Digite um número válido para o ID.")

        elif opcao == "4":
            try:
                id_excluir = int(input("Digite o ID da tarefa para EXCLUIR: "))
                if sistema.excluir_tarefa(id_excluir):
                    print(f"\n>> Sucesso: Tarefa {id_excluir} removida permanentemente.")
                else:
                    print("\n>> Erro: ID não localizado.")
            except ValueError:
                print("\n>> Erro: Digite um número válido.")

        elif opcao == "5":
            print("\nEncerrando sistema... Até logo!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")
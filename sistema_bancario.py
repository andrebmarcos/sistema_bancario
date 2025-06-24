import textwrap
from datetime import datetime

def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def encontrar_conta_cliente(cliente):
    if not cliente['contas']:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente['contas'][0]

def depositar(conta, valor):
    if valor > 0:
        conta['saldo'] += valor
        conta['transacoes'].append({
            "tipo": "Depósito",
            "valor": valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return True

def sacar(*, conta, valor, limite_saque_valor, limite_saques_diarios):
    hoje = datetime.now().date()
    saques_hoje = [
        t for t in conta['transacoes'] 
        if t['tipo'] == 'Saque' and datetime.strptime(t['data'], "%d-%m-%Y %H:%M:%S").date() == hoje
    ]
    numero_saques_hoje = len(saques_hoje)

    excedeu_saldo = valor > conta['saldo']
    excedeu_limite_valor = valor > limite_saque_valor
    excedeu_limite_quantidade = numero_saques_hoje >= limite_saques_diarios

    if excedeu_saldo:
        print(f"\n@@@ Operação falhou! Saldo insuficiente. (Saldo atual: R$ {conta['saldo']:.2f}) @@@")
    elif excedeu_limite_valor:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite por operação de R$ {limite_saque_valor:.2f}. @@@")
    elif excedeu_limite_quantidade:
        print(f"\n@@@ Operação falhou! Número máximo de saques diários ({limite_saques_diarios}) excedido. @@@")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['transacoes'].append({
            "tipo": "Saque",
            "valor": valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta['transacoes']:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta['transacoes']:
            print(f"{transacao['data']}\t{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}")
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = {
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, 
        "endereco": endereco,
        "contas": []
    }
    usuarios.append(novo_usuario)

    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta_sequencial, usuarios):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        nova_conta = {
            "agencia": agencia, 
            "numero_conta": numero_conta_sequencial, 
            "usuario": usuario,
            "saldo": 0,
            "transacoes": []
        }
        usuario['contas'].append(nova_conta)
        print("\n=== Conta criada com sucesso! ===")
        return nova_conta

    print("\n@@@ Usuário não encontrado! A conta não pode ser criada. @@@")
    return None

def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta foi criada ainda.")
        return
        
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            CPF:\t\t{conta['usuario']['cpf']}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES_DIARIOS = 3
    LIMITE_SAQUE_VALOR = 500
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                conta = encontrar_conta_cliente(usuario)
                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    depositar(conta, valor)
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                conta = encontrar_conta_cliente(usuario)
                if conta:
                    valor = float(input("Informe o valor do saque: "))
                    sacar(
                        conta=conta,
                        valor=valor,
                        limite_saque_valor=LIMITE_SAQUE_VALOR,
                        limite_saques_diarios=LIMITE_SAQUES_DIARIOS
                    )
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                conta = encontrar_conta_cliente(usuario)
                if conta:
                    exibir_extrato(conta)
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            nova_conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema. Até logo!\n")
            break

        else:
            print("\n@@@ Operação inválida! Por favor, selecione novamente a operação desejada. @@@")

main()
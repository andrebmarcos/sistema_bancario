import datetime

titulo = "##### BANCO SANTOANDRE #####"
menu = """
##### MENU #####

[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Sair

"""

saldo = 0
limite = 500
extrato = ""
saques = []
numero_saques = 0
LIMITE_SAQUES = 3

print("\n",titulo)

while True:

    opcao = input(menu)
    #deposito
    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saques.append({'data': datetime.date.today(), 'valor': valor, 'tipo': 'Depósito'})
        if valor > 0:
            saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")

        else:
            print("Opção invalida! Operação falhou!")
    #saques
    elif opcao == "2":
        
        hoje = datetime.date.today()
    
    # Filtra os saques feitos hoje
        saques_hoje = [s for s in saques if s['data'] == hoje and s['tipo'] == 'Saque']
        valor_sacado_hoje = sum([s['valor'] for s in saques_hoje])

        valor = float(input("Informe o valor do saque: "))

        saldo_excedido = valor > saldo

        limite_excedido = valor > limite

        saques_excedido = numero_saques >= LIMITE_SAQUES

        if saldo_excedido:
            print("Você não tem saldo suficiente! Verifique seu extrato")

        elif limite_excedido:
            print("Excedeu o valor de saque diario!!! Entre em contato com seu gerente")
        
        elif saques_excedido:
            print("Excedeu o limite de saques diario!!! Entre em contato com seu gerente")

        elif valor > 0:
            saldo -= valor
            saques.append({'data': hoje, 'valor': valor, 'tipo': 'Saque'})
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
            numero_saques += 1
        else:
            print("Opção invalida!!!")
    #Extrato
    if opcao == "3":
     
        print("\n##### Extrato #####\n")
        if not saques:
            print("Não foram realizadas movimentações.")
        else:
            for saque in saques:
                print(f"Data: {saque['data']}, Tipo: {saque['tipo']}, Valor: R${saque['valor']:.2f}")
                
        print(f"Saldo atual: R${saldo:.2f}\n")

    elif opcao == "4":
        print(f"\n Sistema encerrado")
        break
        
    
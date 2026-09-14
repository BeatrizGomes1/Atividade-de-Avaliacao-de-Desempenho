from line_solver import *

taxa = 0.40
limite = 2.43966

# Alternativas testadas
alternativas = [
    ("Original", 1, 1, 1),
    ("CPU 2x mais rápida", 2, 1, 1),
    ("Disco1 2x mais rápido", 1, 2, 1),
    ("Disco2 2x mais rápido", 1, 1, 2),
    ("CPU + Disco1", 2, 2, 1),
    ("CPU + Disco2", 2, 1, 2),
    ("CPU + Disco1 + Disco2", 2, 2, 2)
]

for nome, fator_cpu, fator_disco1, fator_disco2 in alternativas:

    modelo = Network("Exercicio 3.12")

    fonte = Source(modelo, "Fonte")
    think = Delay(modelo, "Think")
    cpu = Queue(modelo, "CPU", SchedStrategy.FCFS)
    disco1 = Queue(modelo, "Disco1", SchedStrategy.FCFS)
    disco2 = Queue(modelo, "Disco2", SchedStrategy.FCFS)
    saida = Sink(modelo, "Saida")

    transaction = OpenClass(modelo, "Transaction")
    interactive = ClosedClass(modelo, "Interactive", 20, think)

    fonte.set_arrival(transaction, Exp(taxa))

    think.set_service(interactive, Exp(1 / 30))

    cpu.set_service(transaction, Exp(1 / (0.80 / fator_cpu)))
    disco1.set_service(transaction, Exp(1 / (0.75 / fator_disco1)))
    disco2.set_service(transaction, Exp(1 / (0.25 / fator_disco2)))

    cpu.set_service(interactive, Exp(1 / (0.30 / fator_cpu)))
    disco1.set_service(interactive, Exp(1 / (0.45 / fator_disco1)))
    disco2.set_service(interactive, Exp(1 / (0.30 / fator_disco2)))

    P = modelo.init_routing_matrix()

    P.set(transaction, transaction, fonte, cpu, 1.0)
    P.set(transaction, transaction, cpu, disco1, 1.0)
    P.set(transaction, transaction, disco1, disco2, 1.0)
    P.set(transaction, transaction, disco2, saida, 1.0)

    P.set(interactive, interactive, think, cpu, 1.0)
    P.set(interactive, interactive, cpu, disco1, 1.0)
    P.set(interactive, interactive, disco1, disco2, 1.0)
    P.set(interactive, interactive, disco2, think, 1.0)

    modelo.link(P)

    resultado = MVA(modelo)
    tabela = resultado.avg_table()

    resposta_cpu = tabela[
        (tabela["Station"] == "CPU") &
        (tabela["JobClass"] == "Transaction")
    ]["RespT"].iloc[0]

    resposta_disco1 = tabela[
        (tabela["Station"] == "Disco1") &
        (tabela["JobClass"] == "Transaction")
    ]["RespT"].iloc[0]

    resposta_disco2 = tabela[
        (tabela["Station"] == "Disco2") &
        (tabela["JobClass"] == "Transaction")
    ]["RespT"].iloc[0]

    # Tempo de resposta total
    resposta = resposta_cpu + resposta_disco1 + resposta_disco2

    print("\nAlternativa:", nome)
    print("Tempo de resposta:", round(resposta, 5), "s")

    # Verifica se atende ao limite
    if resposta <= limite:
        print("Atende ao limite de 10%")
    else:
        print("Não atende ao limite de 10%")
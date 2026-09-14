from line_solver import *

taxa = 30
tempo = 0.020

variacoes = [-200, -100, -50, -10, 10, 50, 100, 200]

print("VARIAÇÃO DA CARGA DE TRABALHO")

for variacao in variacoes:

    chegada = taxa * (1 + variacao / 100)

    print("\nVariação:", variacao, "%")

    if chegada <= 0:
        print("Carga inválida")
        continue

    modelo = Network("Exercicio 4.1")

    fonte = Source(modelo, "Fonte")
    cpu = Queue(modelo, "CPU", SchedStrategy.FCFS)
    saida = Sink(modelo, "Saida")

    classe = OpenClass(modelo, "Transacoes")

    fonte.set_arrival(classe, Exp(chegada))

    # Exp recebe a taxa de serviço
    # tempo médio = 0.020 s → taxa = 1 / 0.020 = 50
    cpu.set_service(classe, Exp(1 / tempo))

    modelo.link(Network.serial_routing(fonte, cpu, saida))

    resultado = MVA(modelo)

    print(resultado.avg_table())


print("\nVARIAÇÃO DA VELOCIDADE DO PROCESSADOR")

for variacao in variacoes:

    velocidade = 1 + variacao / 100

    print("\nVariação:", variacao, "%")

    if velocidade <= 0:
        print("Velocidade inválida")
        continue

    novo_tempo = tempo / velocidade

    modelo = Network("Exercicio 4.1")

    fonte = Source(modelo, "Fonte")
    cpu = Queue(modelo, "CPU", SchedStrategy.FCFS)
    saida = Sink(modelo, "Saida")

    classe = OpenClass(modelo, "Transacoes")

    fonte.set_arrival(classe, Exp(taxa))

    # LINE recebe a taxa, então usamos 1 / novo_tempo
    cpu.set_service(classe, Exp(1 / novo_tempo))

    modelo.link(Network.serial_routing(fonte, cpu, saida))

    resultado = MVA(modelo)

    print(resultado.avg_table())
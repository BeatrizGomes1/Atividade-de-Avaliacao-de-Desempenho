from line_solver import *

taxa = 30
tempo = 0.020
resposta_original = 0.050

valores_p = range(0, 201, 10)

for p in valores_p:
    chegada = taxa * (1 + p / 100)
    taxa_servico = chegada + 1 / resposta_original
    aceleracao = ((taxa_servico / (1 / tempo)) - 1) * 100

    modelo = Network("Exercicio 4.2")

    fonte = Source(modelo, "Fonte")
    cpu = Queue(modelo, "CPU", SchedStrategy.FCFS)
    saida = Sink(modelo, "Saida")

    classe = OpenClass(modelo, "Transacoes")

    fonte.set_arrival(classe, Exp(chegada))
    cpu.set_service(classe, Exp(taxa_servico))

    modelo.link(Network.serial_routing(fonte, cpu, saida))

    solver = MVA(modelo)

    print(f"Aumento da carga: {p}%")
    print(f"Aceleração necessária: {round(aceleracao, 2)}%")
    print()
from line_solver import *

taxa = 30
tempo = 0.020
resposta_original = 0.050

valores_q = range(0, 201, 10)

for q in valores_q:
    taxa_servico = (1 / tempo) * (1 + q / 100)
    chegada = taxa_servico - 1 / resposta_original
    aumento_carga = ((chegada / taxa) - 1) * 100

    modelo = Network("Exercicio 4.3")

    fonte = Source(modelo, "Fonte")
    cpu = Queue(modelo, "CPU", SchedStrategy.FCFS)
    saida = Sink(modelo, "Saida")

    classe = OpenClass(modelo, "Transacoes")

    fonte.set_arrival(classe, Exp(chegada))
    cpu.set_service(classe, Exp(taxa_servico))

    modelo.link(Network.serial_routing(fonte, cpu, saida))

    solver = MVA(modelo)

    print(f"Aceleração do processador: {q}%")
    print(f"Aumento possível da carga: {round(aumento_carga, 2)}%")
    print()
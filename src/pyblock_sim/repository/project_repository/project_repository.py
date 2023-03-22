class PlanRepository:
    pass
    # problemas possiveis
    #   - o arquivo descreve um bloco que não está na biblioteca
    #   - o arquivo contem conexoes que não correspondem às portas
    #   - arquivo contem instance_id repetidos
    #
    #   - verificar o que ocorre se eu tentar adicionar uma conexão em um grafo de blocos não-inicializados
    #
    # participantes
    #   BlockEntity
    #   BlockRuntimes
    #   Connections
    #
    # pseudocode
    #   - load file into object
    #   - read blocks and add to graph
    #   - load blocks in graph
    #   - add conections
    #
    # Project
    #   GraphSpec
    #      - blocks [dist_id, instance_id, name]
    #           - params
    #      - connections [port_u, port_v]
    #   Analyses
    #      ...

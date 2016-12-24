def flood_fill(board, x, y):
    pointer = board.array[x][y]
    cluster = [i for i in board.array[x][y].touching]
    cluster.append(board.array[x][y])
    interior, exterior= [], []
    while True:
        if pointer.value == 0:
            interior.append(pointer)
            cluster += [square for square in pointer.touching if not square in cluster]
        elif pointer.value != 0:
            exterior.append(pointer)
        if len(interior + exterior) == len(cluster):
            print(cluster)
            print(interior + exterior)
            break
        cluster_freeze = cluster.copy()
        while cluster[0] in interior + exterior:
            cluster = cluster[1:] + cluster[0]
            if cluster == cluster_freeze:
                break
        if cluster == cluster_freeze:
            break
        pointer = cluster[0]
    for square in interior + exterior:
        print(square)
        square.show = True

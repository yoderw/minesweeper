def flood_fill(board, x, y):
    pointer = board.array[x][y]
    cluster = [board.array[x][y]] + [i for i in board.array[x][y].touching]
    interior, exterior= [], []
    while True:
        if pointer.value == 0:
            interior.append(pointer)
            cluster += [square for square in pointer.touching if square not in cluster]
        elif pointer.value != 0:
            exterior.append(pointer)
        if len(interior + exterior) == len(cluster) or cluster.index(pointer) == cluster[-1:]: break
        pointer = cluster[cluster.index(pointer) + 1]
    for square in interior + exterior:
        square.show = True

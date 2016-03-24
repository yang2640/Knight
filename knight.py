import sys
from collections import defaultdict

def printBoard(board):
    for row in board:
        line = ""
        for x in row:
            line = line + x + "  " 
        print line
    print

def validate(moves, board, start, end, debug=False):
    m = len(board)
    n = len(board[0])
    cur = start

    # draw start and end on the board
    if debug:
        board[start[0]][start[1]] = "S"
        board[end[0]][end[1]] = "E"

    for mv in moves:
        orig = cur
        cur = (cur[0] + mv[0], cur[1] + mv[1])
        if (cur[0] < 0 or cur[0] >= m or cur[1] < 0 or cur[1] >= n) or (board[cur[0]][cur[1]] != "T" and not mv in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]):
            return False

        if weight(board, orig, cur) == -1:
            return False

        if debug:
            board[cur[0]][cur[1]] = "K"
            printBoard(board)
            print "*********************************************"
            board[cur[0]][cur[1]] = "."
    if debug:
        print "Number of moves: ", len(moves) 

    return (cur == end)

def dfs(board, visit, cur, end, path):
    # find the target
    if cur == end:
        path.append(cur)
        return True

    m = len(board)
    n = len(board[0])
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    # for trace brack
    visit[cur[0]][cur[1]] = 1
    path.append(cur)
    
    # depth first search valid and un-visited adjecent points
    for mv in moves:
        adj = (cur[0] + mv[0], cur[1] + mv[1])
        if adj[0] < 0 or adj[0] >= m or adj[1] < 0 or adj[1] >= n or visit[adj[0]][adj[1]] == 1:
            continue
        # prune the searching branch to return the first found valid path
        if dfs(board, visit, adj, end, path):
            return True

    # for trace brack
    visit[cur[0]][cur[1]] = 0
    path.pop()

    return False

def searchLevel2(board, start, end):
    m = len(board)
    n = len(board[0])
    visit = [[0 for j in xrange(n)] for i in xrange(m)]
    path = []

    # dfs search with one path
    dfs(board, visit, start, end, path)

    # path -> moves
    moves = []
    for i in xrange(1, len(path)):
        moves.append((path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]))

    return moves

def genPath(path, cur, start, neibors, distance):
    if cur == start:
        path.append(list(cur))
        return True
    
    path.append(cur)
    for x in neibors[cur]:
        if distance[cur] - distance[x] != 1:
            continue
        if genPath(path, x, start, neibors, distance):
            return True
    path.pop()
    return False


def bfs(board, start, end, neibors, distance):
    m = len(board)
    n = len(board[0])
    distance[start] = 0
    found = False
    queue = []
    queue.append(start)

    while len(queue) > 0:
        cur = queue.pop(0)

        # search adjcent points
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for mv in moves:
            adj = (cur[0] + mv[0], cur[1] + mv[1])
            neibors[adj].append(cur)
            # find the target
            if adj == end:
                distance[adj] = distance[cur] + 1
                found = True
                break

            if adj[0] < 0 or adj[0] >= m or adj[1] < 0 or adj[1] >= n or adj in distance:
                continue

            queue.append(adj)
            distance[adj] = distance[cur] + 1

        if found:
            break

def searchLevel3(board, start, end):
    neibors = defaultdict(list)
    distance = {}

    bfs(board, start, end, neibors, distance)

    path = []
    genPath(path, end, start, neibors, distance)
    path.reverse()

    # path -> moves
    moves = []
    for i in xrange(1, len(path)):
        moves.append((path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]))

    return moves

def isBlocked(board, x, y):
    mv = (y[0] - x[0], y[1] - x[1])
    if abs(y[1] - x[1]) == 2:
        return (board[(x[0])][(x[1] + mv[1]/2)] == "B" or board[(x[0])][(x[1] + mv[1])] == "B") and (board[(x[0] + mv[0])][(x[1])] == "B" or board[(x[0] + mv[0])][(x[1] + mv[1]/2)] == "B")
    elif abs(y[0] - x[0]) == 2:
        return (board[(x[0])][(x[1] + mv[1])] == "B" or board[(x[0] + mv[0]/2)][(x[1] + mv[1])] == "B") and (board[(x[0] + mv[0]/2)][(x[1])] == "B" or board[(x[0] + mv[0])][(x[1])] == "B")
    return False

def weight(board, x, y):
    # return -1 when the node can't be arrived
    if board[y[0]][y[1]] == "R" or board[y[0]][y[1]] == "B" or isBlocked(board, x, y):
        return -1
    elif board[y[0]][y[1]] == "W":
        return 2
    elif board[y[0]][y[1]] == "L":
        return 5
    else:
        return 1

def getT(board):
    m = len(board)
    n = len(board[0])
    T = []
    for i in xrange(m):
        for j in xrange(n):
            if board[i][j] == "T":
                T.append((i, j))
    return T


def dijkstra(board, start, end, neibors, distance):
    m = len(board)
    n = len(board[0])
    T = getT(board)

    distance[start] = 0
    queue = []
    queue.append((0, start))

    while len(queue) > 0:
        node = min(queue)
        dist, cur = node 
        # find the target
        if cur == end:
            break
        queue.remove(node)

        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for mv in moves:
            adj = (cur[0] + mv[0], cur[1] + mv[1])
            if adj[0] < 0 or adj[0] >= m or adj[1] < 0 or adj[1] >= n:
                continue

            if board[adj[0]][adj[1]] == "T" and adj == T[0]:
                adj = T[1]
            elif board[adj[0]][adj[1]] == "T" and adj == T[1]:
                adj = T[0]


            w = weight(board, cur, adj)
            if w == -1:
                continue

            neibors[adj].append((cur, w))
            if not adj in distance:
                distance[adj] = dist + w
                queue.append((distance[adj], adj))
            # relax the distance of adj to source
            elif dist + w < distance[adj]:
                idx = queue.index((distance[adj], adj))
                distance[adj] = dist + w
                queue[idx] = distance[adj]

def genDijkstraPath(path, cur, start, neibors, distance):
    if cur == start:
        path.append(list(cur))
        return True
    
    path.append(cur)
    for x, w in neibors[cur]:
        if not x in distance or distance[cur] - distance[x] != w:
            continue
        if genDijkstraPath(path, x, start, neibors, distance):
            return True
    path.pop()
    return False

def searchLevel4(board, start, end):
    neibors = defaultdict(list)
    distance = {}

    dijkstra(board, start, end, neibors, distance)

    path = []
    genDijkstraPath(path, end, start, neibors, distance)
    path.reverse()

    # path -> moves
    moves = []
    for i in xrange(1, len(path)):
        moves.append((path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]))
    
    return moves
    

def dfsAll(board, visit, cur, end, path, res):
    # find the target
    if cur == end:
        path.append(cur)
        res.append(list(path))
        path.pop()
        return

    m = len(board)
    n = len(board[0])
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    # for trace brack
    visit[cur[0]][cur[1]] = 1
    path.append(cur)
    
    # depth first search valid and un-visited adjecent points
    for mv in moves:
        adj = (cur[0] + mv[0], cur[1] + mv[1])
        if adj[0] < 0 or adj[0] >= m or adj[1] < 0 or adj[1] >= n or visit[adj[0]][adj[1]] == 1:
            continue

        dfsAll(board, visit, adj, end, path, res)

    # for trace brack
    visit[cur[0]][cur[1]] = 0
    path.pop()


def searchLevel5(board, start, end):
    m = len(board)
    n = len(board[0])
    visit = [[0 for j in xrange(n)] for i in xrange(m)]
    path = []
    res = []

    # dfs search with one path
    dfsAll(board, visit, start, end, path, res)

    # get longest path
    maxLen = 0
    path = []
    for x in res:
        if len(x) > maxLen:
            maxLen = len(x)
            path = x

    # path -> moves
    moves = []
    for i in xrange(1, len(path)):
        moves.append((path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]))

    return moves

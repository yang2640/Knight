from knight import searchLevel2
from knight import validate

board = [list(row) for row in open("board_8by8.txt").read().splitlines()]
start = (2, 1)
end = (4, 5)
moves = searchLevel2(board, start, end)
# put False at last argument to turn debug off
print validate(moves, board, start, end, True)


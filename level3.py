from knight import searchLevel3
from knight import validate

board = [list(row) for row in open("board_8by8.txt").read().splitlines()]
start = (0, 0)
end = (7, 7)
moves = searchLevel3(board, start, end)
# put False at last argument to turn debug off
print validate(moves, board, start, end, True)


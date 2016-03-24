from knight import searchLevel4
from knight import validate

board = [list(row) for row in open("board_32by32.txt").read().splitlines()]
start = (0, 0)
end = (31, 31)
moves = searchLevel4(board, start, end)
# put False at last argument to turn debug off
print validate(moves, board, start, end, True)


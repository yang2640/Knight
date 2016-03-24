from knight import searchLevel5
from knight import validate

# This problem is hard because it's NP hard, but can be compromised by some approximation, I only use naive depth first search, but it is not efficient, solving the 5 * 5 board is efficient, but very in-efficient for larger size board. I don't have time to invesigate into more efficient method. Thanks for giving out this challenge, very interesting !!!

board = [list(row) for row in open("board_5by5.txt").read().splitlines()]
start = (0, 0)
end = (4, 4)
moves = searchLevel5(board, start, end)
# put False at last argument to turn debug off
print validate(moves, board, start, end, True)


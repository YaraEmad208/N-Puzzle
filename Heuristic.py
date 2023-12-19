# from Board import Board
# import math as m
# import numpy as np
#
#
# class Heuristic:
#     def Hamming(self, board):
#         board = np.array(board)
#
#         goal = np.array(Board(len(board)).getGoal())
#
#         non_zero_elements = board[board != 0]  # select all non_zero_value and return one array
#         goal_elements = goal[goal != None]     # select all non_none_value and return one array
#         # print(non_zero_elements)
#         # print(goal_elements)
#
#         # Count the number of misplaced tiles
#         heuristic = np.sum(non_zero_elements != goal_elements)
#         # if element in non != element in goal is true  increment heuristic with 1
#         return heuristic
#
#
#     def Euclidean(self, board):  # board this is input we want solve it
#         def Euclidean(self, board):
#             b = Board(len(board))
#             board = np.array(board)
#             goal = np.array(b.getGoal())
#             heuristic = 0
#             for x1 in range(len(board)):
#                 for y1 in range(len(board)):
#                     value1 = board[y1][x1]
#                     if value1 != 0:
#                         x2, y2 = np.where(goal == value1)
#                         x2, y2 = x2[0], y2[0]
#
#                         dx = int(np.abs(x2 - x1))
#                         dy = int(np.abs(y2 - y1))
#                         heuristic += int(m.floor(np.sqrt(dx * dx + dy * dy)))
#
#             return heuristic
#
#     def Manhattan(self, board):
#         heuristic = 0
#         board = np.array(board)
#         object_board = Board(len(board))
#         goal = np.array(object_board.getGoal())  #get goal
#         for x in range(len(board)):
#             for y in range(len(board)):
#                 if board[y][x] and goal[y][x] != board[y][x]:
#                     row, col = np.where(goal == board[y][x])
#                     heuristic += abs(row[0] - y) + abs(col[0] - x)
#         return heuristic
#
#     def Permutation(self, board):
#         heuristic = 0
#         flat_board=np.transpose(np.array(board)).flatten();
#         for i in range(len(flat_board) - 1):
#             for j in range(i + 1, len(flat_board)):
#                 if flat_board[i] and flat_board[j] and flat_board[i] > flat_board[j]:
#                     heuristic += 1
#
#         if flat_board[-1]:
#             heuristic += 1
#
#         return heuristic
#
#

import math
from Board import Board
import math as m
import numpy as np


class Heuristic:
    def Hamming(self, board):
        heuristic = 0
        for x in range(len(board)):
            for y in range(len(board)):
                if board[y][x] and Board(len(board)).getGoal()[y][x] != board[y][x]:
                    heuristic += 1
        return heuristic

    def Euclidean(self, board):
        size = len(board)
        goal_positions = {}
        # Find positions of numbers in the goal board
        for i in range(size):
            for j in range(size):
                goal_positions[board[i][j]] = (i, j)
        # Calculate Euclidean distance
        heuristic = 0
        for i in range(size):
            for j in range(size):
                goal_x, goal_y = goal_positions[Board(len(board)).getGoal()[i][j]]
                dx = abs(i - goal_x)
                dy = abs(j - goal_y)
                heuristic += int(math.sqrt(dx * dx + dy * dy))

        return heuristic

    def Manhattan(self, board):
        heuristic = 0
        board = np.array(board)
        b = Board(len(board))
        goal = np.array(b.getGoal())
        for x in range(len(board)):
            for y in range(len(board)):
                if board[y][x] and goal[y][x] != board[y][x]:
                    row, col = np.where(goal == board[y][x])
                    heuristic += abs(row[0] - y) + abs(col[0] - x)
        return heuristic

    def Permutation(self, board):
        heuristic = 0
        board = np.array(board)
        board = np.transpose(board).flatten()
        for x in range(len(board) - 1):
            for y in range(x + 1, len(board)):
                if board[x] and board[y] and board[x] > board[y]:
                    heuristic += 1

        if board[len(board) - 1]:
            heuristic += 1
        return heuristic



    def LinearConflict(self, board):
        heuristic = self.Manhattan(board)
        for x in range(len(board)):
            for y1 in range(len(board)):
                value1 = board[y1][x]
                if value1 is not None and (value1 - 1) != 0:
                    for y2 in range(y1 + 1, len(board)):
                        value2 = board[y2][x]
                        if value2 is not None and (value2 - 1) != 0:
                            heuristic += 2

        return heuristic

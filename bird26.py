import math
from functools import lru_cache

BLACK = 1
WHITE = 2
INF = math.inf

# 位置評価マトリクス（静的評価に使用）
POSITIONAL_WEIGHT = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2, 5, 5, -2, 10],
    [10, -2, 5, 5, -2, 10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100]
]

@lru_cache(None)  # キャッシュを使用して効率化
def evaluate_board(board_tuple, stone):
    """
    改良された評価関数（静的評価 + 動的評価）。
    """
    board = [list(row) for row in board_tuple]
    opponent = 3 - stone
    score = 0

    # 角・辺・位置評価
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += POSITIONAL_WEIGHT[y][x]
            elif board[y][x] == opponent:
                score -= POSITIONAL_WEIGHT[y][x]

    # モビリティ（合法手の数）
    mobility = len(get_possible_moves(board, stone))
    opponent_mobility = len(get_possible_moves(board, opponent))
    score += (mobility - opponent_mobility) * 10

    return score

def is_stable(board, x, y, stone):
    """
    石が安定しているかを判定。
    """
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] == 0:
                return False
            nx += dx
            ny += dy
    return True

def get_possible_moves(board, stone):
    """
    石を置けるすべての合法手を取得。
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def can_place_x_y(board, stone, x, y):
    """
    その位置に石を置けるかを判定。
    """
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def minimax(board, depth, alpha, beta, maximizing_player, stone):
    """
    アルファベータ探索。
    """
    possible_moves = get_possible_moves(board, stone)
    opponent = 3 - stone

    if depth == 0 or not possible_moves:
        board_tuple = tuple(tuple(row) for row in board)  # キャッシュ用に変換
        return evaluate_board(board_tuple, stone)

    if maximizing_player:
        max_eval = -INF
        for move in sorted(possible_moves, key=lambda m: POSITIONAL_WEIGHT[m[1]][m[0]], reverse=True):
            x, y = move
            board[y][x] = stone
            eval = minimax(board, depth - 1, alpha, beta, False, stone)
            board[y][x] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = INF
        for move in sorted(possible_moves, key=lambda m: POSITIONAL_WEIGHT[m[1]][m[0]]):
            x, y = move
            board[y][x] = opponent
            eval = minimax(board, depth - 1, alpha, beta, True, stone)
            board[y][x] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, stone):
    """
    最善手を探索。
    """
    best_value = -INF
    best_move = None
    possible_moves = get_possible_moves(board, stone)

    for move in possible_moves:
        x, y = move
        board[y][x] = stone
        move_value = minimax(board, 6, -INF, INF, False, stone)
        board[y][x] = 0

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

class birdAI:
    def face(self):
        return "🦉"

    def place(self, board, stone):
        return best_move(board, stone)

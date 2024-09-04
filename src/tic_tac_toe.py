from enum import Enum


class Symbol(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False

    def is_within_bounds(self, size: int) -> bool:
        return 0 <= self.x < size and 0 <= self.y < size


class Tile:
    def __init__(self, coordinate: Coordinate):
        self._coordinate = coordinate
        self._symbol = Symbol.EMPTY

    @property
    def coordinate(self) -> Coordinate:
        return self._coordinate

    def set_symbol(self, symbol: Symbol) -> None:
        self._validate_symbol(symbol)
        self._validate_tile_is_empty()
        self._symbol = symbol

    def get_symbol(self) -> Symbol:
        return self._symbol

    def _validate_symbol(self, symbol: Symbol) -> None:
        if symbol not in (Symbol.O, Symbol.X):
            raise ValueError("Symbol must be either 'O' or 'X'")

    def _validate_tile_is_empty(self) -> None:
        if self._symbol != Symbol.EMPTY:
            raise ValueError("Tile already occupied")


class Board:
    def __init__(self, size: int = 3):
        self._size = size
        self._tiles = [Tile(Coordinate(x, y)) for y in range(self._size) for x in range(self._size)]

    def get_tile(self, coordinate: Coordinate) -> Tile:
        self._validate_coordinate(coordinate)
        for tile in self._tiles:
            if tile.coordinate == coordinate:
                return tile

    def set_tile_symbol(self, symbol: Symbol, coordinate: Coordinate) -> None:
        tile = self.get_tile(coordinate)
        tile.set_symbol(symbol)

    def is_full(self):
        return all(tile.get_symbol() != Symbol.EMPTY for tile in self._tiles)

    def is_empty(self):
        return all(tile.get_symbol() == Symbol.EMPTY for tile in self._tiles)

    def get_row(self, row: int) -> list[Tile]:
        return [self.get_tile(Coordinate(x, row)) for x in range(self._size)]

    def get_column(self, column: int) -> list[Tile]:
        return [self.get_tile(Coordinate(column, y)) for y in range(self._size)]

    def get_positive_diagonal(self) -> list[Tile]:
        return [self.get_tile(Coordinate(i, i)) for i in range(self._size)]

    def get_negative_diagonal(self) -> list[Tile]:
        return [self.get_tile(Coordinate(i, (self._size - 1 - i))) for i in range(self._size)]

    def _validate_coordinate(self, coordinate: Coordinate) -> None:
        if not coordinate.is_within_bounds(self._size):
            raise ValueError("Coordinate out of bounds")


class TicTacToe:
    def __init__(self, board: Board = None):
        self._current_player = Symbol.X
        self._board = board or Board()

    def play(self, player_symbol: str, x: int, y: int) -> str:
        symbol = self._convert_to_symbol(player_symbol)
        coordinate = Coordinate(x, y)
        self._validate_turn(symbol)
        self._set_move_on_board(coordinate)

        if self._check_winner(coordinate):
            return f"{self._current_player.value} is the winner!"

        if self._board.is_full():
            return "It's a draw!"

        self._switch_turn()
        return "Next players turn"

    def _convert_to_symbol(self, player_symbol: str) -> Symbol:
        try:
            return Symbol(player_symbol.upper())
        except ValueError:
            raise ValueError(f"Invalid symbol. Choose 'X' or 'O'.")

    def _validate_turn(self, player_symbol: Symbol) -> None:
        if player_symbol != self._current_player:
            raise ValueError("It's not your turn")

    def _set_move_on_board(self, coordinate: Coordinate) -> None:
        board = self._board
        board.set_tile_symbol(self._current_player, coordinate)

    def _switch_turn(self):
        self._current_player = Symbol.O if self._current_player == Symbol.X else Symbol.X

    def _check_winner(self, coordinate: Coordinate) -> bool:
        return (
                self._check_row(coordinate.y) or
                self._check_column(coordinate.x) or
                self._check_diagonals()
        )

    def _check_row(self, row_index: int) -> bool:
        board = self._board
        row = board.get_row(row_index)
        return self._all_same_symbol(row)

    def _check_column(self, column_index: int) -> bool:
        board = self._board
        column = board.get_column(column_index)
        return self._all_same_symbol(column)

    def _check_diagonals(self) -> bool:
        board = self._board
        positive_diagonal = board.get_positive_diagonal()
        negative_diagonal = board.get_negative_diagonal()
        return self._all_same_symbol(positive_diagonal) or self._all_same_symbol(negative_diagonal)

    def _all_same_symbol(self, tiles: list[Tile]) -> bool:
        first_tile_symbol = tiles[0].get_symbol()

        if first_tile_symbol == Symbol.EMPTY:
            return False

        return all(tile.get_symbol() == first_tile_symbol for tile in tiles)

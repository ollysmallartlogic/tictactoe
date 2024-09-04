import pytest

from src.tic_tac_toe import TicTacToe, Board, Tile, Symbol, Coordinate


def test_o_cannot_be_first_player():
    game = TicTacToe()

    with pytest.raises(ValueError, match="It's not your turn"):
        game.play('O', 1, 1)


def test_tile_stores_position():
    coordinate = Coordinate(1, 2)

    tile = Tile(coordinate)

    assert tile.coordinate == coordinate


def test_tile_symbol_defaults_to_empty_string():
    coordinate = Coordinate(1, 2)

    tile = Tile(coordinate)

    assert tile.get_symbol() == Symbol.EMPTY


def test_tile_stores_symbol():
    coordinate = Coordinate(1, 2)
    tile = Tile(coordinate)

    tile.set_symbol(Symbol.X)

    assert tile.get_symbol() == Symbol.X


def test_only_valid_player_symbols_accepted():
    game = TicTacToe()

    with pytest.raises(ValueError, match="Invalid symbol. Choose 'X' or 'O'."):
        game.play('h', 0, 0)


def test_move_not_valid_if_tile_not_empty():
    coordinate = Coordinate(1, 2)
    tile = Tile(coordinate)
    tile.set_symbol(Symbol.X)

    with pytest.raises(ValueError, match="Tile already occupied"):
        tile.set_symbol(Symbol.O)


def test_board_initialisation():
    board = Board()

    assert len(board._tiles) == 9
    assert board.is_empty() == True


def test_retrieve_tile_at_given_coordinates():
    board = Board()
    coordinate = Coordinate(1, 2)

    tile = board.get_tile(coordinate)

    assert tile.coordinate == coordinate
    assert tile.get_symbol() == Symbol.EMPTY


def test_first_player_can_set_symbol_on_board():
    game = TicTacToe()

    game.play('X', 1, 2)
    board = game._board
    coordinate = Coordinate(1, 2)
    tile = board.get_tile(coordinate)

    assert tile.coordinate == coordinate
    assert tile.get_symbol() == Symbol.X


def test_player_switches_after_each_move():
    game = TicTacToe()

    assert game._current_player == Symbol.X
    game.play('X', 1, 2)
    assert game._current_player == Symbol.O
    game.play('O', 2, 2)
    assert game._current_player == Symbol.X


def test_player_cant_play_twice_in_a_row():
    game = TicTacToe()
    game.play('X', 1, 2)

    with pytest.raises(ValueError, match="It's not your turn"):
        game.play('X', 2, 2)


def test_x_winner_1st_row():
    game = TicTacToe()

    game.play('X', 0, 0)
    game.play('O', 1, 1)
    game.play('X', 1, 0)
    game.play('O', 2, 1)

    assert game.play('X', 2, 0) == 'X is the winner!'


def test_o_winner_2nd_row():
    game = TicTacToe()

    game.play('X', 0, 0)
    game.play('O', 0, 1)
    game.play('X', 2, 2)
    game.play('O', 1, 1)
    game.play('X', 2, 0)

    assert game.play('O', 2, 1) == 'O is the winner!'


def test_x_winner_3rd_row():
    game = TicTacToe()

    game.play('X', 0, 2)
    game.play('O', 1, 1)
    game.play('X', 1, 2)
    game.play('O', 2, 1)

    assert game.play('X', 2, 2) == 'X is the winner!'


def test_x_winner_1st_column():
    game = TicTacToe()

    game.play('X', 0, 0)
    game.play('O', 1, 1)
    game.play('X', 0, 1)
    game.play('O', 2, 1)

    assert game.play('X', 0, 2) == 'X is the winner!'


def test_x_winner_2nd_column():
    game = TicTacToe()

    game.play('X', 1, 0)
    game.play('O', 0, 1)
    game.play('X', 1, 1)
    game.play('O', 2, 1)

    assert game.play('X', 1, 2) == 'X is the winner!'


def test_x_winner_3rd_column():
    game = TicTacToe()

    game.play('X', 2, 0)
    game.play('O', 1, 1)
    game.play('X', 2, 1)
    game.play('O', 0, 1)

    assert game.play('X', 2, 2) == 'X is the winner!'


def test_x_winner_positive_diagonal():
    game = TicTacToe()

    game.play('X', 0, 0)
    game.play('O', 2, 1)
    game.play('X', 1, 1)
    game.play('O', 0, 1)

    assert game.play('X', 2, 2) == 'X is the winner!'


def test_x_winner_negative_diagonal():
    game = TicTacToe()

    game.play('X', 0, 2)
    game.play('O', 2, 1)
    game.play('X', 1, 1)
    game.play('O', 0, 1)

    assert game.play('X', 2, 0) == 'X is the winner!'


def test_if_game_is_a_draw():
    game = TicTacToe()

    game.play('X', 0, 0)
    game.play('O', 1, 0)
    game.play('X', 2, 0)
    game.play('O', 1, 1)
    game.play('X', 0, 1)
    game.play('O', 2, 1)
    game.play('X', 1, 2)
    game.play('O', 0, 2)

    assert game.play('X', 2, 2) == "It's a draw!"


@pytest.mark.parametrize("x, y", [
    (-1, 0),  # x below lower bound
    (3, 0),  # x above upper bound
    (0, -1),  # y below lower bound
    (0, 3),  # y above upper bound
    (-1, -1),  # both x and y below lower bound
    (3, 3),  # both x and y above upper bound
    (100, 100)  # far out of bounds
])
def test_invalid_coordinates(x, y):
    game = TicTacToe()

    with pytest.raises(ValueError, match="Coordinate out of bounds"):
        game.play('X', x, y)

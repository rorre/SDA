from typing import Literal

c = 0


def game(current: Literal["Kenneth", "Tara"], left: int, right: int):
    global c
    c += 1
    # Define next player, that is the opposite of our current player
    # Previous player is also the next player
    next_player: Literal["Kenneth", "Tara"] = (
        "Tara" if current == "Kenneth" else "Kenneth"
    )

    # The boxes are empty now, then previous player took the last turn and won
    if right == 0 and left == 0:
        return next_player

    # The idea here is to basically try all options and see if we could win,
    # if we cannot win with that move, we backtrack and choose another move.
    #
    # This idea makes use of lazy evaluation, so if there is already a solution
    # that we found in earlier stages, we simply do not care about all of other
    # possible moves.
    #
    # However, if the box does not contain enough beads, we skip the move.
    if (
        (right >= 1 and game(next_player, left, right - 1) == current)
        or (left >= 1 and game(next_player, left - 1, right) == current)
        or (
            right >= 1
            and left >= 1
            and game(next_player, left - 1, right - 1) == current
        )
        or (right >= 2 and game(next_player, left, right - 2) == current)
        or (left >= 2 and game(next_player, left - 2, right) == current)
    ):
        return current

    # By this point all possible move loses us, we simply set
    # the other player as the winner.
    return next_player


if __name__ == "__main__":
    first: Literal["Kenneth", "Tara"] = input()  # type: ignore
    left, right = map(int, input().split())
    print(game(first, left, right), c)

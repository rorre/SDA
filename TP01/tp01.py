# To run, it requires at least Python 3.8 (Literal typing)
# Simply run this file and insert the inputs
from typing import Literal


def game(current: Literal["Kenneth", "Tara"], left: int, right: int):
    # Define next player, that is the opposite of our current player
    # Previous player is also the next player
    next_player: Literal["Kenneth", "Tara"] = (
        "Tara" if current == "Kenneth" else "Kenneth"
    )

    # The boxes are empty now, then previous player took the last turn and won
    if right == 0 and left == 0:
        return next_player

    # The idea here is to try the options one by one and see if we could win,
    # if we cannot win with that move, we backtrack and choose another move
    #
    # This idea makes use of lazy evaluation, so if there is already a solution
    # that we found in earlier stages, we simply do not care about all of other
    # possible moves
    #
    # However, if the box does not contain enough beads, we skip the move
    #
    # The bigger delta (taking 2 beads) is preferred first, since we can easily
    # get to the end much quicker. This leads to (hopefully) lower execution
    # time and reduced recursive call when the bigger deltas can already
    # be proven to win current player
    if (
        (right >= 2 and game(next_player, left, right - 2) == current)
        or (left >= 2 and game(next_player, left - 2, right) == current)
        or (
            right >= 1
            and left >= 1
            and game(next_player, left - 1, right - 1) == current
        )
        or (right >= 1 and game(next_player, left, right - 1) == current)
        or (left >= 1 and game(next_player, left - 1, right) == current)
    ):
        # If we get here, then any of possible move can make us win so
        # return current player
        return current

    # By this point all possible move loses us, we simply set
    # the other player as the winner.
    return next_player


if __name__ == "__main__":
    # Input first player
    first: Literal["Kenneth", "Tara"] = input()  # type: ignore

    # Input left and right boxes
    left, right = map(int, input().split())
    print(game(first, left, right))

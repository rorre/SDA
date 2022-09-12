from typing import Literal


def game(current: Literal["Kenneth", "Tara"], left: int, right: int):
    next_player: Literal["Kenneth", "Tara"] = (
        "Tara" if current == "Kenneth" else "Kenneth"
    )
    if right == 0 and left == 0:
        return next_player
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
        return current
    return next_player


first: Literal["Kenneth", "Tara"] = input()  # type: ignore
left, right = map(int, input().split())
game(first, left, right)

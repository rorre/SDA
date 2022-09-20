package main

import (
	"fmt"
)

func game(player string, left int, right int) string {
	var nextPlayer string
	if player == "Tara" {
		nextPlayer = "Kenneth"
	} else {
		nextPlayer = "Tara"
	}

	if right == 0 && left == 0 {
		return nextPlayer
	}

	if (right >= 2 && game(nextPlayer, left, right-2) == player) ||
		(left >= 2 && game(nextPlayer, left-2, right) == player) ||
		(right >= 1 && left >= 1 && game(nextPlayer, left-1, right-1) == player) ||
		(right >= 1 && game(nextPlayer, left, right-1) == player) ||
		(left >= 1 && game(nextPlayer, left-1, right) == player) {
		return player
	}
	return nextPlayer
}

func main() {
	var first string
	var left, right int

	fmt.Scanf("%s\n", &first)
	fmt.Scanf("%d %d", &left, &right)

	fmt.Println(game(first, left, right))
}

package main

import "fmt"

/* Run the memory game for the specified number of rounds */
func memoryGame(startingNumbers []int, rounds int) {

	/* Keep track of prior spoken words via a map */
	spoken := map[int]int{}

	/* Run the initial rounds */
	turn := 1
	for _, number := range startingNumbers[:len(startingNumbers)-1] {
		spoken[number] = turn
		turn++
	}

	/* Run all of the following rounds */
	nextNum := startingNumbers[len(startingNumbers)-1]
	for ; turn < rounds; turn++ {
		last, found := spoken[nextNum]
		spoken[nextNum] = turn
		if found {
			nextNum = turn - last
		} else {
			nextNum = 0
		}
	}

	fmt.Println("Spoken at turn", turn, ":", nextNum)
}

func main() {
	startingNumbers := []int{13, 16, 0, 12, 15, 1}

	memoryGame(startingNumbers, 2020)
	memoryGame(startingNumbers, 30000000)
}

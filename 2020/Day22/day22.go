package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read and parse the input data. */
func readFile(filename string) (*list.List, *list.List) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	initDecks := strings.Split(string(content), "\n\n")
	player1 := parseDeck(initDecks[0])
	player2 := parseDeck(initDecks[1][:len(initDecks[1])-1])

	return player1, player2
}

/* Print a deck (useful for debug mostly) */
func printDeck(deck *list.List) {
	for e := deck.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value, "->")
	}
	fmt.Println("NIL")
}

/* Convert the input file's format to a linked list. */
func parseDeck(input string) *list.List {
	initFrom := strings.Split(input, "\n")[1:]
	deck := list.New()
	for _, val := range initFrom {
		ival, _ := strconv.Atoi(val)
		deck.PushBack(ival)
	}
	return deck
}

/* Get and delete first element of a linked list. */
func PopFront(l *list.List) interface{} {
	val := l.Front()
	l.Remove(val)
	return val.Value
}

/* Run a single round of the basic combat game */
func singleRound(player1 *list.List, player2 *list.List) {
	drawP1 := PopFront(player1).(int)
	drawP2 := PopFront(player2).(int)
	if drawP1 > drawP2 {
		player1.PushBack(drawP1)
		player1.PushBack(drawP2)
	} else {
		player2.PushBack(drawP2)
		player2.PushBack(drawP1)
	}
}

/* Calculate the winner's score to answer prompt */
func calcScore(winner *list.List) int {
	score := 0
	value := winner.Len()
	for e := winner.Front(); e != nil; e = e.Next() {
		score += e.Value.(int) * value
		value--
	}
	return score
}

/* Run the combat game for part 1 */
func part1() {
	player1, player2 := readFile("input")
	for player1.Len() > 0 && player2.Len() > 0 {
		singleRound(player1, player2)
	}

	winner := player1
	if player1.Len() == 0 {
		winner = player2
	}
	score := calcScore(winner)
	fmt.Println("Part 1 score:", score)
}

/* Run a single round of the recursive game. */
func singleRoundRecursive(player1 *list.List, player2 *list.List) {
	drawP1 := PopFront(player1).(int)
	drawP2 := PopFront(player2).(int)

	if drawP1 <= player1.Len() && drawP2 <= player2.Len() {
		// Copy-initialize new lists.
		subP1 := list.New()
		subP2 := list.New()
		e := player1.Front()
		for i := 0; i < drawP1; i++ {
			subP1.PushBack(e.Value)
			e = e.Next()
		}
		e = player2.Front()
		for i := 0; i < drawP2; i++ {
			subP2.PushBack(e.Value)
			e = e.Next()
		}
		// Play the sub-game.
		winner := RecursiveCombat(subP1, subP2)
		if winner == 1 {
			player1.PushBack(drawP1)
			player1.PushBack(drawP2)
		} else {
			player2.PushBack(drawP2)
			player2.PushBack(drawP1)
		}
	} else if drawP1 > drawP2 {
		player1.PushBack(drawP1)
		player1.PushBack(drawP2)
	} else {
		player2.PushBack(drawP2)
		player2.PushBack(drawP1)
	}
}

/* Write the current deck order as a string, to stop looping configurations */
func StringifyGame(player1 *list.List, player2 *list.List) string {
	outstring := ""
	for e := player1.Front(); e != nil; e = e.Next() {
		sval := strconv.Itoa(e.Value.(int))
		outstring += sval + "->"
	}
	outstring += "_vs_"
	for e := player2.Front(); e != nil; e = e.Next() {
		sval := strconv.Itoa(e.Value.(int))
		outstring += sval + "->"
	}
	return outstring
}

/* Run the recurse combat game. */
func RecursiveCombat(player1 *list.List, player2 *list.List) int {

	prior := make(map[string]interface{})

	for player1.Len() > 0 && player2.Len() > 0 {
		strgame := StringifyGame(player1, player2)
		if _, ok := prior[strgame]; ok {
			return 1
		} else {
			prior[strgame] = 1
		}

		singleRoundRecursive(player1, player2)
	}
	// Return int stating the winner.

	if player1.Len() == 0 {
		return 2
	} else {
		return 1
	}

}

/* Run the combat game for part 2 */
func part2() {
	player1, player2 := readFile("input")

	winID := RecursiveCombat(player1, player2)
	winner := player1
	if winID != 1 {
		winner = player2
	}
	score := calcScore(winner)
	fmt.Println("Part 2 score:", score)
}

func main() {
	part1()
	part2()
}

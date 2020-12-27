package main // Change to main to run...

import (
	"container/list"
	"fmt"
)

/* Print the list (useful for debug mostly) */
func printLL(LL *list.List) {
	for e := LL.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value, " ")
	}
	fmt.Println("NIL")
}

/* Determine if a given value is in the next 3 values. */
func InNext3(LL *list.List, current *list.Element, val int) bool {
	tmp := current
	for i := 0; i < 3; i++ {
		tmp = loopingNext(LL, tmp)
		if tmp.Value.(int) == val {
			return true
		}
	}
	return false
}

/* Go to next element or loop if at the end. */
func loopingNext(LL *list.List, current *list.Element) *list.Element {
	if tmp := current.Next(); tmp != nil {
		return tmp
	}
	return LL.Front()
}

/* Perform a number of moves. */
func moves(LL *list.List, locs *[]*list.Element, numMoves int) {
	current := LL.Front()

	for j := 0; j < numMoves; j++ {
		// Determine what the value of the destination is
		nextVal := current.Value.(int) - 1
		if nextVal == 0 {
			nextVal = LL.Len()
		}
		for InNext3(LL, current, nextVal) {
			nextVal--
			if nextVal == 0 {
				nextVal = LL.Len()
			}
		}

		// Look up the value after the destination(to insert before it = after dest)
		destNext := loopingNext(LL, (*locs)[nextVal])
		for i := 0; i < 3; i++ {
			tmpNext := loopingNext(LL, current)
			LL.MoveBefore(tmpNext, destNext)
		}
		current = loopingNext(LL, current)
	}
}

func main() {
	// Part 1
	// We keep the pointers to the LL in a slice to enable fast lookups (necessary for p2)
	locs := make([]*list.Element, 1000001)
	game1 := list.New()
	for _, val := range []int{4, 6, 9, 2, 1, 7, 5, 3, 8} {
		game1.PushBack(val)
		locs[val] = game1.Back()
	}
	moves(game1, &locs, 100)
	fmt.Println("Final ordering in P1:")
	printLL(game1)

	// Part 2
	game := list.New()
	i := 1
	for _, val := range []int{4, 6, 9, 2, 1, 7, 5, 3, 8} {
		game.PushBack(val)
		i++
		locs[val] = game.Back()
	}

	for ; i <= 1000000; i++ {
		game.PushBack(i)
		locs[i] = game.Back()
	}
	moves(game, &locs, 10000000)

	one := locs[1]
	cup1 := loopingNext(game, one)
	cup2 := loopingNext(game, cup1)

	fmt.Println("Part 2 next cups:", cup1.Value.(int), cup2.Value.(int))
	fmt.Println("Part 2 answer:", one.Next().Value.(int)*one.Next().Next().Value.(int))

}

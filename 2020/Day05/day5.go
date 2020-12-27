package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/* Read file and return slice of maps */
func readFile(fname string) []string {

	// Read the entire file as a string
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	seats := strings.Split(string(b), "\n")
	return seats[:len(seats)-1]
}

/* Translate the seat representation to row/column */
func parseSeatLoc(seat string) (int, int) {

	// First eight characters describe the row.
	row := 0
	for i, char := range seat[:7] {
		if char == 'B' {
			row |= (1 << (6 - i))
		}
	}

	// Last three characters describe the column.
	col := 0
	for i, char := range seat[7:] {
		if char == 'R' {
			col |= (1 << (2 - i))
		}
	}

	return row, col
}

/* Find the maximum seat ID for part 1 */
func maxSeatID(seats []string) int {
	maxVal := -1
	for _, seat := range seats {
		row, col := parseSeatLoc(seat)
		if seatID := row*8 + col; seatID > maxVal {
			maxVal = seatID
		}
	}
	return maxVal
}

/* Find the lost seat number for part 2 */
func findMySeat(seats []string) int {
	// Generate a seating chart.
	seatingList := make([]int, maxSeatID(seats)+1)
	for _, seat := range seats {
		row, col := parseSeatLoc(seat)
		seatID := row*8 + col
		seatingList[seatID] = 1
	}

	// Now we can look for an empty seat (ours) not at the front,
	// Since those at the front are not actually existing
	for i := range seatingList {
		if seatingList[len(seatingList)-1-i] == 0 {
			return len(seatingList) - 1 - i
		}
	}
	panic("Didn't find seat!")
}

func main() {
	seats := readFile("input")
	fmt.Println("The maximum seat ID is", maxSeatID(seats))
	fmt.Println("My seat is", findMySeat(seats))

}

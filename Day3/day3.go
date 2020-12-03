package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func readFile(fname string) [][]bool {
	// Read the entire file as a string
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(b), "\n")
	lines = lines[:len(lines)-1] // Last line is empty

	// Preallocate output slice
	treemap := make([][]bool, len(lines))
	for i, line := range lines {
		treemap[i] = make([]bool, len(line))
		fmt.Println(line)
		for j, char := range line {
			if char == '.' {
				treemap[i][j] = false
			} else {
				treemap[i][j] = true
			}
		}
	}
	return treemap
}

/* Given a slope (down, right), count number of trees hit */
func countCollisions(treemap [][]bool, down int, right int) int {

	num_collisions := 0

	// Toboggan ride starts in upper left corner.
	current_row := 0
	current_col := 0
	num_columns := len(treemap[0])

	for current_row < len(treemap) {
		if treemap[current_row][current_col] {
			// Ouch! We hit a tree...
			num_collisions++
		}
		current_row += down
		current_col = (current_col + right) % num_columns
	}

	return num_collisions
}

func main() {

	treemap := readFile("input")

	/* For part one we use the function. */
	ans1 := countCollisions(treemap, 1, 3)
	fmt.Println("Number of collisions with (3,1) slope = ", ans1)

	/* We are in luck, part 2 is easy and we reuse the function above. */
	ansA := countCollisions(treemap, 1, 1)
	ansB := countCollisions(treemap, 1, 5)
	ansC := countCollisions(treemap, 1, 7)
	ansD := countCollisions(treemap, 2, 1)

	fmt.Println("Number of collisions with (1,1) slope = ", ansA)
	fmt.Println("Number of collisions with (5,1) slope = ", ansB)
	fmt.Println("Number of collisions with (7,1) slope = ", ansC)
	fmt.Println("Number of collisions with (1,2) slope = ", ansD)

	fmt.Println("Multiplied together = ", ans1*ansA*ansB*ansC*ansD)
}

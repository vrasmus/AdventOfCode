package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/* Read the input file and return the grid. */
func readFile(filename string) [][]string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]

	grid := make([][]string, len(lines))

	for i, line := range lines {
		grid[i] = strings.Split(line, "")
	}

	return grid
}

/* Prepare an integer grid with the specified size. */
func initGrid(rows int, columns int) [][]int {
	grid := make([][]int, rows)
	for row := range grid {
		grid[row] = make([]int, columns)
	}
	return grid
}

/* Count neighbors as requested by part 1.
Too elaborate solution, but not changing it now :D */
func countSeatedNeighbors(row_i int, col_j int, grid *[][]string) int {
	count := 0
	// Count neighbors in row above.
	if row_i != 0 {
		// Up-left
		if col_j != 0 {
			if (*grid)[row_i-1][col_j-1] == "#" {
				count++
			}
		}
		// Up
		if (*grid)[row_i-1][col_j] == "#" {
			count++
		}
		// Up-right
		if col_j != len((*grid)[0])-1 {
			if (*grid)[row_i-1][col_j+1] == "#" {
				count++
			}
		}
	}

	// Count neighbors in row below
	if row_i != len(*grid)-1 {
		// Down-left
		if col_j != 0 {
			if (*grid)[row_i+1][col_j-1] == "#" {
				count++
			}
		}
		// Down
		if (*grid)[row_i+1][col_j] == "#" {
			count++
		}
		// Down-right
		if col_j != len((*grid)[0])-1 {
			if (*grid)[row_i+1][col_j+1] == "#" {
				count++
			}
		}
	}

	// Count the left neighbor
	if col_j != 0 {
		if (*grid)[row_i][col_j-1] == "#" {
			count++
		}
	}

	// Count the right neighbor
	if col_j < len((*grid)[0])-1 {
		if (*grid)[row_i][col_j+1] == "#" {
			count++
		}
	}

	return count
}

/* Count neighbors from all seats */
func discoverNeighbors(grid *[][]string) [][]int {
	neighbors := initGrid(len(*grid), len((*grid)[0]))

	for row_i := range neighbors {
		for col_j := range neighbors[0] {
			neighbors[row_i][col_j] = countSeatedNeighbors(row_i, col_j, grid)
		}
	}

	return neighbors
}

/* Flip the seats specified */
func flipSeats(grid *[][]string, neighbors [][]int, num_to_flip int) int {
	num_flips := 0
	for row_i := range *grid {
		for col_j, seat := range (*grid)[row_i] {
			// Check if this particular seat should change.
			if seat == "L" && neighbors[row_i][col_j] == 0 {
				(*grid)[row_i][col_j] = "#"
				num_flips++
			} else if seat == "#" && neighbors[row_i][col_j] >= num_to_flip {
				(*grid)[row_i][col_j] = "L"
				num_flips++
			}
		}
	}
	return num_flips
}

/* Apply the process until completion */
func applyProcess(grid *[][]string) {
	flips := -1
	for flips != 0 {
		neighbors := discoverNeighbors(grid)
		flips = flipSeats(grid, neighbors, 4)
	}
}

/* Loop through to count occupied seats */
func countOccupied(grid [][]string) int {
	count := 0
	for row_i := range grid {
		for _, seat := range grid[row_i] {
			if seat == "#" {
				count++
			}
		}
	}
	return count
}

/* Count visbily occupied seats as per part two */
func countVisibleNeighbors(row_i int, col_j int, grid *[][]string) int {
	count := 0

	dir_row := []int{-1, 0, 1, -1, 0, 1, -1, 1}
	dir_col := []int{-1, -1, -1, 1, 1, 1, 0, 0}

	// Loop through all directions.
	for dir_idx := range dir_row {
		delta := 0
		// Continue until a non-empty floor spot is found
		for {
			delta++
			x := row_i + dir_row[dir_idx]*delta
			y := col_j + dir_col[dir_idx]*delta
			// Stop if out of grid
			if x < 0 || x >= len(*grid) || y < 0 || y >= len((*grid)[0]) {
				break
			}
			// Check the seat.
			if (*grid)[x][y] == "L" {
				break
			}
			if (*grid)[x][y] == "#" {
				count++
				break
			}
		}
	}
	return count
}

/* Discover neighbors visible from all seats */
func discoverVisibleNeighbors(grid *[][]string) [][]int {
	neighbors := initGrid(len(*grid), len((*grid)[0]))

	for row_i := range neighbors {
		for col_j := range neighbors[0] {
			neighbors[row_i][col_j] = countVisibleNeighbors(row_i, col_j, grid)
		}
	}

	return neighbors
}

/* Apply the process until completion */
func applyNewProcess(grid *[][]string) {
	flips := -1
	for flips != 0 {
		neighbors := discoverVisibleNeighbors(grid)
		flips = flipSeats(grid, neighbors, 5)
	}
}

func main() {
	seatingGrid := readFile("input")
	applyProcess(&seatingGrid)
	fmt.Println("Part1, occupied seats after stabilization:", countOccupied(seatingGrid))

	seatingGridV2 := readFile("input")
	applyNewProcess(&seatingGridV2)
	fmt.Println("Part2, occupied seats after stabilization:", countOccupied(seatingGridV2))
}

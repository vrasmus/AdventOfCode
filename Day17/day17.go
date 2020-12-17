package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/* Read and parse the input file */
func readFile(input string) [][]string {
	content, err := ioutil.ReadFile(input)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")

	grid := make([][]string, len(lines)-1)

	for i, line := range lines[:len(lines)-1] {
		lineVals := make([]string, len(line))
		for j, char := range line {
			lineVals[j] = string(char)
		}
		grid[i] = lineVals
	}
	return grid
}

/* Print a 3-dimensional grid. */
func printGrid(grid [][][]string) {

	for z, zgrid := range grid {
		fmt.Println("z=", -len(grid)/2+z)
		for _, row := range zgrid {
			fmt.Println(row)
		}
		fmt.Println("")
	}
}

/* Create a larger grid to do operations in */
func embedInLarger(initGrid [][]string, pad int) [][][]string {

	grid := make([][][]string, 1+2*pad)
	for z := range grid {
		grid[z] = make([][]string, len(initGrid)+2*pad)
		for x := range grid[z] {
			grid[z][x] = make([]string, len(initGrid)+2*pad)
			for y := range grid[z][x] {
				grid[z][x][y] = "."
			}
		}
	}

	for x, line := range initGrid {
		for y, char := range line {
			grid[pad][pad+x][pad+y] = string(char)
		}
	}

	return grid
}
func embedInLarger4D(initGrid [][]string, pad int) [][][][]string {

	grid := make([][][][]string, 1+2*pad)
	for w := range grid {
		grid[w] = make([][][]string, 1+2*pad)
		for z := range grid {
			grid[w][z] = make([][]string, len(initGrid)+2*pad)
			for x := range grid[w][z] {
				grid[w][z][x] = make([]string, len(initGrid)+2*pad)
				for y := range grid[w][z][x] {
					grid[w][z][x][y] = "."
				}
			}
		}
	}

	for x, line := range initGrid {
		for y, char := range line {
			grid[pad][pad][pad+x][pad+y] = string(char)
		}
	}

	return grid
}

/* Count # active neighbors of any position */
func numActiveNeighbors(grid *[][][]string, x, y, z int) int {
	delta := []int{-1, 0, 1}
	count := 0
	for _, dx := range delta {
		for _, dy := range delta {
			for _, dz := range delta {
				if dx == 0 && dy == 0 && dz == 0 {
					continue
				}
				if (*grid)[z+dz][x+dx][y+dy] == "#" {
					count += 1
				}
			}
		}
	}
	return count
}

func numActiveNeighbors4D(grid *[][][][]string, x, y, z, w int) int {
	delta := []int{-1, 0, 1}
	count := 0
	for _, dw := range delta {
		for _, dx := range delta {
			for _, dy := range delta {
				for _, dz := range delta {
					if dx == 0 && dy == 0 && dz == 0 && dw == 0 {
						continue
					}
					if (*grid)[w+dw][z+dz][x+dx][y+dy] == "#" {
						count += 1
					}
				}
			}
		}
	}
	return count
}

/* Make a grid deciding whether to flip each cube */
func determineFlips(grid [][][]string) [][][]bool {
	flips := make([][][]bool, len(grid)) //, len(initGrid)+2*pad, len(initGrid)+2*pad)

	for z := range grid {
		flips[z] = make([][]bool, len(grid[z]))
		for x := range grid[z] {
			flips[z][x] = make([]bool, len(grid[z][x]))
			for y := range grid[z][x] {
				if x == 0 || y == 0 || z == 0 || x == len(flips[0])-1 || y == len(flips[0])-1 || z == len(flips)-1 {
					// Skip boundaries (assumes large enough grid)
					continue
				}
				neighborCount := numActiveNeighbors(&grid, x, y, z)
				if neighborCount == 3 && grid[z][x][y] == "." {
					// We have exactly 2 neighbors active, so flip
					flips[z][x][y] = true
				} else if (neighborCount != 2 && neighborCount != 3) && grid[z][x][y] == "#" {
					// We don't have EXACTLY 2 or 3 neighors active, so flip
					flips[z][x][y] = true
				}
			}
		}
	}
	return flips
}
func determineFlips4D(grid [][][][]string) [][][][]bool {
	flips := make([][][][]bool, len(grid))
	for w := range grid {
		flips[w] = make([][][]bool, len(grid[w]))
		for z := range grid {
			flips[w][z] = make([][]bool, len(grid[w][z]))
			for x := range grid[w][z] {
				flips[w][z][x] = make([]bool, len(grid[w][z][x]))
				for y := range grid[w][z][x] {
					if x == 0 || y == 0 || z == 0 || w == 0 || x == len(flips[0][0])-1 || y == len(flips[0][0])-1 || z == len(flips)-1 || w == len(flips)-1 {
						// Skip boundaries (assumes large enough grid)
						continue
					}
					neighborCount := numActiveNeighbors4D(&grid, x, y, z, w)
					if neighborCount == 3 && grid[w][z][x][y] == "." {
						// We have exactly 2 neighbors active, so flip
						flips[w][z][x][y] = true
					} else if (neighborCount != 2 && neighborCount != 3) && grid[w][z][x][y] == "#" {
						// We don't have EXACTLY 2 or 3 neighors active, so flip
						flips[w][z][x][y] = true
					}
				}
			}
		}
	}
	return flips
}

/* Flip the grid according to the flips determine previously */
func flipGrid(grid *[][][]string, flips [][][]bool) {
	for z := range *grid {
		for x := range (*grid)[z] {
			for y := range (*grid)[z][x] {
				if flips[z][x][y] {
					if (*grid)[z][x][y] == "#" {
						(*grid)[z][x][y] = "."
					} else if (*grid)[z][x][y] == "." {
						(*grid)[z][x][y] = "#"
					}
				}
			}
		}
	}
}
func flipGrid4D(grid *[][][][]string, flips [][][][]bool) {
	for w := range *grid {
		for z := range *grid {
			for x := range (*grid)[w][z] {
				for y := range (*grid)[w][z][x] {
					if flips[w][z][x][y] {
						if (*grid)[w][z][x][y] == "#" {
							(*grid)[w][z][x][y] = "."
						} else if (*grid)[w][z][x][y] == "." {
							(*grid)[w][z][x][y] = "#"
						}
					}
				}
			}
		}
	}
}

/* Count the number of active nodes in 3D or 4D*/
func countActive(grid [][][]string) {
	count := 0
	for z := range grid {
		for x := range grid[z] {
			for y := range grid[z][x] {
				if grid[z][x][y] == "#" {
					count++
				}
			}
		}
	}
	fmt.Println("Active:", count)
}
func countActive4D(grid [][][][]string) {
	count := 0
	for w := range grid {
		for z := range grid {
			for x := range grid[w][z] {
				for y := range grid[w][z][x] {
					if grid[w][z][x][y] == "#" {
						count++
					}
				}
			}
		}
	}
	fmt.Println("Active:", count)
}

func part1(initGrid [][]string) {
	cycles := 6

	pad := cycles + 1
	grid := embedInLarger(initGrid, pad)
	printGrid(grid)

	for i := 0; i < cycles; i++ {
		flips := determineFlips(grid)
		flipGrid(&grid, flips)
	}

	countActive(grid)
}

/* To not ruin my part 1 solution, the easiest
apporach for part 2 was to add new 4D functions.
It would be possible to reuse and make generic, but
not worth the effort here. */
func part2(initGrid [][]string) {
	cycles := 6

	pad := cycles + 1
	grid := embedInLarger4D(initGrid, pad)

	for i := 0; i < cycles; i++ {
		flips := determineFlips4D(grid)
		flipGrid4D(&grid, flips)
	}

	countActive4D(grid)
}

func main() {

	initGrid := readFile("input")

	part1(initGrid)
	part2(initGrid)

}

package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/* Read file at return lines as a slice of strings */
func readFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	return lines[:len(lines)-1]
}

/* Flip a tile, turning it black if white and vice versa */
func flipTile(hexgrid *map[int]map[int]string, x, y int) {
	if _, foundX := (*hexgrid)[x]; !foundX {
		(*hexgrid)[x] = make(map[int]string)
	}

	if old, foundY := (*hexgrid)[x][y]; foundY {
		if old == "b" {
			(*hexgrid)[x][y] = "w"
			return
		}
	}
	(*hexgrid)[x][y] = "b"
}

/* Decode an instruction, determining its x and y coordinates */
func decode(instruction string) (int, int) {
	x, y := 0, 0

	for i := 0; i < len(instruction); i++ {
		if instruction[i:i+1] == "e" {
			x += 2
		} else if instruction[i:i+1] == "w" {
			x -= 2
		} else if instruction[i:i+2] == "se" {
			x++
			y--
			i++
		} else if instruction[i:i+2] == "sw" {
			x--
			y--
			i++
		} else if instruction[i:i+2] == "nw" {
			x--
			y++
			i++
		} else if instruction[i:i+2] == "ne" {
			x++
			y++
			i++
		} else {
			panic("Unexpected direction")
		}
	}
	return x, y
}

/* Loop through the hex grid to find num. titles */
func countBlackTiles(hexgrid map[int]map[int]string) int {
	count := 0
	for _, row := range hexgrid {
		for _, val := range row {
			if val == "b" {
				count++
			}
		}
	}
	return count
}

/* Count the number of neighboring black tiles */
func countBlackNeighbors(hexgrid *map[int]map[int]string, x, y int) int {
	// Each tile has 6 neighbors.
	nX := []int{2, -2, 1, 1, -1, -1}
	nY := []int{0, 0, 1, -1, 1, -1}

	count := 0
	for i := 0; i < 6; i++ {
		if color, exists := (*hexgrid)[x+nX[i]][y+nY[i]]; exists {
			if color == "b" {
				count++
			}
		}
	}

	return count
}

/* Make a new map by doing all the flips for a day. */
func dailyFlip(oldGrid map[int]map[int]string) map[int]map[int]string {

	// Find max values that might flip
	maxE := -1000000
	maxW := 1000000
	maxN := -1000000
	maxS := 1000000

	// Copy old configuration to a new map and find max distance from origin.
	newGrid := make(map[int]map[int]string)
	for xkey, xval := range oldGrid {
		newGrid[xkey] = make(map[int]string)
		for ykey, val := range xval {
			newGrid[xkey][ykey] = val
			if ykey > maxN {
				maxN = ykey
			}
			if ykey < maxS {
				maxS = ykey
			}
		}
		if xkey > maxE {
			maxE = xkey
		}
		if xkey < maxW {
			maxW = xkey
		}
	}

	// Loop through potential locations No need to handle required empty spots, as they always have 0 black neighbors.
	for x := maxW - 2; x < maxE+2; x++ {
		// Make sure that we have this particular x-map
		if _, exists := newGrid[x]; !exists {
			newGrid[x] = make(map[int]string)
		}

		for y := maxS - 2; y < maxN+2; y++ {
			neighbors := countBlackNeighbors(&oldGrid, x, y)
			old, exists := oldGrid[x][y]
			if !exists || old == "w" {
				// The tile was white before
				if neighbors == 2 {
					newGrid[x][y] = "b"
				}
			} else {
				// The tile was black previously
				if neighbors == 0 || neighbors > 2 {
					newGrid[x][y] = "w"
				}
			}
		}
	}
	return newGrid
}

func main() {
	instructions := readFile("input")
	hexgrid := make(map[int]map[int]string)

	// Flip all the required tiles for part 1
	for _, instruction := range instructions {
		x, y := decode(instruction)

		flipTile(&hexgrid, x, y)
	}
	fmt.Println("Black tiles after flipping:", countBlackTiles(hexgrid))

	// Do 100 daily flips for part 2
	for i := 0; i < 100; i++ {
		hexgrid = dailyFlip(hexgrid)
	}

	fmt.Println("Black tiles after 100 days:", countBlackTiles(hexgrid))
}

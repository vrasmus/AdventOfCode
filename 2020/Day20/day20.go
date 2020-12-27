package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read and parse the input data. */
func readFile(input string) []tile {
	content, err := ioutil.ReadFile(input)
	if err != nil {
		panic(err)
	}

	// Split by tile.
	rawTiles := strings.Split(string(content), "\n\n")
	tiles := make([]tile, len(rawTiles))
	for i, tile := range rawTiles {
		tiles[i] = makeTile(tile)
	}
	return tiles
}

// Define a tile to work with
type tile struct {
	id   int
	data []string
}

// Form a tile from the input description
func makeTile(input string) tile {
	this := tile{}

	lines := strings.Split(input, "\n")
	idstr := lines[0][5 : len(lines[0])-1]
	this.id, _ = strconv.Atoi(idstr)
	this.data = lines[1:]
	return this
}

// Rotate a tile 90 deg counterclockwise
func (t *tile) Rotate() {
	rotated := make([]string, len(t.data))
	for i := 0; i < 10; i++ {
		rotated[i] = ""
		for j := 0; j < 10; j++ {
			rotated[i] += string(t.data[j][9-i])
		}
	}
	t.data = rotated
}

// Flip a tile vertically
func (t *tile) Flip() {
	flipped := make([]string, len(t.data))
	for i := 0; i < 10; i++ {
		flipped[i] = t.data[9-i]
	}
	t.data = flipped
}

// Print a tile
func (t *tile) Print() {
	for _, line := range t.data {
		fmt.Println(line)
	}
	fmt.Println("")
}

/* Check to see if two tiles fit together vertically */
func (t *tile) FitsBelow(other tile) bool {

	if t.data[0] == other.data[9] {
		return true
	} else {
		return false
	}

}

/* Check to see if two tiles fit together horizontally*/
func (t *tile) FitsRight(other tile) bool {

	for i := 0; i < 10; i++ {
		if t.data[i][0] != other.data[i][9] {
			return false
		}
	}
	return true
}

/* Init a square image of tiles. */
func initSquareImage(size int) [][]tile {
	img := make([][]tile, size)
	for i := range img {
		img[i] = make([]tile, size)
	}
	return img
}

/* Check if a given tile can be picked or is already used. */
func canPick(id int, img *[][]tile) bool {
	for _, row := range *img {
		for _, used := range row {
			if used.id == id {
				return false
			}
		}
	}
	return true
}

/* Find the next location to insert a tile in */
func findNextLoc(img [][]tile) (int, int) {
	found := false
	nextRow := 0
	nextCol := 0

	for i, row := range img {
		for j, x := range row {
			if x.id == 0 {
				nextRow = i
				nextCol = j
				found = true
				break
			}
		}
		if found {
			break
		}
	}

	return nextRow, nextCol
}

/* Add a tile to the image -- if it fits with the current ones */
func tryAddTile(t tile, img *[][]tile) bool {
	nextRow, nextCol := findNextLoc(*img)

	if (nextRow > 0 && t.FitsBelow((*img)[nextRow-1][nextCol])) &&
		(nextCol > 0 && t.FitsRight((*img)[nextRow][nextCol-1])) {
		// We are in the interior of the image.
		(*img)[nextRow][nextCol] = t
		return true
	} else if nextRow == 0 && (nextCol > 0 && t.FitsRight((*img)[nextRow][nextCol-1])) {
		// We are considering leftmost column
		(*img)[nextRow][nextCol] = t
		return true
	} else if nextCol == 0 && (nextRow > 0 && t.FitsBelow((*img)[nextRow-1][nextCol])) {
		// We are considering top column
		(*img)[nextRow][nextCol] = t
		return true
	} else if nextRow == 0 && nextCol == 0 {
		// We are considering upper left cornerr (any works)
		(*img)[nextRow][nextCol] = t
		return true
	} else {
		return false
	}
}

/* Remove the last added tile */
func removePriorTile(img *[][]tile) {
	row, col := findNextLoc(*img)
	if col == 0 {
		row--
		col = len(*img) - 1
	} else {
		col--
	}
	(*img)[row][col] = tile{}
}

/* Use a backtracking solution to find the correct image */
func backtracking(tiles *[]tile, img *[][]tile) bool {
	for _, tile := range *tiles {
		if !canPick(tile.id, img) {
			continue
		}
		// Try all configurations of this tile.
		for i := 0; i < 4; i++ {
			tile.Rotate()
			if fit := tryAddTile(tile, img); fit {
				if valid := backtracking(tiles, img); valid {
					return valid
				} else {
					removePriorTile(img)
				}
			}
		}
		tile.Flip()
		for i := 0; i < 4; i++ {
			tile.Rotate()
			if fit := tryAddTile(tile, img); fit {
				if valid := backtracking(tiles, img); valid {
					return valid
				} else {
					removePriorTile(img)
				}
			}
		}
	}
	// If we did not yet use all, we return false.
	for _, tile := range *tiles {
		if canPick(tile.id, img) {
			return false
		}
	}
	// If all was used, we are done.
	return true
}

/* Print out the answer for part 1 */
func part1(img [][]tile) {
	s := len(img) - 1
	fmt.Println("Part 1 answer:", img[0][0].id*img[0][s].id*img[s][0].id*img[s][s].id)
}

/* We can now build the full image! */
func reconstructImage(orderedTiles [][]tile) []string {
	size := len(orderedTiles)
	img := make([]string, size*8)
	for iTiles, tRow := range orderedTiles {
		for _, t := range tRow {
			for i, row := range t.data[1:9] {
				img[iTiles*8+i] += row[1:9]
			}
		}
	}
	return img
}

/* This just prints out indices where the monster should be */
func seaMonsterPattern(x, y int) {
	fmt.Print("row 0:")
	for i, char := range ".#...#.###...#.##.O#.." {
		if char == 'O' {
			fmt.Print(i, " ")
		}
	}
	fmt.Println("")
	fmt.Print("row 1:")
	for i, char := range "O.##.OO#.#.OO.##.OOO##" {
		if char == 'O' {
			fmt.Print(i, " ")
		}
	}
	fmt.Println("")
	fmt.Print("row 2:")
	for i, char := range "#O.#O#.O##O..O.#O##.##" {
		if char == 'O' {
			fmt.Print(i, " ")
		}
	}
	fmt.Println("")

}

/* Hardcoded check if a seamonster exists */
func seaMonsterAt(x, y int, img []string) bool {

	//row 0:18
	//row 1:0 5 6 11 12 17 18 19
	//row 2:1 4 7 10 13 16

	if img[x][y+18] == '#' {
		if img[x+1][y] == '#' && img[x+1][y+5] == '#' && img[x+1][y+6] == '#' &&
			img[x+1][y+11] == '#' && img[x+1][y+12] == '#' && img[x+1][y+17] == '#' &&
			img[x+1][y+18] == '#' && img[x+1][y+19] == '#' {
			if img[x+2][y+1] == '#' && img[x+2][y+4] == '#' && img[x+2][y+7] == '#' &&
				img[x+2][y+10] == '#' && img[x+2][y+13] == '#' && img[x+2][y+16] == '#' {
				return true
			}
		}
	}
	return false
}

/* Search entire image for sea monsters*/
func searchMonsters(img []string) int {
	monsterCount := 0
	for x := 0; x < len(img[0])-2; x++ {
		for y := 0; y < len(img)-20; y++ {
			if seaMonsterAt(x, y, img) {
				monsterCount++
			}
		}
	}
	return monsterCount
}

/* Count the number of waves in the water */
func howRoughWaters(img []string) int {
	count := 0
	for x := 0; x < len(img[0]); x++ {
		for y := 0; y < len(img); y++ {
			if img[x][y] == '#' {
				count++
			}
		}
	}
	// Remember to subtract those part of monster
	return count
}

/* We try the habitats roughness. Works without rotating, so won't bother. */
func part2(img [][]tile) {
	full := reconstructImage(img)
	monsters := searchMonsters(full)
	fmt.Println("Habitat's roughness:", howRoughWaters(full)-monsters*15)
}

func main() {
	tiles := readFile("input")
	img := initSquareImage(12)
	fmt.Println("Solved:", backtracking(&tiles, &img))
	part1(img)
	part2(img)
}

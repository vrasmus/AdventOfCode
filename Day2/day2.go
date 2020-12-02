package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// Read the file and parse the content as four slices.
func readInput(fname string) (minNumLetter []int, maxNumLetter []int, letters []rune, passwords []string) {
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(b), "\n")

	minNumLetter = make([]int, 0, len(lines))
	maxNumLetter = make([]int, 0, len(lines))
	letters = make([]rune, 0, len(lines))
	passwords = make([]string, 0, len(lines))

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		lwords := strings.Split(line, " ")

		minVal, _ := strconv.Atoi(strings.Split(lwords[0], "-")[0]) // First half
		maxVal, _ := strconv.Atoi(strings.Split(lwords[0], "-")[1]) // Other half
		letter := rune(lwords[1][0])                                // First character of 2nd word
		pw := lwords[2]

		minNumLetter = append(minNumLetter, minVal)
		maxNumLetter = append(maxNumLetter, maxVal)
		letters = append(letters, letter)
		passwords = append(passwords, pw)
	}

	return minNumLetter, maxNumLetter, letters, passwords
}

/* For the first part, we just iterate through each password to count the number of occurences */
func Part1(minVal int, maxVal int, letter rune, password string) bool {
	count := 0
	for _, char := range password {
		if char == letter {
			count++
		}
	}
	if count >= minVal && count <= maxVal {
		return true
	} else {
		return false
	}
}

/* For the second part, we need to check only the two locations specified. */
func Part2(firstLoc int, secondLoc int, letter rune, password string) bool {
	// We compare each location to the specified letter (locs are 1-indexed)
	firstLocIs := password[firstLoc-1] == byte(letter)
	secondLocIs := password[secondLoc-1] == byte(letter)

	// ...and xor the outputs
	return firstLocIs != secondLocIs
}

func main() {
	minNumLetter, maxNumLetter, letters, passwords := readInput("input")

	//	fmt.Println(minNumLetter, maxNumLetter, letters, passwords)

	numValid := 0
	for i, pw := range passwords {
		if Part1(minNumLetter[i], maxNumLetter[i], letters[i], pw) {
			numValid++
		}
	}
	fmt.Println("Part 1: Num valid=", numValid)

	numValid2 := 0
	for i, pw := range passwords {
		if Part2(minNumLetter[i], maxNumLetter[i], letters[i], pw) {
			numValid2++
		}
	}
	fmt.Println("Part 1: Num valid=", numValid2)

}

package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read the input file */
func readFile(filename string) []int {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]

	/* Convert to integer slice */
	numbers := make([]int, len(lines))
	for i, line := range lines {
		num, _ := strconv.Atoi(line)
		numbers[i] = num
	}

	return numbers

}

/* Find first element without the summation property */
func findFirstWithoutProperty(numbers []int) int {
	/* We keep a set of currently useful numbers.
	We do this as a map with an empty struct, as the struct uses 0 memory */
	possibleNumbers := map[int]struct{}{}

	/* First we handle the XMAS preamble */
	preambleLength := 25
	for _, num := range numbers[:preambleLength] {
		possibleNumbers[num] = struct{}{}
	}

	/* Now we look for the first entry that isn't a sum of two 'close' before */
	for i, num := range numbers[preambleLength:] {
		works := false
		// Brute-force check all values
		for key, _ := range possibleNumbers {
			// Check if a sum with this element works
			if _, ok := possibleNumbers[num-key]; ok == true {
				works = true
				break
			}
		}
		if !works {
			fmt.Println("Not possible to construct", num)
			return num
		}

		// Remove now obsolete value and add new one
		delete(possibleNumbers, numbers[i])
		possibleNumbers[num] = struct{}{}
	}
	return -1
}

/* Need to find min and max over a window */
func minMaxSlice(slice []int) (int, int) {
	min := slice[0]
	max := slice[0]
	for _, num := range slice[1:] {
		if num < min {
			min = num
		}
		if num > max {
			max = num
		}
	}
	return min, max
}

/* Find contigous elements summing to given number */
func findContigousSum(numbers []int, sum int) {

	// Look for a congious sum of at least 2 numbers summing to given value
	for windowSize := 2; windowSize < len(numbers); windowSize++ {
		// We use a rolling sum. First window:
		tmpsum := 0
		for _, num := range numbers[:windowSize] {
			tmpsum += num
		}

		/* Generally it makes sense to check if first sum is the right one,
		but no need here since first values are so small */

		for i := range numbers[:len(numbers)-windowSize] {
			tmpsum -= numbers[i]
			tmpsum += numbers[i+windowSize]
			if tmpsum == sum {
				min, max := minMaxSlice(numbers[i+1 : 1+i+windowSize])
				fmt.Println("Summing slice found. Its min+max =", min+max)
				return
			}
		}
	}
}

func main() {
	numbers := readFile("input")

	firstWithout := findFirstWithoutProperty(numbers)

	findContigousSum(numbers, firstWithout)
}

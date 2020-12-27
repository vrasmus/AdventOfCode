package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

/* Read the input file. */
func readFile(filename string) []int {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]

	jolts := make([]int, len(lines))
	for i, line := range lines {
		adapter, _ := strconv.Atoi(line)

		jolts[i] = adapter
	}
	return jolts
}

/* Find distribution of cumulative entires in the sorted array */
func findDistribution(jolts []int) {

	// Count the differences.
	counts := []int{0, 0, 0}
	for i := range jolts[:len(jolts)-1] {
		diff := jolts[i+1] - jolts[i]
		counts[diff-1]++
	}

	fmt.Println("Num ones * Num threes =", counts[0], "*", counts[2], "=", counts[0]*counts[2])
}

/* Recursively count the number of possible configurations. Works but too slow. */
func countConfigurations(jolts []int) int {
	if len(jolts) == 1 {
		return 1
	}

	count := 0
	i := 1
	// There might be three valid connecters. Will follow in list:
	for jolts[i]-jolts[0] < 4 {
		count += countConfigurations(jolts[i:])
		i++
		if i == len(jolts) {
			break
		}
	}
	return count
}

/* Recursively count the number of possible configurations -- with memoization */

//Define global cache variable.
var cache = make(map[int]int)

func memoizedCountConfigurations(jolts []int) int {

	// Check if previosly calculated for this adapter.
	if count, ok := cache[jolts[0]]; ok {
		return count
	}

	// If last element, only one configuration.
	if len(jolts) == 1 {
		return 1
	}

	// Determine the count.
	count := 0
	i := 1
	for jolts[i]-jolts[0] < 4 {
		count += memoizedCountConfigurations(jolts[i:])
		i++
		if i == len(jolts) {
			break
		}
	}
	// Save this result for later use.
	cache[jolts[0]] = count
	return count
}

func main() {
	adapters := readFile("input")
	sort.Ints(adapters)

	// Let's have the entire set of jolts.
	jolts := []int{0}
	jolts = append(append(jolts, adapters...), 3+adapters[len(adapters)-1])

	// Part 1:
	findDistribution(jolts)

	// Part 2:
	configurations := memoizedCountConfigurations(jolts)
	fmt.Println("Number of configurations:", configurations)
}

package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/*
File loading inspired by
https://stackoverflow.com/questions/9862443/golang-is-there-a-better-way-read-a-file-of-integers-into-an-array
*/
func readFile(fname string) []int {
	// Read the entire file as a string
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(b), "\n")

	// Preallocate output slice
	numbers := make([]int, 0, len(lines))

	for _, l := range lines {
		// Empty line occurs at the end of the file when we use Split.
		if len(l) == 0 {
			continue
		}

		// Convert string repr of line to integer
		num, err := strconv.Atoi(l)
		if err != nil {
			panic(err)
		}
		numbers = append(numbers, num)
	}

	return numbers
}

func main() {
	// First load in the file.
	numbers := readFile("input")
	fmt.Println(numbers)

	/*
		Part 1: Find two numbers fitting the criteria.

		We have several options for how to solve this problem.
		The most intuitive is looping through the list twice, which is O(n^2).
		This should be fine given the input size.
		We can also do O(n) with the use of some space, so let's do that instead.
	*/

	// Preallocate a bool array telling if a number has already been seen.
	occurs := make([]bool, 2020)

	// Now go through the numbers to find a solution.
	for _, n := range numbers {
		if occurs[2020-n] {
			fmt.Println("Numbers are found.")
			fmt.Println(n, "+", 2020-n, " = ", n+(2020-n))
			fmt.Println(n, "*", 2020-n, " = ", n*(2020-n))
		} else {
			occurs[n] = true
		}
	}

	/*
		Part 2: Find three numbers fitting the criteria.

		Now we can go for an O(n^2) approach and utilize the slice from before.
	*/
	for _, n1 := range numbers {
		for _, n2 := range numbers {
			if n1+n2 < 2020 && occurs[2020-n1-n2] {
				fmt.Println("Numbers are found.")
				fmt.Println(n1, "+", n2, "+", 2020-n1-n2, " = ", n1+n2+(2020-n1-n2))
				fmt.Println(n1, "*", n2, "*", 2020-n1-n2, " = ", n1*n2*(2020-n1-n2))
			}
		}
	}

}

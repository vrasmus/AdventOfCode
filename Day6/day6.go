package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/* Load the input file */
func readFile(fname string) []string {
	content, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	// Remove final newline
	content = content[:len(content)-1]

	// Split the content into their groups
	groups := strings.Split(string(content), "\n\n")

	return groups
}

/* Sum the values of an integer slice */
func sum(slice []int) int {
	result := 0
	for _, value := range slice {
		result += value
	}
	return result
}

/*
Determine the answer of a single group, when ANYONE can say yes for all
We return it as a 'truth array'
*/
func groupAnswerPart1(group string) []int {
	individualAnswers := strings.Split(group, "\n")

	observed := make([]int, 26)
	for _, answer := range individualAnswers {
		for _, q := range answer {
			observed[q-'a'] = 1
		}
	}
	return observed
}

/*
Determine the answer of a single group, when ALL must say yes
We return it as a 'truth array'
*/
func groupAnswerPart2(group string) []int {
	individualAnswers := strings.Split(group, "\n")

	// Count number of times "yes" is said in the group.
	observed := make([]int, 26)
	for _, answer := range individualAnswers {
		for _, q := range answer {
			observed[q-'a'] += 1
		}
	}
	// Determine questions ALL said yes to.
	for i, count := range observed {
		observed[i] = count / len(individualAnswers)
	}

	return observed
}

func main() {
	groups := readFile("input")

	// Count the total for all groups, part 1
	counts := 0
	for _, group := range groups {
		answer := groupAnswerPart1(group)
		counts += sum(answer)
	}
	fmt.Println("Part 1 total yes answers:", counts)

	// Count the total for all groups, part 2
	counts = 0
	for _, group := range groups {
		answer := groupAnswerPart2(group)
		counts += sum(answer)
	}
	fmt.Println("Part 2 total yes answers:", counts)
}

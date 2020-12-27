package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read input data file */
func readFile(filename string) (int, []string) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")

	earliest, _ := strconv.Atoi(lines[0])
	schedule := strings.Split(lines[1], ",")

	return earliest, schedule
}

/*
Parse the schedule.
*/
func parseScheduleWithOffsets(schedule []string) ([]int, []int) {
	busses := make([]int, 0)
	offsets := make([]int, 0)
	for i, entry := range schedule {
		if entry != "x" {
			intE, _ := strconv.Atoi(entry)
			busses = append(busses, intE)
			offsets = append(offsets, i)
		}
	}
	return busses, offsets
}

/* Since there are only few busses, we just manually inspect output for part 1. */
func findEarliestPossible(earliest int, busses []int) {
	for _, bus := range busses {
		waitingTime := bus - (earliest % bus)
		fmt.Println("Waiting time: ", waitingTime, "ID*WT = ", waitingTime*bus)
	}
}

func findMatchingTimestamp(busses []int, offsets []int) {
	// Big numbers incoming, using big unsigned int
	var t uint64 = uint64(busses[0])
	var step uint64 = 1

	for i := range busses {
		for (t+uint64(offsets[i]))%uint64(busses[i]) != 0 {
			// Step to next time old values appear,
			// until we find a match for new value as well.
			t += step
		}
		step *= uint64(busses[i])
	}
	fmt.Println("The first occurence time is:", t)
}

func main() {
	earliest, schedule := readFile("input")
	busses, offsets := parseScheduleWithOffsets(schedule)
	findEarliestPossible(earliest, busses)
	findMatchingTimestamp(busses, offsets)
}

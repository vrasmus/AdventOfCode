package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

type ticketRule struct {
	name string
	// The lower and upper values of the two ranges are recorded.
	fromA int
	toA   int
	fromB int
	toB   int
}

func parseSingleRule(rule string) (int, int) {
	strInts := strings.Split(rule, "-")
	from, _ := strconv.Atoi(strInts[0])
	to, _ := strconv.Atoi(strInts[1])
	return from, to
}

func parseTicketRule(rule string) ticketRule {
	splitRules := strings.Split(rule, " or ")
	fromA, toA := parseSingleRule(splitRules[0])
	fromB, toB := parseSingleRule(splitRules[1])
	return ticketRule{"", fromA, toA, fromB, toB}
}

func parseTicketLine(line string) []int {
	fields := strings.Split(line, ",")
	ticket := make([]int, len(fields))
	for i, field := range fields {
		ticket[i], _ = strconv.Atoi(field)
	}
	return ticket

}

/* Read and parse the input file. */
func readFile(filename string) ([]ticketRule, []int, [][]int) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	contentGroups := strings.Split(string(content), "\n\n")

	ruleLines := strings.Split(contentGroups[0], "\n")
	ticketRules := make([]ticketRule, len(ruleLines))
	for i, line := range ruleLines {
		field := strings.Split(line, ": ")
		rules := parseTicketRule(field[1])
		ticketRules[i] = rules
		ticketRules[i].name = field[0]
	}

	myTicketLines := strings.Split(contentGroups[1], "\n")
	myTicket := parseTicketLine(myTicketLines[1])

	ticketLines := strings.Split(contentGroups[2], "\n")
	ticketLines = ticketLines[:len(ticketLines)-1]
	tickets := make([][]int, len(ticketLines)-1)
	for j, line := range ticketLines[1:] {
		tickets[j] = parseTicketLine(line)
	}

	return ticketRules, myTicket, tickets
}

/* For part one, we find the 'ticket scanning error rate' and discard wrong tickets */
func ticketScan(rules []ticketRule, tickets [][]int) [][]int {
	// We first generate a boolean list of all valid values.
	validValues := make([]bool, 1000)

	for _, rule := range rules {
		for i := rule.fromA; i <= rule.toA; i++ {
			validValues[i] = true
		}
		for i := rule.fromB; i <= rule.toB; i++ {
			validValues[i] = true
		}
	}

	validTickets := make([][]int, 0)
	TSER := 0
	for _, ticket := range tickets {
		valid := true
		for _, value := range ticket {
			if !validValues[value] {
				TSER += value
				valid = false
			}
		}
		if valid {
			validTickets = append(validTickets, ticket)
		}
	}
	fmt.Println("Ticket scanning error rate:", TSER)
	return validTickets
}

// Check if a given rule is satisfied with the value.
func ruleNotSatisfied(rule ticketRule, value int) bool {
	return (value < rule.fromA || value > rule.toA) &&
		(value < rule.fromB || value > rule.toB)
}

// Small struct to keep name and possible locs together.
type field struct {
	name         string
	possibleLocs []int
}

/* Determine which fields a certain rule works for (and which it doesn't */
func matchRule(rule ticketRule, tickets [][]int) field {
	locs := make([]int, 0)
	for i := range tickets[0] {
		// Loop over all ticket fields
		match := true
		for j := range tickets {
			if ruleNotSatisfied(rule, tickets[j][i]) {
				match = false
				break
			}
		}
		if match {
			locs = append(locs, i)
		}
	}

	// An output [0, 10] means that the rule matches either field 0 or 10.
	return field{rule.name, locs}
}

/* Method to check if slice contains a given element */
func contains(s []int, e int) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

func findValid(alreadyChosen []int, names []string, matches []field) ([]int, []string, bool) {
	// When we have used all elements, we found a solution.
	if len(alreadyChosen) == 20 {
		return alreadyChosen, names, true
	}

	for _, guess := range matches[len(alreadyChosen)].possibleLocs {
		if contains(alreadyChosen, guess) {
			// can't use any value twice
			continue
		}
		// Recursively try values.
		order, names, done := findValid(append(alreadyChosen, guess),
			append(names, matches[len(alreadyChosen)].name),
			matches)
		if done {
			return order, names, done
		}
	}

	return alreadyChosen, names, false
}

/* For part two, we must find our what each field means... */
func determineMeaning(rules []ticketRule, tickets [][]int) ([]int, []string) {

	/* Determine which fields match where. */
	matches := make([]field, len(rules))
	for ruleID, rule := range rules {
		matches[ruleID] = matchRule(rule, tickets)
	}

	/* We sort the matchings, sicne some have many possibilities. */
	sort.SliceStable(matches, func(i, j int) bool {
		return len(matches[i].possibleLocs) < len(matches[j].possibleLocs)
	})

	actualOrder, names, _ := findValid([]int{}, []string{}, matches)
	return actualOrder, names
}

func main() {
	ticketRules, myTicket, otherTickets := readFile("input")
	validTickets := ticketScan(ticketRules, otherTickets)

	order, names := determineMeaning(ticketRules, validTickets)

	// Product of those starting with departure
	prod := 1
	for i := range order {
		if len(names[i]) > 8 && names[i][:9] == "departure" {
			prod *= myTicket[order[i]]
		}
	}
	fmt.Println("Final result:", prod)
}

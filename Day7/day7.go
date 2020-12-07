package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read the input file and split by lines. */
func readFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	return lines[:len(lines)-1]
}

/* Split a content description into number and type */
func parseContent(content string) (int, string) {
	// Assumes one digit only
	num, _ := strconv.Atoi(content[:1])
	bagtype := strings.Split(content, " bag")[0][2:]
	return num, bagtype
}

/* Parse a rule to useful format */
func parseRule(rule string) (string, map[string]int) {
	myColor := strings.Split(rule, " bags contain ")[0]

	parsedContents := make(map[string]int)
	contents := strings.Split(strings.Split(rule, " bags contain ")[1], ", ")
	for _, content := range contents {
		num, bagtype := parseContent(content)
		parsedContents[bagtype] = num
	}
	return myColor, parsedContents
}

/* Parse entire input */
func parseRules(rules []string) map[string]map[string]int {

	parsedRules := make(map[string]map[string]int)
	for _, rule := range rules {
		bagcolor, contents := parseRule(rule)
		parsedRules[bagcolor] = contents
	}
	return parsedRules
}

/* Find out if a given color can contain at least one shiny gold bag */
func canContainShinyGold(name string, rulebook map[string]map[string]int) bool {

	for content := range rulebook[name] {
		if content == "shiny gold" {
			return true
		} else {
			// Recursively check if content can have a shiny gold bag inside
			if canContainShinyGold(content, rulebook) {
				return true
			}
		}
	}
	// No path to shiny gold was found from here. Return false
	return false

}

/* Determine number of bags required inside a specific bag */
func numInside(name string, rulebook map[string]map[string]int) int {

	count := 0
	for content, number := range rulebook[name] {
		// First add number of bags directly inside.
		count += number
		// Recursively count number in bags inside those.
		count += numInside(content, rulebook) * number
	}
	return count
}

func main() {
	rules := readFile("input")
	rulebook := parseRules(rules)

	numCanContain := 0
	for bagcolor := range rulebook {
		if canContainShinyGold(bagcolor, rulebook) {
			numCanContain++
		}
	}
	fmt.Println("Part 1: Number of bags that eventually can contain =", numCanContain)

	fmt.Println("Part 2: Number of bags inside shiny gold =", numInside("shiny gold", rulebook))
}

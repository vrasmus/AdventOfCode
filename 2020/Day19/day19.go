package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
)

/* Read the input and split in the two distinct parts. */
func readFile(input string) (string, []string) {
	content, err := ioutil.ReadFile(input)
	if err != nil {
		panic(err)
	}

	parts := strings.Split(string(content), "\n\n")

	messages := strings.Split(parts[1], "\n")
	messages = messages[:len(messages)-1]
	return parts[0], messages
}

/* Sort the rules by inserting into a slice. */
func orderRules(ruleInput string) []string {
	rawRules := strings.Split(ruleInput, "\n")

	rules := make([]string, len(rawRules))
	for _, r := range rawRules {
		sep := strings.Split(r, ": ")
		id, _ := strconv.Atoi(sep[0])
		rules[id] = sep[1]
	}
	return rules
}

/* Generate a regexp corresponding to a certain rule. */
func evaluateRule(id int, rules *[]string) string {
	if (*rules)[id] == "\"a\"" {
		return `a`
	}
	if (*rules)[id] == "\"b\"" {
		return `b`
	}

	rule := ``
	parts := strings.Split((*rules)[id], " | ")
	for _, part := range parts {
		partString := `(`
		fields := strings.Fields(part)
		for _, field := range fields {
			subId, _ := strconv.Atoi(field)
			partString += `(` + evaluateRule(subId, rules) + `)`
		}
		rule += partString + `)|`
	}
	return rule[:len(rule)-1]
}

/* Count number of msgs matching rule 0 */
func matchingRuleZero(rules []string, msgs []string) int {
	re := evaluateRule(0, &rules)
	count := 0
	for _, msg := range msgs {
		matched, _ := regexp.MatchString(`^`+re+`$`, msg)
		if matched {
			count++
		}
	}
	return count
}

func main() {
	ruleInput, msgs := readFile("input")
	rules := orderRules(ruleInput)

	/* Part 1 */
	fmt.Println("Part 1 valid matches to rule 0:", matchingRuleZero(rules, msgs))

	/* Part 2 -- we basically just update the rules for 8 and 11
	with a number of "loops", since they include themselves.
	Guessing that 10 is enough. */
	for i := 1; i < 10; i++ {
		rules[8] += " |"
		rules[11] += " |"
		for j := 0; j < i+1; j++ {
			rules[8] += " 42"
			rules[11] += " 42"
		}
		for j := 0; j < i+1; j++ {
			rules[11] += " 31"
		}
	}
	count := matchingRuleZero(rules, msgs)
	fmt.Println("Part2 valid matches to rule 0:", count)
}

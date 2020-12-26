package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strings"
)

/* Read the file. */
func readFile(name string) []string {
	content, err := ioutil.ReadFile(name)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]
	return lines
}

/* Parse a particular input line */
func parseFood(line string) ([]string, []string) {
	split := strings.Split(line, " (contains ")

	ingredients := strings.Fields(split[0])
	allergens := strings.Split(split[1][:len(split[1])-1], ", ")

	return ingredients, allergens
}

/* Ask if a given slice contains a particular element */
func contains(list []string, x string) bool {
	for _, v := range list {
		if v == x {
			return true
		}
	}
	return false
}

/* Append a new element to a slice if it is not already there. */
func appendNew(list []string, from []string) []string {
	for _, str := range from {
		if !contains(list, str) {
			list = append(list, str)
		}
	}
	return list
}

/* Delete an value from a slice, if it exists */
func deleteIfExists(list []string, x string) []string {
	for i, elem := range list {
		if elem == x {
			return append(list[:i], list[i+1:]...)
		}
	}
	return list
}

/* Eliminate a particular string in all the map's values */
func eliminateValueString(from *map[string][]string, strval string) {
	for key, value := range *from {
		(*from)[key] = deleteIfExists(value, strval)
	}
}

/* Parse all of the input data */
func parseLines(inputLines []string) ([]food, map[string][]string, map[string][]string) {
	foods := make([]food, len(inputLines))
	algmap := make(map[string][]string)
	ingmap := make(map[string][]string)
	for i, line := range inputLines {
		ingredients, allergens := parseFood(line)
		foods[i] = food{ingredients, allergens}
		for _, ing := range ingredients {
			if old, ok := ingmap[ing]; ok {
				ingmap[ing] = appendNew(old, allergens)
			} else {
				ingmap[ing] = make([]string, 0)
				ingmap[ing] = appendNew(ingmap[ing], allergens)
			}
		}
		for _, alg := range allergens {
			if old, ok := algmap[alg]; ok {
				algmap[alg] = appendNew(old, ingredients)
			} else {
				algmap[alg] = make([]string, 0)
				algmap[alg] = appendNew(algmap[alg], ingredients)
			}
		}
	}
	return foods, algmap, ingmap
}

// Each particular food has a list of ingredients and allergens
type food struct {
	ingredients []string
	allergens   []string
}

func main() {
	lines := readFile("input")
	foods, algmap, ingmap := parseLines(lines)

	// Determine which elements that are NOT dangerous at all.
	count := 0
	for ing, possibleAlgs := range ingmap {
		possiblyDangerous := false
		for _, alg := range possibleAlgs {
			ingInAllFoodsWithAlg := true
			for _, food := range foods {
				if contains(food.allergens, alg) {
					if !contains(food.ingredients, ing) {
						ingInAllFoodsWithAlg = false
					}
				}
			}
			if ingInAllFoodsWithAlg {
				possiblyDangerous = true
			}
		}

		if !possiblyDangerous {
			for _, food := range foods {
				if contains(food.ingredients, ing) {
					count++
				}
			}
			eliminateValueString(&algmap, ing)
		}
	}
	fmt.Println("Final count:", count)

	// First eliminate all ingredients not present in a food containing a specific allergen
	matched := make(map[string]string, 0)
	for alg, ingredients := range algmap {
		for _, food := range foods {
			if contains(food.allergens, alg) {
				for _, ing := range ingredients {
					if !contains(food.ingredients, ing) {
						algmap[alg] = deleteIfExists(algmap[alg], ing)
					}
				}
				if len(algmap[alg]) == 1 {
					matched[alg] = algmap[alg][0]
				}
			}
		}
	}

	/*
		Eliminate elements as they are identified.
		Could specify more sophisticated stopping condition, but will just run some iterations.
	*/
	for i := 0; i < 5; i++ {
		for _, matchedIng := range matched {
			eliminateValueString(&algmap, matchedIng)
			for alg, ingredients := range algmap {
				if len(ingredients) == 1 {
					matched[alg] = ingredients[0]
				}
			}
		}
	}

	// Now we need to sort keys and print requested order.
	keys := make([]string, len(matched))
	i := 0
	for k := range matched {
		keys[i] = k
		i++
	}
	sort.Strings(keys)
	fmt.Println("Part 2 answer:")
	for _, key := range keys {
		fmt.Print(matched[key], ",")
	}
	fmt.Println("")
}

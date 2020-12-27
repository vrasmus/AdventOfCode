package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
)

/* Read file and return slice of maps */
func readFile(fname string) []map[string]string {

	// Read the entire file as a string
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	// Passports are separated by double newline.
	passportsData := strings.Split(string(b), "\n\n")

	// Allocate output slice.
	passports := make([]map[string]string, len(passportsData))

	for i, pp := range passportsData {
		// Split each passport by whitespace characters
		fields := strings.Fields(pp)

		// Each passport becomes a map with strings as both keys and values.
		ppMap := make(map[string]string)

		for _, field := range fields {
			fieldSplit := strings.Split(field, ":")
			ppMap[fieldSplit[0]] = fieldSplit[1]
		}
		passports[i] = ppMap
	}
	return passports
}

/* Check if a specific passport is valid. */
func hasEntries(passport map[string]string) bool {
	requiredEntries := [7]string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

	for _, required := range requiredEntries {
		_, success := passport[required]
		if success == false {
			return false
		}
	}
	return true
}

/* Count the number of valid passports */
func countHasEntries(passports []map[string]string) int {
	count := 0
	for _, pp := range passports {
		if hasEntries(pp) {
			count++
		}
	}
	return count
}

/* Check if birth year is valid */
func validByr(byr string) bool {
	year, _ := strconv.Atoi(byr)
	if 1920 <= year && year <= 2002 {
		return true
	}
	return false
}

/* Check if issue year is valid */
func validIyr(iyr string) bool {
	year, _ := strconv.Atoi(iyr)
	if 2010 <= year && year <= 2020 {
		return true
	}
	return false
}

/* Check if expiration year is valid */
func validEyr(eyr string) bool {
	year, _ := strconv.Atoi(eyr)
	if 2020 <= year && year <= 2030 {
		return true
	}
	return false
}

/* Check if height is valid */
func validHgt(hgt string) bool {

	num, _ := strconv.Atoi(hgt[:len(hgt)-2])
	unit := hgt[len(hgt)-2:]

	if unit == "cm" {
		if 150 <= num && num <= 193 {
			return true
		}
	} else if unit == "in" {
		if 59 <= num && num <= 76 {
			return true
		}
	}
	return false
}

/* Check if hair color is valid */
func validHcl(hcl string) bool {
	// Use regex to check if correctly formatted
	matches, _ := regexp.MatchString(`#[a-f0-9]{6}`, hcl)
	return matches
}

/* Check if eye color is valid */
func validEcl(ecl string) bool {
	// Use regex to check if correct
	matches, _ := regexp.MatchString(`(amb|blu|brn|gry|grn|hzl|oth)`, ecl)
	return matches
}

/* Check if passport id is valid */
func validPid(pid string) bool {
	if len(pid) != 9 {
		return false
	}
	// Use regex to check if correct
	matches, _ := regexp.MatchString(`[0-9]{9}`, pid)
	return matches
}

/* We need to check that the entries are actually valid */
func checkValid(passport map[string]string) bool {
	if !hasEntries(passport) {
		return false
	}

	if validByr(passport["byr"]) &&
		validIyr(passport["iyr"]) &&
		validEyr(passport["eyr"]) &&
		validHgt(passport["hgt"]) &&
		validHcl(passport["hcl"]) &&
		validEcl(passport["ecl"]) &&
		validPid(passport["pid"]) {
		return true
	} else {
		return false
	}
}

/* We count the number of actually valid passports */
func countValid(passports []map[string]string) int {
	count := 0
	for _, pp := range passports {
		if checkValid(pp) {
			count++
		}
	}
	return count
}

func main() {

	passports := readFile("input")

	fmt.Println("Number of passports with the required entries:", countHasEntries(passports))
	fmt.Println("Number of valid passports:", countValid(passports))
}

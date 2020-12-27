package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type memop struct {
	addr uint64
	val  uint64
}

func readFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	program := strings.Split(string(content), "\n")
	program = program[:len(program)-1]
	return program
}

/* Apply a particular bit mask to the input value */
func applyMask(mask string, value uint64) uint64 {
	// First we make the binary masks
	var zeroMask uint64 = 0
	var onesMask uint64 = 0
	for i, mval := range mask {
		if mval == '0' {
			zeroMask |= (1 << (35 - i))
		} else if mval == '1' {
			onesMask |= (1 << (35 - i))
		}
	}
	zeroMask = ^zeroMask
	// Then we change the value.
	value = value & zeroMask
	value = value | onesMask
	return value
}

/* Transform a line to a memory operation. */
func parseMemop(line string) memop {
	tmp := strings.Split(line, "[")[1]
	location, _ := strconv.Atoi(strings.Split(tmp, "]")[0])

	value, _ := strconv.Atoi(strings.Split(line, " = ")[1])
	return memop{uint64(location), uint64(value)}
}

/* Count memory sum */
func countSum(memory map[uint64]uint64) uint64 {
	var sum uint64 = 0
	for _, val := range memory {
		sum += val
	}
	return sum
}

/* For part 1, main program */
func part1(program []string) {
	// We keep memory in a map to handle overwrites
	memory := make(map[uint64]uint64, 0)

	mask := ""
	for _, line := range program {
		if line[:7] == "mask = " {
			mask = line[7:]
		} else {
			// The line is a memory operation.
			op := parseMemop(line)
			masked := applyMask(mask, op.val)
			memory[op.addr] = masked
		}
	}
	memorySum := countSum(memory)
	fmt.Println("Memory sum in part 1:", memorySum)
}

/* Recursively generate all valid addresses */
func maskedAddresses(mask string, baseaddr uint64) []uint64 {
	addresses := make([]uint64, 0)
	for i, mval := range mask {
		if mval == 'X' {
			tmp_mask0 := mask[:i] + "0" + mask[i+1:]
			tmp_mask1 := mask[:i] + "1" + mask[i+1:]
			addresses = append(addresses, maskedAddresses(tmp_mask0, baseaddr)...)
			addresses = append(addresses, maskedAddresses(tmp_mask1, baseaddr)...)
			return addresses
		}
	}

	addresses = append(addresses, applyMask(mask, baseaddr))
	return addresses
}

/* Mark unchanging in mask */
func markUnchanging(mask string) string {
	for i, mval := range mask {
		if mval == '0' {
			mask = mask[:i] + "U" + mask[i+1:]
		}
	}
	return mask
}

/* Run part 2 main program*/
func part2(program []string) {
	// We keep memory in a map to handle overwrites
	memory := make(map[uint64]uint64, 0)

	mask := ""
	for _, line := range program {
		if line[:7] == "mask = " {
			mask = line[7:]
		} else {
			// The line is a memory operation.
			op := parseMemop(line)
			mask = markUnchanging(mask)
			for _, addr := range maskedAddresses(mask, op.addr) {
				memory[addr] = op.val
			}
		}
	}
	memorySum := countSum(memory)
	fmt.Println("Memory sum in part 2:", memorySum)
}

func main() {
	program := readFile("input")
	part1(program)
	part2(program)
}

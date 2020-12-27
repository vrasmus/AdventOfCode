package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Let's keep the information together */
type instruction struct {
	op    string
	value int
	// We store directly here if it has been executed before.
	executed bool
}

/* Read the content of the file. */
func readFile(filename string) []instruction {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]

	program := make([]instruction, 0, len(lines))
	for _, line := range lines {
		program = append(program, parseLine(line))
	}

	return program
}

/* Convert an input string to an instruction */
func parseLine(line string) instruction {
	op := line[:3]
	value, _ := strconv.Atoi(line[4:])
	return instruction{op: op, value: value}
}

/* Execute until repeating an instruction */
func execute(program []instruction) bool {
	instructionPtr := 0
	accumulator := 0

	nextOp := &program[0]
	for {
		// Check if already executed this
		if nextOp.executed {
			fmt.Println("Found infinite loop. Accumulator was", accumulator)
			return false
		} else {
			nextOp.executed = true
		}

		// Handle this operation
		if nextOp.op == "acc" {
			accumulator += nextOp.value
			instructionPtr++
		} else if nextOp.op == "jmp" {
			instructionPtr += nextOp.value
		} else {
			instructionPtr++
		}

		// For part two, check if we conclude correctly with this program.
		if instructionPtr == len(program) {
			fmt.Println("Termination reached correctly. Accumulator was", accumulator)
			return true
		}
		nextOp = &program[instructionPtr]
	}
}

/* Brute-force solution to modify the program until it terminates correctly. */
func fixProgram(program []instruction) {
	/* First clear execution state */
	for i := range program {
		program[i].executed = false
	}

	for toModify := range program {
		// Make a copy of program to modify
		modified := append(make([]instruction, 0, len(program)), program...)

		if modified[toModify].op == "jmp" {
			modified[toModify].op = "nop"
		} else if modified[toModify].op == "nop" {
			modified[toModify].op = "jmp"
		}
		if execute(modified) {
			break
		}
	}
}

func main() {
	program := readFile("input")
	execute(program)
	fixProgram(program)
}

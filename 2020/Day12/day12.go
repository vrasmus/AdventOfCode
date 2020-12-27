package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Keep the ship's status together */
type location struct {
	north  int
	east   int
	facing int // Degrees (0 = east)
}

/* Define an instruction pair */
type instruction struct {
	action string
	value  int
}

/* Read the input file */
func readFile(input string) []instruction {
	content, err := ioutil.ReadFile(input)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")
	lines = lines[:len(lines)-1]

	instructions := make([]instruction, len(lines))
	for i, line := range lines {
		instructions[i].action = line[:1]
		instructions[i].value, _ = strconv.Atoi(line[1:])
	}
	return instructions
}

/* Turn the ship a number of degrees */
func turn(ship *location, degrees int) {
	newDir := (360 + ((*ship).facing + degrees)) % 360
	(*ship).facing = newDir
}

func forward(ship *location, steps int) {
	newInstr := instruction{"", steps}
	if (*ship).facing == 0 { // Facing east
		newInstr.action = "E"
	} else if (*ship).facing == 90 {
		newInstr.action = "S"
	} else if (*ship).facing == 180 {
		newInstr.action = "W"
	} else if (*ship).facing == 270 {
		newInstr.action = "N"
	}
	move(ship, newInstr)
}

func move(ship *location, instr instruction) {
	if instr.action == "E" {
		(*ship).east += instr.value
		return
	}
	if instr.action == "W" {
		(*ship).east -= instr.value
		return
	}
	if instr.action == "N" {
		(*ship).north += instr.value
		return
	}
	if instr.action == "S" {
		(*ship).north -= instr.value
		return
	}
}

/* Move the ship according to given instruction */
func executeInstruction(ship *location, instr instruction) {
	if instr.action == "R" {
		turn(ship, instr.value)
		return
	} else if instr.action == "L" {
		turn(ship, -instr.value)
		return
	} else if instr.action == "F" {
		forward(ship, instr.value)
		return
	} else {
		move(ship, instr)
		return
	}
}

/* Find Manhattan distance of the ship from origin */
func manhattanDist(ship location) int {
	dist := 0

	if ship.north < 0 {
		dist -= ship.north
	} else {
		dist += ship.north
	}

	if ship.east < 0 {
		dist -= ship.east
	} else {
		dist += ship.east
	}

	return dist
}

/* Execute part 1 */
func part1(instructions []instruction) {
	ship := location{}
	for _, instr := range instructions {
		executeInstruction(&ship, instr)
	}
	fmt.Println("Final configuration:", ship, "dist:", manhattanDist(ship))
}

/*
For part 2, things are a bit different.
Still, we don't need to write much more code, since we can reuse most..
*/

/* Rotate the waypoint around the ship */
func (w *location) rotateClockwise(degrees int) {
	if degrees == 90 {
		tmp := w.north
		w.north = -w.east
		w.east = tmp
		return
	}
	if degrees == 180 {
		w.north = -w.north
		w.east = -w.east
		return
	}
	if degrees == 270 {
		tmp := w.east
		w.east = -w.north
		w.north = tmp
	}
}

/* Execute an instruction according to specification in part 2 */
func executeInstructionPart2(ship *location, w *location, instr instruction) {
	if instr.action == "R" {
		w.rotateClockwise(instr.value)
		return
	} else if instr.action == "L" {
		w.rotateClockwise(360 - instr.value)
		return
	} else if instr.action == "F" {
		eastInstr := instruction{"E", instr.value * w.east}
		northInstr := instruction{"N", instr.value * w.north}
		move(ship, eastInstr)
		move(ship, northInstr)
		return
	} else {
		move(w, instr)
		return
	}
}

/* Execute part 2 */
func part2(instructions []instruction) {
	ship := location{}
	waypoint := location{1, 10, 0}
	for _, instr := range instructions {
		executeInstructionPart2(&ship, &waypoint, instr)
	}
	fmt.Println("Final configuration:", ship, "dist:", manhattanDist(ship))
}

func main() {
	instructions := readFile("input")
	part1(instructions)
	part2(instructions)

}

package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

/* Read all the expressions. */
func readFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")
	return lines[:len(lines)-1]
}

/* Add or multiply to integers in string format */
func operate(x, y, operator string) string {
	xi, _ := strconv.Atoi(x)
	yi, _ := strconv.Atoi(y)
	if operator == "+" {
		return strconv.Itoa(xi + yi)
	} else if operator == "*" {
		return strconv.Itoa(xi * yi)
	}
	panic("Unknown operator")
}

/* Solve an expression with no parentheses & equal precedences */
func evalNoParentheses(strippedExpr string) string {
	for i, char := range strippedExpr {
		if char == '+' || char == '*' {
			nextOp := i + 1
			for ; nextOp < len(strippedExpr); nextOp++ {
				if strippedExpr[nextOp] == '+' || strippedExpr[nextOp] == '*' {
					break
				}
			}
			sol := operate(strippedExpr[:i], strippedExpr[i+1:nextOp], string(char))
			return evalNoParentheses(sol + strippedExpr[nextOp:])
		}
	}
	return strippedExpr
}

/* Solve an expression with precedence for additions:
recurse until done with additions, then evaluate multiplications.*/
func evalNoParenthesesAdds(strippedExpr string) string {

	priorOp := 0
	for i, char := range strippedExpr {
		// We isolate each addition and handle it individually, updating the expression each time.
		if char == '*' {
			priorOp = i
		} else if char == '+' {
			nextOp := i + 1
			for ; nextOp < len(strippedExpr); nextOp++ {
				if strippedExpr[nextOp] == '+' || strippedExpr[nextOp] == '*' {
					break
				}
			}
			if priorOp == 0 {
				sol := operate(strippedExpr[:i], strippedExpr[i+1:nextOp], "+")
				return evalNoParenthesesAdds(sol + strippedExpr[nextOp:])
			} else {
				sol := operate(strippedExpr[priorOp+1:i], strippedExpr[i+1:nextOp], "+")
				return evalNoParenthesesAdds(strippedExpr[:priorOp+1] + sol + strippedExpr[nextOp:])
			}
		}
	}
	return evalNoParenthesesMults(strippedExpr)
}

/* Eval mults after all additions are gone. Recurse until all gone */
func evalNoParenthesesMults(strippedExpr string) string {
	for i, char := range strippedExpr {
		if char == '*' {
			nextOp := i + 1
			for ; nextOp < len(strippedExpr); nextOp++ {
				if strippedExpr[nextOp] == '*' {
					break
				}
			}
			sol := operate(strippedExpr[:i], strippedExpr[i+1:nextOp], "*")
			return evalNoParenthesesMults(sol + strippedExpr[nextOp:])
		}
	}
	return strippedExpr
}

/* Evaluate an expression with parentheses by recursing and solving subexpressions first. */
func evalParentheses(strippedExpr string) string {
	openedAt := 0
	open := 0

	for i, char := range strippedExpr {
		if char == '(' {
			open++
			if open == 1 {
				openedAt = i
			}
		} else if char == ')' {
			open--
			if open == 0 {
				sol := evalParentheses(strippedExpr[openedAt+1 : i])
				return evalParentheses(strippedExpr[:openedAt] + sol + strippedExpr[i+1:])
			}
		}
	}
	return evalNoParentheses(strippedExpr)
}
func evalParenthesesPart2(strippedExpr string) string {
	openedAt := 0
	open := 0

	for i, char := range strippedExpr {
		if char == '(' {
			open++
			if open == 1 {
				openedAt = i
			}
		} else if char == ')' {
			open--
			if open == 0 {
				sol := evalParenthesesPart2(strippedExpr[openedAt+1 : i])
				return evalParenthesesPart2(strippedExpr[:openedAt] + sol + strippedExpr[i+1:])
			}
		}
	}
	return evalNoParenthesesAdds(strippedExpr)
}

/* Evaluate a given expression string according to new math rules */
func eval(expression string) int {

	// Strip whitespace from the string to avoid dealing with it.
	stripped := strings.Join(strings.Fields(expression), "")
	res, _ := strconv.Atoi(evalParentheses(stripped))

	return res
}

/* For part two, the operators have different precence levels: Evaluate addition first. */
func evalPart2(expression string) int {
	// Strip whitespace from the string to avoid dealing with it.
	stripped := strings.Join(strings.Fields(expression), "")
	res, _ := strconv.Atoi(evalParenthesesPart2(stripped))

	return res
}

func main() {
	expressions := readFile("input")

	sum1 := 0
	sum2 := 0
	for _, expr := range expressions {
		sum1 += eval(expr)
		sum2 += evalPart2(expr)
	}
	fmt.Println("Part 1 sum of all expressions' solutions:", sum1)
	fmt.Println("Part 2 sum of all expressions' solutions:", sum2)

}

package main

import "fmt"

func transform(num uint64, subjectNumber uint64) uint64 {
	num = num * subjectNumber
	return num % 20201227
}

func findLoopSize(target uint64, subjectNumber uint64) int {
	var guess uint64 = 1
	for i := 1; guess != target; i++ {
		guess = transform(guess, subjectNumber)
		if guess == target {
			return i
		}
	}
	panic("Didn't succeed")
}

func main() {
	var pk1 uint64 = 11349501
	var pk2 uint64 = 5107328

	// Find number of loops required
	loops1 := findLoopSize(pk1, 7)
	loops2 := findLoopSize(pk2, 7)
	fmt.Println("Loops for pk 1:", loops1)
	fmt.Println("Loops for pk 2:", loops2)

	// Transform both keys to confirm that we get the same result
	var sharedKeyA uint64 = 1
	for i := 0; i < loops2; i++ {
		sharedKeyA = transform(sharedKeyA, pk1)
	}
	var sharedKeyB uint64 = 1
	for i := 0; i < loops1; i++ {
		sharedKeyB = transform(sharedKeyB, pk2)
	}
	fmt.Println("They are trying to established shared key:", sharedKeyA, sharedKeyB)
}

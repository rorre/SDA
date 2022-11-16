package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Node struct {
	value    string
	previous *Node
	next     *Node
}

type DoublyLinkedList struct {
	head    *Node
	tail    *Node
	pointer *Node
	size    int
}

func CreateList() DoublyLinkedList {
	headNode := Node{value: "_HEAD"}
	tailNode := Node{value: "_TAIL"}

	headNode.next = &tailNode
	tailNode.previous = &headNode

	return DoublyLinkedList{
		head:    &headNode,
		tail:    &tailNode,
		pointer: &headNode,
		size:    0,
	}
}

func (dList *DoublyLinkedList) String() string {
	var b strings.Builder

	pointer := dList.head
	for pointer != nil {
		if pointer != dList.head {
			b.WriteString("<->")
		}

		b.WriteString(fmt.Sprintf("['%s'", pointer.value))
		if pointer == dList.pointer {
			b.WriteString(" (P)")
		}
		b.WriteString("]")

		pointer = pointer.next
	}

	return b.String()
}

func (dList *DoublyLinkedList) InsertAfter(pointer *Node, value string) error {
	if dList.tail == pointer {
		return errors.New("Insertion out of bound error")
	}

	var newNode = Node{value, pointer, pointer.next}
	if pointer.next != nil {
		pointer.next.previous = &newNode
	}

	pointer.next = &newNode
	dList.size++
	return nil
}

func (dList *DoublyLinkedList) InsertBefore(pointer *Node, value string) error {
	if dList.head == pointer {
		return errors.New("Insertion out of bound error")
	}

	var newNode = Node{value, pointer.previous, pointer}

	if pointer.previous != nil {
		pointer.previous.next = &newNode
	}

	pointer.previous = &newNode
	dList.size++
	return nil
}

func (dList *DoublyLinkedList) RemoveNode(pointer *Node) error {
	if pointer == dList.head || pointer == dList.tail {
		return errors.New("Unable to remove head or tail")
	}

	if pointer.previous != nil {
		pointer.previous.next = pointer.next
	}

	if pointer.next != nil {
		pointer.next.previous = pointer.previous
	}

	dList.size--
	return nil
}

func (dList *DoublyLinkedList) RemoveHead() error {
	var toRemove = dList.head.next
	err := dList.RemoveNode(toRemove)

	if err != nil {
		return err
	}

	if dList.pointer == toRemove {
		dList.pointer = dList.head
	}
	return nil
}

func (dList *DoublyLinkedList) RemoveTail() error {
	var toRemove = dList.tail.previous
	err := dList.RemoveNode(toRemove)

	if err != nil {
		return err
	}

	if dList.pointer == toRemove {
		dList.pointer = dList.tail
	}

	return nil
}

func (dList *DoublyLinkedList) InsertPointer(arrow string, value string) error {
	if arrow == "NEXT" {
		return dList.InsertAfter(dList.pointer, value)
	} else {
		return dList.InsertBefore(dList.pointer, value)
	}
}

func (dList *DoublyLinkedList) RemovePointer(arrow string) error {
	var pointerRemove *Node
	if arrow == "NEXT" {
		if dList.pointer == dList.tail {
			return errors.New("Tail do not have next node")
		}

		pointerRemove = dList.pointer.next
	} else {
		if dList.pointer == dList.head {
			return errors.New("Head do not have previous node")
		}

		pointerRemove = dList.pointer.previous
	}

	return dList.RemoveNode(pointerRemove)
}

func (dList *DoublyLinkedList) MovePointer(arrow string, steps int) error {
	for i := 0; i < steps; i++ {
		var nextPointer *Node
		if arrow == "NEXT" {
			nextPointer = dList.pointer.next
		} else {
			nextPointer = dList.pointer.previous
		}

		if nextPointer == nil {
			return errors.New("Steps out of bound error")
		}
		dList.pointer = nextPointer
	}
	return nil
}

func (dList *DoublyLinkedList) IsEmpty() bool {
	return dList.size == 0
}

func (dList *DoublyLinkedList) GetSize() int {
	return dList.size
}

func ValidateArgs(cmd string, args []string) bool {
	argsLen := len(args)

	switch cmd {
	case "INSERT_HEAD":
		return argsLen == 1
	case "REMOVE_HEAD":
		return argsLen == 0
	case "INSERT_TAIL":
		return argsLen == 1
	case "REMOVE_TAIL":
		return argsLen == 0
	case "INSERT_NODE_USING_POINTER":
		return argsLen == 2 && (args[0] == "NEXT" || args[0] == "PREV")
	case "REMOVE_NODE_USING_POINTER":
		return argsLen == 1 && (args[0] == "NEXT" || args[0] == "PREV")
	case "MOVE_POINTER":
		if argsLen != 2 {
			return false
		}
		if args[0] != "NEXT" && args[0] != "PREV" {
			return false
		}

		value, err := strconv.Atoi(args[1])
		if err != nil {
			return false
		}
		return value > 0
	case "IS_EMPTY":
		return argsLen == 0
	case "SIZE":
		return argsLen == 0
	}
	return false
}

func RunCommand(dList *DoublyLinkedList, cmd string, args []string) {
	fmt.Println("    Before: ")
	fmt.Printf("    %s\n", dList.String())
	fmt.Println()

	if !(ValidateArgs(cmd, args)) {
		fmt.Println("    Syntax error")
		return
	}

	var err error
	switch cmd {
	case "INSERT_HEAD":
		err = dList.InsertAfter(dList.head, args[0])
	case "REMOVE_HEAD":
		err = dList.RemoveHead()
	case "INSERT_TAIL":
		err = dList.InsertBefore(dList.tail, args[0])
	case "REMOVE_TAIL":
		err = dList.RemoveTail()
	case "INSERT_NODE_USING_POINTER":
		err = dList.InsertPointer(args[0], args[1])
	case "REMOVE_NODE_USING_POINTER":
		err = dList.RemovePointer(args[0])
	case "MOVE_POINTER":
		val, _ := strconv.Atoi(args[1])
		err = dList.MovePointer(args[0], val)
	}

	if err != nil {
		fmt.Printf("    %s\n", err)
	} else {
		fmt.Println("    After: ")
		fmt.Printf("    %s\n", dList.String())
	}
}

func main() {
	dList := CreateList()

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		currentLine := scanner.Text()
		if currentLine == "EXIT" {
			break
		}

		cmdArgs := strings.Split(currentLine, " ")
		cmd := cmdArgs[0]
		args := cmdArgs[1:]

		fmt.Println(currentLine)
		if cmd == "SIZE" {
			fmt.Printf("    %d\n", dList.size)
		} else if cmd == "IS_EMPTY" {
			if dList.IsEmpty() {
				fmt.Println("    TRUE")
			} else {
				fmt.Println("    FALSE")
			}
		} else {
			RunCommand(&dList, cmd, args)
		}

		fmt.Println()
	}
}

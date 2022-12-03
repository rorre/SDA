package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strings"
)

type StringHeap []string

func (h *StringHeap) Append(elem string) {
	*h = append(*h, elem)
	h.upheap(len(*h) - 1)
}

func (h StringHeap) swap(i int, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h StringHeap) upheap(j int) {
	parentIdx := (j - 1) >> 1
	if j > 0 && h[j] < h[parentIdx] {
		h.swap(j, parentIdx)
		h.upheap(parentIdx)
	}
}

func (h StringHeap) downheap(j int) {
	leftIdx := 2*j + 1
	if leftIdx >= len(h) {
		return
	}

	smallestChildIdx := leftIdx

	rightIdx := 2*j + 2
	if rightIdx < len(h) && h[rightIdx] < h[leftIdx] {
		smallestChildIdx = rightIdx
	}

	if h[smallestChildIdx] < h[j] {
		h.swap(j, smallestChildIdx)
		h.downheap(smallestChildIdx)
	}
}

func (h *StringHeap) Pop() (string, error) {
	arrLen := len(*h)
	if arrLen == 0 {
		return "", errors.New("Attempting to pop an empty heap")
	}

	h.swap(0, arrLen-1)
	item := (*h)[arrLen-1]
	*h = (*h)[:arrLen-1]
	h.downheap(0)
	return item, nil
}

var inside map[string][]string = make(map[string][]string)
var outside map[string][]string = make(map[string][]string)
var vertexes []string = make([]string, 0)

func AddVertex(v string) {
	inside[v] = make([]string, 0)
	outside[v] = make([]string, 0)
	vertexes = append(vertexes, v)
}

func AddEdge(source string, target string) {
	outside[source] = append(outside[source], target)
	inside[target] = append(inside[target], source)
}

func RemoveElement[T comparable](l []T, item T) []T {
	for i, other := range l {
		if other == item {
			return append(l[:i], l[i+1:]...)
		}
	}
	return l
}

func RemoveEdge(source string, target string) {
	outside[source] = RemoveElement(outside[source], target)
	inside[target] = RemoveElement(inside[target], source)
}

func AddMatkul(matkul string, deps ...string) {
	if _, ok := inside[matkul]; ok {
		fmt.Printf("Matkul %s sudah ada", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := inside[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan", dep)
			return
		}
	}

	AddVertex(matkul)
	for _, dep := range deps {
		AddEdge(dep, matkul)
	}
}

func EditMatkul(matkul string, deps ...string) {
	if _, ok := inside[matkul]; !ok {
		fmt.Printf("Matkul %s tidak ditemukan", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := inside[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan", dep)
			return
		}
	}

	var prevDeps []string
	copy(prevDeps, inside[matkul])
	for _, dep := range prevDeps {
		RemoveEdge(dep, matkul)
	}

	for _, dep := range deps {
		AddEdge(dep, matkul)
	}
}

func VisitVertex(state map[string]bool, leveled *[]StringHeap, v string, level int) {
	curLeveled := *leveled
	if len(*leveled) < level {
		curLeveled = append(curLeveled, StringHeap{v})
		*leveled = curLeveled
	} else {
		curLeveled[level-1].Append(v)
	}

	state[v] = true
	for _, adjV := range outside[v] {
		if !state[adjV] {
			VisitVertex(state, leveled, adjV, level+1)
		}
	}
}

func PrintSorted() {
	state := make(map[string]bool)
	leveled := make([]StringHeap, 0)

	for _, k := range vertexes {
		state[k] = false
	}

	for _, v := range vertexes {
		if !state[v] {
			VisitVertex(state, &leveled, v, 1)
		}
	}

	sorted := make([]string, 0)
	for _, levelArr := range leveled {
		for range levelArr {
			matkul, _ := levelArr.Pop()
			sorted = append(sorted, matkul)
		}
	}

	fmt.Println(strings.Join(sorted, ", "))
}

func PrintVars() {
	for k, v := range inside {
		fmt.Println("[IN] ", k, "value is", v)
	}
	for k, v := range outside {
		fmt.Println("[OU] ", k, "value is", v)
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		currentLine := scanner.Text()
		if currentLine == "EXIT" {
			break
		}

		cmdArgs := strings.Split(currentLine, " ")
		cmd := cmdArgs[0]
		args := cmdArgs[1:]
		switch cmd {
		case "ADD_MATKUL":
			AddMatkul(args[0], args[1:]...)
		case "EDIT_MATKUL":
			EditMatkul(args[0], args[1:]...)
		case "CETAK_URUTAN":
			PrintSorted()
		case "PRINT":
			PrintVars()
		default:
			fmt.Println("Perintah tidak ditemukan")
		}
	}
}

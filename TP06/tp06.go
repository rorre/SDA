package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strings"
)

type Vertex struct {
	name  string
	level int
	state bool
}

type VertexHeap []*Vertex

func (h *VertexHeap) Append(elem *Vertex) {
	*h = append(*h, elem)
	h.upheap(len(*h) - 1)
}

func (h VertexHeap) swap(i int, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h VertexHeap) upheap(j int) {
	parentIdx := (j - 1) >> 1
	if j > 0 && h[j].name < h[parentIdx].name {
		h.swap(j, parentIdx)
		h.upheap(parentIdx)
	}
}

func (h VertexHeap) downheap(j int) {
	leftIdx := 2*j + 1
	if leftIdx >= len(h) {
		return
	}

	smallestChildIdx := leftIdx

	rightIdx := 2*j + 2
	if rightIdx < len(h) && h[rightIdx].name < h[leftIdx].name {
		smallestChildIdx = rightIdx
	}

	if h[smallestChildIdx].name < h[j].name {
		h.swap(j, smallestChildIdx)
		h.downheap(smallestChildIdx)
	}
}

func (h *VertexHeap) Pop() (*Vertex, error) {
	arrLen := len(*h)
	if arrLen == 0 {
		return &Vertex{}, errors.New("Attempting to pop an empty heap")
	}

	h.swap(0, arrLen-1)
	item := (*h)[arrLen-1]
	*h = (*h)[:arrLen-1]
	h.downheap(0)
	return item, nil
}

var inside map[*Vertex][]*Vertex = make(map[*Vertex][]*Vertex)
var outside map[*Vertex][]*Vertex = make(map[*Vertex][]*Vertex)
var vertexesMap map[string]*Vertex = make(map[string]*Vertex)
var vertexes []*Vertex = make([]*Vertex, 0)

func AddVertex(vName string) *Vertex {
	v := Vertex{name: vName}
	inside[&v] = make([]*Vertex, 0)
	outside[&v] = make([]*Vertex, 0)

	vertexes = append(vertexes, &v)
	vertexesMap[vName] = &v
	return &v
}

func AddEdge(source *Vertex, target *Vertex) {
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

func RemoveEdge(source *Vertex, target *Vertex) {
	outside[source] = RemoveElement(outside[source], target)
	inside[target] = RemoveElement(inside[target], source)
}

func AddMatkul(matkul string, deps ...string) {
	if _, ok := vertexesMap[matkul]; ok {
		fmt.Printf("Matkul %s sudah ada", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := vertexesMap[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan", dep)
			return
		}
	}

	matkulV := AddVertex(matkul)
	for _, dep := range deps {
		depV := vertexesMap[dep]
		AddEdge(depV, matkulV)
	}
}

func EditMatkul(matkul string, deps ...string) {
	if _, ok := vertexesMap[matkul]; !ok {
		fmt.Printf("Matkul %s tidak ditemukan", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := vertexesMap[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan", dep)
			return
		}
	}

	matkulV := vertexesMap[matkul]

	var prevDeps []*Vertex = make([]*Vertex, len(inside[matkulV]))
	copy(prevDeps, inside[matkulV])
	for _, dep := range prevDeps {
		RemoveEdge(dep, matkulV)
	}

	for _, dep := range deps {
		depV := vertexesMap[dep]
		AddEdge(depV, matkulV)
	}
}

func VisitVertex(v *Vertex, level int) {
	v.state = true
	v.level = level

	for _, adjV := range outside[v] {
		if !adjV.state || adjV.level < level+1 {
			VisitVertex(adjV, level+1)
		}
	}
}

func PrintSorted() {
	for _, k := range vertexes {
		k.state = false
		k.level = -1
	}

	for _, v := range vertexes {
		if !v.state {
			VisitVertex(v, 1)
		}
	}

	leveled := make([]VertexHeap, 0)
	for _, k := range vertexes {
		if len(leveled) < k.level {
			leveled = append(leveled, VertexHeap{k})
		} else {
			leveled[k.level-1].Append(k)
		}
	}

	sorted := make([]string, 0)
	for _, levelArr := range leveled {
		for range levelArr {
			matkul, _ := levelArr.Pop()
			sorted = append(sorted, matkul.name)
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

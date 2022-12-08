package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strings"
)

type Vertex struct {
	name    string
	level   int
	visited bool
}

func VertexCompare(u *Vertex, v *Vertex) bool {
	return u.level < v.level || (u.level == v.level && u.name < v.name)
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
	if j > 0 && VertexCompare(h[j], h[parentIdx]) {
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
	if rightIdx < len(h) && VertexCompare(h[rightIdx], h[leftIdx]) {
		smallestChildIdx = rightIdx
	}

	if VertexCompare(h[smallestChildIdx], h[j]) {
		h.swap(j, smallestChildIdx)
		h.downheap(smallestChildIdx)
	}
}

func (h *VertexHeap) Pop() (*Vertex, error) {
	arrLen := len(*h)
	if arrLen == 0 {
		return nil, errors.New("attempting to pop an empty heap")
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

func RemoveElement(l []*Vertex, item *Vertex) []*Vertex {
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
		fmt.Printf("Matkul %s sudah ada\n", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := vertexesMap[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan\n", dep)
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
		fmt.Printf("Matkul %s tidak ditemukan\n", matkul)
		return
	}

	for _, dep := range deps {
		if _, ok := vertexesMap[dep]; !ok {
			fmt.Printf("Matkul %s tidak ditemukan\n", dep)
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

func VisitVertex(v *Vertex) {
	v.visited = true

	level := 1
	for _, adjV := range inside[v] {
		if !adjV.visited {
			VisitVertex(adjV)
		}

		if adjV.level > level {
			level = adjV.level
		}
	}
	v.level = level + 1
}

func PrintSorted() {
	leveledHeap := VertexHeap{}
	for _, k := range vertexes {
		if len(inside[k]) == 0 {
			k.visited = true
			k.level = 1
		} else {
			k.visited = false
			k.level = -1
		}
	}

	for _, v := range vertexes {
		if !v.visited {
			VisitVertex(v)
		}
		leveledHeap.Append(v)
	}

	sorted := make([]string, 0)
	totalElem := len(leveledHeap)
	for i := 0; i < totalElem; i++ {
		matkul, _ := leveledHeap.Pop()
		sorted = append(sorted, matkul.name)
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
		currentLine := strings.TrimSpace(scanner.Text())
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

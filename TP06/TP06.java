import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

class Vertex {
    public String name;
    public int level;
    public boolean state;

    public Vertex(String name) {
        this.name = name;
    }
}

class Graph {
    private ArrayList<Vertex> vertexes;
    private HashMap<String, Vertex> vMap;
    private HashMap<String, ArrayList<Vertex>> inside;
    private HashMap<String, ArrayList<Vertex>> outside;

    public Graph() {
        vertexes = new ArrayList<Vertex>();
        vMap = new HashMap<String, Vertex>();
        inside = new HashMap<String, ArrayList<Vertex>>();
        outside = new HashMap<String, ArrayList<Vertex>>();
    }

    public ArrayList<Vertex> getVertexes() {
        return vertexes;
    }

    public HashMap<String, ArrayList<Vertex>> getInside() {
        return inside;
    }

    public HashMap<String, ArrayList<Vertex>> getOutside() {
        return outside;
    }

    public HashMap<String, Vertex> getvMap() {
        return vMap;
    }

    public Vertex addVertex(String name) {
        var v = new Vertex(name);
        inside.put(name, new ArrayList<Vertex>());
        outside.put(name, new ArrayList<Vertex>());
        vertexes.add(v);
        vMap.put(name, v);

        return v;
    }

    public void addEdge(Vertex source, Vertex target) {
        outside.get(source.name).add(target);
        inside.get(target.name).add(source);
    }

    public void removeEdge(Vertex source, Vertex target) {
        outside.get(source.name).remove(target);
        inside.get(target.name).remove(source);
    }
}

public class TP06 {
    private static InputReader in;
    private static PrintWriter out = new PrintWriter(System.out);
    private static Graph graph = new Graph();

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        in = new InputReader(inputStream);

        boolean running = true;
        while (running) {
            var cmdLine = in.nextLine();
            var cmds = cmdLine.split(" ");
            var cmd = cmds[0];
            var cmdArgs = Arrays.copyOfRange(cmds, 1, cmds.length);

            switch (cmd) {
                case "ADD_MATKUL":
                    addMatkul(cmdArgs);
                    break;

                case "EDIT_MATKUL":
                    editMatkul(cmdArgs);
                    break;

                case "CETAK_URUTAN":
                    printOrdered();
                    break;

                case "EXIT":
                    running = false;
                    break;

                default:
                    out.println("Perintah tidak ditemukan");
                    break;
            }
        }

        out.close();
    }

    public static void addMatkul(String[] cmdArgs) {
        var matkulName = cmdArgs[0];
        if (graph.getvMap().containsKey(matkulName)) {
            out.printf("Matkul %s sudah ada\n", matkulName);
            return;
        }

        var deps = Arrays.copyOfRange(cmdArgs, 1, cmdArgs.length);
        for (String dep : deps) {
            if (!graph.getvMap().containsKey(dep)) {
                out.printf("Matkul %s tidak ditemukan\n", dep);
                return;
            }
        }

        var v = graph.addVertex(matkulName);
        for (String dep : deps) {
            graph.addEdge(graph.getvMap().get(dep), v);
        }
    }

    public static void editMatkul(String[] cmdArgs) {
        var matkulName = cmdArgs[0];
        if (!graph.getvMap().containsKey(matkulName)) {
            out.printf("Matkul %s tidak ditemukan\n", matkulName);
            return;
        }

        var deps = Arrays.copyOfRange(cmdArgs, 1, cmdArgs.length);
        for (String dep : deps) {
            if (!graph.getvMap().containsKey(dep)) {
                out.printf("Matkul %s tidak ditemukan\n", dep);
                return;
            }
        }

        var v = graph.getvMap().get(matkulName);
        var prevDeps = (ArrayList<Vertex>) graph.getInside().get(matkulName).clone();
        for (Vertex dep : prevDeps) {
            graph.removeEdge(dep, v);
        }

        for (String dep : deps) {
            graph.addEdge(graph.getvMap().get(dep), v);
        }
    }

    public static void visitVertex(Vertex v, int level) {
        v.state = true;
        v.level = level;

        for (Vertex adjV : graph.getOutside().get(v.name)) {
            if (!adjV.state || adjV.level < level + 1) {
                visitVertex(adjV, level + 1);
            }
        }
    }

    public static void printOrdered() {
        for (Vertex v : graph.getVertexes()) {
            v.state = false;
            v.level = -1;
        }

        for (Vertex v : graph.getVertexes()) {
            if (!v.state) {
                visitVertex(v, 1);
            }
        }

        var leveled = new ArrayList<PriorityQueue<Vertex>>();
        for (Vertex v : graph.getVertexes()) {
            PriorityQueue<Vertex> q;
            if (leveled.size() < v.level) {
                q = new PriorityQueue<Vertex>((o1, o2) -> o1.name.compareTo(o2.name));
                leveled.add(q);
            } else {
                q = leveled.get(v.level - 1);
            }

            q.add(v);
        }

        ArrayList<String> sortedNames = new ArrayList<>();
        for (int i = 0; i < leveled.size(); i++) {
            var q = leveled.get(i);
            while (!q.isEmpty()) {
                sortedNames.add(q.poll().name);
            }
        }

        out.println(String.join(", ", sortedNames));
    }

    // taken from https://codeforces.com/submissions/Petr
    // together with PrintWriter, these input-output (IO) is much faster than the
    // usual Scanner(System.in) and System.out
    // please use these classes to avoid your fast algorithm gets Time Limit
    // Exceeded caused by slow input-output (IO)
    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }

        public String nextLine() {
            try {
                return reader.readLine();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

    }
}
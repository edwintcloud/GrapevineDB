# RAG_Project

A graph theory project for resource allocation and deadlock avoidance from a fundemental approach in operating system design.

## Abstract

Deadlock arises when a set of processes is blocked waiting on a resource that another process in the set holds access to. For deadlock to occur, each of the following four conditions must be true:

- Mutual Exclusion: Only one process can hold access to the resource at a given time.
- Hold and Wait: A process can hold one resource while waiting for other resources.
- No Preemption: Resources previously granted to a process cannot be forcefully taken away.
- Circular Wait: The set of processes is waiting on each other in circular form.

We can analyze and prevent deadlock using graph theory by constructing a resource allocation graph (RAG) and using an algorithm such as the Banker's Algorithm (proposed by Dijkstra's algorithm research in 1965). The vertexes in a RAG are processess and resources. The edges represent the possible changes in the system (or paths the process will take to gain access to the resource).

## Resources

- https://www.geeksforgeeks.org/operating-system-resource-allocation-graph-rag/
- https://www.geeksforgeeks.org/deadlock-prevention/
- https://www.geeksforgeeks.org/operating-system-process-management-deadlock-introduction/
- https://pdfs.semanticscholar.org/066e/0344e3bde43fb15606cae560806b41764330.pdf

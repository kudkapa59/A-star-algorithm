# A-star-algorithm

We are implementing A* path finding algorithm to find the smallest route.
The route needs to be found between two given nodes. We find this route
by ranking according to F = G + H 
1)H - the heuristic distance(which is guessed) from the end node.
2)G - the cost of the path from the start node.
We also have to remember the previous node of the current one.
In the beginning we assign infinity to G and H to all the nodes, however
G and H of an original point are equal to 0. 
Then we continue by taking the next node to the initial point. We know its G 
and we guess its H. Then we add this node to the openset as (F,node_name).

After that we go to the next node and do the same operation. 
We'll add it to the open set.
We will take its score as the smallest one if it's smaller
than all the others in the open set.
As we reached the final point we find its F and nodes which led us to it.
By doing that we reconstruct the path and can show it on the screen.

The algorithm is provided with fun animation thanks to pygame module. 
### HOW TO USE ANIMATION:
1) First LEFT mouse click - start node. Orange color.
2) Second LEFT mouse click - end node. Purple color.
3) All the proceeding LEFTS clicks produce black impassable blocks, where the path
is prohibited. Black color.
The nodes can be cancelled by RIGHT click button.
4) SPACE button - the algorithm starts to find the path. Blue color for unchecked nodes.
Red color for nodes with high cost. Green color for reconstructing the cheapest path. 
5) C button is used to start from the scratch. Cancels all the nodes definings.
Recommended literature: https://en.wikipedia.org/wiki/A*_search_algorithm

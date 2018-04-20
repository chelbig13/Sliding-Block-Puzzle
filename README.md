
# Sliding Block Puzzle AI

## Project Overview
This project includes the implementation for a sliding block puzzle, sample
sliding block puzzles in ```*.txt``` format, and several algorithms for
efficiently finding solutions to a generic puzzle. The solutions include A*,
breadth first search, depth first search, and iterative deepening search. 

## Running this program
To run this program, run ```main.py``` on its intended platform, ```Python 2.7```.
```main.py``` takes two inputs, the name of a text file containing the sliding
block puzzle to be attempted, and a string denoting which algorithm should
be used.

There are several example puzzles included with this program that it can be
tested on, please see the 'puzzles' folder.

The options for the second argument are as follows:
```bfs```     :  use breadth first search to solve the puzzle
```dfs```     :  use depth first search to solve the puzzle
```id```       :  use iterative deepening search to solve the puzzle
```astar``` :  use an A* search to solve the puzzle



## Mechanics
Sliding block puzzles must be loaded from a ```*txt``` file. Each text file must
only contain one puzzle. The first line of the file must include the
dimensions of the puzzle board. The following lines depict the actual
puzzle. 

```0``` : denotes an empty space
```1``` : denotes a wall, which can not be occupied
```2``` : denotes the solution block, which must be moved off of the board
```3+```: denotes an obstacle block, they are only distinguishable by having
		different numbers

A move consists of changing the position of a block by one row or column
index. The entire block must be moved simultaneously, and all newly occupied
spaces must be empty prior to the move. 


## Architecture
### Algorithm file
The ```algorithms.py``` file includes only the core algorithms, all helper
functions are located in a separate file. The algorithm file includes: A*,
breadth first search, depth first search, and iterative deepening search. It
also includes a heuristic function which is utilized by the A* algorithm. 


### Helper Function file
The ```helperFunct.py``` file includes helper functions and the sliding block
mechanics which are used by the ```algorithms.py``` and ```driver.py``` files. 

### Driver file
The ```driver.py``` file contains the main function utilized by this project.
It has two inputs, one to specify the ```*.txt``` file to be used as the puzzle,
and the other to specify the search strategy to utilize. 
Sliding Block Puzzle AI


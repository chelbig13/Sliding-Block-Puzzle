#!/usr/bin/env python
# Program: Block Puzzle 
# Author: Craig Helbig
# Platform: Python 2.7
# Main function

import sys
import random
import time
import algorithms
import helper

def main( ) :
	
	if validInput( sys.argv ) :
		fileName = sys.argv[1]
		board = helper.loadState( fileName )

		print "Puzzle: " + fileName	
		
		time0 = time.clock()

		if (sys.argv[2] == "bfs" ) :
			metrics = algorithms.BFS( board )
		elif (sys.argv[2] == "dfs" ) :
			metrics = algorithms.DFS( board )
		elif (sys.argv[2] == "id" ) :
			metrics = algorithms.IDS( board )
		elif (sys.argv[2] == "astar") :
			metrics = algorithms.aStar( board )
	
		time1 = time.clock()
		delTime = time1-time0

		print "Nodes Explored: " + str(metrics[0])
		print "Solution Length: " + str(metrics[1])
		print "Time Elapsed: " + str(delTime) + " sec"
		print ""

	else :
		print "invalid input"
	print ""


#error checking 
def validInput( sysInput ) :

	if (len(sysInput) < 3) :
		return False
	return True



main()


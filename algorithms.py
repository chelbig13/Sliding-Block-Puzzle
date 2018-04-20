#!/usr/bin/env python
# Program: Sliding Block Puzzle AI
# Author: Craig Helbig
# Platform: Python 2.7
# 

import sys
import random
import time
import helper 


def aStar( state ) :
#an A* search implementation. 

	nState =  helper.cloneState( state )
	helper.normalize( nState )
	exploredList = list()
	discList = [[nState, -1, -1, 0, -1]]
	exploredNode = discList.pop()
	while( not(helper.isComplete( exploredNode[0] ))) :
		exploredList.append( exploredNode )
		moves  = helper.moveListBoard( exploredNode[0] )
		for move in moves :
			newState = helper.applyMoveCloning( exploredNode[0], move )
			helper.normalize( newState )	
			if( not( helper.containsState( newState, exploredList ) or \
                 helper.containsState( newState, discList ))) :	
				parent = len( exploredList )-1
				depth = exploredList[parent][3] + 1
				g = depth + heur( newState )
				node = [newState, parent, move, depth, g]
				discList.append( node )

		discList = helper.sortNodes( discList )
		exploredNode = discList.pop( 0 )
	
	pathLength = helper.displayPath( exploredNode, exploredList )
	return [len( exploredList ), pathLength ]


#Heuristic Function
#returns the closest distance between the solution block and the goal space

def heur( state ) :
	brick = helper.findBlock( state, 2 )
	goal = helper.findBlock( state, -1 )[0]
	if( goal[0] == -1 ):
		return 0 #Return 0 when goal state is achieved

	hList = [] 
	for c in brick :
		H = abs( c[0]-goal[0] ) + abs( c[1] - goal[1] )  
		hList.append( H )

	return min(hList); 
		
		

#Breadth First Search
#Expands the search tree by exploring the lowest depth nodes first

def BFS( state ) :
	nState =  helper.cloneState( state )
	helper.normalize( nState )
	exploredList = list()
	discList = [[nState, -1, -1]]
	exploredNode = discList.pop()
	while( not( helper.isComplete( exploredNode[0] ))) :
		if( not( helper.containsState( exploredNode[0], exploredList ))) :
			exploredList.append( exploredNode )
			moves  = helper.moveListBoard( exploredNode[0] )
			for move in moves :
				newState = helper.applyMoveCloning( exploredNode[0], move )
				helper.normalize( newState )	
				parent = len( exploredList )-1
				node = [newState, parent, move]
				discList.append( node )

		exploredNode = discList.pop( 0 )

	pathLength = helper.displayPath( exploredNode, exploredList )
	print str( len( exploredList ))
	return [len( exploredList ), pathLength ]


#Depth First Search
#Expands the search tree by exploring the deepest discovered nodes first

def DFS( state ) :
	nState = helper.cloneState( state )
	helper.normalize( nState )
	exploredList = list()
	discList = [[nState, -1, -1]]
	exploredNode = discList.pop()
	while( not( helper.isComplete( exploredNode[0] ))):
		if( not( helper.containsState( exploredNode[0], exploredList ))) :
			exploredList.append( exploredNode )
			moves  = helper.moveListBoard( exploredNode[0] )
			for move in moves :
				newState = helper.applyMoveCloning( exploredNode[0], move )
				helper.normalize( newState )	
				parent = len( exploredList )-1
				node = [newState, parent, move]
				discList.append( node )
	
		exploredNode = discList.pop( len( discList )-1 ) #difference from BFS

	pathLength = helper.displayPath( exploredNode, exploredList )
	return [len( exploredList ), pathLength ]


#Iterative Deepening Search
#Expands the search tree by the Depth First Search strategy, with a maximum
#depth. If a solution is not found then the maximum depth is increased.

def IDS( state ) :
	nState = helper.cloneState( state )
	helper.normalize( nState )
	exploredNode = [ nState, -1, -1, 0]
	itDepth = 0
	while( not( helper.isComplete( exploredNode[0] ))) :
		exploredList = list()
		discList = [[nState, -1, -1, 0]] 
		itDepth += 1
		while( not( helper.isComplete( exploredNode[0] )) and ( len(discList) > 0 )) :
			exploredNode = discList.pop( len( discList )-1 )
			if( not( helper.containsState( exploredNode[0], exploredList ))) :
				if( exploredNode[3] < itDepth ) : #main difference from DFS
					exploredList.append( exploredNode )
					moves  = helper.moveListBoard( exploredNode[0] )
					for move in moves :
						newState = helper.applyMoveCloning( exploredNode[0], move )
						helper.normalize( newState )	
						parent = len( exploredList )-1
						depth = exploredNode[3] + 1
						node = [newState, parent, move, depth]
						discList.append( node )

	pathLength = helper.displayPath( exploredNode, exploredList )
	return [len( exploredList ), pathLength ]


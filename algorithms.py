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

	#initialize variables
	nState =  helper.cloneState( state )       #store the starting state 
	helper.normalize( nState )
	exploredList = list()
	discList = [[nState, -1, -1, 0, -1]]       #create the root node
	exploredNode = discList.pop()              #begin searching from the root

	
	#search until next node is complete (solved)
	while( not(helper.isComplete( exploredNode[0] ))) :       
		exploredList.append( exploredNode )
		moves  = helper.moveListBoard( exploredNode[0] )


		#for each valid move, make a clone state and apply the move
		for move in moves :
			newState = helper.applyMoveCloning( exploredNode[0], move )
			helper.normalize( newState )


			#check if identical state has already been explored
			#if not, add a new node containing the new state
			if( not( helper.containsState( newState, exploredList ) or \
                 helper.containsState( newState, discList ))) :	

				parent = len( exploredList )-1				
				depth = exploredList[parent][3] + 1
				
				#approximate distance from solution plus distance froms start
				g = depth + heur( newState )			

				node = [newState, parent, move, depth, g]
				discList.append( node )

		#sort nodes by 'g'
		discList = helper.sortNodes( discList )

		#continue searching from the node with the lowest value for 'g'
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

	#initialize variables
	nState =  helper.cloneState( state ) 		#store starting state
	helper.normalize( nState )					
	exploredList = list()				
	discList = [[nState, -1, -1]]					#define the root node
	exploredNode = discList.pop()					#start searching at root node


	#continue to search until the next node has a solved state
	while( not( helper.isComplete( exploredNode[0] ))) :

		#check if the current state is already in another node	
		if( not( helper.containsState( exploredNode[0], exploredList ))) :
			exploredList.append( exploredNode )
			moves  = helper.moveListBoard( exploredNode[0] ) 	

			#for each valid move, make a clone state and apply the move
			for move in moves :
				newState = helper.applyMoveCloning( exploredNode[0], move )
				helper.normalize( newState )	
				parent = len( exploredList )-1
				node = [newState, parent, move]		#create node
				discList.append( node ) 				#add new node to queue

		#take next node from queue (front of the list)
		exploredNode = discList.pop( 0 ) 

	
	#display results
	pathLength = helper.displayPath( exploredNode, exploredList )
	print str( len( exploredList ))
	return [len( exploredList ), pathLength ]


#Depth First Search
#Expands the search tree by exploring the deepest discovered nodes first

def DFS( state ) :
	
	#initialize variables
	nState = helper.cloneState( state )		#store starting state
	helper.normalize( nState )
	exploredList = list()
	discList = [[nState, -1, -1]]				#create root node
	exploredNode = discList.pop()				#start at root node


	#continue to search until next node contains a solution
	while( not( helper.isComplete( exploredNode[0] ))):

		#check if next node contains an already explored state
		if( not( helper.containsState( exploredNode[0], exploredList ))) :
			exploredList.append( exploredNode )
			moves  = helper.moveListBoard( exploredNode[0] )

			#for each valid move, make a clone state and apply the move
			for move in moves :
				newState = helper.applyMoveCloning( exploredNode[0], move )
				helper.normalize( newState )	
				parent = len( exploredList )-1
				node = [newState, parent, move]		#create new node
				discList.append( node )					#add new node to stack
	
		#take next node from the stack (end of the list)
		exploredNode = discList.pop( len( discList )-1 ) 


	#display results
	pathLength = helper.displayPath( exploredNode, exploredList )
	return [len( exploredList ), pathLength ]


#Iterative Deepening Search
#Expands the search tree by the Depth First Search strategy, with a maximum
#depth. If a solution is not found then the maximum depth is increased.

def IDS( state ) :
	
	#initialize variables
	nState = helper.cloneState( state )			#store starting state
	helper.normalize( nState )
	exploredNode = [ nState, -1, -1, 0]			#create root node
	itDepth = 0											#set starting search depth

	#continue searching until next state contains a solution
	while( not( helper.isComplete( exploredNode[0] ))) :

		#initialize search tree
		#a new search tree is created for each iteration in search depth
		exploredList = list()
		discList = [[nState, -1, -1, 0]] 
		itDepth += 1 							#iterate search depth

		#continue searching until list of valid nodes is exhausted
		#valid nodes are nodes above the current set search depth
		while( not( helper.isComplete( exploredNode[0] )) and ( len(discList) > 0 )) :
			exploredNode = discList.pop( len( discList )-1 )
	
			#check if current state has already been explored				
			if( not( helper.containsState( exploredNode[0], exploredList ))) :

				#check if current state is deeper than max depth
				if( exploredNode[3] < itDepth ) : 

					exploredList.append( exploredNode )
					moves  = helper.moveListBoard( exploredNode[0] )
					
					#for each valid move, make clone of current state and apply move
					for move in moves :

						newState = helper.applyMoveCloning( exploredNode[0], move )
						helper.normalize( newState )	
						parent = len( exploredList )-1
						depth = exploredNode[3] + 1
						node = [newState, parent, move, depth]		#create new node
						discList.append( node )							#add to stack

	#display results
	pathLength = helper.displayPath( exploredNode, exploredList )
	return [len( exploredList ), pathLength ]


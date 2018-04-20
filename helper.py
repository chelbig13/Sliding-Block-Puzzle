#!/usr/bin/env python
# Program: Sliding Block Puzzle AI
# Author: Craig Helbig
# Platform: Python 2.7
# Mechanics and Helper Functions

import sys
import random
import time


#-------------------------------BOARD STATES-------------------------------



#load a board state from a file specified by filename
#all values separated by commas, all rows separated by newlines
#first line of text contains number of rows, number of columns
#returns a list of lists, each inner list represents one horizontal row of
#the board
#values are stored as integers
def loadState( fileName ) :
	
	f = open( fileName, 'r' )
	board = list()
	for line in f:
		intList = list()
		lineList = line.split(",")	
		lineList = lineList[0:len(lineList)-1]
		for val in lineList :
			intList.append( int(val) )
		board.append( intList )
	f.close
	return board
	
 
#displays a board state stored in input variable, state
#prints in same text format as source file used in loadState()
def dispState( state ) :
	for row in state :
		for item in row :
			sys.stdout.write( str( item ) + ", " )
		print""
	print "\n\n"


#displays a move to console using the formatting defined in 'moveToString()'
def dispMove( move ) :
	
	print( moveToString( move ))


#return a printable string representation of a move
def moveToString( move ) :
		
	if ( move[1] == 'r'):
		direction  = 'right'
	elif ( move[1] == 'l'):
		direction = 'left'
	elif ( move[1] == 'u'):
		direction = 'up'
	elif ( move[1] == 'd'):
		direction = 'down'

	mvString = str( move[0] ) + ', ' + direction
	return mvString


#returns a deep copy of the given state
#does not modify the given state
def cloneState( state ) :

	stateClone = list()
	for row in state :
		rowClone = list() 
		for item in row :
			rowClone.append( item )
		stateClone.append( rowClone )

	return stateClone

			
#checks if board is complete, returns True or False
#if any -1 remains on board, false, otherwise true
def isComplete( state ) :
	for row in state :
		for val in row :
			if ( val == -1 ) :
				return False 
	return True


#searches a given state for a block number
#returns each coordinate where that block number is found
#returns [-1,-1] if the block number is not found in the state
def findBlock( state, blockNum ) :

	coordList = []
	for r in range( 1, len( state )):
		for c in range(0, len( state[r] )):
			if ( state[r][c] == blockNum ) :
				coordList.append( [r,c] )

	if( len( coordList ) < 1 ) :
		return [[-1,-1]]
	else :
		return coordList


#returns true if the nodeList already contain 'state'
#returns false if the nodeLIst does not contain 'state'
def containsState( state, nodeList ) :
	
	for n in nodeList :
		if compStates( n[0], state ) :
			return True
	return False


#returns true if the given position ['row','col'] is a valid destination
# for 'blockNum' to move to, returns false if it is an invalid destination 
def isOpen ( board, blockNum, row, col ) :
	if ( row-1 < 0 ) :
		return False
	if ( row > board[0][0] ) :
		return False
	if ( col < 0 ) :
		return False
	if ( col+1 > board[0][1] ) :
		return False 

	if( blockNum == 2 ) :
		if ( board[row][col] < 1 or board[row][col] == blockNum ) :
			return True
			#for goal brick, valid move is empty space or goal space (0 or -1)
			#or another piece of itself (which will simultaneously move)
	elif ( board[row][col] == 0 or board[row][col] == blockNum ) : 
			return True
			#for normal bricks, valid move is to an empty space (0) or onto a
			#tile with the same brick number (which is simultaneously moving)
	
	return False


#returns true if 'board', contains a block denoted by 'blockNum'
def containsBlock( board, blockNum ) :

	for row in board[1:] : #ignore first row
		for val in row :
			if ( val == blockNum ) :
				return True
	return False


#returns true if 'state1' is identical to 'state2'
#returns false otherwise
def compStates( state1, state2 ) :
	for r in range( 0,len( state1 )) :
		for c in range(0,len( state1[r] )) :
			if ( not( state1[r][c] == state2[r][c] )) :
				return False
	return True


# reassign block numbers to a standard numbering system
# this is necessary for identifying some duplicate states
# the uppper leftmost block is designated as '3'
# each row is searched from left to right, and 
# each subsequent block is designated by the next integer
def normalize( board ) :
	nextIndex = 3
	for r in range( 1,len( board )) :
		for c in range(0,len( board[r] )) :
			if ( board[r][c] == nextIndex ) :
				nextIndex += 1
			elif ( board[r][c] > nextIndex ) :
				swapIndex( board, board[r][c], nextIndex )
				nextIndex += 1	


# rewrite each occurence of 'index1' with 'index2' and vice versa
def swapIndex( board, index1, index2 ) :
	for r in range( 1,len(board )) :
		for c in range( 0,len(board[r] )) :
			if ( board[r][c] == index1 ) :
				board[r][c] = index2 
			elif ( board[r][c] == index2 ) :
				board[r][c] = index1


def sortNodes( nodeList ) :
	sortedList = sorted( nodeList, key = lambda x: int( x[4] ))
	return sortedList



#-----------------------------MOVES-------------------------------

def applyMove (board, move) :

	blockPos = list()
	for r in range( 1,len( board )) :
		for c in range( 1, len( board[r] )) :
			if ( board[r][c] == move[0] ) :
				mRow = r + dirDict( move[1] )[0]
				mCol = c + dirDict( move[1] )[1]
				blockPos.append( [mRow,mCol] )
				board[r][c]=0

	for pos in blockPos :
		board[pos[0]][pos[1]]=move[0]


#apply 'move' to a cloned version of 'board'
def applyMoveCloning ( board, move) :

	cloneBoard = cloneState( board )
	applyMove( cloneBoard, move )
	return cloneBoard

	
#encode the numerical shifts associated with each direction
#  to characters
def dirDict ( char ) :
	key = {'u':[-1, 0], 'd':[1, 0], 'l':[0, -1], 'r':[0,1]}
	return key[char]


#return a list of all valid moves for the block with the number 'blockNum'
def moveListBlock ( board, blockNum ) :

	if( not( containsBlock( board, blockNum))) :
		return []
	
	charList = ['u','d','l','r']
	moveList = list()
	for r in range( 1, len( board )) : #start at 1, to skip board dimensions
		for c in range( 0, len( board[r] )) :
			if ( board[r][c] == blockNum ) :
				if ( not( isOpen( board, blockNum, r-1, c ))) :
					charList[0]= 'n'
				if ( not( isOpen( board, blockNum, r+1, c ))) :
					charList[1]= 'n'
				if ( not( isOpen( board, blockNum, r, c-1 ))) :
					charList[2]= 'n'
				if ( not( isOpen( board, blockNum, r, c+1 ))) :
					charList[3]= 'n'
	for char in charList :
		if ( not( char == 'n' )) :
			moveList.append( [blockNum, char] )

	return moveList


#return a list of all valid moves that could be applied to 'board'	
def moveListBoard ( board ) :

	blockNum = 2
	moveList = list()
	while( containsBlock( board, blockNum )) :
		moveList.extend( moveListBlock( board, blockNum ))
		blockNum += 1
	
	for i in range( 0,len( moveList )) :
		if ( len( moveList[i] ) < 1 ) :
			moveList.pop( i )
			
	return moveList


#-------------------------------INTERFACE-------------------------------


#print the move sequence from the root of a tree to
#  the given node.
#also returns the length of the path
def displayPath ( node, tree ) :

	currentNode = node	
	moveList = list()
	while ( currentNode[1] > -1 ) :
		moveList.append( currentNode[2] )
		currentNode = tree[ currentNode[1]]

	for move in reversed( moveList ) :
		dispMove( move )

	dispState( node[0] )	
	return len( moveList )







		


			




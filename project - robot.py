#!/usr/bin/env python3
import queue
from ev3dev.ev3 import *
from movement.ev3movement.movement import *
btn = ev3.Button()
#__________________________________________________________________________________________________

'''The start parameter takes in where the wavefront planning should start
    Could be anything point in the cell, usually the current pos of robot'''


def create_map(goal, grid_map): #Because we start planning the path from the goal
    queue = [goal]
    while len(queue) != 0:
        cell = queue.pop(0)
        neighbors = generate_neighbouring_cells(cell, grid_map)
        for neighbor in neighbors:
            if(get_value(neighbor, grid_map) < 0 and get_value(neighbor, grid_map) != 1):
                grid_map[neighbor[0]][neighbor[1]] = get_value(cell, grid_map) + abs(get_value(neighbor,grid_map))
                queue.append(neighbor)
    return grid_map

#____________________________________________________________________________________________________

#4 POINT CONNECTIVITY Cell Generator
def generate_neighbouring_cells(current_cell, grid_map):
    cells = []
    cur_row = current_cell[0]
    cur_col = current_cell[1]
    X_SIZE = len(grid_map[0])
    Y_SIZE = len(grid_map)

    #UP CELL
    if cur_row - 1 >= 0:
        #cur_row = cur_row - 1
        cells.append((cur_row-1, cur_col))#, grid_map[cur_row-1][cur_col], 'up'))
        #cells.append((cur_col, cur_row-1, grid_map[cur_col][cur_row-1], 'up'))

    #DOWN CELL
    if cur_row + 1 < Y_SIZE:
        #cur_row = cur_row + 1
        cells.append((cur_row+1,cur_col))#, grid_map[cur_row+1][cur_col], 'down'))
        #cells.append((cur_col, cur_row+1, grid_map[cur_col][cur_row+1], 'down'))

    #RIGHT CELL
    if cur_col + 1 < X_SIZE:
        #cur_col = cur_col + 1
        cells.append((cur_row, cur_col+1))#, grid_map[cur_row][cur_col+1], 'right'))
        #cells.append((cur_col+1, cur_row, grid_map[cur_col+1][cur_row], 'right'))

    #LEFT CELL
    if cur_col - 1 >= 0:
        #cur_col = cur_col - 1
        cells.append((cur_row, cur_col-1))#, grid_map[cur_row][cur_col-1], 'left'))
        #cells.append((cur_col-1, cur_row,grid_map[cur_col-1][cur_row], 'left'))

    return cells
#___________________________________________________________________________________________________________________________
def get_value(cell, grid_map): #a method to return the actual value of the map as is in grid_map
    ans = grid_map[cell[0]][cell[1]]
    return ans

#______________________________________________________________________________________________________________________________
def graph_cost(cellx, celly, grid_map):
    #try some vaildation
    ans = get_value(cellx, grid_map) - get_value(celly, grid_map)
    return ans
#____________________________________________________________________________________________________________________
def heuristic(cellx, celly):
    row_difference = cellx[0] - celly[0]
    col_difference = cellx[1] - celly[1]
    ans = abs(row_difference + col_difference)
    return ans
#______________________________________________________________________________________________________________
'''Plans a path from the start tuple to the goal tuple. Does not consider all possible states from current state,
    no cost, first discovered cell is used'''

def a_star_planner(start, goal, grid_map):
    explore = queue.PriorityQueue()
    explore.put(start, 0)#insert start tuple with a key of 0
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not explore.empty():
        current = explore.get()
        if(get_value(current, grid_map) != get_value(goal,grid_map)):
            neighbors = generate_neighbouring_cells(current, grid_map)
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + graph_cost(current, neighbor,grid_map)
                if get_value(neighbor, grid_map) != 1 and (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]):
                    cost_so_far[neighbor] = new_cost
                    key = new_cost + heuristic(goal, neighbor)
                    explore.put(neighbor, key)
                    came_from[neighbor] = current

    return came_from
    
            
#_________________________________________________________________________________________________________________________________
def a_star_plan(start, goal, grid_map):
    came_from = a_star_planner(start, goal, grid_map)
    current = goal
    path = []
    while get_value(current, grid_map) != get_value(start, grid_map):
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

#________________________________________________________________________________________________________________________
def follow(came_from):
    cur = came_from[0]
    del came_from[0]
    for cell in came_from:
        if(cur[0] > cell[0]):
            print('move up')
        elif(cur[0] < cell[0]):
            print('Move down')
        elif(cur[1] < cell[1]):
            print('Move right')
        elif(cur[1] > cell[1]):
            print('Move left')
        cur = cell
        
#__________________________________________________________________________________________________________________________________
def main(start, goal, cost_map):
    while not btn.any():
        weighted_map = create_map(goal,cost_map)
        came_from = a_star_plan(start,goal,weighted_map)
        follow(came_from)
    
#_________________________________________________________________________________________________________________________________
#EXTRAS
#_____________________________________________________________________________________________________________

'''8 POINT CONNECTIVITY

def generate_neighbouring_cells(current_cell, grid_map):
    cells = []
    cur_row = current_cell[0]
    cur_col = current_cell[1]
    X_SIZE = len(grid_map[0])
    Y_SIZE = len(grid_map)

    #UP CELL
    if cur_row - 1 >= 0:
        #cur_row = cur_row - 1
        cells.append((cur_row-1, cur_col, grid_map[cur_row-1][cur_col], 'up'))
        #cells.append((cur_col, cur_row-1, grid_map[cur_col][cur_row-1], 'up'))

    #UPPER_RIGHT CORNER CELL
    if((cur_row - 1 >= 0) and (cur_col + 1 < Y_SIZE)):
        cells.append((cur_row - 1, cur_col + 1, grid_map[cur_row - 1][cur_col + 1], 'Upper right corner'))

    #DOWN CELL
    if cur_row + 1 < Y_SIZE:
        #cur_row = cur_row + 1
        cells.append((cur_row+1,cur_col, grid_map[cur_row+1][cur_col], 'down'))
        #cells.append((cur_col, cur_row+1, grid_map[cur_col][cur_row+1], 'down'))

    #BOTTOM_RIGHT CORNER CELL
    if((cur_row + 1 < Y_SIZE) and (cur_col + 1 < X_SIZE)):
        cells.append((cur_row + 1, cur_col + 1, grid_map[cur_row + 1][cur_col + 1], 'Bottom right corner'))

    #RIGHT CELL
    if cur_col + 1 < X_SIZE:
        #cur_col = cur_col + 1
        cells.append((cur_row, cur_col+1, grid_map[cur_row][cur_col+1], 'right'))
        #cells.append((cur_col+1, cur_row, grid_map[cur_col+1][cur_row], 'right'))

    #BOTTOM LEFT CORNER CELL
    if((cur_row + 1 < Y_SIZE) and (cur_col - 1 >= 0)):
        cells.append((cur_row + 1, cur_col - 1, grid_map[cur_row + 1][cur_col - 1], 'Bottom left corner'))

    #UPPER LEFT CORNER CELL
    if((cur_row - 1 >= 0) and (cur_col - 1 >= 0)):
        cells.append((cur_row - 1, cur_col - 1, grid_map[cur_row - 1][cur_col - 1], 'Upper left corner'))
        
    #LEFT CELL
    if cur_col - 1 >= 0:
        #cur_col = cur_col - 1
        cells.append((cur_row, cur_col-1, grid_map[cur_row][cur_col-1], 'left'))
        #cells.append((cur_col-1, cur_row,grid_map[cur_col-1][cur_row], 'left'))

    return cells
'''

import pprint
import random
import heapq

def main():
    #size can be 3 for 8-puzzle or 4 for 15-puzzle
    #15-puzzle takes longer
    size=3
    
    #create the initial grid and the final goal
    initial_state=createRandomStartGrid(size)
    goal_state=createSolutionGrid(size)
    
    #prints the initial grid and the goal sought-after 
    pp=setPprintParams(size)
    print("\nInitial State:\n")
    pp.pprint(initial_state)
    print("\nGoal State:\n")
    pp.pprint(goal_state)
    
    misplaced_tiles=heuristic_1(initial_state, goal_state, size)
    print ("\nNumber of Misplaced Tiles: "+ str(misplaced_tiles))
    
    manhattan_distance=heuristic_2(initial_state, goal_state, size)
    print ("\nManhattan Distance: "+ str(manhattan_distance))
    
    heuristics={heuristic_1:"Misplaced Tile", heuristic_2:"Manhattan Distance"}
    for i in range(2):
        picked_heuristic=heuristics.keys()[i]
        print("\nUsing Heuristic: "+heuristics[picked_heuristic]+"\n")
        solve_puzzle_astar(initial_state, goal_state, picked_heuristic, size)
        

def createRandomStartGrid(grid_size):
    #range is specified from 0. In this program 0 would represent the blank tile
    start_numbers=random.sample(range(0,grid_size**2),grid_size**2)
    start_positions=[]
    for i in range(0, grid_size**2, grid_size):
        start_positions.append(start_numbers[i:i + grid_size])
    return start_positions

def createSolutionGrid(grid_size):
    goal_numbers=range(1,grid_size**2)+[0]
    goal_positions=[]
    for i in range(0, grid_size**2, grid_size):
        goal_positions.append(goal_numbers[i:i + grid_size])
    return goal_positions

def setPprintParams(grid_size):
    return pprint.PrettyPrinter(width=10*grid_size)

def findZeroLocation(state, grid_size):
    for row in range(grid_size):
        for col in range(grid_size):
            if state[row][col] == 0:
                return(row, col)

def heuristic_1(current, goal, grid_size):
    misplaced_tiles=0
    for i in range(grid_size):
        for j in range(grid_size):
            if(current[i][j]!=goal[i][j]):
                misplaced_tiles+=1
    return misplaced_tiles

def heuristic_2(current, goal, grid_size):
    manhattan_distance=0
    c=[]
    g=[]
    for t in eval(str(current)):
        c+=t
    for t in eval(str(goal)):
        g+=t
    for i in c:
        manhattan_distance += abs(c.index(i)-g.index(i))
    return manhattan_distance

def getPossibleMoves(state, grid_size):
    moves_list = []
    moves_grid = eval(str(state)) 
    zero_row , zero_col=findZeroLocation(moves_grid, grid_size)
    
    if zero_row > 0:                                   
        moves_grid[zero_row][zero_col], moves_grid[zero_row-1][zero_col] = moves_grid[zero_row-1][zero_col], moves_grid[zero_row][zero_col];  #move up
        moves_list.append(moves_grid)
        moves_grid = eval(str(state)) 

    if zero_row < grid_size-1: 
        moves_grid[zero_row][zero_col], moves_grid[zero_row+1][zero_col] = moves_grid[zero_row+1][zero_col], moves_grid[zero_row][zero_col]   #move down
        moves_list.append(moves_grid)
        moves_grid = eval(str(state)) 

    if zero_col > 0:                                                      
        moves_grid[zero_row][zero_col], moves_grid[zero_row][zero_col-1] = moves_grid[zero_row][zero_col-1], moves_grid[zero_row][zero_col]   #move left
        moves_list.append(moves_grid)
        moves_grid = eval(str(state)) 

    if zero_col < grid_size-1:                                   
        moves_grid[zero_row][zero_col], moves_grid[zero_row][zero_col+1] = moves_grid[zero_row][zero_col+1], moves_grid[zero_row][zero_col]   #move right
        moves_list.append(moves_grid)
        moves_grid = eval(str(state)) 
    return(moves_list)

def solve_puzzle_astar(initial, goal, heuristic, grid_size):
    processing_queue=[]
    heapq.heappush(processing_queue, (heuristic(initial, goal, grid_size), [initial]))
    solution_path=[]
    processed_nodes=[]
    while len(processing_queue)>0:
        h_of_node, path=heapq.heappop(processing_queue)
        node=path[-1]
        #print("Current node: "+ str(node))
                
        if(heuristic_1(node, goal, grid_size)==0):
            solution_path=path
            break
        if node not in processed_nodes:
            for next_node in getPossibleMoves(node, grid_size):
                if next_node not in processed_nodes:
                    #print("Next node: " + str(next_node))
                    new_path=path[:]+[next_node]
                    heapq.heappush(processing_queue, (len(new_path)+heuristic(next_node, goal, grid_size) , new_path))
                    processed_nodes.append(node)
    pp=setPprintParams(10)    
    pp.pprint(solution_path)
    print("\nLength of solution path: "+str(len(solution_path)))
    print("\nNumber of nodes processed: "+str(len(processed_nodes)))


main()
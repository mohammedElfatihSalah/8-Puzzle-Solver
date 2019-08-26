# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 23:59:09 2019

@author: MohamedElfatih
"""
import time
class Problem:
    ACTIONS    = ['right' , 'down' , 'left' ,'up']
    GOAL_STATE = [0,1,2,3,4,5,6,7,8]
    WIDTH      = 3
    HEIGHT     = 3
    def __init__(self , initial_state):
        self.initial_state = initial_state
        
    def goal_test(self ,state):
        return self.GOAL_STATE == state
    def actions(self,state):
        index_1D = state.index(0)
        index_x  = int(index_1D/self.WIDTH)
        index_y  = int(index_1D%self.WIDTH)

        result   = ['right' , 'down' , 'left' ,'up']
        if index_x == 0:
            result.remove('up')
        elif index_x ==2:
            result.remove('down')
            
        if index_y == 0:
            result.remove('left')
        elif index_y ==2:
            result.remove('right')    
        return result
    
    def result(self , state , action):
        result_state = state.copy()
        index_1D = state.index(0)
        index_x  = int(index_1D/self.WIDTH)
        index_y  = int(index_1D%self.WIDTH)
        
        if action == 'up':
            index_x -=1
        elif action == 'down':
            index_x +=1
        elif action == 'right':
            index_y +=1
        elif action == 'left':
            index_y -= 1
            
        index_1D_new = index_x * self.WIDTH + index_y
        
        result_state[index_1D] = state[index_1D_new]
        result_state[index_1D_new] = 0
        
        return result_state
        
    def path_cost(self,state1 , action , state2):
        return 1;
#defining the basic data structure for the tree
#the constructor take the state as argument   
class Node:
    def __init__(self , state):
        self.path_cost = 0
        self.parent    = None
        self.action    = None
        self.depth     = 0
        self.state     = state
        #the function return ,
        #a child node given an action and 
        #parent node
    def child_node(self , problem , action):
        node = Node(problem.result(self.state , action))
        node.parent = self
        node.path_cost = self.path_cost + problem.path_cost(self.state , action ,node.state) 
        node.action = action
        node.depth  = self.depth + 1
        return node
    
    
#implementing breadth first search
def breadth_first_search(problem):
    #creating max_depth variable
    max_depth = 0
    #creating number_of_expanded_nodes
    number_of_expanded_nodes = 0
    #creating an initial_node and 
    #testing it for the goal
    initial_node = Node(problem.initial_state)
    if problem.goal_test(initial_node.state):
        return initial_node , max_depth , number_of_expanded_nodes
    
    #creating the frontier and the explored_Set
    frontier     = list()
    explored_set = list()
    frontier.append(initial_node)
    
    #making a maximum loop of a number
    for i in range(0 , 400000):
        #testing if the frontier is empty
        if len(frontier) == 0:
            return -1
        node = frontier.pop(0)
        #increasing the number of expanded nodes
        number_of_expanded_nodes += 1
        #testing the genrated node if it is the goal
        if problem.goal_test(node.state):
            return node , max_depth , number_of_expanded_nodes
        #adding the expanded node to the explored set
        explored_set.append(node.state)
        #looping throught the possible set of actions
        for action in (problem.actions(node.state)):
            new_node = node.child_node(problem , action)
            #changing the max_depth
            if(max_depth < new_node.depth):
                max_depth = new_node.depth
            #===
            #addign the generated node to frontier
            #if the they are not explored yet
            if new_node.state not in explored_set:
                frontier.append(new_node)
    return 0;

#implementing depth first_search
def depth_first_search(problem):
    initial_node = Node(problem.initial_state)
    
    if problem.goal_test(initial_node.state):
        return initial_node
    #defining the frontier
    frontier = list()
    #we dont need an explored set, to save the memory
    frontier.append(initial_node)
    while(len(frontier) > 0):

        #pop the top of the frontier
        node = frontier.pop(-1)
        if problem.goal_test(node.state):
            return node
        for action in problem.actions(node.state):
            #check if the node in the current path
            child_node_state = problem.result(node.state , action)
            nodeInPath       = False
            node_in_path = node
        
            
            while(node_in_path != None):
                
                if node_in_path.state == child_node_state:
                    nodeInPath = True
                    break
                node_in_path = node_in_path.parent
            
                
            if not nodeInPath:
                child_node   = node.child_node(problem , action )
                if problem.goal_test(child_node.state):
                    return child_node
                frontier.append(child_node)

    #no solution exist            
    return -1

#take problem, and limit as parameter
#implementing limited_depth_first_search
#return goal node if found
#return 0 if not found within the specified limit
#it save space
def limited_depth_first_search(problem , limit):
    node  = Node(problem.initial_state)
    return recursive_depth_first_search(node , problem , limit)

def recursive_depth_first_search(node , problem , limit):
    if problem.goal_test(node.state):
        return node
    elif limit == 0:
        #it is a cutoff
        return 0
    else:
        for action in problem.actions(node.state):
            child = node.child_node(problem , action)
            result= recursive_depth_first_search(child , problem , limit - 1)
            if result == 0:
                continue
            else:
                return result
        return 0

#take problem
#return -1 if  no result
#return the goal node if found
#it save space
def iterative_depth_limited_search(problem):
    for i in range(0 , 100):
        result = limited_depth_first_search(problem , i)
        if (result != 0):
            return result
    #no solution at that depth
    return -1
def h2(state,width):
    cost =0;
    locations = [state.index(i) for i in range(0,8)]
    for i in range(0,8):
        index_x_begin = int(locations[i]/width)
        index_y_begin = int(locations[i]%width)
        
        index_x_end = int(i/width)
        index_y_end= int(i%width)
        
        diff_x     = abs(index_x_begin - index_x_end)
        diff_y     = abs(index_y_begin - index_y_end)
        cost+= diff_x + diff_y
    return cost

#the least cost node will be in the front
def push(node , frontier):
    #checking for the trivil case,
    #when frontier empty
    if len(frontier) == 0:
        frontier.append(node)
    else:
        nodeRepeated = False
        for i in range(0,len(frontier)):
            if node.state == frontier[i].state:
                nodeRepeated = True
                #update the value and locations
                #if the new node cost is less
                if node.path_cost < frontier[i].path_cost:
                    frontier[i].path_cost = node.path_cost
                    #now updating the locattion
                    for  j in range(i-1 , -1 , -1):
                        if frontier[i].path_cost < frontier[j].path_cost:
                            k = frontier[i]
                            frontier[i] = frontier[j]
                            frontier[j] = k
                            i = j
                        else:
                            break
            if nodeRepeated:
                break
            
        #if the state is not repeated in the frontier
        if not nodeRepeated:
            i = len(frontier) 
            for j in range(len(frontier)-1 , -1 , -1):
                if node.path_cost < frontier[j].path_cost:
                    i = i -1
                else:
                    break
            frontier.insert(i,node)
            
                
def A_star_search(problem):
    initial_node  = Node(problem.initial_state)
    if problem.goal_test(initial_node.state):
        return initial_node
    
    frontier = list()
    push(initial_node , frontier)
    firstLoop = True
    while(len(frontier) > 0):
        node = frontier.pop(0)
        if problem.goal_test(node.state):
            return node
        if(not firstLoop):
            node.path_cost -= h2(node.state ,3)
            
        for action in problem.actions(node.state):
            child_node = node.child_node(problem , action)
            child_node.path_cost += h2(child_node.state , 3)
            push(child_node , frontier)
            
        firstLoop = False

#take the goal node and empty list
#return the required steps
def solution(goal_node , steps):
    if (goal_node == 0):
        print("exceeds the number of loops")
    elif (goal_node == -1):
        print("no solution exist")
    elif (goal_node == None):
        return
    else:
        solution(goal_node.parent , steps)
        if goal_node.action != None:
            steps.append(goal_node.action)
    
    
        
def memory():
    import os
    from wmi import WMI
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)
    
'''========================testing section========================'''   

'''
k = h2([1,0,2,3,4,5,6,7,8] , 3)   
node1 = Node([1,2])
node1.path_cost = 10

node2 = Node([1,2])
node2.path_cost = 5

node3 = Node([1,2])
node3.path_cost = 11

node4 = Node([1,3])
node4.path_cost = 11

node5 = Node([1,7])
node5.path_cost = 23

node6 = Node([1,4])
node6.path_cost = 11

node7 = Node([1,3,8])
node7.path_cost = 11

node8 = Node([1,3,8])
node8.path_cost = 1

node9 = Node([1,2])
node9.path_cost = 0

node10 = Node([1,2,9])
node10.path_cost = 3

f = list()
push(node1,f)
push(node2,f)
push(node3,f)
push(node4,f)
push(node5,f)
push(node6,f)
push(node7,f)
push(node8,f)
push(node9,f)
push(node10,f)
for i in range(0 , len(f)):
    print("state ", f[i].state , " cost : ", f[i].path_cost)
'''


test = Problem([1,2,5,3,4,0,6,7,8])

begin = time.time()
k ,max_depth , n= breadth_first_search(test)
end = time.time()
print( "bfs search : ",float((end - begin))*1000.0)
print("max_depth : " , max_depth)
print("number of expanded nodes : ", n)
print("search_depth: ", k.depth)



steps = list()
solution(k,steps)

if k != -1 and k !=0:
    print(steps)
    print("path cost : " , k.path_cost)

#print(8/3)'''

        
        
    
    

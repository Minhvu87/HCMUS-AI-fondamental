#!/usr/bin/env python
# coding: utf-8

# In[1]:


from queue import Queue, PriorityQueue
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


# In[2]:


input_file = open('/home/minhvu/Documents/A.I/A.I lab1/BFS.txt', 'r')
f = input_file.read().splitlines()

N = int(f[0])#Number of node
goal = f[1].split()
start = 1#int(goal[0])#Start node
end = 18#int(goal[1])#End node
matrix = [f[i].split() for i in range(2, len(f))]
wt_matrix = [[int(char) for char in line]for line in matrix]
input_file.close()


# In[3]:


wt_matrix


# In[4]:


def bfs(wt_matrix, start, end):
    
    frontier = Queue()
    list_father = []
    explored = []
    initial_state = start -1
    frontier.put(initial_state)
    
    while(1):
        if frontier.empty():
            return False, "No way Exception"
        current_node = frontier.get()
        explored.append(current_node)
        
        # Check if node is goal-node
        if current_node == end - 1:
            result = []
            result.append(end)
            
            #Find end
            end_index = 0
            for i in range(-1, -len(list_father)-1, -1):
                sons, father = list_father[i]
                if end -1 in sons:
                    end_index = i
                    break
            #Start tracking
            find = father
            result.append(find + 1)
            for i in range(end_index - 1, -len(list_father)-1, -1):
                sons, father = list_father[i]
                if find in sons:
                    result.append(father + 1)
                    find = father
            
            result = result[::-1]
            result = [str(num) for num in result]
            return True, '->'.join(result)
        #Expand current node
        temp = []
        for i in range(len(wt_matrix[current_node])):
            if wt_matrix[current_node][i] and i not in explored:
                frontier.put(i)
                temp.append(i)
        list_father.append((temp, current_node))


# In[5]:


a, path = bfs(wt_matrix, start, end)
print("BFS : ", a, path)


# In[6]:


def dfs(wt_matrix, start, end):
    
    frontier = []#stack
    explored = []
    list_father = []
    initial_state = start -1
    frontier.append(initial_state)
    while(1):
        if len(frontier) == 0:
            return False, "No way Exception"
        current_node = frontier.pop()
        explored.append(current_node)
        
        if current_node == end - 1:
            result = []
            result.append(end)
            #Find end
            end_index = 0
            for i in range(-1, -len(list_father) - 1, - 1):
                sons, father =list_father[i]
                if end - 1 in sons:
                    end_index = i
                    break
            #Start tracking
            find = father
            result.append(find + 1)
            for i in range(end_index - 1, -len(list_father) - 1, -1):
                sons, father = list_father[i]
                if find in sons:
                    result.append(father + 1)
                    find = father
            #Write result
            result = result[::-1]
            result = [str(num) for num in result]
            return True, '->'.join(result)
        temp = []
        for i in range(len(wt_matrix[current_node])):
            if wt_matrix[current_node][i] and i not in explored:
                frontier.append(i)
                temp.append(i)
        list_father.append((temp, current_node))


# In[7]:


a, path = dfs(wt_matrix, start, end)
print("DFS : ",a, path)


# In[14]:


def ucs(wt_matrix1, start, end):
    
    frontier =PriorityQueue()
    explored = []
    history = []
    result = []
    #Ini tial state
    frontier.put((0, 0, start -1))
    while(1):
        if frontier.empty():
            return False, "No way Exception", None
        cur_cost, father, current = frontier.get()
        explored.append(current)

        if current == end - 1:
            #Find dst in history
            dst_index = -1
            for i in range(-1, -len(history) -1, -1):
                tcur_cost, tfather, tcurrent = history[i]
                if tcur_cost == cur_cost:
                    end_index = i
                    result.append(history[i])
                    break
            fcur_cost, ffather, fcurrent = history[end_index]
            #Track path through history, return a list of node
            for i in range(dst_index - 1, -len(history) - 1, -1):
                tcur_cost, tfather, tcurrent = history[i]
                if tcurrent == ffather:
                    path_index = i
                    min_cost = tcur_cost
                    for j in range(i - 1, -len(history), -1):
                        t1cur_cost, t1father, t1current = history[j]
                        if t1current == tcurrent and min_cost > t1cur_cost:
                            min_cost = t1cur_cost
                            path_index = j
                    fcur_cost, ffather, fcurrent = history[path_index]
                    result.append(history[path_index])
            #Write path
            path = str(start)
            for i in range(-1, -len(result)-1, -1):
                _, _, p = result[i]
                path += "->" + str(p + 1)
            return True, path, cur_cost

        #Expand current node
        for i in range(len(wt_matrix1[current])):
            if wt_matrix1[current][i] and i not in explored:
                node = (wt_matrix1[current][i] + cur_cost, current, i)
                frontier.put(node)
                history.append(node)


# In[19]:


#File for UCS
input_file1 = open('/home/minhvu/Documents/A.I/A.I lab1/UCS.txt', 'r')
f1 = input_file1.read().splitlines()
start=1
end=18
matrix1 = [f1[i].split() for i in range(2, len(f1))]
wt_matrix1 = [[int(char) for char in b]for b in matrix1]
input_file1.close()


# In[20]:


a, path, cost = ucs(wt_matrix1, start, end)
print("UCS : ",a, path,"with lowest cost : ", cost)


# In[ ]:





# In[ ]:





# In[ ]:





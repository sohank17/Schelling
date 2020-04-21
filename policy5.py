### Read the attached Readme file to see steps to run program
### Group members: Sohan Karkera, Prachi Rathod, Sana Rajani

import random
import numpy as np
import matplotlib.pyplot as plt


def initialize(rows, columns,empty_percent,population_percent,no_friends):
    grid = np.zeros((rows, columns))

    arr_flat = grid.flatten()
    total_length = len(arr_flat)
    empty_cell_length = int(total_length - ((1 - empty_percent) * total_length))

    population_length = total_length - empty_cell_length

    arr_flat[0:int((population_percent * population_length) - 1)] = 1
    arr_flat[int(population_percent * population_length):int(
        (population_percent * population_length) + ((1 - population_percent) * population_length))] = 2
    grid = np.reshape(arr_flat, (rows, columns))
    np.random.shuffle(grid.flat)
    grid_dict = dict()
    count = 0
    empty_list_key = []
    agent_list_key = []
    for rows in range(0, len(grid)):
        for columns in range(0, len(grid)):
            grid_dict[count] = dict()
            grid_dict[count]['value'] = grid[rows, columns]
            if grid_dict[count]['value'] == 0:
                empty_list_key.append(count)
            else:
                agent_list_key.append(count)
            grid_dict[count]['init_position'] = (rows, columns)
            grid_dict[count]['position'] = [[rows, columns]]
            grid_dict[count]['happiness'] = [['unhappy', 0]]
            grid_dict[count]['friends'] = []
            count += 1
    for key in grid_dict.keys():
        for i in range(0,no_friends):
                grid_dict[key]['friends'].append(random.choice(agent_list_key))
    return grid, grid_dict, empty_list_key, rows, columns


def update(iterations=30,k=4,rows=40,columns=40,m=3):
    happy_agents=[]
    for iter in range(0, iterations):
        latest_grid = np.zeros((rows, columns ))
        for key in grid_dict.keys():
            latest_position = grid_dict[key]['position'][-1]
            latest_grid[latest_position[0], latest_position[1]] = grid_dict[key]['value']

        for key in grid_dict.keys():
            if grid_dict[key]['value'] != 0:
                score, latest_position = happy_score(latest_grid, key,rows,columns)
                if score >= k:
                    grid_dict[key]['happiness'].append(['happy', score])
                    grid_dict[key]['position'].append(latest_position)
                else:
                    grid_dict[key]['happiness'].append(['unhappy', score])
                    grid_dict[key]['position'].append(latest_position)
                    if_unhappy(key, latest_grid, score, k,rows,columns,m)
        count=0
        for key in grid_dict.keys():
            if grid_dict[key]['happiness'][-1][0]== 'happy':
                count += 1
        happy_agents.append([count, iter])
        print("Iteration",iter)
    print(latest_grid.shape)
    return happy_agents




def if_unhappy(key, latest_grid, score, k,rows,columns,m):
    initial_pos=grid_dict[key]['position'][-1]
    friend_list(key,latest_grid,m)
    if initial_pos == grid_dict[key]['position'][-1]:
        least_unhappy_score = 0
        least_unhappy_key = None
        for empty_key in empty_list_key:
            Escore, Epos = empty_happy_score(latest_grid, key, empty_key, rows, columns)
            if score < Escore and Escore >= k:
                empty_loc = grid_dict[empty_key]['position'][-1]
                key_loc = grid_dict[key]['position'][-1]
                grid_dict[key]['position'].append(empty_loc)
                grid_dict[key]['happiness'].append(['unhappy', 0])
                grid_dict[empty_key]['position'].append(key_loc)
                break
            elif score < Escore and least_unhappy_score < Escore:
                least_unhappy_score = Escore
                least_unhappy_key = empty_key

        if least_unhappy_key != None:
            empty_loc = grid_dict[least_unhappy_key]['position'][-1]
            key_loc = grid_dict[key]['position'][-1]
            grid_dict[key]['position'].append(empty_loc)
            grid_dict[key]['happiness'].append(['unhappy', 0])
            grid_dict[least_unhappy_key]['position'].append(key_loc)


def friend_list(agent_key,latest_grid,m):
    available_empty_keys=[]
    for friend in  grid_dict[agent_key]['friends']:
        #print(friend)
        list = matrix_process(friend,latest_grid,m)
        #print("List",list)
        #print(available_empty_keys)
        for key in grid_dict.keys():
            for position in list:
                if grid_dict[key]['position'][-1] == position:
                    available_empty_keys.append(key)

    max_score = 0
    #print("After", available_empty_keys)
    if len(available_empty_keys) != 0 :
        for empty_key in available_empty_keys:
            score, posl = empty_happy_score(latest_grid, agent_key, empty_key)
            #print(score)
            if max_score <= score:
                max_score = score
                opt_key = empty_key

    if max_score>=4:
        #print(max_score,opt_key)
        empty_loc = grid_dict[opt_key]['position'][-1]
        key_loc = grid_dict[agent_key]['position'][-1]
        grid_dict[agent_key]['position'].append(empty_loc)
        grid_dict[agent_key]['happiness'].append(['unhappy', 0])
        grid_dict[opt_key]['position'].append(key_loc)

def matrix_process(key,grid,m):
    #print("Matrice",key)
    empty_list=[]
    pos = grid_dict[key]['position'][-1]
    #print(pos)
    for i in range(0, m):
        for j in range(0, m):
            if m == 3:
                x = i + int(pos[0]) - 1
            elif m == 5:
                x = i + int(pos[0]) - 2
            if m == 3:
                y = j + int(pos[1]) - 1
            elif m == 5:
                y = j + int(pos[1]) - 2
            if x>=rows:
                x=0
            if y>=columns:
                y=0
            if x<=-1:
                x=rows-1
            if y<=-1:
                y=columns-1
            #print("Final x",x)
            #print("Final y",y)
            #print(grid[x,y])
            if grid[x,y]== 0:
                empty_list.append([x,y])
            #print(empty_list)

    return empty_list

def empty_happy_score(grid, key, empty_key, rows=40,columns=40):
    happy_score = 0
    latest_position = grid_dict[empty_key]['position'][-1]
    #print(empty_key,latest_position,grid_dict[key]['value'],key)
    if latest_position[0] == 0 and 0 < latest_position[1] < (rows - 1):
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] - 1] != 0:
            if grid[(rows - 1), latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] + 1] != 0:
            if grid[(rows - 1), latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and 0 < latest_position[1] < (rows - 1):
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] - 1] != 0:
            if grid[0, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] + 1] != 0:
            if grid[0, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[1] == 0 and 0 < latest_position[0] < (rows - 1):
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, rows - 1] != 0:
            if grid[latest_position[0] - 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, rows - 1] != 0:
            if grid[latest_position[0] + 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[1] == (rows - 1) and 0 < latest_position[0] < (rows - 1):
        if grid[latest_position[0], 0] != 0:
            if grid[latest_position[0], 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, 0] != 0:
            if grid[latest_position[0] - 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, 0] != 0:
            if grid[latest_position[0] + 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1


    if latest_position[0] == 0 and latest_position[1] == 0:
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, rows - 1] != 0:
            if grid[(rows - 1), (rows - 1)] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] + 1] != 0:
            if grid[(rows - 1), latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, rows - 1] != 0:
            if grid[latest_position[0] + 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == 0 and latest_position[1] == (rows - 1):
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, 0] != 0:
            if grid[(rows - 1), 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] - 1] != 0:
            if grid[(rows - 1), latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, 0] != 0:
            if grid[0, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, 0] != 0:
            if grid[latest_position[0] + 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and latest_position[1] == 0:
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] + 1] != 0:
            if grid[0, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, rows - 1] != 0:
            if grid[0, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, rows - 1] != 0:
            if grid[latest_position[0] - 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and latest_position[1] == (rows - 1):
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] - 1] != 0:
            if grid[0, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, 0] != 0:
            if grid[0, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], 0] != 0:
            if grid[latest_position[0], 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, 0] != 0:
            if grid[latest_position[0] - 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if 0 < latest_position[0] < (rows - 1) and 0 < latest_position[1] < (rows - 1):
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
    return happy_score, latest_position

def happy_score(grid, key, rows=40,columns=40):
    happy_score = 0
    latest_position = grid_dict[key]['position'][-1]
    if latest_position[0] == 0 and 0 < latest_position[1] < (rows - 1):
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] - 1] != 0:
            if grid[(rows - 1), latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] + 1] != 0:
            if grid[(rows - 1), latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and 0 < latest_position[1] < (rows - 1):
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] - 1] != 0:
            if grid[0, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] + 1] != 0:
            if grid[0, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[1] == 0 and 0 < latest_position[0] < (rows - 1):
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, rows - 1] != 0:
            if grid[latest_position[0] - 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, rows - 1] != 0:
            if grid[latest_position[0] + 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[1] == (rows - 1) and 0 < latest_position[0] < (rows - 1):
        if grid[latest_position[0], 0] != 0:
            if grid[latest_position[0], 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, 0] != 0:
            if grid[latest_position[0] - 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, 0] != 0:
            if grid[latest_position[0] + 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1


    if latest_position[0] == 0 and latest_position[1] == 0:
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, rows - 1] != 0:
            if grid[(rows - 1), (rows - 1)] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] + 1] != 0:
            if grid[(rows - 1), latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, rows - 1] != 0:
            if grid[latest_position[0] + 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == 0 and latest_position[1] == (rows - 1):
        if grid[rows - 1, latest_position[1]] != 0:
            if grid[(rows - 1), latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, 0] != 0:
            if grid[(rows - 1), 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[rows - 1, latest_position[1] - 1] != 0:
            if grid[(rows - 1), latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, 0] != 0:
            if grid[0, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, 0] != 0:
            if grid[latest_position[0] + 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and latest_position[1] == 0:
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] + 1] != 0:
            if grid[0, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, rows - 1] != 0:
            if grid[0, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], rows - 1] != 0:
            if grid[latest_position[0], rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, rows - 1] != 0:
            if grid[latest_position[0] - 1, rows - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1

    if latest_position[0] == (rows - 1) and latest_position[1] == (rows - 1):
        if grid[0, latest_position[1]] != 0:
            if grid[0, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, latest_position[1] - 1] != 0:
            if grid[0, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[0, 0] != 0:
            if grid[0, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], 0] != 0:
            if grid[latest_position[0], 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, 0] != 0:
            if grid[latest_position[0] - 1, 0] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1

    if 0 < latest_position[0] < (rows - 1) and 0 < latest_position[1] < (rows - 1):
        if grid[latest_position[0] - 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] - 1] != 0:
            if grid[latest_position[0], latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] - 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] - 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1]] != 0:
            if grid[latest_position[0] + 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] + 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] + 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0], latest_position[1] + 1] != 0:
            if grid[latest_position[0], latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1] + 1] != 0:
            if grid[latest_position[0] - 1, latest_position[1] + 1] == grid_dict[key]['value']:
                happy_score += 1
        if grid[latest_position[0] - 1, latest_position[1]] != 0:
            if grid[latest_position[0] - 1, latest_position[1]] == grid_dict[key]['value']:
                happy_score += 1

    return happy_score, latest_position

def plot(height, width, name,file):
    fig, ax = plt.subplots()
    agent_colors = {0.0: 'w', 1.0: 'r', 2.0: 'g'}

    for key in grid_dict.keys():
        latest_position = grid_dict[key]['position'][-1]
        x = latest_position[0]
        y = latest_position[1]
        #print(x, y, grid_dict[key]['value'], key)
        ax.scatter(x + 0.5, y + 0.5, color=agent_colors[grid_dict[key]['value']])
    ax.set_title(name, fontsize=10, fontweight='bold')
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    ax.set_xticks([])
    ax.set_yticks([])
    plt.savefig(file)
    plt.clf()

def plot_graph(happy_agents,file):
    x_values=[]
    y_values=[]
    for count in happy_agents:
        x_values.append(count[1])
        y_values.append(count[0])
    plt.plot(x_values,y_values)
    plt.xlabel('Iterations')
    plt.ylabel('Happy Agents')
    plt.savefig(file)
    plt.clf()



## Variables ##
rows = 40
columns = 40
empty_percent = 0.1
population_percent = 0.5
iterations=50
k= 4
friends=5
neighbour_matrix=3
initial_plot='First_Sohan'
final_plot='Final_Sohan'
graph_plot='graph_Sohan'

grid, grid_dict, empty_list_key, rows,columns = initialize(rows, columns,empty_percent,population_percent,friends)
plot(40, 40, 'First', initial_plot)
happy_agents = update(iterations,k,rows,columns,neighbour_matrix)

print("Happy Agents:", happy_agents[-1][0])
plot(40, 40, 'Last',  final_plot)
plot_graph(happy_agents,graph_plot)

import random
import time
import GRIDS

m, n = 4, 1
initial = [['Vinyl'],
          ['ThickCarpet'],
          ['ThinCarpet'],
          ['ThickCarpet']]
          
actions = ['UP', 'DOWN', 'RIGHT', 'LEFT', 'CLEAN']

grids = GRIDS.grids4x1
all_states = []
for i in range(m):
    for j in range(n):
        for grid in grids:
            all_states.append([grid,(i,j)])

def transition(s,a,next_s):
    i = s[1][0]
    j = s[1][1]
    if a == 'UP':
        if next_s[1][0] == s[1][0]-1 and next_s[0]==s[0]:
            return 1
        if next_s == s and i == 0:
            return 1
    if a == 'DOWN':
        if next_s[1][0] == s[1][0]+1 and next_s[0]==s[0]:
            return 1
        if next_s == s and i == m-1:
            return 1
    if a == 'RIGHT':
        if next_s[1][1] == s[1][1]+1 and next_s[0]==s[0]:
            return 1
        if next_s == s and j == n-1:
            return 1
    if a == 'LEFT':
        if next_s[1][1] == s[1][1]-1 and next_s[0]==s[0]:
            return 1
        if next_s == s and j == 0:
            return 1
    if a == 'CLEAN':
        for row in range(m):
            for column in range(n):
                if row==i and column==j:
                    continue
                else:
                    if next_s[0][row][column] != s[0][row][column]:
                        return 0
        if next_s[0][i][j] == 1 and s[0][i][j] == 0 and initial[i][j]== 'Vinyl' and next_s[1]==s[1]:
            return 0.95
        if next_s[0][i][j] == 1 and s[0][i][j] == 1 and initial[i][j]== 'Vinyl'and next_s[1]==s[1]:
            return 1
        if next_s[0][i][j] == 0 and s[0][i][j] == 0 and initial[i][j]== 'Vinyl'and next_s[1]==s[1]:
            return 0.05
        if next_s[0][i][j] == 1 and s[0][i][j] == 0 and initial[i][j]== 'ThinCarpet'and next_s[1]==s[1]:
            return 0.85
        if next_s[0][i][j] == 1 and s[0][i][j] == 1 and initial[i][j]== 'ThinCarpet'and next_s[1]==s[1]:
            return 1
        if next_s[0][i][j] == 0 and s[0][i][j] == 0 and initial[i][j]== 'ThinCarpet'and next_s[1]==s[1]:
            return 0.15
        if next_s[0][i][j] == 1 and s[0][i][j] == 0 and initial[i][j]== 'ThickCarpet'and next_s[1]==s[1]:
            return 0.75
        if next_s[0][i][j] == 1 and s[0][i][j] == 1 and initial[i][j]== 'ThickCarpet'and next_s[1]==s[1]:
            return 1
        if next_s[0][i][j] == 0 and s[0][i][j] == 0 and initial[i][j]== 'ThickCarpet'and next_s[1]==s[1]:
            return 0.25
    return 0

def all_clean(grid):
    for i in range(m):
        for j in range(n):
            if grid[i][j] != 1:
                return False
    return True

def rewards(s,a,next_s):
    if transition(s,a,next_s) != 0:
        if a == 'UP' or a == 'DOWN' or a == 'LEFT' or a == 'RIGHT':
            return -1
        if a == 'CLEAN' and all_clean(next_s[0]):
            return 200
        i = s[1][0]
        j = s[1][1]
        if a == 'CLEAN' and s[0][i][j] == 0 and next_s[0][i][j] == 1:
            return 50
    return 0

start_time = time.time()
maps = {}
for i in range(len(all_states)):
    maps[i] = all_states[i]


values = {k: 0 for k in range(len(all_states))}
policy = {k: None for k in range(len(all_states))}

max_iterations = 100  

gamma = 0.99

initial_state_index = 0
terminal_states = []  
for index in range(len(all_states)):
    if all_clean(all_states[index][0]):
        values[index] = 0
        terminal_states.append(index)

i = 0
while i < max_iterations:
    S = initial_state_index
    while S not in terminal_states:
        s = maps[S]
        v = values[S]
        action_values = []
        for a in actions:
            action_value = 0
            for next_index in range(len(all_states)):
                next_s = maps[next_index]
                action_value += transition(s, a, next_s) * (rewards(s, a, next_s) + gamma * values[next_index])
            action_values.append(action_value)
        values[S] = max(action_values)
        best_action_index = action_values.index(max(action_values))
        possible = []
        for next_state in range(len(all_states)):
            for a in actions:
                if transition(maps[S],a,maps[next_state])!=0:
                    possible.append((a,next_state))
        r = random.randint(0,len(possible)-1)
        policy[S] = possible[r][0]
        S = possible[r][1]
    i+=1

end_time = time.time()
for k,v in values.items():
    print(str(maps[k]) + " " + str(v))
for k,v in policy.items():
    print(str(maps[k]) + " " + str(v))

elapsed = end_time - start_time
print(f"Elapsed time: {elapsed:.6f} seconds")
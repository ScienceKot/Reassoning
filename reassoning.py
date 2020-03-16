# The length of the environment matrix
length = 7
# The width of the environment matrix
width = 4
# Creation of the AND-OR Tree
AND_OR_TREE = []
def create_free_matrix(length, width):
    ''' This function creates an empty matrix '''
    matrix = []
    for i in range(width):
        matrix.append([])
        for j in range(length):
            matrix[-1].append(0)
    return matrix
# Creation of a matrix environment
matrix = create_free_matrix(length, width)
# This variable is use as temporal holder for blocks that are taken by our imaginary hand :)
temp_holder = None
# The coordinates of blocks in the matrix environment
blocks = {"b1":(3, 0), 'b2':(2, 0), 'b5':(1, 0), 'b3':(3, 2), 'b4':(2, 2)}
# The state of the task
finish_state = False
def put_on(block1, block2):
    ''' This function trys to put block1 on block2 '''
    global blocks
    global matrix
    global temp_holder
    print(matrix)
    if matrix[blocks[block2][0]-1][blocks[block2][1]] != block1:
        if matrix[blocks[block2][0]-1][blocks[block2][1]] !=0:
            # Taking by the holder of the top of the block2
            AND_OR_TREE.append("clearing the top of {}".format(block2))
            grasp(matrix[blocks[block2][0]-1][blocks[block2][1]])
            move(block1, block2, get_rid_of=True)
        elif matrix[blocks[block1][0]-1][blocks[block1][1]] !=0:
            # Taking by the holder of the top of the block1
            for i in range(len(matrix)):
                if matrix[i][blocks[block1][1]] !=0:
                    AND_OR_TREE.append("clearing the top of {}".format(matrix[i+1][blocks[block1][1]]))
                    grasp(matrix[i][blocks[block1][1]])
                    move(block1, block2, get_rid_of=True)
                    break
        else:
            # Taking by the holder of block1
            AND_OR_TREE.append("putting {} on {}".format(block1, block2))
            grasp(block1)
            move(block1, block2, get_rid_of=False)
def grasp(block):
    ''' This function allows the holder to take a block '''
    global blocks
    global matrix
    global temp_holder
    # Taking by the holder of the block 1
    AND_OR_TREE.append("grasping {}".format(block))
    temp_holder = block
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == block:
                matrix[i][j] = 0
def move(block1, block2, get_rid_of=False):
    ''' This functions places the block1 depeneding on 3 cases:
            1. When the system must get rid of the blocks that are on top of block2
            2. When the system must get rid of the blocks that are on top of block1
            3. When the system must get put block1 on block2
    '''
    global blocks
    global matrix
    global temp_holder
    PUT_ON = None
    if get_rid_of==True:
        AND_OR_TREE.append("getting rid of {}".format(temp_holder))
        # Replacing the the block that is above block1 and placing in the first free place in the lowest level
        for i in range(len(matrix)-1, -1, -1):
            if temp_holder == None:
                break
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    matrix[i][j] = temp_holder
                    if i == len(matrix)-1:
                        PUT_ON = 'table'
                    else:
                        PUT_ON = matrix[i+1][j]
                    AND_OR_TREE.append("putting {} on {}".format(temp_holder, PUT_ON))
                    temp_holder = None
                    break
    else:
        AND_OR_TREE.append("placing the {} on the top of {}".format(block1, block2))
        # Placing the blcok1 on the top of the block2
        matrix[blocks[block2][0]-1][blocks[block2][1]] = temp_holder
    put_on(block1, block2)
# Placing the blocks in their places in matrix
for key in blocks:
    matrix[blocks[key][0]][blocks[key][1]] = key
put_on('b1', 'b3')
def cmd_handler(cmd):
    ''' This function sends questions to the system of 2 types:
            1. WHY
            2. HOW
        the system takes an action?
     '''
    if cmd.startswith("How did you"):
        # The brunch that analyses the 'HOW' questions
        if "clear top" in cmd:
            # The subbrunch - How a did you clear the top of X
            block = cmd.replace('How did you clear the top of', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "clearring the top of {}".format(block) in AND_OR_TREE[i]:
                    if i == len(AND_OR_TREE)+1:
                        print(AND_OR_TREE[i])
                    else:
                        print("By {}".format(AND_OR_TREE[i+1]))
        elif "grasp" in cmd:
            # The subbrunch - How did you grasped X
            block = cmd.replace('How did you grasp', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "grasping {}".format(block) in AND_OR_TREE[i]:
                    if i == len(AND_OR_TREE)+1:
                        print(AND_OR_TREE[i])
                    else:
                        print("By {}".format(AND_OR_TREE[i+1]))
        elif "get rid" in cmd:
            # The subbrunch - How did you get rid of X
            block = cmd.replace('How did you get rid of', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "getting rid of {}".format(block) in AND_OR_TREE[i]:
                    if i == len(AND_OR_TREE)+1:
                        print(AND_OR_TREE[i])
                    else:
                        print("By {}".format(AND_OR_TREE[i+1]))
        elif "put" in cmd:
            # The subbrunch - How did you put X on Y
            block = cmd.replace('How did you put', '')
            block = block.replace("?", '')
            block = block.split('on')
            block = [bl.replace(' ', '') for bl in block]
            for i in range(len(AND_OR_TREE)):
                if "putting {} on {}".format(block[0], block[1]) in AND_OR_TREE[i]:
                    if i == len(AND_OR_TREE)+1 or block[1] == 'table':
                        print('By {}'.format(AND_OR_TREE[i]))
                    else:
                        print('By {}'.format(AND_OR_TREE[i+1]))
    elif cmd.startswith("Why did you"):
        # The brunch that analyses the 'WHY' questions
        if "cleared the top" in cmd:
            # The subbrunch - Why did you cleared the top of X
            block = cmd.replace('Why did you cleared the top of', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "clearring the top of {}".format(block) in AND_OR_TREE[i]:
                    if i == 0:
                        print(AND_OR_TREE[i])
                    else:
                        block = AND_OR_TREE[i - 1].replace('putting', '')
                        block = block.split('on')
                        block = [bl.replace(' ', '') for bl in block]
                        print("Because I put {} on {}".format(block[0], block[1]))
        elif "grasp" in cmd:
            # The subbrunch - Why did you grasped X
            block = cmd.replace('Why did you grasped', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "grasping {}".format(block) in AND_OR_TREE[i]:
                    if i == 0:
                        print(AND_OR_TREE[i])
                    else:
                        block = AND_OR_TREE[i - 1].replace('clearing the top of', '')
                        block = block.replace("?", '')
                        block = block.replace(' ', '')
                        print("Because I have to clear the top of {}".format(block))
                        break
        elif "get rid" in cmd:
            # The subbrunch - Why did you get rid of X
            block = cmd.replace('Why did you get rid of', '')
            block = block.replace("?", '')
            block = block.replace(' ', '')
            for i in range(len(AND_OR_TREE)):
                if "getting rid of {}".format(block) in AND_OR_TREE[i]:
                    if i == 0:
                        print(AND_OR_TREE[i])
                    else:
                        block = AND_OR_TREE[i - 1].replace('grasping', '')
                        block = block.replace("?", '')
                        block = block.replace(' ', '')
                        print("Because I grasped {}".format(block))
        elif "put" in cmd:
            # The subbrunch - Why did you put X on Y
            block = cmd.replace('Why did you put', '')
            block = block.replace("?", '')
            block = block.split('on')
            block = [bl.replace(' ', '') for bl in block]
            for i in range(len(AND_OR_TREE)):
                if "putting {} on {}".format(block[0], block[1]) in AND_OR_TREE[i]:
                    if i == 0:
                        print('Because {}'.format(AND_OR_TREE[i]))
                    else:
                        if "getting rid of" in AND_OR_TREE[i - 1]:
                            block = AND_OR_TREE[i - 1].replace('getting rid of', '')
                            block = block.replace("?", '')
                            block = block.replace(' ', '')
                            print("Because I must get rid of {}".format(block))
                        elif "putting" in AND_OR_TREE[i - 1]:
                            block = AND_OR_TREE[i - 1].replace('putting', '')
                            block = block.split('on')
                            block = [bl.replace(' ', '') for bl in block]
                            print("Because I put {} on {}".format(block[0], block[1]))
    elif cmd == 'kill':
        # This command quits the program
        quit()
    else:
        # This branch activates when the command doesn't exist
        print("No such command !")
while True:
    cmd = input(">")
    cmd_handler(cmd)


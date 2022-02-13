""""
Team member:
nouran ahmed ibrahim
sama medhat farouk
menna tullah abdelhalem
nada yoseef abdelmo3z
yomnna atef abdelmon3m
abeer husien mohamed
"""
from ete3 import Tree

input_file_path = "distance matrix"
result_file_path = "result file"


def read_File():
    file = open(input_file_path, "r")
    matrix = [line.split(' ') for line in file.readlines()]
    file.close()
    return matrix


def update_file(new_Matrix, min_Ind):
    file = open(result_file_path, "a")
    min_Val = matrix[min_Ind[0]][min_Ind[1]]
    file.write('\nAlign ' + matrix[0][min_Ind[0]] + ' to ' + matrix[0][min_Ind[1]] + " with distance " + str(min_Val) + '\n')
    file.write('\n           *************\n')
    for row in new_Matrix:
        for cell in row:
            file.write(str(cell)+' ')
        file.write('\n')
    file.close()


def print_relation_file(tree):
    file = open(result_file_path, "a")
    file.write('\n'+tree)
    file.close()


def prepare_Matrix(unprepared_Matrix):
    unprepared_Matrix[0][-1] = unprepared_Matrix[0][-1][0:len(unprepared_Matrix[0][-1])-1]   # to remove \n from last cell in first row
    unprepared_Matrix[0].insert(0, ' ')   # insert ' ' cell at the first of the 1st row
    for ListIdx in range(1, len(unprepared_Matrix)):  # to convert every cell to num & remove \n from last cell in each row
        innerList = unprepared_Matrix[ListIdx]
        for idx in range(1, len(innerList)):
            if idx < (len(innerList) - 1):
                innerList[idx] = int(innerList[idx])
            else:
                innerList[idx] = int(innerList[idx][0:len(innerList)-1])
    return unprepared_Matrix


def find_Min():
    global relations
    min_idx = [2, 1]
    min_Value = matrix[2][1]
    for rowIdx in range(1, len(matrix)):
        innerList = matrix[rowIdx]
        for col_Idx in range(1,rowIdx):  # from 1 to row num to skip repeated value
            if innerList[col_Idx] < min_Value:
               min_idx = [rowIdx, col_Idx]
               min_Value = innerList[col_Idx]
    relations.append([matrix[0][min_idx[1]], matrix[0][min_idx[0]]])
    return min_idx


def prepare_new_Matrix():
    min_idx = find_Min()
    merged_Columns = matrix[0][min_idx[1]] + matrix[0][min_idx[0]]
    new_Matrix = [[] for row_Idx in range(len(matrix)-1)]
    new_Matrix[0].append(' ')
    new_Matrix[0].append(merged_Columns)
    new_Matrix[1].append(merged_Columns)
    x = 2

    for col_Idx in range(1, len(matrix[0])):
        if not(matrix[0][col_Idx] in merged_Columns):
            new_Matrix[0].append(matrix[0][col_Idx])

    for row_Idx in range(1, len(matrix)):
        if not (matrix[row_Idx][0] in merged_Columns):
            new_Matrix[x].append(matrix[row_Idx][0])
            x += 1

    for rowIdx in range(1, len(new_Matrix)):
        innerList = new_Matrix[rowIdx]
        for col_Idx in range(1, len(new_Matrix[0])):
            innerList.append(0)
    return [new_Matrix, min_idx]


def find_Cell_Value(row_char, min_Idx):
    summation = 0
    for row in range(1, len(matrix)):
        if matrix[row][0] == row_char:
           summation = matrix[row][min_Idx[0]] + matrix[row][min_Idx[1]]
           break
    return summation/2


def find_old_value(row_char, col_char):
    for row in range(1, len(matrix)):
        if matrix[row][0] == row_char:
            for col_idx in range(1, len(matrix[0])):
                if matrix[0][col_idx] == col_char:
                    return matrix[row][col_idx]


def update_matrix():
    new_Matrix, min_Idx = prepare_new_Matrix()

    for rowIdx in range(1, len(new_Matrix)):
        innerList = new_Matrix[rowIdx]
        for col_Idx in range(1, len(innerList)):
            if col_Idx == 1:
                innerList[col_Idx] = (find_Cell_Value(innerList[0], min_Idx))
            else:
                innerList[col_Idx] = (find_old_value(innerList[0], new_Matrix[0][col_Idx]))

    for rowIdx in range(2, len(new_Matrix)):
        new_Matrix[1][rowIdx] = new_Matrix[rowIdx][1]
    update_file(new_Matrix, min_Idx)
    return new_Matrix


def build_Phylogenetic_tree():
    global matrix
    while len(matrix) > 3:
        matrix = update_matrix()


def find_Relation(target_relation):
    for relation in relations:
        if target_relation in str(relation):
            r = relation
            relations.remove(r)
            return r


def create_Tree_Line():
    tree_Line = ''
    for char in str(relations[-1]):
        if char == '[':
            tree_Line = tree_Line + '('
        elif char == ']':
            tree_Line = tree_Line + ')'
        elif char == "'" or char == ' ':
            continue
        else:
            tree_Line = tree_Line + char

    tree_Line = tree_Line + ';'
    return tree_Line


def show_Graph():
    global relations
    relation_idx = 0
    while relation_idx != len(relations):
        relation = relations[relation_idx]
        deleted = False
        decreasing_value = -1
        for idx in range(len(relation)):
           if len(relation[idx]) > 1:
               deleted = True
               decreasing_value += 1
               relation[idx] = find_Relation(relation[idx][-1])
        if not deleted:
            relation_idx += 1
        else:
            relation_idx -= decreasing_value

    treeline = create_Tree_Line()
    print_relation_file(treeline)
    tree = Tree(treeline)
    tree.show()


rela
tions = []
matrix = prepare_Matrix(read_File())
build_Phylogenetic_tree()
relations.append([matrix[0][1], matrix[0][2]])
show_Graph()

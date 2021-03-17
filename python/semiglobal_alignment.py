import numpy as np
import global_alignment

# LLENA LA PRIMER FILA Y LA PRIMER COLUMNA DE LA MATRIZ CON LOS VALORES CORRESPONDIENTES
def fill_first_values():
    # FILL FIRST ROW
    first_line = global_alignment.matrix[0]
    for column in range(1, len(first_line)):
        first_line[column] = first_line[column-1] + 0
    global_alignment.matrix[0] = first_line

    # FILL FIRST COLUMN
    for row in range(1, len(global_alignment.matrix)):
        global_alignment.matrix[row][0] = global_alignment.matrix[row-1][0]+ 0


# OBTIENE EL NuMERO MaXIMO DE LA uLTIMA FILA Y COLUMNA
def max_number_semiglobal():
    amount_rows = len(global_alignment.matrix)-1
    num_max_row = max(global_alignment.matrix[amount_rows])
    last_numb_col = []
    i = 0

    while amount_rows >= 0:
        amount_rows = amount_rows + -1
        row = global_alignment.matrix[i]
        i = i + 1
        last_numb_col += [row[-1]]

    col_max = max(last_numb_col)
    num_max = max(col_max, num_max_row)
    return num_max

# CONSTRUYE EL ALINEAMIENTO OPTIMO CON LOS PUNTAJES DE LA MATRIZ
def traceback(sequence1, sequence2):
    alignments = []
    alignmentA = ""
    alignmentB = ""
    i = len(sequence2)-1
    j = len(sequence1)-1

    max_number = max_number_semiglobal()


    try:
        j = global_alignment.matrix[len(global_alignment.matrix)-1].index(max_number)
        i = len(global_alignment.matrix)-1
    except:
        j = len(global_alignment.matrix[0])-1
        i=0
        while True:
            if(global_alignment.matrix[i][j]==max_number):
                break
            i += 1

    while(i>0 or j>0):
        if(i>0 and j>0 and global_alignment.matrix[i][j] == global_alignment.matrix[i-1][j-1] +
        global_alignment.getScore(sequence1, sequence2, i, j)):
            alignmentA = sequence1[j] + alignmentA
            alignmentB = sequence2[i] + alignmentB
            global_alignment.matrix[i][j] = 'D'+str(global_alignment.matrix[i][j])

            i = i-1
            j = j-1
        elif((i>0 and global_alignment.matrix[i][j] == global_alignment.matrix[i-1][j] + global_alignment.GAP) or j==0):
            alignmentA = "--" + alignmentA
            alignmentB = sequence2[i] + alignmentB
            global_alignment.matrix[i][j] = "A" + str(global_alignment.matrix[i][j])

            i = i-1
        elif((j>0 and global_alignment.matrix[i][j] == global_alignment.matrix[i][j-1] + global_alignment.GAP) or i==0):
            alignmentA = sequence1[j] + alignmentA
            alignmentB = "--" + alignmentB
            global_alignment.matrix[i][j] = "I"+str(global_alignment.matrix[i][j])

            j = j-1

    alignments.append(alignmentA)
    alignments.append(alignmentB)
    global_alignment.add_sequences(sequence1, sequence2)
    return alignments

# EJECUTA EL ALGORITMO COMPLETO
def semiglobal_alignment(sequence1, sequence2, newMatch, newMismatch, newGap):
	global_alignment.setValues(newMatch, newMismatch, newGap)
	global_alignment.clean_matrix()
	global_alignment.init_matrix(sequence1, sequence2) # INICIALIZA LA MATRIZ DE PUNTAJES CON CEROS
	fill_first_values() # LLENA LA PRIMER FILA Y LA PRIMERA COLUMNA
	global_alignment.fill_matrix(sequence1, sequence2) # CALCULA TODOS LOS PUNTAJES
	new_col = max_number_semiglobal()
	alignments = traceback(["--"]+sequence1,["--"]+sequence2) # OBTIENE EL ALINEAMIENTO OPTIMO
	alignments.append(global_alignment.alignmentScore(alignments[0], alignments[1]))
	return alignments

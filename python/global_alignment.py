# VARIABLES GLOBALES
global MISMATCH
global MATCH
global GAP

MISMATCH = -1
MATCH = 1
GAP = -2

matrix = []

def clean_matrix():
	global matrix
	matrix = []

# MODIFICA LOS VALORES DE MATCH, MISMATCH Y GAP SI EL USUARIO LO SOLICITA
def setValues(new_match, new_mismatch, new_gap):
	global MISMATCH
	global MATCH
	global GAP

	MISMATCH = int(new_mismatch)
	MATCH = int(new_match)
	GAP = int(new_gap)

# INICIALIZA LA MATRIZ DE PUNTAJES CON CEROS
def init_matrix(sequence1, sequence2):
	global matrix

	columns = len(sequence1) + 1
	rows = len(sequence2) + 1

	for row in range(0, rows):
		r = []
		for column in range(0, columns):
			r.append(0)
		matrix.append(r)

# LLENA LA PRIMER FILA Y LA PRIMER COLUMNA DE LA MATRIZ CON LOS VALORES CORRESPONDIENTES
def fill_first_values():
	global matrix

	# FILL FIRST ROW
	first_line = matrix[0]
	for column in range(1, len(first_line)):
		first_line[column] = first_line[column-1] + GAP
	matrix[0] = first_line

	# FILL FIRST COLUMN
	for row in range(1, len(matrix)):
		matrix[row][0] = matrix[row-1][0]+ GAP

# INSERTA UN GAP EN UNA SECUENCIA, DADA UNA POSICION ESPECIFICA
def insert_gap(sequence, position):
	new_sequence = sequence[:position] + ['--'] + sequence[position:]
	return new_sequence

# OBTIENE EL PUNTAJE DE LA DIAGONAL
def getScore(sequence1, sequence2, row, col):
	if(sequence1[col] == sequence2[row]):
		return MATCH
	return MISMATCH

# CALCULA LOS PUNTAJES PARA TODA LA MATRIZ
def fill_matrix(sequence1, sequence2):
	global matrix
	sequence1 = insert_gap(sequence1, 0)
	sequence2 = insert_gap(sequence2, 0)

	num_rows = len(matrix)
	for i in range(1,num_rows):
		num_cols = len(matrix[i])
		for j in range(1, num_cols):
			up = matrix[i-1][j] + GAP
			left = matrix[i][j-1] + GAP
			diagonal = matrix[i-1][j-1] + getScore(sequence1, sequence2, i, j)

			matrix[i][j] = max(up, left, diagonal)

def add_sequences(sequence1, sequence2):
	global matrix

	first_row = list(sequence1)
	first_row.insert(0, " ")
	matrix.insert(0, first_row)

	for row in range(1, len(matrix)):
		matrix[row].insert(0, sequence2[row-1])

# CONSTRUYE EL ALINEAMIENTO OPTIMO CON LOS PUNTAJES DE LA MATRIZ
def traceback(sequence1, sequence2):
	alignments = []
	alignmentA = ""
	alignmentB = ""
	i = len(sequence2)-1
	j = len(sequence1)-1

	while(i>0 or j>0):
		if(i>0 and j>0 and matrix[i][j] == matrix[i-1][j-1] + getScore(sequence1, sequence2, i, j)):
			alignmentA = sequence1[j] + alignmentA
			alignmentB = sequence2[i] + alignmentB
			matrix[i][j] = 'D'+str(matrix[i][j])
			i = i-1
			j = j-1
		elif(i>0 and matrix[i][j] == matrix[i-1][j] + GAP):
			alignmentA = "--" + alignmentA
			alignmentB = sequence2[i] + alignmentB
			matrix[i][j] = "A" + str(matrix[i][j])
			i = i-1
		else:
			alignmentA = sequence1[j] + alignmentA
			alignmentB = "--" + alignmentB
			matrix[i][j] = "I"+str(matrix[i][j])
			j = j-1

	alignments.append(alignmentA)
	alignments.append(alignmentB)

	add_sequences(sequence1, sequence2)
	return alignments

# OBTIENE EL PUNTAJE DEL ALINEAMIENTO
def alignmentScore(alignmentA, alignmentB):
	score = 0
	s = ""
	for i in range(0, len(alignmentA),2):
		if(alignmentA[i:i+2] == alignmentB[i:i+2]):
			score += MATCH
		elif(alignmentA[i:i+2] == "--" or alignmentB[i:i+2] == "--"):
			score += GAP
		else:
			score += MISMATCH
	return score

# EJECUTA EL ALGORITMO COMPLETO
def needleman_wunsch(sequence1, sequence2, newMatch, newMismatch, newGap):
	setValues(newMatch, newMismatch, newGap)
	clean_matrix()
	init_matrix(sequence1, sequence2) # INICIALIZA LA MATRIZ DE PUNTAJES CON CEROS
	fill_first_values() # LLENA LA PRIMER FILA Y LA PRIMERA COLUMNA
	fill_matrix(sequence1, sequence2) # CALCULA TODOS LOS PUNTAJES

	alignments = traceback(["--"]+sequence1,["--"]+sequence2) # OBTIENE EL ALINEAMIENTO OPTIMO
	alignments.append(alignmentScore(alignments[0], alignments[1]))
	return alignments

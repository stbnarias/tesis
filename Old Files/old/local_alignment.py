import global_alignment
import numpy as np

def fill_matrix(sequence1, sequence2):
     sequence1 = global_alignment.insert_gap(sequence1, 0)
     sequence2 = global_alignment.insert_gap(sequence2, 0)
 
    #  print(sequence1)
    #  print(sequence2)
 
     num_rows = len(global_alignment.matrix)
     for i in range(1,num_rows):
         num_cols = len(global_alignment.matrix[i])
         for j in range(1, num_cols):
             up = global_alignment.matrix[i-1][j] + global_alignment.GAP
             left = global_alignment.matrix[i][j-1] + global_alignment.GAP
             diagonal = global_alignment.matrix[i-1][j-1] + global_alignment.getScore(sequence1, sequence2, i, j)
 
             global_alignment.matrix[i][j] = max(up, left, diagonal, 0)

# CONSTRUYE EL ALINEAMIENTO OPTIMO CON LOS PUNTAJES DE LA MATRIZ
def traceback(sequence1, sequence2):
    alignments = []
    alignmentA = ""
    alignmentB = ""

    argmax = np.where(global_alignment.matrix == np.matrix(global_alignment.matrix).max())
    i = argmax[0][0]
    j = argmax[1][0]

    while((i>0 or j>0) and global_alignment.matrix[i][j] != 0):
        if(i>0 and j>0 and global_alignment.matrix[i][j] == global_alignment.matrix[i-1][j-1] + global_alignment.getScore(sequence1, sequence2, i, j)):
            alignmentA = sequence1[j] + alignmentA
            alignmentB = sequence2[i] + alignmentB
            global_alignment.matrix[i][j] = 'D'+str(global_alignment.matrix[i][j]) #CAMINO
            i = i-1
            j = j-1
        elif(i>0 and global_alignment.matrix[i][j] == global_alignment.matrix[i-1][j] + GAP):
            alignmentA = "--" + alignmentA
            alignmentB = sequence2[i] + alignmentB
            global_alignment.matrix[i][j] = "A" + str(global_alignment.matrix[i][j]) #CAMINO
            i = i-1
        else:
            alignmentA = sequence1[j] + alignmentA
            alignmentB = "--" + alignmentB
            global_alignment.matrix[i][j] = "I"+str(global_alignment.matrix[i][j]) #CAMINO
            j = j-1

    alignments.append(alignmentA)
    alignments.append(alignmentB)
    
    global_alignment.add_sequences(sequence1, sequence2)
    return alignments

# EJECUTA EL ALGORITMO COMPLETO
def local_alignment(sequence1, sequence2):
	global_alignment.clean_matrix()
	global_alignment.init_matrix(sequence1, sequence2) # INICIALIZA LA MATRIZ DE PUNTAJES CON CEROS
	fill_matrix(sequence1, sequence2) # CALCULA TODOS LOS PUNTAJES
	alignments = traceback(["--"]+sequence1,["--"]+sequence2) # OBTIENE EL ALINEAMIENTO OPTIMO
	alignments.append(global_alignment.alignmentScore(alignments[0], alignments[1]))
	return alignments

# UPDATE: Test case for Metabolic-Pathways, by @kecastro.
#ROUTE0 = 'ABCDEFGHIJ'
#ROUTE1 = 'KLMNOPQRST'
#print(local_alignment(ROUTE0, ROUTE1))
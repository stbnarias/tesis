__author__ = 'marti'
import Util

#---General parameters---#
MAX_PATHS = 1000
tinvScoreThreshold = 0.8
compute_paths_tree = True
align_tinvariants_reactions = True # if set to true, this program will compute an alignment similar to the proper MP-Align
# If compute_paths_tree is False, paths'll be computed, but paths_tree won't be in the output
skip_align = False
reversed_reactions_canbe_initial_nodes = True
simReact_enzimes_weight = 0.4
simReact_inputs_weight = 0.3
simReact_outputs_weight = 0.3

#---Batch alignment (loaded if no arguments specified)---#
# To load organisms from CSV, insert Util.loadFromCSV("path/to/file.csv", "delimiterChar", columnNumber, rowsToSkip, maxNumber)
# Keep in mind that organism_from must be only one organism, so if you load from CSV, a list is returned and you have to index it
# organism_from = 'hsa' #Util.loadFromCSV("Extras/Eukaryotes.csv", " ", 0, 1, 1)[0]
# organism_to = ['oaa','xla','tgu','smm','bdi','mja','afu']
# paths = ['00020']
#-----------------------------------------------------------

# organism_from = 'ani'
# organism_to = ['pan']
# paths = ['00254']

organism_from = "PWY-5100"
organism_to = ["PWY-5600"]
paths = [""]


#---Directories---#
results_path_part1 = 'TFG/TMPAlign/Results/'
results_path_part2 = 'Path_Info/'
results_path = results_path_part1 + results_path_part2
summary_file_cache = results_path_part1 + 'summaryCache.pkl'
summary_file = results_path_part1 + 'summary.csv'
ec_path = results_path_part1 + 'ECs/'
alignment_path = results_path_part1 + 'Align/'
alignment_info_path = alignment_path + 'T-inv-Alignament_SUMMARY/'
libraries_path = 'Libraries/'
cache_folder = results_path_part1 + "Scorecache/"
comp_cache = "compscore.pkl"
react_cache = "reactscore.pkl"
comp_info_file = "compound2"

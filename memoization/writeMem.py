import csv 

'''
This script was made to record all the outputs
'''

def write(seq1,seq2,n,time):
    with open('results_mem.csv', 'a') as f:        #MUDAR ISTO 
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        #writer.writerow(["language_detected","file","k","alpha","n_words","time","correct","wrong"])
        
        #falta ir por a cruz no ficheiro
        writer.writerow([seq1,seq2,n,time])


#h = "../seqs/seq1.txt"
#f = open(h).read()
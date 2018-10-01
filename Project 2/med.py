import sys;

'''Function to create a matrix of the required lengths'''
def matrixer(source, target):
    n = len(source);
    m = len(target);
    matrix = [[0 for j in range(m + 1)] for i in range(n + 1)]; 
    return matrix;


'''Function to calculate the substitution cost'''
def sub_cost(i,j, source,target):
    if source[i - 1] == target[j - 1]:
        subs = 0;
    elif source[i - 1] != target[j - 1]:
        subs = 2;
    return subs;


'''Function to fill and find minimum path through matrix'''
def main(source, target):
    source = source.lower();
    target = target.lower();
    matrix = matrixer(source, target);
    matrix[0][0] = 0;
    DEL = 1;
    INS = 1;
    for i in range (1,len(source) + 1):
        matrix[i][0] = matrix[i-1][0] + DEL;
    for j in range (1, len(target) + 1):
        matrix[0][j] = matrix[0][j-1] + INS;

    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            matrix[i][j] = min((matrix[i-1][j] + DEL),(matrix[i-1][j-1] + sub_cost(i,j, source, target)),(matrix[i][j-1] + INS))
    
    print("The Minimum Edit Distance between " + source + " and " + target + " is " + str(matrix[len(source)][len(target)]));
            

'''Run from commandline in the form: python(3) med.py source_word target_word'''
if __name__ == "__main__":
    source = str(sys.argv[1]);
    target = str(sys.argv[2]);
    main(source, target);
    

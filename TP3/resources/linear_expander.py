def wacky_format(list):
    return "   "+str(list).strip("[]").replace(",","  ")+"\n"

M = [[2,3,-1],[1,-2,2],[2,-4,4]]
Y = [7,-1,-2]
MAX_SCALAR = 5

input_file = open("resources/linear.txt","w")
output_file = open("resources/zeta_linear.txt","w")

for i in range(0,len(M)):
    for scalar in range(0,MAX_SCALAR):
        aux_m = []
        aux_y = Y[i]*(scalar+1)
        for k in range(0, len(M[0])):
            aux_m.append(M[i][k]*(scalar+1))

        M.append(aux_m)
        Y.append(aux_y)
        input_file.write(wacky_format(aux_m))
        output_file.write(wacky_format(aux_y))
for i in range(0, len(M)):
    for j in range(0, len(M)):
        aux_m = []
        aux_y = Y[i]+Y[j]
        for k in range(0, len(M[0])):
            aux_m.append(M[i][k]+M[j][k])
        
        input_file.write(wacky_format(aux_m))
        output_file.write(wacky_format(aux_y))

input_file.close()
output_file.close()

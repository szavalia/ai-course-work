from main import __main__ as genetic_algorithm

RUNS = 10

for i in range(0, RUNS):
    print('------------------------------------------------------')
    print('RUN NUMBER '+str(i+1))
    genetic_algorithm(i+1)
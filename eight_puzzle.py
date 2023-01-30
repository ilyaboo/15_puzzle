#
# eight_puzzle.py (Final project)
#
# driver/test code for state-space search on Eight Puzzles   
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
        searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()



def  process_file(filename, algorithm, param):
    """ opens the file with the specified filename for reading, and uses
    a loop to process the file one line at a time """
    num_puzzles_solved = 0
    moves_in_solutions = []
    states_tested = []
    file = open(filename, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        searcher = create_searcher(algorithm, param)
        soln = None
        try:
            init_state = State(Board(lines[i]), None, 'init')
            soln = searcher.find_solution(init_state)
            if soln == None:
                print(lines[i] + ': no solution')
            else:
                num_puzzles_solved += 1
                moves_in_solutions += [soln.num_moves]
                states_tested += [searcher.num_tested]
                s = lines[i] + ': '
                s += str(soln.num_moves)
                s += ' moves, '
                s += str(searcher.num_tested)
                s += ' states tested'
                print(s)
        except KeyboardInterrupt:
            print(lines[i] + ': search terminated, no solution')
    print()
    print('solved ' + str(num_puzzles_solved) + ' puzzles')
    if num_puzzles_solved != 0:
        avg_moves = sum(moves_in_solutions) / num_puzzles_solved
        avg_states_tested = sum(states_tested) / num_puzzles_solved
        print('averages: ' + str(avg_moves) + ' moves, ' + str(avg_states_tested)\
              + ' states tested')
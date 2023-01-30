#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """ constructs a new Searcher object """
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
        
        

    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    
    
    def add_state(self, new_state):
        """ takes a single State object called new_state and adds it 
        to the Searcher‘s list of untested states """
        self.states += [new_state]
    
    
    
    def should_add(self, state):
        """ takes a State object called state and returns True if the
        called Searcher should add state to its list of untested states,
        and False otherwise """
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        elif state.creates_cycle() == True:
            return False
        return True
    
    
    
    def add_states(self, new_states):
        """ takes a list State objects called new_states, 
        and that processes the elements of new_states one at a time """
        for state in new_states:
            if self.should_add(state) == True:
                self.add_state(state)
    
    
    
    def next_state(self):
        """ chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
            """
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    
    
    def find_solution(self, init_state):
        """ performs a full state-space search that begins at the specified 
        initial state init_state and ends when the goal state is found or 
        when the Searcher runs out of untested states """
        self.add_state(init_state)
        while len(self.states) > 0:
            state = self.next_state()
            self.num_tested += 1
            if state.is_goal() == True:
                return state
            succ = state.generate_successors()
            succ_to_add = []
            for i in range(len(succ)):
                if self.should_add(succ[i]) == True:
                    succ_to_add += [succ[i]]
            self.add_states(succ_to_add)
        return None

### Add your BFSeacher and DFSearcher class definitions below. ###
    

class BFSearcher(Searcher):
    """ a class called BFSearcher for searcher objects that
    perform breadth-first search (BFS) """
    
    
    
    def next_state(self):
        """ overrides (i.e., replaces) the next_state method that is
        inherited from Searcher. Rather than choosing at random from the
        list of untested states, this version of next_state should follow
        FIFO (first-in first-out) ordering – choosing the state that has been 
        in the list the longest """
        s = self.states[0]
        self.states.remove(s)
        return s



class DFSearcher(Searcher):
    """ a class called DFSearcher for searcher objects that 
    erform depth-first search (DFS) """
    
    
    
    def next_state(self):
        """ follow LIFO (last-in first-out) ordering – choosing the state 
        that was most recently added to the list """
        s = self.states[-1]
        self.states.remove(s)
        return s
    
                
        
            
            

def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###

def h1(state):
    """ takes a State object called state, and that computes and returns
    an estimate of how many additional moves are needed to get from state
    to the goal state """
    ans = state.board.num_misplaced()
    return ans



def h2(state):
    """ uses how_far_misplaced() from the board class to estimate the number
    of moves required to put the tiles on the goal places """
    ans = state.board.how_far_misplaced()
    return ans
    


class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###
    def __init__(self, heuristic):
        """ constructs a new GreedySearcher object """
        super().__init__(-1)
        self.heuristic = heuristic
        
        

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s



    def priority(self, state):
        """ computes and returns the priority of the specified state, 
        based on the heuristic function used by the searcher """
        return -1 * self.heuristic(state)



    def add_state(self, state):
        """ adds a sublist that is a [priority, state] pair, where priority
        is the priority of state that is determined by calling the 
        priority method """
        element = []
        element += [self.priority(state)]
        element += [state]
        self.states += [element]



    def next_state(self):
        """ should choose one of the states with the highest priority """
        state_pair = max(self.states)
        self.states.remove(state_pair)
        return state_pair[1]






### Add your AStarSeacher class definition below. ###

class AStarSearcher(GreedySearcher):
    """ informed search algorithm that assigns a priority to a state 
    taking into account the cost that has already been expended to get to 
    that state """
    
    
    
    def priority(self, state):
        """ computes and returns the priority of the specified state, 
        based on the heuristic function used by the searcher """
        ans = -1 * (self.heuristic(state) + state.num_moves)
        return ans
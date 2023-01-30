#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        counter = 0
        for i in range(3):
            for j in range(3):
                self.tiles[i][j] = digitstr[counter]
                if digitstr[counter] == '0':
                    self.blank_r = i
                    self.blank_c = j
                counter += 1

    ### Add your other method definitions below. ###
    
    
    
    def __repr__(self):
        """ returns a string representation of a Board object """
        s = ''
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == '0':
                    s += '_'
                    s += ' '
                else:
                    s += self.tiles[i][j]
                    s += ' '
            s += '\n'
        return s
    
    
    
    def move_blank(self, direction):
        """ attempts to modify the contents of the called Board 
        object accordingly """
        if direction not in ['up', 'down', 'left', 'right']:
            return False
        temp_c = self.blank_c
        temp_r = self.blank_r
        if direction == 'left':
            temp_c = self.blank_c - 1
            if temp_c < 0:
                return False
        elif direction == 'right':
            temp_c = self.blank_c + 1
            if temp_c > 2:
                return False
        elif direction == 'up':
            temp_r = self.blank_r - 1
            if temp_r < 0:
                return False
        elif direction == 'down':
            temp_r = self.blank_r + 1
            if temp_r > 2:
                return False
        self.tiles[self.blank_r][self.blank_c] = self.tiles[temp_r][temp_c]
        self.tiles[temp_r][temp_c] = '0'
        self.blank_c = temp_c
        self.blank_r = temp_r
        return True
    
    
    
    def digit_string(self):
        """ creates and returns a string of digits that corresponds to the 
        current contents of the called Board object’s tiles attribute """
        s = ''
        for i in range(3):
            for j in range(3):
                s += self.tiles[i][j]
        return s
    
    
    
    def copy(self):
        """ returns a newly-constructed Board object that is 
        a deep copy of the called object """
        string = self.digit_string()
        b = Board(string)
        return b
    
    
    
    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board 
        object that are not where they should be in the goal state """
        ans = 0
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] != GOAL_TILES[i][j] and self.tiles[i][j] \
                    != '0':
                    ans += 1
        return ans
    
    
    
    def __eq__(self, other):
        """ called when the == operator is used to compare two 
        Board objects """
        if self.tiles == other.tiles:
            return True
        return False
    
    
    
    def how_far_misplaced(self):
        """ analog of num_misplaced which instead of just calculating the
        number of musplaced tiled and suming them up, sums up the distances 
        between misplaced tiles and their positions (distance is calculated
        by the minimal number of moves required to put the tile to its
        correct position) """
        ans = 0
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] != GOAL_TILES[i][j] and self.tiles[i][j] \
                    != '0':
                    distance = 0
                    correct_row = int(self.tiles[i][j]) // 3
                    correct_column = int(self.tiles[i][j]) % 3
                    distance = abs(correct_row - i) + abs(correct_column - j)
                    ans += distance
        return ans
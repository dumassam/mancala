from typing import List

class Player:
    """Represents a player for the game."""
    
    def __init__(self, p_num: int, p_name: str, p_side: str) -> None:
        """Initialize a player."""
        self.num = p_num
        self.name = p_name
        self.side = p_side

class Pockets:
    """Represents a mancala store or pocket for a mancala board."""
    
    def __init__(self, num_stones: int, idd: str) -> None:
        """Initialize a mancala pocket."""
        self.ns = num_stones
        self.idd = idd
        
    def __str__(self) -> str:
        """Returns a str representation of any type of mancala pocket."""
        if self.ns > 9:
            return str(self.ns)
        return str(self.ns) + ' '
        
        
    def add(self, num_stones: int = 1) -> None:
        """Adds <num_stones> to <self.ns>. <num_stones> has a default value of 
        1.
        >>> p = Pockets(4, '1R')
        >>> p.add()
        >>> p.ns
        5
        >>> p.add(2, '1R')
        >>> p.ns
        7
        """
        self.ns += num_stones
        
        
class Pocket(Pockets):
    """Represents a pocket on a mancala board.
    >>> p = Pocket(5, '1R')
    >>> p.is_empty()
    False
    >>> p = Pocket(0, '1R')
    >>> p.is_empty()
    True
    """
    
    def is_empty(self) -> bool:
        """Returns True iff <self.ns> is equal to 0."""
        if self.ns == 0:
            return True
        return False
    
    def remove(self, num_stones: int = 1) -> None:
        """Removes <num_stones> to <self.ns>. <num_stones> has a default value 
        of 1.
        >>> p = Pocket(4, '1R')
        >>> p.remove()
        >>> p.ns
        3
        >>> p.remove(2, '1R')
        >>> p.ns
        1
        """
        self.ns -= num_stones
        
class MancalaStore(Pockets):
    """Represents a mancala store on a mancala board."""
    
    def __init__(self, idd: str) -> None:
        """Initialize a MancalaStore with 0 stones."""
        self.ns = 0
        self.idd = idd
        
class MancalaBoard:
    """Represents a mancala board."""
    
    def __init__(self) -> None:
        """Initialize a MancalaBoard."""
        self.left = [Pocket(4, '6L'), Pocket(4, '5L'), Pocket(4, '4L'), 
                     Pocket(4, '3L'), Pocket(4, '2L'), Pocket(4, '1L')]
        self.right = [Pocket(4, '6R'), Pocket(4, '5R'), Pocket(4, '4R'), 
                      Pocket(4, '3R'), Pocket(4, '2R'), Pocket(4, '1R')]
        self.p1_store = MancalaStore('1S')
        self.p2_store = MancalaStore('2S')
        self.full = self.left + [self.p1_store] + self.right + [self.p2_store]
        
    def __str__(self) -> str:
        """Return a str representation of a MancalaBoard."""
        num_l = ' |   |  / {0}\   / {1}\   / {2}\   / {3}\   / {4}\ ' + \
                '  / {5}\  |   |\n'
        store_l = ' | {0}|                                              ' + \
            '   | {1}|\n'
        l1 = '         1L      2L      3L      4L      5L      6L         \n' 
        l2 = '  ___    ___     ___     ___     ___     ___     ___    ___ \n'
        l3 = num_l.format(self.left[5], self.left[4], self.left[3],
                          self.left[2], self.left[1], self.left[0])
        l4 = ' |   |  \___/   \___/   \___/   \___/   \___/   \___/  |   |\n'
        l5 = store_l.format(self.p1_store, self.p2_store)
        l6 = ' |   |   ___     ___     ___     ___     ___     ___   |   |\n'
        l7 = num_l.format(self.right[0], self.right[1], self.right[2],
                          self.right[3], self.right[4], self.right[5])
        l8 = ' |___|  \___/   \___/   \___/   \___/   \___/   \___/  |___|\n'
        l9 = '         6R      5R      4R      3R      2R      1R         \n' 
        return l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9
        
    def pocket_order(self, pocket: 'Pocket') -> List['Pockets']:
        """Return the order of stone placement starting from <pocket>.
        >>> m = MancalaBoard()
        >>> m.pocket_order(m.left[5])
        """
        if 'L' in pocket.idd:
            i = self.left.index(pocket)
            lst = self.left[i:] + [self.p1_store] + self.right + \
            self.left[:i + 1]
            return lst[1:]
        else:
            i = self.right.index(pocket)
            lst = self.right[i:] + [self.p2_store] + self.left + \
            self.right[:i + 1]
            return lst[1:]
        
    def idd_to_poc(self, idd: str) -> 'Pocket':
        """Returns the Pocket that matches <idd>."""
        num = int('-' + idd[0])
        if 'L' in idd:
            return self.left[num]
        return self.right[num]
    
    def idd_to_opp(self, idd: str) -> str:
        """Returns the pocket opposite to <idd>."""
        if 'L' in idd:
            return str(7 - int(idd[0])) + 'R'
        return str(7 - int(idd[0])) + 'L'
        
    def move(self, pocket: 'Pocket') -> 'Pocket':
        """Applies the move made if <pocket> is chosen."""
        i = 0
        m_lst = self.pocket_order(pocket)
        while pocket.ns > 0:
            m_lst[i].add()
            last_pocket = m_lst[i]
            pocket.remove()
            if i == (len(m_lst) - 1):
                i = 0
            else:
                i += 1
        return last_pocket
    
    def steal(self, idd: str) -> None:
        """Represents a steal move in a game."""
        if 'L' in idd and self.right[int(idd[0])-7].ns != 0:
            self.idd_to_poc(idd).ns = 0
            n = self.right[int(idd[0])-7].ns
            self.right[int(idd[0])-7].remove(n)
            self.p1_store.ns += n + 1
        elif 'R' in idd and self.left[int(idd[0])-7].ns != 0:
            self.idd_to_poc(idd).ns = 0
            n = self.left[int(idd[0])-7].ns
            self.left[int(idd[0])-7].remove(n)
            self.p2_store.ns += n + 1
            
    def game_over(self) -> bool:
        """Returns True iff the game is over."""
        sum1 = 0
        sum2 = 0
        for i in range(6):
            sum1 += self.left[i].ns
            sum2 += self.right[i].ns
        return sum1 == 0 or sum2 == 0
    
    def remaining_stones(self) -> None:
        """Add the remaining stones to their respective store."""
        sum1 = 0
        sum2 = 0
        for i in range(6):
            sum1 += self.left[i].ns
            self.left[i].ns = 0
            sum2 += self.right[i].ns
            self.right[i].ns = 0
        self.p1_store.ns += sum1
        self.p2_store.ns += sum2
    
    def winner(self) -> str:
        """Returns the winner of the game."""
        if self.p1_store.ns == self.p2_store.ns:
            return "Tie!"
        elif self.p1_store.ns > self.p2_store.ns:
            return "Player 1!"
        return "Player 2!"
    
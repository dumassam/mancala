import mancala_functions as mf

def next_player(cp: 'Player', p1: 'Player', p2: 'Player') -> 'Player':
    """Returns the next player to play."""
    if cp == p1:
        return p2
    return p1

m = mf.MancalaBoard()
p1_name = input('Player 1\'s name: ')
p2_name = input('Player 2\'s name: ')
p1 = mf.Player(1, p1_name, 'L')
p2 = mf.Player(2, p2_name, 'R')
rules = '\nPlay always moves around the board in a counter-clockwise circle' +\
        ' (to the right). \n' +\
        'The store on your right belongs to you. That is where you keep the' +\
        'seeds you win. \n' +\
        'Only put stones in your own store, not your opponent’s store. \n' +\
        'Once a pocket is moved, a singular stone is placed in each pocket' +\
        'following the one moved until there are no more stones to play. \n'

check_rules = input('Would you like to see the rules before the game starts? ')
if check_rules == 'Yes':
    print(rules)
else:
    print('\nLet\'s Start!\n')
current_player = p1
while not m.game_over():
    print('\nIt is ' + current_player.name + '\'s turn!')
    print(m)
    move_made = False
    while move_made is False:
        move = input('What will be your move? ')
        pocket = m.idd_to_poc(move)
        if current_player.side in move and pocket.ns != 0:
            move_made = True
            last_p = m.move(pocket)
            opp = m.idd_to_opp(last_p.idd)
            if 'S' in last_p.idd:
                print('\nFree Turn!')
            elif last_p.ns == 1 and m.idd_to_poc(opp).ns != 0 \
                 and last_p.idd[1] == current_player.side :
                m.steal(last_p.idd)
                current_player = next_player(current_player, p1, p2)
                print('\nNice Steal!')
            else:
                current_player = next_player(current_player, p1, p2)

m.remaining_stones()
print(m)
print('\n{0} has {1} stones!'.format(p1.name, m.p1_store.ns))
print('\n{0} has {1} stones!'.format(p2.name, m.p2_store.ns))
input()
        
from copy import deepcopy
import math
import time

first_player_number = 1
second_player_number = 2

def get_neighbors(coords, boardIndexes):

    mapIndexes = boardIndexes.keys()

    x = coords[0]
    y = coords[1]
    
    neighbors = []

    if (x + 1, y) in mapIndexes:
        neighbors.append((x + 1, y))

    if (x - 1, y) in mapIndexes:
        neighbors.append((x - 1, y))

    if (x, y + 1) in mapIndexes:
        neighbors.append((x, y + 1))

    if (x, y - 1) in mapIndexes:
        neighbors.append((x, y - 1))

    if (x - 1, y - 1) in mapIndexes:
        neighbors.append((x - 1, y - 1))

    if (x + 1, y + 1) in mapIndexes:
        neighbors.append((x + 1, y + 1))


    return neighbors

#------------------------------------------------------------------------------------




class Bot():

    def __init__(self, player_num, field_size):

        global first_player_number
        global second_player_number

        self.player_number = player_num
        
        if self.player_number == first_player_number:
            self.color = 1
            self.anticolor = -1
            self._12rule = True
            
        elif self.player_number == second_player_number:
            self.color = -1
            self.anticolor = 1
            self._12rule = False
  
            
        self.field_size = field_size + 1

        self.map = {}
        self.generate_map()

        self.all_previous_boards = []

        self.enemy_move = ((),())

        self.maxdepth = 2

        self.numberOfOperations = 0
                  
        

#------------------------------------------------------------------------------------

    def recieve_move(self, turn):

        if turn[0] != ():
            self.map[turn[0]] = 1 * self.anticolor  

        if turn[1] != ():
            self.map[turn[1]] = 2 * self.anticolor

        self.enemy_move = tuple(turn)

            
        self.all_previous_boards.append(deepcopy(self.map))
        self.remove_chips(self.anticolor)


#------------------------------------------------------------------------------------

    def make_move(self):
        t = time.time()

        if self._12rule:
            self._12rule = False
            self.map[(0,0)] = 1
            self.all_previous_boards.append(deepcopy(self.map))    
            self.remove_chips(self.color)
            return ((0,0),())

        value = self.calculate_value_of_move(((),()), self.map, self.color)
        if self.enemy_move == ((),()) and value * self.color > 0:
            return ((),())

        

        move = self.minimax(self.maxdepth, self.map, self.color)

        if move[0] != ():
            self.map[move[0]] = self.color * 1

        if move[1] != ():
            self.map[move[1]] = self.color * 2

        self.all_previous_boards.append(deepcopy(self.map))    
        self.remove_chips(self.color)

        print("Jenya number of operations: {}\nTime: {}\n".format(self.numberOfOperations, time.time() - t))
        self.numberOfOperations = 0
        return move
        



        
#------------------------------------------------------------------------------------

    


    def minimax(self, depth, _map, color, alpha = 999999):

       
        beta = abs(alpha)

        if depth == 0:
            self.numberOfOperations += 1
            return self.calculate_value_of_move(((),()), _map, color)

        good_cells = []

        already_observed = []

        distance_to_center = 9999999
        closest_to_center = ((),())
        last_closest = ((),())

        forbidden = []
        remove_from_forbidden = []
        

        for position in _map.keys():


            if position in already_observed:
                continue

            if _map[position] == 0:
                if True or depth == self.maxdepth:

                    coords = list(position)

                    if self.move_is_possible((position, ()), _map, color) and abs(coords[0]) + abs(coords[1]) <= distance_to_center:

                        last_closest = closest_to_center                   
                        closest_to_center = position
                        distance_to_center = abs(coords[0] + coords[1])           
                

            if _map[position] * color < 0:

                temp, bloom = self.is_position_in_fenced_bloom(position, _map)

                free_spaces = self.find_free_spaces(position, _map, False)
                good_cells += free_spaces
                remove_from_forbidden.append(good_cells)
                

                already_observed += bloom

            if _map[position] * color > 0:# and depth == self.maxdepth:

                temp, bloom = self.is_position_in_fenced_bloom(position, _map)

                free_spaces = self.find_free_spaces(position, _map, True)

                if len(free_spaces) > 4:
                    good_cells += free_spaces
                else:
                    forbidden+=free_spaces
                    
                already_observed += bloom

        if True or depth == self.maxdepth:
            corner_cells =  [closest_to_center, last_closest]
            good_cells += corner_cells


        for i in range(len(remove_from_forbidden)):
            while remove_from_forbidden[i] in forbidden:
                forbidden.remove(remove_from_forbidden[i])

##        if forbidden and depth == self.maxdepth:
##            print(forbidden)

        forbidden = []
                

        good_cells.append(())
        good_cells = list(set(good_cells))

        possible_moves = []

        for cell1 in good_cells:

            if cell1 == ((),()):
                continue

            for cell2 in good_cells:

                if cell2 == ((),()):
                    continue

                if cell1 != cell2 and self.move_is_possible((cell1, cell2), _map, color):
                    possible_moves.append((cell1, cell2))

        if not possible_moves and depth == self.maxdepth:
            for cell1 in corner_cells:
                
                if cell1 in forbidden or cell1 == ((),()):
                    continue

                for cell2 in corner_cells:

                    if cell2 in forbidden or cell2 == ((),()):
                        continue

                    if cell1 != cell2 and self.move_is_possible((cell1, cell2), _map, color):
                        possible_moves.append((cell1, cell2))
                


       
      
        bestValue = -999999*color
        bestMove = ((),())

        for move in possible_moves:

            new_map = deepcopy(_map)

            if move[0] != ():
                new_map[move[0]] = 1 * color

            if move[1] != ():
                new_map[move[1]] = 2 * color

            new_map = self.remove_chips(color, True, new_map)

            if depth == 0:
                value = self.calculate_value_of_move(((),()),new_map)
            else:
                value = self.minimax(depth - 1, new_map, color*(-1), abs(beta))

            if value * color > abs(alpha):
                return alpha*color

            beta = abs(value*color)

            if value * color > bestValue * color:
                bestValue = value
                bestMove = move


        if depth == self.maxdepth:
            return bestMove
        else:
            return bestValue

            

            
#------------------------------------------------------------------------------------


    def get_corners(self, color, _map):

        return_value = []
        field_size = self.field_size - 1

        corners = [
                (-field_size,-field_size),
                (field_size,field_size),
                (0,-field_size),
                (0,field_size),
                (-field_size,0),
                (field_size,0)
            ]

       

        for corner in corners:
            neighbors = self.get_neighbors(corner, _map)
            neighborsAdd = deepcopy(neighbors)
            for neighbor in neighbors:
                if _map[neighbor]*color < 0:
                    neighborsAdd = []
                    break
                elif _map[neighbor]*color > 0:
                    neighborsAdd = list(set(neighborsAdd) - set([neighbor]))
                    
            return_value += neighborsAdd

        return return_value
            

                
                
        

            
            

#------------------------------------------------------------------------------------

    def find_best_out_of_moves(self, moves, forbidden_moves):        
               
        double_moves = self.make_pairs(moves, forbidden_moves)

        best_move = self.choose_best_move(double_moves)

        return tuple(best_move)

#------------------------------------------------------------------------------------

    def make_pairs(self, moves, forbidden_moves = []):
        moves = list(set(moves))

        single_moves1 = [move for move in list(moves) if move[1] == ()]
        single_moves2 = [move for move in list(moves) if move[0] == ()]
        double_moves = list(set(moves) - set(single_moves1) - set(single_moves2))

        single_moves1.append(((), ()))
        single_moves2.append(((), ()))

        for move1 in single_moves1:

            for move2 in single_moves2:

                if move1[0] == move2[1] and not (move1[0] == ()):
                    continue

                if not self.move_is_possible((move1[0], move2[1])) or (move1[0] in forbidden_moves or move2[1] in forbidden_moves):
                    continue

                double_moves.append((move1[0], move2[1]))

        

        return double_moves
        

#------------------------------------------------------------------------------------

    def move_is_possible(self, move, _map = None, color = None):


        if color == None:
            color = self.color

        if _map == None:
            _map = self.map

        if move == ((), ()):
            return True

        try:
            if (move[0] != () and _map[move[0]] != 0) or (move[1] != () and _map[move[1]] != 0):
                #print("Bot -> Other stone blocks the way!")
                return False
        except KeyError:
            print("error",move)
            return False

        new_map = deepcopy(_map)

        if move[0] != ():
            new_map[move[0]] = 1 * color

        if move[1] != ():
            new_map[move[1]] = 2 * color

        if new_map in self.all_previous_boards:# and new_map != self.all_previous_boards[-1]:
            #print("Recreating previous position")
            return False

        for movement in move:

            if movement == ():
                continue

            kill_list = []

            for neighbor in self.get_neighbors(movement, new_map):

                if new_map[neighbor] * color >= 0:
                    continue

                fenced, bloom = self.is_position_in_fenced_bloom(neighbor, new_map)
                
                if fenced:
                    kill_list.append(bloom)


##            if move[0] == (-4,-1):
##                print(move, kill_list)



            fenced, bloom =  self.is_position_in_fenced_bloom(movement, new_map)

            if fenced:
                if not kill_list:
                    #print("Bot -> This way you would have fenced yourself!")
                    return False

            for neighbor in self.get_neighbors(movement, new_map):

                if new_map[neighbor] * color <= 0:# or (movement == move[0] and neighbor == move[1]) or (movement == move[1] and neighbor == move[0]):
                    continue

                fenced, bloom = self.is_position_in_fenced_bloom(neighbor, new_map)
##                if move[0] == (-4,-1):
##                    print(fenced, bloom)
                
                if fenced:
                    for another_neighbor in self.get_neighbors(neighbor, new_map):
                        
                        if not fenced:
                            break
                        
                        for bloom in kill_list:
                            
                            if another_neighbor in bloom:
                                fenced = False
                                break


                    if fenced:
                        #print("Bot -> Don`t fence your buddies!")
                        return False


        return True

#------------------------------------------------------------------------------------


    def choose_best_move(self, moves):

        best_value = -999999
        best_move = ((), ())

        if self._12rule:
            self._12rule = False
            self.map[(0,0)] = 1
            self.all_previous_boards.append(deepcopy(self.map))    
            self.remove_chips(self.color)
            return ((0,0),())

        for move in moves:

            new_board = deepcopy(self.map)

            if move[0] != ():
                new_board[move[0]] = 1 * self.color

            if move[1] != ():
                new_board[move[1]] = 2 * self.color

            value = self.calculate_value_of_move(move, new_board, self.color)

            if value > best_value:
                best_value = value
                best_move = move


        #print(best_move)

        if best_move[0] != ():
            self.map[best_move[0]] = 1 * self.color
            
           
        if best_move[1] != ():
            self.map[best_move[1]] = 2 * self.color

        self.all_previous_boards.append(deepcopy(self.map))    

        self.remove_chips(self.color)

        
        return best_move

            

                    

#------------------------------------------------------------------------------------

    def get_neighbors(self, coords, boardIndexes):

        if coords == ():
            return ()

        mapIndexes = boardIndexes.keys()

        x = coords[0]
        y = coords[1]
        
        neighbors = []

        if (x + 1, y) in mapIndexes:
            neighbors.append((x + 1, y))

        if (x - 1, y) in mapIndexes:
            neighbors.append((x - 1, y))

        if (x, y + 1) in mapIndexes:
            neighbors.append((x, y + 1))

        if (x, y - 1) in mapIndexes:
            neighbors.append((x, y - 1))

        if (x - 1, y - 1) in mapIndexes:
            neighbors.append((x - 1, y - 1))

        if (x + 1, y + 1) in mapIndexes:
            neighbors.append((x + 1, y + 1))


        return neighbors

#------------------------------------------------------------------------------------
    def is_position_in_fenced_bloom(self, position, customMap = None):

        if position == ():
            return False, ()
        
        if customMap != None:
            current_map = customMap
        else:
            current_map = self.map
        
        bloom = [position]
        bloom_is_fenced = True

        exhausted = [position]
        toDiscover = self.get_neighbors(position, current_map)
        color = current_map[position]

        while(toDiscover):

            cell = toDiscover.pop(len(toDiscover) - 1)

            if cell in exhausted:
                continue

            if current_map[cell] == 0:
                bloom_is_fenced = False
                break

            if current_map[cell] != color:
                continue

            toDiscover += self.get_neighbors(cell, current_map)
            exhausted.append(cell)
            bloom.append(cell)

        return bloom_is_fenced, bloom
    
#------------------------------------------------------------------------------------            
    def find_free_spaces(self, position, current_map, friendly = False):

        spaces = []
        
        exhausted = [position]
        toDiscover = self.get_neighbors(position, current_map)
        color = current_map[position]

        while(toDiscover):

            cell = toDiscover.pop(len(toDiscover) - 1)

            if cell in exhausted:
                continue

            if current_map[cell] == 0:
                spaces.append(cell)
                if not friendly and len(spaces) > 2:
                    return [(),(),(),()]

            if current_map[cell] != color:
                continue

            toDiscover += self.get_neighbors(cell, current_map)
            exhausted.append(cell)
            

        return spaces       
        
        
#------------------------------------------------------------------------------------

    def calculate_value_of_move(self, move, board, player_desire = 0):
        observed = []
    
        first_player_score = 0
        second_player_score = 0

        for cell in board.keys():

            if board[cell] > 0:
                first_player_score += 1

            elif board[cell] < 0:
                second_player_score += 1

            else:

                if cell in observed:
                    continue

                observed.append(cell)

                owner_color = 0

                toDiscover = [cell]
                exhausted = []
                cluster = []

            

                while toDiscover:

                    position = toDiscover.pop(len(toDiscover) - 1)

                    if position in exhausted:
                        continue

                    if board[position] != 0 and (board[position] * owner_color < 0 or owner_color == 0):

                        if owner_color == 0:
                            owner_color = board[position]

                        else:
                            owner_color = 0
                            break
                            
                    if board[position] == 0:
                        cluster.append(position)
                        
                        exhausted.append(position)
                        toDiscover += get_neighbors(position, board)

                cluster = list(set(cluster))

                if owner_color > 0:
                    first_player_score += len(cluster)*1
                    
                elif owner_color < 0:
                    second_player_score += len(cluster)*1

                observed += cluster


##        if player_desire > 0:
##            if move[0] != ():
##                first_player_score += self.field_size/2 - abs(move[0][0]) - abs(move[0][1])
##
##            if move[1] != ():
##                first_player_score += self.field_size/2 - abs(move[1][0]) - abs(move[1][1])
##                
##    
##
##        else:
##            if move[0] != ():
##                second_player_score += self.field_size/2 - abs(move[0][0]) - abs(move[0][1])
##
##            if move[1] != ():
##                second_player_score += self.field_size/2 - abs(move[1][0]) - abs(move[1][1])



        return (first_player_score - second_player_score)

#------------------------------------------------------------------------------------
    
    def remove_chips(self, priority, original = True, mapForWork = None):

        if mapForWork == None:
            mapForWork = self.map

        blooms_to_remove = []

        for position in mapForWork.keys():

            if mapForWork[position] * priority >= 0:
                continue

            remove_bloom, bloom = self.is_position_in_fenced_bloom(position)
            
            if remove_bloom:
                blooms_to_remove.append(bloom)


        for fenced_bloom in blooms_to_remove:
            result = self.remove_area(fenced_bloom, mapForWork)
            if mapForWork != self.map:
                mapForWork = result

        if original:
            return self.remove_chips(priority*(-1), original = False, mapForWork = mapForWork)

        
        return mapForWork

#------------------------------------------------------------------------------------

    def remove_area(self, area, mapForWork = None):

        if mapForWork == None:
            mapForWork = self.map

        for position in area:
            mapForWork[position] = 0

        return mapForWork


#------------------------------------------------------------------------------------

    def generate_map(self):

        for j in range(-self.field_size + 1, self.field_size):

            if j >= 0:
                start = -self.field_size + j
                end = self.field_size
                
            else:
                start = -self.field_size
                end = self.field_size + j


            for i in range(start + 1, end):

                xcoord = i
                ycoord = j

                self.map[(xcoord, ycoord)] = 0


    def make_move_depth(self, depth, _map, color):

        move = [(), ()]

        value = self.calculate_value_of_move(((),()), _map, color)

        if self.enemy_move == ((),()) and value > 0:
            #print(color, "passes")
            return ((),())

        good_moves = []
        forbidden_moves = []

        closest_to_center = (0,0)
        distance_to_center = 999999
        last_closest = (0,0)

        closing_move = (0,0)
        number_of_freedom = 9999999


        for position in _map.keys():

            if _map[position] * color < 0:

                free_spaces = self.find_free_spaces(position, _map)

                if 0 < len(free_spaces) < 3:

                    if len(free_spaces) == 1:

                        if self.move_is_possible((free_spaces[0], ()), _map, color):
                            good_moves.append((free_spaces[0], ()))
                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[0])
                            forbidden_moves = list(forbidden_moves)

                        if self.move_is_possible(((), free_spaces[0]), _map, color):
                            good_moves.append(((), free_spaces[0]))
                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[0])
                            forbidden_moves = list(forbidden_moves)

                       
                        

                    elif len(free_spaces) == 2:

                        if self.move_is_possible((free_spaces[0], free_spaces[1]), _map, color):
                            good_moves.append((free_spaces[0], free_spaces[1]))
            
                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[0])
                            forbidden_moves = list(forbidden_moves)

                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[1])
                            forbidden_moves = list(forbidden_moves)
                            

                        if self.move_is_possible((free_spaces[1], free_spaces[0]), _map, color):
                            good_moves.append((free_spaces[1], free_spaces[0]))

                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[0])
                            forbidden_moves = list(forbidden_moves)

                            forbidden_moves = set(forbidden_moves)
                            forbidden_moves.discard(free_spaces[1])
                            forbidden_moves = list(forbidden_moves)
                        




            elif _map[position] * color > 0 and depth == self.maxdepth:

                color = _map[position]


                free_spaces = self.find_free_spaces(position, _map, friendly = True)

                if len(free_spaces) > 3:

                    for space in free_spaces:

                        neighbors = self.get_neighbors(space, _map)
                        blank_counter = 0
                        enemy_found = False
                        
                        for neighbor in neighbors:
                            if _map[neighbor] == 0:
                                blank_counter += 1

                            if blank_counter > 1:
                                break

                            if _map[neighbor] * color < 0:
                                enemy_found = True
                                break

                        if enemy_found or blank_counter > 1:
                            
                            if abs(color) == 1:
                                good_moves.append((space, ()))

                            else:
                                good_moves.append(((), space))

                        else:
                            add = True
                            for move in good_moves:
                                if space in move:
                                    add = False
                                    break
                            if add:
                                forbidden_moves += space
                            

                else:
                    for spc in free_spaces:
                        add = True
                        for move in good_moves:
                            if spc in move:
                                add = False
                                break

                        if add:
                            forbidden_moves += spc


            else:

                if depth == self.maxdepth:

                    coords = list(position)

                    if self.move_is_possible((position, ()), _map, color) and abs(coords[0]) + abs(coords[1]) <= distance_to_center and not position in forbidden_moves:

                        last_closest = closest_to_center                   
                        closest_to_center = position
                        distance_to_center = abs(coords[0] + coords[1])           




        if depth == self.maxdepth:
            if self.move_is_possible((closest_to_center, ()), _map, color) and not closest_to_center in forbidden_moves:
                good_moves.append((closest_to_center, ()))


            if self.move_is_possible(((),closest_to_center), _map, color) and not closest_to_center in forbidden_moves:
                good_moves.append(((), closest_to_center))


            if self.move_is_possible((last_closest, ()), _map, color) and not last_closest in forbidden_moves:
                good_moves.append((last_closest, ()))


            if self.move_is_possible(((), last_closest), _map, color) and not last_closest in forbidden_moves:
                good_moves.append(((), last_closest))



        moves = self.make_pairs(good_moves, forbidden_moves)
        

        best_move = ((),())
        best_value = -999999 * color

        for move in moves:
            new_board = deepcopy(_map)

            if move[0] != ():
                new_board[move[0]] = 1 * color

            if move[1] != ():
                new_board[move[1]] = 2 * color
 
            new_board = self.remove_chips(color, True, new_board)

            if depth == 0:
                
                value = self.calculate_value_of_move(move, new_board, color)

            else:

                if color == 1:
                    anticolor = -1
                else:
                    anticolor = 1

                value = self.make_move_depth(depth - 1, new_board, anticolor)



            if value * color > best_value * color:
                best_value = value
                best_move = move



        if depth != self.maxdepth:
            return best_value
                
        return best_move




        

        

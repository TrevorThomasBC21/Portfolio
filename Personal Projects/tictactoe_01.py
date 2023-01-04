import numpy as np
import pickle


dimensions = 3
rows = dimensions
cols = dimensions

class Game:
    def __init__(self, p1, p2):
        self.board = np.zeros((rows, cols))
        self.p1 = p1
        self.p2 = p2
        self.current_board = None
        self.player_mark = 1
        self.game_over = False

    def check_board(self):
        self.current_board = str(self.board.reshape(rows * cols))
        return self.current_board

    def win_checker(self):
        diag_01 = sum([self.board[i,i] for i in range(dimensions)])
        diag_02 = sum([self.board[i, dimensions - i - 1] for i in range(dimensions)])
        for i in range(dimensions):
            if sum(self.board[i,:]) == dimensions or sum(self.board[:,i]) == dimensions or diag_01 == dimensions or diag_02 == dimensions:
                self.game_over = True
                return 1
            if sum(self.board[i,:]) == -dimensions or sum(self.board[:,i]) == -dimensions or diag_01 == -dimensions or diag_02 == -dimensions:
                self.game_over = True
                return -1

        if len(self.open_positions()) == 0:
            self.game_over = True
            return 0
        # not end
        self.game_over = False
        return None

    def board_update(self, position):
        self.board[position] = self.player_mark
        self.player_mark = self.player_mark * -1

    def open_positions(self):
        positions = []
        for i in range(rows):
            for j in range(cols):
                if self.board[i,j] == 0:
                    positions.append((i,j))
        return positions

    def trainer(self, rounds = 100):
        for i in range(rounds):
            if i % 1000 == 0:
                print(f"Rounds: {i}")
            while not self.game_over:
                options = self.open_positions()
                p1_action = self.p1.choose_move(options, self.board, self.player_mark)
                self.board_update(p1_action)
                get_board = self.check_board()
                self.p1.state_saver(get_board)
                win = self.win_checker()
                if win is not None:
                    self.reward_func()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    options = self.open_positions()
                    p2_action = self.p2.choose_move(options, self.board, self.player_mark)
                    self.board_update(p2_action)
                    get_board = self.check_board()
                    self.p2.state_saver(get_board)
                    win = self.win_checker()
                    if win is not None:
                        self.reward_func()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def reward_func(self):
        result = self.win_checker()
        if result == 1:
            self.p1.reward_saver(1)
            self.p2.reward_saver(0)
        elif result == -1:
            self.p1.reward_saver(0)
            self.p2.reward_saver(1)
        else:
            self.p1.reward_saver(.5)
            self.p2.reward_saver(.5)

    def play(self):
        while not self.game_over:
            options = self.open_positions()
            p1_action = self.p1.choose_move(options, self.board, self.player_mark)
            self.board_update(p1_action)
            self.show_board()
            win = self.win_checker()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("Tie!")
                self.reset()
                break
            else:
                options = self.open_positions()
                p2_action = self.p2.choose_move(options)
                self.board_update(p2_action)
                self.show_board()
                win = self.win_checker()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("Tie!")
                    self.reset()
                    break

    def show_board(self):
        for i in range(0, rows):
            print('-------------')
            out = '| '
            for j in range(0, cols):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')
        
    def reset(self):
        self.board = np.zeros((rows, cols))
        self.current_board = None
        self.game_over = False
        self.player_mark = 1

class ComputerPlayer:
    def __init__(self, name, explore_rate = .3):
        self.name = name
        self.board_states = []
        self.learn_rate = .2
        self.explore_rate = explore_rate
        self.learning_decay = .9
        self.policy_dict = {}

    def check_board(self, board):
        flat_board = str(board.reshape(rows * cols))
        return flat_board

    def choose_move(self, positions, board, mark):
        explore_exploit = np.random.uniform(0,1)
        if explore_exploit <= self.explore_rate:
            rand_choice = np.random.choice(len(positions))
            move = positions[rand_choice]
        else:
            value_max = -999
            value = 0
            for position in positions:
                board_option = board.copy()
                board_option[position] = mark
                new_board = self.check_board(board_option)
                if self.policy_dict.get(new_board) is None:
                    value = 0
                else:
                    value = self.policy_dict.get(new_board)
                if value >= value_max:
                    value_max = value
                    move = position
        return move

    def state_saver(self, state):
        self.board_states.append(state)

    def reward_saver(self, reward):
        for state in reversed(self.board_states):
            if self.policy_dict.get(state) is None:
                self.policy_dict[state] = 0
            self.policy_dict[state] += self.learn_rate * (self.learning_decay * reward - self.policy_dict[state])
            reward = self.policy_dict[state]

    def reset(self):
        self.board_states = []

    def policy_update(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.policy_dict, fw)
        fw.close()

    def policy_load(self, file):
        fr = open(file, 'rb')
        self.policy_dict = pickle.load(fr)
        fr.close()

class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_move(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

def main():
    # training
    p1 = ComputerPlayer("p1")
    p2 = ComputerPlayer("p2")

    st = Game(p1, p2)
    print("training...")
    st.trainer(5000)
    p1.policy_update()

    # play with human
    p1 = ComputerPlayer("computer", explore_rate=0)
    p1.policy_load("policy_p1")

    p2 = HumanPlayer("human")

    st = Game(p1, p2)
    st.play()

main()

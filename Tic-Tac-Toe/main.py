import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToe:
    def __init__(self,root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg='brown')
        self.buttons = []
        self.board = [" " for _ in range(9)]
        self.player_letter = "X"
        self.computer_letter = "O"
        self.create_buttons()
        self.player_starts = True
        self.ask_start()

    def create_buttons(self):
        for i in range(9):
            button = tk.Button(
                self.root, text=" ", font=('Arial', 50, 'bold'),
                height=2, width=5, bg='lightyellow',
                command=lambda i=i: self.player_move(i)
            )
            button.grid(row=i // 3, column=i % 3, padx= 5, pady= 5)
            self.buttons.append(button)

    def ask_start(self):
        answer = messagebox.askyesno("Start?","Do You Want To Start First?")
        self.player_starts = answer
        if not self.player_starts:
            self.root.after(500, self.computer_move)

    def player_move(self,index):
        if self.board[index] == " ":
            self.make_move(index,self.player_letter)
            if self.check_game_over(self.player_letter):
                return
            self.root.after(500, self.computer_move)

    def computer_move(self):
        move = self.get_computer_move()
        self.make_move(move,self.computer_letter)
        self.check_game_over(self.computer_letter)     

    def make_move(self,index,letter):
        self.board[index] = letter
        self.buttons[index].config(
            text=letter,
            fg='blue' if letter== 'X' else 'red',
            bg='lightblue' if letter=='X' else 'lightpink',
            activebackground='lightblue' if letter=='X' else 'lightpink',
            command=lambda:None    # we stop the button without disabling it
        )   
    def available_moves(self, state=None):
        if state is None:
            state= self.board
        return[i for i, spot in enumerate(state) if spot== " "]
        
    def winner(self, board_state, letter):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], #rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], #columns
            [0, 4, 8], [2, 4, 6]             #diagonals 
        ]    
        for condition in win_conditions:
            if all(board_state[i] == letter for i in condition):
                return True
        return False
    
    def is_full(self, state=None):
        if state is None:
            state = self.board
        return " " not in state
    def check_game_over(self,letter):
        if self.winner(self.board, letter):
            messag = f"{'You Have Win :)' if letter == self.player_letter else 'Computer Has Win'}"
            self.ask_play_again(messag)
            return True
        elif self.is_full():
            self.ask_play_again("No one Won")
            return True
        return False
    
    def ask_play_again(self, result_message):
        answer = messagebox.askyesno("The End", f"{result_message}\n\nDo You Want To Play Again?")
        if answer:
            self.reset_game()
        else:
            self.root.destroy()

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(
                text = " ",
                fg= "black",
                bg="lightyellow",
                activebackground = "lightyellow",
                command = lambda i = self.buttons.index(button): self.player_move(i)
            )
        self.ask_start()                

    def minimax(self, state, player):
        max_player = self.computer_letter
        other_player = self.player_letter if player == self.computer_letter else self.computer_letter
        if self.winner(state, other_player):
            return{"position": None, "score": 1 *(len(self.available_moves(state)) + 1) if other_player == max_player else -1 *(len(self.available_moves(state)) + 1)}
        elif " " not in state:
            return {"position":None, "score":0}
        if player == max_player:
            best = {"position":None, "score": -math.inf}
        else:
            best = {"position":None, "score": math.inf}
        for possible_move in self.available_moves(state):
            state[possible_move] = player
            sim_score = self.minimax(state, other_player)
            state[possible_move] = " "
            sim_score["position"] = possible_move   

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score
        return best
    def get_computer_move(self):
        if random.random() < 0.8:
            move = self.minimax(self.board.copy(), self.computer_letter)["position"]                         
        else:
            move = random.choice(self.available_moves())
        return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()            
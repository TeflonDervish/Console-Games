import os
import numpy as np
import time
import keyboard as kb



class Game_parts:
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

class Snake_parts(Game_parts):
    pass

class Queue:
    
    def __init__(self):
        self.arr = []
        
    def add(self, val):
        self.arr = [val] + self.arr
        
    def pop(self):
        val = self.arr[-1]
        self.arr = self.arr[:-1]
        return val
        
    def getHead(self):
        return self.arr[0]
        
    def __str__(self):
        return str(self.arr)

class Field:
    
    def __init__(self, width, height, startPosX, startPosY):
        
        self.snake = Queue()
        
        self.currentDirection = 'right'
        self.width = width
        self.height = height
        self.field = np.empty((width, height), dtype=Game_parts)
                
        self.field[startPosX, startPosY] = Snake_parts(startPosX, startPosY)
        self.field[startPosX - 1, startPosY] = Snake_parts(startPosX - 1, startPosY)
        
        self.snake.add(self.field[startPosX, startPosY])
        self.snake.add(self.field[startPosX - 1, startPosY])
        
        
    def moveSnake(self, direction = '-1'):
        
        if direction == '-1':
            direction = self.currentDirection
        
        if direction == 'right' and self.currentDirection != 'left':
            
            self.field[(self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY()] = \
                Snake_parts((self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY())
                
            self.snake.add(self.field[(self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY()])
            
            snake_tail = self.snake.pop()
            self.field[snake_tail.getX(), snake_tail.getY()] = None
        
        elif direction == 'left' and self.currentDirection != 'right':
            
            self.field[(self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY()] = \
                Snake_parts((self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY())
                
            self.snake.add(self.field[(self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY()])
            
            snake_tail = self.snake.pop()
            self.field[snake_tail.getX(), snake_tail.getY()] = None
        
        elif direction == 'down' and self.currentDirection != 'up':
            
            self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height] = \
                Snake_parts(self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height)
                
            self.snake.add(self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height])
            
            snake_tail = self.snake.pop()
            self.field[snake_tail.getX(), snake_tail.getY()] = None
        
        elif direction == 'up' and self.currentDirection != 'down':
            
            self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height] = \
                Snake_parts(self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height)
                
            self.snake.add(self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height])
            
            snake_tail = self.snake.pop()
            self.field[snake_tail.getX(), snake_tail.getY()] = None
        
        self.currentDirection = direction
        
    
    def __str__(self):
        
        s = "_" * (self.width + 2) + '\n'
        for i in range(self.height):
            s += '|'
            for j in range(self.width):
                if self.field[j, i]:
                    s += '0'
                else:
                    s += ' '
            s += '|\n'
        s += "_" * (self.width + 2) + '\n'
        
        return s
        
    def getDirection(self):
        return self.currentDirection



def on_key_pressed(e):
    global direction
    if e.event_type == kb.KEY_DOWN:
        direction = e.name
            
        
        
        
direction = 'right'       
        
        
        
if __name__ == "__main__":
    
    field = Field(40, 15, 10, 5)
    
    
    while True:
        kb.hook(on_key_pressed)
        print(direction)
        field.moveSnake(direction)
        print(field)
        
        time.sleep(0.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        
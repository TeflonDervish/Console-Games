import os
import numpy as np
import time
import keyboard as kb
import random

class GameOver(Exception):
    def __init__(self, message="Игра окончена"):
        self.message = message
        super().__init__(self.message)
        
    
class Game_parts:
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getType(self):
        pass
    

class Snake_parts(Game_parts):
    
    def getType(self):
        return "snake"
    

class Fruits(Game_parts):
    
    def getType(self):
        return "fruit"
    
    def setCoordinates(self, x, y):
        self.x = x
        self.y = y


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
        
        self.score = 0
        
        self.fruit = Fruits(0, 0)
        
        self.snake = Queue()
        
        self.currentDirection = 'right'
        self.width = width
        self.height = height
        self.field = np.empty((width, height), dtype=Game_parts)
                
        self.field[startPosX, startPosY] = Snake_parts(startPosX, startPosY)
        self.field[startPosX + 1, startPosY] = Snake_parts(startPosX + 1, startPosY)
        
        self.snake.add(self.field[startPosX, startPosY])
        self.snake.add(self.field[startPosX + 1, startPosY])
        
        self.spawnFruit()
        
        
    def moveSnake(self, direction = '-1'):
        
        if direction == '-1':
            direction = self.currentDirection
        
        if direction == 'right':
            
            val = self.collisions((self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY())
            
            if val == -1:
                raise GameOver()
            
            self.field[(self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY()] = \
                Snake_parts((self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY())
                
            self.snake.add(self.field[(self.snake.getHead().getX() + 1) % self.width, self.snake.getHead().getY()])
            
        
                
        elif direction == 'left':
            
            val = self.collisions((self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY())
            
            if val == -1:
                raise GameOver()
            
            self.field[(self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY()] = \
                Snake_parts((self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY())
                
            self.snake.add(self.field[(self.snake.getHead().getX() - 1) % self.width, self.snake.getHead().getY()])
            
            
        
        elif direction == 'down':
            
            val = self.collisions(self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height)
            
            if val == -1:
                raise GameOver()
            
            self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height] = \
                Snake_parts(self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height)
                
            self.snake.add(self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() + 1) % self.height])
            
            
        
        elif direction == 'up':
            
            val = self.collisions(self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height)
            
            if val == -1:
                raise GameOver()
            
            self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height] = \
                Snake_parts(self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height)
                
            self.snake.add(self.field[self.snake.getHead().getX(), (self.snake.getHead().getY() - 1) % self.height])
            
        if val == 0:
            
            snake_tail = self.snake.pop()
            self.field[snake_tail.getX(), snake_tail.getY()] = None
            
        elif val == 1:
            self.score += 1
            self.spawnFruit() 
                
                

    def collisions(self, x, y):
        if self.field[x, y]:
            if self.field[x, y].getType() == 'snake':
                return -1
            else:
                return 1
        else:
            return 0
        
    def spawnFruit(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        
        while self.collisions(x, y) == -1:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
        self.fruit.setCoordinates(x, y)
        self.field[x, y] = self.fruit
    
    def __str__(self):
        
        s = "_" * (self.width + 2) + '\n'
        for i in range(self.height):
            s += '|'
            for j in range(self.width):
                if self.field[j, i]:
                    if self.field[j, i].getType() == 'snake':
                        s += '0'
                    elif self.field[j, i].getType() == 'fruit':
                        s += '*'
                else:
                    s += ' '
            s += '|\n'
        s += "_" * (self.width + 2) + '\n'
        
        return s
        
    def getDirection(self):
        return self.currentDirection



def on_key_pressed(e):
    global direction
    if e.event_type == kb.KEY_DOWN and e.name in ('left', 'right', 'up', 'down'):
        direction = e.name
            
        
        
        
direction = 'right'       
        
        
        
if __name__ == "__main__":
    
    field = Field(40, 15, 10, 5)
    
    
    while True:
        kb.hook(on_key_pressed)
        if (direction == 'left' and field.getDirection() == 'right') or \
            (direction == 'right' and field.getDirection() == 'left') or \
            (direction == 'up' and field.getDirection() == 'down') or \
            (direction == 'down' and field.getDirection() == 'up'):
                
            direction = field.currentDirection[:]
            
        print(f"Scores: {field.score}")
        field.currentDirection = direction[:]
        field.moveSnake(direction)
        print(field)
        
        time.sleep(0.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        
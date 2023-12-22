import numpy as np


class Snake_parts:
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

class Queue:
    
    def __init__(self):
        self.arr = []
        
    def add(self, val):
        self.arr = [val] + self.arr
        
    def pop(self):
        val = self.arr[-1]
        self.arr = self.arr[:-1]
        return val
        
    def __str__(self):
        return str(self.arr)

class Field:
    
    def __init__(self, size, startPosX, startPosY):
        self.field = np.empty((size, size), dtype=Snake_parts)
        for i in range(size):
            for j in range(size):
                self.field[i, j] = None
        


if __name__ == "__main__":
    
    
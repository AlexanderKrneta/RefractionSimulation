# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:09:45 2021

@author: Alexa
"""
import math
class vec():
    def __init__(self, x, y, z = 0):
        self.x, self.y, self.z = x, y, z
    def __mul__(self, s):
        return vec(s * self.x, s * self.y, s * self.z)
    def __rmul__(self, s):
        return self * s
    def __truediv__(self, s):
        return self * (1 / s)
    def __add__(self, v):
        return vec(self.x + v.x, self.y + v.y, self.z + v.z)
    def __radd__(self, v):
        return self + v
    def __sub__(self, v):
        return self + v * -1
    def __rsub__(self, v):
        return v + self * -1
    def __pow__(self, v): # Dot product '**'
        return self.x*v.x + self.y*v.y + self.z*v.z
    def __mod__(self, v): # Cross product '%'
        return vec(self.y*v.z - self.z*v.y, 
                   self.z*v.x - self.x*v.z, 
                   self.x*v.y - self.y*v.x)
    def __floordiv__(self, n): # Magnatude '//'
        return math.sqrt(self ** self)
    def __xor__(self, n): # Normalize the vector '^'
        return self / (self//1)
    def __str__(self):
        return "< " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + " >"
    def __rshift__(self, v): # Cosine between 2 vectors
        return self**v/((self//1)*(v//1))
    def __lshift__(self, v): # Sine between 2 vectors
        return (self%v//1)/((self//1)*(v//1))
    def rotate(self, T):
        return vec(self.x*math.cos(T) - self.y*math.sin(T), self.x*math.sin(T) + self.y*math.cos(T))   
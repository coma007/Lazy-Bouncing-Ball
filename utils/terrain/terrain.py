import pygame


def create_terrain():
    terrain = {}
    with open("utils\\terrain\\terrain.txt", "r") as file:
        lines = file.readlines()
        i = 0
        j = 0
        for line in lines:
            for char in line:
                terrain[(j, i+10)] = True if char == "1" else False
                j += 1
            i += 1
            j = 0
        return terrain


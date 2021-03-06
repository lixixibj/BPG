# -------------------------#
import pygame
import random
import time
import numpy as np
import csv
# -------------------------#


def finder(line):
    coeff = int(len(line) / 100 * 5)
    dmem = 0
    imem = 0
    for i in xrange(coeff, len(line) - coeff, 1):
        xa = (line[i - coeff][0] + line[i + coeff][0]) / 2
        ya = (line[i - coeff][1] + line[i + coeff][1]) / 2
        d = np.sqrt((xa - line[i][0]) ** 2 + (ya - line[i][1]) ** 2)
        if d > dmem:
            dmem = d
            imem = i
    t = imem * 1.0 / len(line)
    return t, line[imem]


def calculate(first, my, last, t):
    # Points t = 0.5
    # p0 p1 p2 | pc
    # x1 = 2*xc - x0/2 - x2/2
    # y1 = 2*yc - y0/2 - y2/2
    # x1 = 2 * my[0] - first[0] / 2 - last[0] / 2
    # y1 = 2 * my[1] - first[1] / 2 - last[1] / 2
    x1 = (my[0] - first[0] * t ** 2 - last[0] * (1 - t) ** 2) / (2 * t * (1 - t))
    y1 = (my[1] - first[1] * t ** 2 - last[1] * (1 - t) ** 2) / (2 * t * (1 - t))
    return x1, y1


def bezier(first, middle, last):
    # Formula
    # P(t) = P0*t^2 + P1*2*t*(1-t) + P2*(1-t)^2
    tlist = range(0, 101, 1)
    pointslist = []
    for t in tlist:
        # Points
        # xt = x0 * t ** 2 + x1 * 2 * t * (1 - t) + x2 * (1 - t) ** 2
        # yt = y0 * t ** 2 + y1 * 2 * t * (1 - t) + y2 * (1 - t) ** 2
        t /= 100.0
        xt = int(first[0] * t ** 2 + middle[0] * 2 * t * (1 - t) + last[0] * (1 - t) ** 2)
        yt = int(first[1] * t ** 2 + middle[1] * 2 * t * (1 - t) + last[1] * (1 - t) ** 2)
        pointslist.append((xt, yt))
    return pointslist


NAME = "./data/points"

screen = pygame.display.set_mode((800, 600))

color = (255, 255, 255)
radius = 2
running = True
drawn = False

points_collector = []
lines_collector = []

cr = csv.reader(open(NAME + ".csv", "rb"))

# -------------------------#

for row in cr:
    print row
    points_collector = []
    for cell in row:
        cell = tuple(eval(cell))
        print cell, type(cell)
        points_collector.append(cell)
    print points_collector, len(points_collector)
    lines_collector.append(points_collector)
    print "line", len(lines_collector)

# -------------------------#

while running:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        running = False
        print "exit"
        pygame.image.save(screen, NAME + "_bezier.jpg")
    if not drawn:
        for line in lines_collector:
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            #
            # Original
            # for point in line:
            # pygame.draw.circle(screen, color, point, radius)
            #
            # Points
            # pygame.draw.circle(screen, (255,255,255), line[0], 3)
            # pygame.draw.circle(screen, (255,255,255), line[-1], 3)
            # pygame.draw.circle(screen, (255,255,255), line[len(line)/2], 3)
            #
            # Find important point
            # t, impoint = finder(line)
            # pygame.draw.circle(screen, (255, 255, 255), impoint, 3)
            #
            # Calculate middle point
            middle = calculate(line[0], line[len(line)/2], line[-1], 0.5)
            # Bezier curve
            curve = bezier(line[0], middle, line[-1])
            for point in curve:
                pygame.draw.circle(screen, color, point, radius)
        drawn = True
    pygame.display.flip()

pygame.quit()
# -------------------------#
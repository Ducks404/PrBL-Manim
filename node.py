from manim import *
import math as m

def PoltoCar(r, theta):
    x = round(r * m.cos(theta),2)
    y = round(r * m.sin(theta), 2)
    return([x,y,0])

def hyp(a, b):
    c = m.sqrt(a**2+b**2)
    return(c)

def add2lists(l1, l2):
    li = []
    for d, i in enumerate(l1):
        li.append(i-l2[d])
    return li

def stickLine(line, node, target):
    # print(line.get_start_and_end(), node.node.get_center(), target.node.get_center())
    nodeC = node.node.get_center()
    targetC = target.node.get_center()
    angle = angle_of_vector(nodeC - targetC)
    # print(angle)
    start = add2lists(nodeC, PoltoCar(node.radius, angle))
    sign = int(angle<0)
    if sign:
        opp_angle = m.pi + angle
    else:
        opp_angle = -m.pi + angle
    end = add2lists(targetC, PoltoCar(target.radius, opp_angle))
    line.put_start_and_end_on(start, end)


class Node():
    def __init__(self, x, y, color, radius=1):
        self.color = color
        self.radius = radius
        self.node = Circle(radius=radius, color=color).set_fill(BLACK, opacity=1.0).move_to([x,y,0])
        self.edges=[]
        
    def show(self, scene):
        # print(scene)
        scene.play(FadeIn(self.node))
        edge_animations = []
        for i in self.edges:
            edge_animations.append(FadeIn(i))
        scene.play(AnimationGroup(*edge_animations))

    def connect(self, target):
        line = Line()
        stickLine(line, self, target)
        line.add_updater(lambda l: stickLine(l, self, target))
        self.edges.append(line)

'''
Notes:
if you want to connect then target should be the parent because line will show with self


'''
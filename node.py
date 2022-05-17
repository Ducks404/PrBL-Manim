from manim import *
import math as m

config['disable_caching'] = True

def PoltoCar(r, theta):
    x = round(r * m.cos(theta),2)
    y = round(r * m.sin(theta), 2)
    return np.array([x,y,0])

def hyp(a, b):
    c = m.sqrt(a**2+b**2)
    return(c)

def stickLine(line, node, target):
    # print(line.get_start_and_end(), node.node.get_center(), target.node.get_center())
    nodeC = node.node.get_center()
    targetC = target.node.get_center()
    angle = angle_of_vector(nodeC - targetC)
    # print(angle)
    start = nodeC - PoltoCar(node.radius, angle)
    sign = int(angle<0)
    if sign:
        opp_angle = m.pi + angle
    else:
        opp_angle = -m.pi + angle
    end = targetC - PoltoCar(target.radius, opp_angle)
    line.put_start_and_end_on(start, end)

# Takes in 2 points
def lexpression(a, b):
    # vert to avoid divide by zero error
    if b[0]-a[0] != 0:
        m = (b[1]-a[1])/(b[0]-a[0])
        vert = False
    else:
        m = a[0]
        vert = True
    c = a[1]-m*a[0]
    return [round(m, 2), round(c, 2), vert]

# Takes in 2 points and an expression
def checkside(c, d, e):
    # check if (C.y - a(C.x) - b) and (D.y - a(D.x) - b) have the same sign
    if not e[2]:
        return int(c[1] - e[0] * c[0] - e[1] < 0) == int(d[1] - e[0] * d[0] - e[1] < 0)
    else:
        return int(c[0] - e[0] < 0) == int(d[0] - e[0] < 0)

# Takes in 2 expressions
def intersection(e1, e2):
    if e1[2]:
        x = e1[0]
    elif e2[2]:
        x = e2[0]
    else:
        x = (e1[1] - e2[1]) / (e2[0] - e1[0])
    y = e1[0] * x + e1[1]
    return np.array([round(x,2), round(y,2), 0])


def stickLine_server(line, server):
    serverC = server.node.get_center()
    # Check if the server is at the end or start
    if line in server.start_edges.values():
        server_place = 1
        l1 = serverC
        l2 = line.get_end()
    elif line in server.end_edges.values():
        server_place = 0
        l1 = line.get_start()
        l2 - serverC
    else:
        print('something went wrong checking at end or start')
    side = server.node.side_length/2
    TL = serverC + np.array([-side, side, 0])
    TR = serverC + np.array([side, side, 0])
    BL = serverC + np.array([-side, -side, 0])
    BR = serverC + np.array([side, -side, 0])
    
    exp_l = lexpression(l1, l2)
    exp_up = lexpression(TL, TR)
    exp_right = lexpression(TR, BR)
    exp_down = lexpression(BL, BR)
    exp_left = lexpression(TL, BL)

    # print(f'BL:{BL}\nBR:{BR}\nline:{l1}{l2}\nexp_l:{exp_l}\nexp_down:{exp_down}')
    # print(f'TL:{TL}\nBL:{BL}\nexp_left:{exp_left}')

    '''
    Check the intersection Source:(https://stackoverflow.com/questions/385305/efficient-maths-algorithm-to-calculate-intersections#:~:text=express%20the%20straight%20lines%20in,then%20there%20is%20an%20intersection.)
    1. express the straight lines in the form of y = ax + b (line passing A,B) and y = cx + d (line passing C,D)
    2. see if C and D are on the same side of y = ax+b
    3. see if A and B are on the same side of y = cx+d
    4. if the answer to the above are both no, then there is an intersection. otherwise there is no intersection.
    5. find the intersection if there is one.
    '''
    # Find the intersection
    if not checkside(TL, TR, exp_l) and not checkside(l1, l2, exp_up):
        inter = intersection(exp_l, exp_up)
    elif not checkside(TR, BR, exp_l) and not checkside(l1, l2, exp_right):
        inter = intersection(exp_l, exp_right)
    elif not checkside(BL, BR, exp_l) and not checkside(l1, l2, exp_down):
        inter = intersection(exp_l, exp_down)
    elif not checkside(TL, BL, exp_l) and not checkside(l1, l2, exp_left):
        inter = intersection(exp_l, exp_left)
    else:
        print('Something went wrong with finding the intersection')

    # Check if the server is at the end or start
    if server_place:
        line.put_start_and_end_on(inter, line.get_end())
        # print(line.get_start(), 'line start')
    else:
        line.put_start_and_end_on(line.get_start(), inter)
        # print(line.get_end(), 'line end')

class Node():
    def __init__(self, x, y, color, radius=1):
        self.color = color
        self.radius = radius
        self.node = Circle(radius=radius, color=color).move_to(np.array([x,y,0]))
        self.start_edges = {}
        self.end_edges = {}
        self.server = False

    def show(self, scene):
        # print(scene)
        scene.play(FadeIn(self.node))
        edge_animations = []
        for line in self.start_edges.values():
            edge_animations.append(FadeIn(line))
        scene.play(AnimationGroup(*edge_animations))

    def connect(self, target):
        line = Line()
        stickLine(line, self, target)
        line.add_updater(lambda l: stickLine(l, self, target))
        self.start_edges[target] = line
        target.end_edges[self] = line

    def upgrade(self, scene):
        # Transform circle to square and replaces self.node
        x = self.node.get_x()
        y = self.node.get_y()
        temp = Square(side_length=self.radius*2, color=self.color).shift(np.array([x, y, 0]))
        scene.play(Transform(self.node, temp))
        self.node = temp
        self.server = True

        # Adjust edge updaters
        for line in self.start_edges.values():
            line.add_updater(lambda l, self=self: stickLine_server(l, self))
        for line in self.end_edges.values():
            line.add_updater(lambda l, self=self: stickLine_server(l, self))


'''
Notes:
if you want to connect then target should be the parent because line will show with self


'''


# class Server():
#     def __init__(self, x, y, color, side):
#         self.color = color
#         self.side = side
#         self.node = Square(side_length=side)

#     def show(self, scene):
#         scene.play(FadeIn(self.server))
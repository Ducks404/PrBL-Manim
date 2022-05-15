from manim import *
import math as m
import node

def PoltoCar(r, theta):
    theta = m.radians(theta)
    x = round(r * m.cos(theta),2)
    y = round(r * m.sin(theta), 2)
    return({'x':x,'y':y})

def hyp(a, b):
    c = m.sqrt(a**2+b**2)
    return(c)

# circle.get_center

class Test(Scene):
    def construct(self):
        circle = Circle(radius=0.5)
        circ = Circle(radius=0.5)
        circle.set_color(WHITE)
        circ.set_color(WHITE)
        # text = Text(str(circle.radius))
        circle.shift([-1,0,0])
        circ.shift([1,0,0])
        # line = Line(start=[circle.get_x(), circle.get_y(), 0], end=[circ.get_x(), circ.get_y(), 0])
        # line = Line(start=[circle.get_x()+0.5, circle.get_y(), 0], end=[circ.get_x()-0.5, circ.get_y(), 0])
        line = Line(start=[1,1,0], end=[-1,1,0])

        self.add(circle)
        # text.shift(UP*2)
        # self.add(text)
        # self.play(ApplyMethod(circle.move_to, [1,0.5,0]), ApplyMethod(circ.move_to, [1,1,0]))
        # des = PoltoCar(hyp(1,1), 180)
        # self.play(ApplyMethod(circ.shift, [des['x'], des['y'], 0]))
        print(f'Line angle={line.get_angle()} \nLine slope={line.get_slope()}')
        # print(f'Line start={line.get_start_and_end()[0]} \nLine end={line.get_start_and_end()[1]}')
        # line.put_start_and_end_on([-1,-1,0], line.get_end())
        # print(f'Line start={line.get_start_and_end()[0]} \nLine end={line.get_start_and_end()[1]}')

        self.add(circle, circ, line)
        # self.play(Create(line))

class TestNode(Scene):
    def construct(self):
        n = node.Node(0,0, WHITE, radius=0.5)
        n1 = node.Node(0,0, WHITE, radius=0.5)
        n2 = node.Node(0,-3, WHITE, radius=0.5)
        # print(WHITE)
        n.node.shift([-3,3,0])
        n1.node.shift([0,0,0])
        n1.connect(n)
        n1.connect(n2)
        n.show(self)
        n2.show(self)
        n1.show(self)
        self.wait(1)
        self.play(ApplyMethod(n1.node.shift, [1,1,0]), ApplyMethod(n.node.shift, [0,-1,0]))
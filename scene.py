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

class SurveyData(Scene):
    def construct(self):
        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))
        a_neither = 45.8 / 100 * 360
        a_both = 39.8 / 100 * 360
        a_only_c = 9.6 / 100 * 360
        a_only_d = 4.8 / 100 * 360
        r = 1.5
        green = "#81b29a"
        blue = "#454866"
        red = "#e07a5f"
        c1 = RED_E
        c2 = GREEN_E
        c3 = YELLOW_C
        c4 = PURPLE_E
        neither = Sector(outer_radius=r, fill_opacity=1, angle=-(a_neither+1)*DEGREES, start_angle=a_neither*DEGREES, color=c1)
        both = Sector(outer_radius=r, fill_opacity=1, angle=-(a_both+1)*DEGREES, start_angle=(a_neither+a_both)*DEGREES, color=c2)
        only_c = Sector(outer_radius=r, fill_opacity=1, angle=-(a_only_c+1)*DEGREES, start_angle=(a_neither+a_both+a_only_c)*DEGREES, color=c3)
        only_d = Sector(outer_radius=r, fill_opacity=1, angle=-(a_only_d+1)*DEGREES, start_angle=(a_neither+a_both+a_only_c+a_only_d)*DEGREES, color=c4)
        # for i in (neither, both, only_c, only_d): i.set_stroke(width=2, color=BLACK)
        pie = Group(neither, both, only_c, only_d)
        self.add(pie)
        block = Sector(outer_radius=r+0.1, fill_opacity=1, angle=361*DEGREES, color=BLACK)
        self.add(block)
        self.play(Uncreate(block, rate_func=smooth, run_time=2))
        self.play(pie.animate.shift([-4,0,0]))

        neither_percentage = [0.39, 0.5, 0.11]
        one_percentage = [0.08, 0.75, 0.17]
        both_percentage = [0.12, 0.52, 0.36]
        y_axis = NumberLine(
            x_range=[0, 80, 20],
            unit_size=3/80,
            rotation=90 * DEGREES,
            label_direction=np.array([-1, 0, 0]),
            font_size=30
        ).add_labels({0:Tex('0\%'), 20:Tex('20\%'), 40:Tex('40\%'), 60:Tex('60\%'), 80:Tex('80\%')})
        y_axis_len = y_axis.x_range[1]*y_axis.unit_size
        y_axis.shift(np.array([0, y_axis_len/2, 0]))
        spacing = 2
        x_axis =NumberLine(
            x_range=[0, 6, 1],
            unit_size=spacing/2,
            tick_size=0.001,
            numbers_with_elongated_ticks=[1,3,5],
            longer_tick_multiple=100,
            font_size=30
        ).add_labels({1:'Tidak', 3:'Sedikit', 5:'Iya'})
        x_axis_len = y_axis.x_range[1]*y_axis.unit_size
        x_axis.shift(np.array([x_axis_len/2+1.5, 0, 0]))
        lines = Group()
        for l, data in enumerate([neither_percentage, one_percentage, both_percentage]):
            for index, i in enumerate(data[:2]):
                line = Line(np.array([spacing*index, i*(y_axis_len+y_axis.unit_size*20), 0]), 
                               np.array([spacing*(index+1), data[index+1]*(y_axis_len+y_axis.unit_size*20), 0]),
                               color = [c1,c2,c3][l])
                lines.add(line)
                # print(line.get_start_and_end())
        lines.shift([spacing/2,0,0])
        lines.add(y_axis, x_axis)
        lines.shift(np.array([0, -y_axis_len/2, 0]))
        self.play(*[Create(line, rate_func=linear) for index, line in enumerate(lines) if index%2==0 or index==len(lines)-1])
        self.play(*[Create(line, rate_func=linear) for index, line in enumerate(lines) if index%2!=0 and index!=len(lines)-1])
        self.wait(0.5)

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
        # Testing the nodes
        n = node.Node([0,0,0], WHITE, radius=0.5)
        n1 = node.Node([0,0,0], WHITE, radius=0.5)
        n2 = node.Node([0,-3,0], WHITE, radius=0.5)
        # print(WHITE)
        n.node.shift([-3,3,0])
        n1.node.shift([0,0,0])
        n1.connect(n)
        n1.connect(n2)
        n.connect(n2)
        self.play(*n.show(), *n2.show())
        self.play(*n1.show())
        self.play(ApplyMethod(n1.node.shift, [1,1,0]), ApplyMethod(n.node.shift, [0,-1,0]))
        n1.upgrade(self)
        self.play(ApplyMethod(n.node.shift, [7, -5, 0]))
        n1.divide(self)
        self.play(ApplyMethod(n1.node.shift,[-3,0,0]))
        n.send(n1, self)
        n1.send(n, self)
        n2.send_through([n, n1, n2, n1], self)

class TestData(Scene):
    def construct(self):
        # data = node.Data(0, 0, YELLOW, 20)
        # self.add(data.light)
        # data1 = Dot(radius=3).set_color_by_gradient([YELLOW, WHITE])
        # self.add(data1)
        # data = Dot(radius=0.05, color=BLUE)
        # rings = [Annulus(inner_radius=i*0.1, outer_radius=(i+1)*0.1, color=BLUE_A) for i in range(1,10)]
        # rings.reverse()
        # ring = Group(*rings)
        # ring.set_colors_by_radial_gradient(radius=1,inner_color=BLUE,outer_color=BLACK)
        # self.play(FadeIn(data,ring))
        n = node.Node(LEFT*2, WHITE, 0.5)
        n1 = node.Node(RIGHT*2, WHITE, 0.5)
        n1.connect(n)
        self.play(*n.show(), *n1.show())
        n.send(n1, self)
        n1.send(n, self)
        n2.send_through([n, n1, n2, n1], self)

class TestServer(Scene):
    def construct(self):
        # Testing the servers
        s = Square(side_length=3.0, grid_xstep=1.0, grid_ystep=1.0)
        s1 = Square(side_length=0.8)
        s2 = Square(side_length=0.8).next_to(s1, direction=UP, buff=0.3)
        s3 = Square(side_length=0.8).next_to(s2, direction=LEFT, buff=0.3)
        s4 = Square(side_length=0.8).next_to(s2, direction=RIGHT, buff=0.3)
        s5 = Square(side_length=0.8).next_to(s1, direction=LEFT, buff=0.3)
        s6 = Square(side_length=0.8).next_to(s1, direction=RIGHT, buff=0.3)
        s7 = Square(side_length=0.8).next_to(s1, direction=DOWN, buff=0.3)
        s8 = Square(side_length=0.8).next_to(s7, direction=LEFT, buff=0.3)
        s9 = Square(side_length=0.8).next_to(s7, direction=RIGHT, buff=0.3)
        server = Group(*[s1,s2,s3,s4,s5,s6,s7,s8,s9])
        s1 = Square(side_length=0.8)
        s2 = Square(side_length=0.8).next_to(s1, direction=UP, buff=0.2)
        s3 = Square(side_length=0.8).next_to(s2, direction=LEFT, buff=0.2)
        s4 = Square(side_length=0.8).next_to(s2, direction=RIGHT, buff=0.2)
        s5 = Square(side_length=0.8).next_to(s1, direction=LEFT, buff=0.2)
        s6 = Square(side_length=0.8).next_to(s1, direction=RIGHT, buff=0.2)
        s7 = Square(side_length=0.8).next_to(s1, direction=DOWN, buff=0.2)
        s8 = Square(side_length=0.8).next_to(s7, direction=LEFT, buff=0.2)
        s9 = Square(side_length=0.8).next_to(s7, direction=RIGHT, buff=0.2)
        server1 = Group(*[s1,s2,s3,s4,s5,s6,s7,s8,s9])
        s1 = Square(side_length=0.8)
        s2 = Square(side_length=0.8).next_to(s1, direction=UP, buff=0.1)
        s3 = Square(side_length=0.8).next_to(s2, direction=LEFT, buff=0.1)
        s4 = Square(side_length=0.8).next_to(s2, direction=RIGHT, buff=0.1)
        s5 = Square(side_length=0.8).next_to(s1, direction=LEFT, buff=0.1)
        s6 = Square(side_length=0.8).next_to(s1, direction=RIGHT, buff=0.1)
        s7 = Square(side_length=0.8).next_to(s1, direction=DOWN, buff=0.1)
        s8 = Square(side_length=0.8).next_to(s7, direction=LEFT, buff=0.1)
        s9 = Square(side_length=0.8).next_to(s7, direction=RIGHT, buff=0.1)
        server2 = Group(*[s1,s2,s3,s4,s5,s6,s7,s8,s9])
        group = Group(server, server1, server2).arrange(buff=1)
        self.add(group)

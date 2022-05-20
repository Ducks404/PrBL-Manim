from manim import *
import math as m
import random as ran
import node

def PoltoCar(r, theta):
    theta = m.radians(theta)
    x = round(r * m.cos(theta),2)
    y = round(r * m.sin(theta), 2)
    return np.array([x,y,0])

def hyp(a, b):
    c = m.sqrt(a**2+b**2)
    return(c)

class TitleScreen(Scene):
    def construct(self):
        '''
        title = Tex('Internet').move_to([0,-1,0]).scale(2)
        node_pos = [[1,1],
                    [-3,0],
                    [-3,-2],
                    [-5,-2],
                    [-6,-1],
                    [-5,2],
                    [-2,3],
                    [2,3],
                    [3,0],
                    [5.5,2.5],
                    [6,-1],
                    [3,-2],
                    [5,-3]]
        # Initiating each node
        graph = []
        for index, i in enumerate(node_pos):
            globals()[f'n{index}'] = node.Node(i)
            graph.append(globals()[f'n{index}'])
        
        n0.connect(n1,n6,n7,n8)
        n1.connect(n2,n3,n5,n6)
        n2.connect(n3)
        n3.connect(n4)
        n4.connect(n5)
        n5.connect(n6)
        n6.connect(n7)
        n7.connect(n8,n9)
        n8.connect(n9,n10,n11)
        n9.connect(n10)
        n10.connect(n11,n12)
        n11.connect(n12)

        # Show all nodes
        shows = []
        for i in graph:
            shows.extend(i.show())
        self.play(*shows, Write(title))
        '''
        Title = Text('Keadaan Internet:')
        Middle = Text('Sistem Terpusat')
        vs = Text('melawan')
        Down = Text('Terdesentralisasi')
        title = VGroup(Title, Middle, vs, Down).arrange(DOWN)
        self.play(Create(title), run_time=3)


class SurveyData(Scene):
    def construct(self):
        # for x in range(-7, 8):
        #     for y in range(-4, 5):
        #         self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))
        a_neither = 45.8 / 100 * 360
        a_both = 39.8 / 100 * 360
        a_only_c = 9.6 / 100 * 360
        a_only_d = 4.8 / 100 * 360
        r = 1.5
        y_offset = -0.75
        c1 = RED_E
        c2 = GREEN_E
        c3 = YELLOW_C
        c4 = PURPLE_E

        # Start of Pie Chart
        neither = Sector(outer_radius=r, fill_opacity=1, angle=-(a_neither+1)*DEGREES, start_angle=a_neither*DEGREES, color=c1)
        both = Sector(outer_radius=r, fill_opacity=1, angle=-(a_both+1)*DEGREES, start_angle=(a_neither+a_both)*DEGREES, color=c2)
        only_c = Sector(outer_radius=r, fill_opacity=1, angle=-(a_only_c+1)*DEGREES, start_angle=(a_neither+a_both+a_only_c)*DEGREES, color=c3)
        only_d = Sector(outer_radius=r, fill_opacity=1, angle=-(a_only_d+1)*DEGREES, start_angle=(a_neither+a_both+a_only_c+a_only_d)*DEGREES, color=c4)
        # for i in (neither, both, only_c, only_d): i.set_stroke(width=2, color=BLACK)
        pie = Group(neither, both, only_c, only_d).rotate((180-a_neither)*DEGREES).shift([0, y_offset, 0])

        l_neither = Tex('''Tidak tahu\\\\(45.8\%)''', font_size=30).move_to([-3,2,0])
        l_both = Tex('''Dua-duanya\\\\(39.8\%)''', font_size=30).move_to([-3,-2,0])
        l_one_c = Tex('''Hanya terpusat\\\\(9.6\%)''', font_size=30).move_to([3.5,-1,0])
        l_one_d = Tex('''Hanya terdesentralisasi\\\\(4.8\%)''', font_size=30).move_to([4,0.75,0])
        labels = [label.shift([0, y_offset, 0]) for label in (l_neither,l_both, l_one_c, l_one_d)]
        angles = [135, -135, -20, 7]
        boxes = []
        for index, i in enumerate(labels):
            box = Rectangle(width=i.width, height=i.height).set_stroke(width=0).move_to(i.get_center())
            box.add_updater(lambda box, index=index: box.move_to(labels[index].get_center()))
            boxes.append(box)
            inter = node.intersect_rect(pie.get_center(), box.get_center(), box)
            line = Line(pie.get_center()+PoltoCar(r+0.1, angles[index]), inter).set_stroke(width=2)
            line.add_updater(lambda line, index=index, box=box: line.put_start_and_end_on(pie.get_center()+PoltoCar(r+0.1, angles[index]), node.intersect_rect(line.get_start(), box.get_center(), box)))
            boxes.append(line)

        self.add(pie)
        pie_title = Tex('''Persentase responden yang mengetahui\\\\internet terpusat atau terdesentralisasi''', font_size=35).move_to([0, 2.5, 0])
        block = Sector(outer_radius=r+0.1, fill_opacity=1, angle=361*DEGREES, color=BLACK).rotate((180-a_neither)*DEGREES).shift([0, y_offset, 0])
        self.add(block)
        self.play(Write(pie_title), Uncreate(block, rate_func=linear, run_time=2), *[FadeIn(line) for line in labels], *[FadeIn(box) for box in boxes])
        shifts = [[-2.75,0,0],[-2.75,0,0],[-4.75,-0.25,0],[-5.75,1,0]]
        animations = []
        for index, label in enumerate(labels):
            animations.append(ApplyMethod(label.shift, shifts[index]))
        self.play(ApplyMethod(pie_title.shift, [-3.25,0,0]), ApplyMethod(pie.shift, [-4,0,0]), *animations)

        # Start creating line graph
        neither_percentage = [0.39, 0.5, 0.11]
        one_percentage = [0.08, 0.75, 0.17]
        both_percentage = [0.12, 0.52, 0.36]
        y_axis = NumberLine(
            x_range=[0, 100, 20],
            unit_size=4/100,
            rotation=90 * DEGREES,
            label_direction=np.array([-1, 0, 0]),
            font_size=30
        ).add_labels({0:Tex('0\%'), 20:Tex('20\%'), 40:Tex('40\%'), 60:Tex('60\%'), 80:Tex('80\%'), 100:Tex('100\%')})
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
        ).add_labels({1:'Tidak peduli', 3:'Peduli sedikit', 5:'Peduli'})
        x_axis_len = y_axis.x_range[1]*y_axis.unit_size
        x_axis.shift(np.array([x_axis_len/2+1, 0, 0]))
        lines = Group()
        for l, data in enumerate([neither_percentage, one_percentage, both_percentage]):
            for index, i in enumerate(data[:2]):
                line = Line(np.array([spacing*index, i*(y_axis_len), 0]),
                               np.array([spacing*(index+1), data[index+1]*(y_axis_len), 0]),
                               color = [c1,c2,c3][l])
                lines.add(line)
                # print(line.get_start_and_end())
        lines.shift([spacing/2,0,0])
        lines.add(y_axis, x_axis)
        lines.shift(np.array([1, -y_axis_len/2+y_offset, 0]))
        line_labels = Group(Group(Rectangle(height=0.15, width=0.3, color=c1, fill_opacity=1),
                            Tex('''Tidak tahu''', font_size=20)).arrange(RIGHT, buff=0.1),
                            Group(Rectangle(height=0.15, width=0.3, color=c2, fill_opacity=1),
                            Tex('''Hanya satu''', font_size=20)).arrange(RIGHT, buff=0.1),
                            Group(Rectangle(height=0.15, width=0.3, color=c3, fill_opacity=1),
                            Tex('''Dua-duanya''', font_size=20)).arrange(RIGHT, buff=0.1)).arrange(RIGHT)
        line_labels.move_to(lines.get_center() + np.array([0.5, 2, 0]))
        line_title = Tex('''Persentase kepedulian responden\\\\berdasarkan pengetahuan tentang\\\\internet terpusat atau terdesentralisasi''', font_size=35).move_to(lines.get_center() + np.array([0, 3.5, 0]))
        self.play(*[Create(line, rate_func=linear) for index, line in enumerate(lines) if index%2==0 or index==len(lines)-1])
        self.play(FadeIn(line_labels), Write(line_title, run_time=0.5), *[Create(line, rate_func=linear) for index, line in enumerate(lines) if index%2!=0 and index!=len(lines)-1])
        self.wait(0.5)

class TransitionExplanation(Scene):
    def construct(self):
        # Positions of all starting nodes
        nodes=[[0,0],
               [0,2],
               [2,1],
               [2.25,-1.75],
               [0,-3],
               [-2,-1],
               [-3,1],
               [-5,3],
               [-6,0],
               [-6,-2],
               [-3.5,-1.5],
               [4,-3],
               [6,0],
               [4,2],
               [2,5],
               [-7,5],
               [-8,-2],
               [-3,-5],
               [2,-5],
               [8,-5],
               [8,3]]
        colors = [PURE_RED, PURE_GREEN, PURE_BLUE, YELLOW]
        
        # Initiating each node
        graph = []
        for index, i in enumerate(nodes):
            globals()[f'n{index}'] = node.Node(i, color=ran.choice(colors))
            graph.append(globals()[f'n{index}'])
        # n2.change_color(PURE_GREEN)
        # Connecting nodes
        n0.connect(n1,n3,n4,n18)
        n1.connect(n2,n6,n13)
        n2.connect(n3,n11)
        n3.connect(n18)
        n4.connect(n10)
        n5.connect(n6, n10)
        n6.connect(n10,n14)
        n7.connect(n8,n10,n14,n15)
        n8.connect(n9,n10, n16)
        n9.connect(n16)
        n10.connect(n17)
        n11.connect(n12,n1)
        n12.connect(n19,n20)
        n13.connect(n14,n20)
        n16.connect(n17)

        # Show all nodes
        shows = []
        for i in graph:
            shows.extend(i.show())
        self.play(*shows)

        # Upgrade some nodes
        # n12.upgrade(self)
        # n8.upgrade(self)
        # n6.upgrade(self)
        # n7.upgrade(self)
        # n2.upgrade(self)
        # n7.divide(self)
        # n2.divide(self)

        # Slowly shift all nodes
        animations = []
        for i in graph:
            animations.append(i.node.animate.shift([1,1,0]))
        self.play(*animations, rate_func=linear, run_time=5)
        
        animations = []
        for index, i in enumerate(graph):
            if index not in [0,1,3,4,18]:
                animations.extend(i.remove(self))
        self.play(*animations, n3.disconnect(n18,self), run_time=3)
        for i in [n0,n1,n3,n4,n18]:
            self.play(i.change_color(WHITE),run_time=0.2)
        self.play(n0.node.animate.move_to(ORIGIN), n1.node.animate.move_to([-2,2,0]), n3.node.animate.move_to([2,2,0]), n4.node.animate.move_to([-2,-2,0]), n18.node.animate.move_to([2,-2,0]))



class CentralizedExplanation(Scene):
    def construct(self):
        title = Tex('''Terpusat''').move_to([0,3,0])
        node_pos = [[0,0],
                    [2,2],
                    [2,-2],
                    [-2,-2],
                    [-2,2]]
        # Initiating each node
        graph = []
        for index, i in enumerate(node_pos):
            globals()[f'n{index}'] = node.Node(i)
            graph.append(globals()[f'n{index}'])
        
        # Connect all nodes to center node
        for i in graph[1:]:
            i.connect(n0)
        
        # Show all nodes
        shows = []
        for i in graph:
            shows.extend(i.show())
        self.play(*shows)
        self.play(Write(title))

        n0.upgrade(self)
        server = Text('''Server''', font_size=28, color='#6e6e6e').move_to([0,2,0])
        arrow = Arrow(start=[0,1.75,0],end=[0,0.75,0], color='#6e6e6e')
        self.play(Write(server), Create(arrow))

        data1 = Tex('''0b0111\\\\001101\\\\100101''', font_size=23)
        data2 = Tex('''0b0111\\\\001001\\\\110110''', font_size=23)
        data3 = Tex('''0b0110\\\\010101\\\\110010''', font_size=23)
        
        self.play(Write(data1), run_time=0.5)
        self.play(ReplacementTransform(data1, data2), run_time=0.5)
        self.play(ReplacementTransform(data2, data3), run_time=0.5)
        self.play(Unwrite(data3), Unwrite(server), Uncreate(arrow), run_time=0.5)

        self.play(n3.change_color(PURE_BLUE), n2.change_color(PURE_RED), n1.change_color(YELLOW), n4.change_color(LIGHT_BROWN))
        n3.send_through([n0,n2], self)
        n2.send(n0, self)
        n4.send(n0, self)
        n0.send(n3, self, color=n2.color)

        add_node = [[0,-3],
                    [3,0],
                    [-3,0]]

        # Initiating each node
        graph = []
        colors = [PURE_GREEN, LIGHTER_GRAY, RED]
        for index, i in enumerate(add_node):
            globals()[f'n{index+5}'] = node.Node(i, color=colors[index])
            graph.append(globals()[f'n{index+5}'])

        
        # Connect all nodes to center node
        for i in graph:
            i.connect(n0)
        
        # Show all nodes
        shows = []
        for i in graph:
            shows.extend(i.show())
        self.play(*shows)
        
        n0.send(n6, self, color=n4.color)
        n5.send_through([n0,n7], self)
        n3.send_through([n0,n7], self)
        n7.send_through([n0,n3], self)
        n7.send_through([n0,n5,n0,n2], self)


class DecentralizedExplanation(Scene):
    def construct(self):
        nodes = [([0,0],WHITE),
                 ([2,2],YELLOW),
                 ([3,0],LIGHTER_GRAY),
                 ([2,-2],PURE_RED),
                 ([0,-3],PURE_GREEN),
                 ([-2,-2],PURE_BLUE),
                 ([-3,0],RED),
                 ([-2,2],LIGHT_BROWN)]
        graph = []
        for n in nodes:
            graph.append(node.Node(n[0],n[1]))
        graph[0].connect(*graph[1:])
        shows=[]
        for i in graph:
            shows.extend(i.show())
        self.play(*shows)
        graph[0].upgrade(self)
        
            
        node_pos = [[1,1],
                    [2,3],
                    [4,1],
                    [3,-2],
                    [0,-3],
                    [-1,-1],
                    [-3,0],
                    [-2,2],
                    [-5,3],
                    [-6,0],
                    [-4,-2],
                    [5,-3],
                    [6,-1],
                    [6,3]]
        animations = []
        for index, n in enumerate(graph):
            animations.append(n.node.animate.move_to(node_pos[index]+[0]))
        self.play(*animations)
        animations = []
        
        animations.extend([graph[0].disconnect(graph[3],self),
                           graph[0].disconnect(graph[4],self),
                           graph[0].disconnect(graph[5],self)])
        colors = [RED, PURE_RED, PURE_BLUE, PURE_GREEN, YELLOW, DARK_BROWN]
        for index, pos in enumerate(node_pos[len(graph):]):
            graph.append(node.Node(pos, colors[index]))

        graph[3].connect(graph[4])
        graph[4].connect(graph[2], graph[11])
        graph[5].connect(graph[6])
        graph[8].connect(graph[1], graph[7])
        graph[9].connect(graph[8], graph[7], graph[10])
        graph[10].connect(graph[6], graph[5])
        graph[12].connect(graph[11],graph[3],graph[2],graph[13])
        graph[13].connect(graph[0], graph[1])

        # Show all nodes
        
        for index, i in enumerate(graph):
            if index not in (0,1,2,6,7):
                animations.extend(i.show())
        self.play(*animations)

        graph[6].upgrade(self)
        graph[8].upgrade(self)
        graph[12].upgrade(self)
        graph[12].start_edges[graph[13]].clear_updaters()
        graph[12].start_edges[graph[13]].put_start_and_end_on([6,-0.5,0],graph[12].start_edges[graph[13]].get_end())
        self.wait(0.5)

        graph[3].send_through([graph[12],graph[2],graph[0],graph[7]], self)
        graph[6].send_through([graph[10],graph[9],graph[8],graph[7],graph[0],graph[13]], self)
        graph[4].send_through([graph[11],graph[12]], self)

class Examples(Scene):
    def construct(self):
        centralized = Rectangle(height=8, width=14).scale(0.35).move_to([3.5,0.5,0])
        decentralized = Rectangle(height=8, width=14).scale(0.35).move_to([-3.5,0.5,0])
        terpusat = Tex('''Terpusat''').move_to([3.5,2.5,0])
        c_example = Tex(''' - Google\\\\ - Meta''').move_to([3.5,-2,0])
        terdesentralisasi = Tex('''Terdesentralisasi''').move_to([-3.5,2.5,0])
        d_example = Tex(''' - BitTorrent\\\\ - Blockchain''').move_to([-3.5,-2,0])
        self.play(*[FadeIn(m) for m in (centralized, decentralized, terpusat, terdesentralisasi)])
        self.play(*[Write(m) for m in (c_example, d_example)])

class MoreSurveyData(Scene):
    def construct(self):
        Centralized = Tex('Terpusat').move_to([3.5,2.5,0])
        Decentralized = Tex('Terdesentralisasi').move_to([-3.5,2.5,0])
        vs = Tex('melawan', font_size=35)
        self.play(FadeIn(vs), Centralized.animate.shift([0,-2.5,0]), Decentralized.animate.shift([0,-2.5,0]))
        Monitored = Tex('Diawasi').move_to(Centralized.get_center())
        Free = Tex('Bebas').move_to(Decentralized.get_center())
        self.wait(1)
        self.play(Transform(Centralized,Monitored), Transform(Decentralized,Free))
        self.wait(1)
        self.remove(vs)
        chart = BarChart(
            values=[7, 18, 32, 20, 6],
            bar_names=["1", "2", "3", "4", "5"],
            bar_colors=[BLUE_A, BLUE_C, BLUE_E, BLUE_C,BLUE_A],
            y_range=[0, 40, 10],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 36},
        ).shift([0,0.75,0])
        self.play(Create(chart), Centralized.animate.shift([0.5,-3.25,0]), Decentralized.animate.shift([-0.5,-3.25,0]))

class CurrentInternet(Scene):
    def construct(self):
        pass

class FutureInternet(Scene):
    def construcotr(self):
        pass

class Credits(Scene):
    def construct(self):
        pass

'''
Tests might break since I changed stuff throughout doing the actual pugs
'''

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
        n = node.Node([0,0], WHITE, radius=0.5)
        n1 = node.Node([0,0], WHITE, radius=0.5)
        n2 = node.Node([0,-3], WHITE, radius=0.5)
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
        n.upgrade(self)
        self.play(ApplyMethod(n.node.shift, [7, -5, 0]))
        n1.divide(self)
        self.play(ApplyMethod(n1.node.shift,[-3,0,0]))
        n.send(n1, self)
        n1.send(n, self)
        n2.send_through([n, n1, n2, n1], self)
        n1.disconnect(n2, self)
        # n2.send(n1, self)

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

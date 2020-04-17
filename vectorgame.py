# -*- coding: utf-8 -*-

import random
import pygame 
import operator
import math

class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)

    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vec2d(-self.x, -self.y)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)

    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)

    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2

    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def cross(self, other):
        return self.x*other[1] - self.y*other[0]

    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)

    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict


class Shape():
    number = 0
    
    def __init__(self, screen, startpoint, pointlist, zoom=1, angle=0, color=(255,0,0), width=1, borderBounce=True, friction=0.5, move=Vec2d(0,0)):
        self.startpoint = startpoint
        self.pointlist = pointlist
        self.rotationpoint = Vec2d(0,0)
        self.zoom = zoom
        self.angle = angle
        self.color = color
        self.width = width
        self.screen = screen
        self.hitpoints = 1000
        self.number = Shape.number
        Shape.number += 1
        self.borderBounce = borderBounce
        #--- friction: 0 means no frictoin, 1 means no gliding
        self.friction = friction #0.1 # 0 or False means no friction
        self.move = Vec2d(move.x, move.y)
        
        
    
    def forward(self, delta=1):
        deltavec = Vec2d(delta, 0)
        deltavec.rotate(self.angle)
        #self.startpoint += deltavec
        self.move += deltavec
    
    def rotate(self, delta_angle=1):
        """alters pointlist by rotation with angle from rotationpoint"""
        self.angle += delta_angle
        #print(self.angle)
        for point in self.pointlist:
            point.rotate(delta_angle)    
        
    def update(self, seconds):
        """update movement. gets the seconds passed since last frame as parameter"""
        self.startpoint += self.move * seconds
        if self.friction:
            self.move *= (1-self.friction)
        if self.borderBounce:
            if self.startpoint.x < 0:
                self.startpoint.x = 0
                self.move.x = 0
            if self.startpoint.x > PygView.width :
                self.startpoint.x = PygView.width
                self.move.x = 0
            if self.startpoint.y < 0:
                self.startpoint.y = 0
                self.move.y = 0
            if self.startpoint.y > PygView.height:
                self.startpoint.y = PygView.height
                self.move.y = 0
        
    def draw(self):
        oldpoint = self.pointlist[0]
        #pygame.draw.line(self.screen, self.color, (0,0),(100,10),2)
        #pygame.draw.line(self.screen, self.color, (100,10),(10,150),2)
        self.color = (random.randint(0, 255) ,random.randint(0, 255) ,random.randint(0, 255) ) 
        for point in self.pointlist:
            #print("painting from point", oldpoint.x, oldpoint.y, "to", point.x, point.y)
            pygame.draw.line(self.screen, self.color,
                (self.startpoint.x + oldpoint.x * self.zoom,
                 self.startpoint.y + oldpoint.y * self.zoom),
                (self.startpoint.x + point.x * self.zoom,
                 self.startpoint.y + point.y * self.zoom)
                 ,self.width)
            oldpoint = point
                              
class VectorSprite(pygame.sprite.Sprite):
    pointlist = []
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.create_image()
        self.rect = self.image.get_rect()
        
        
    def create_image(self):
        minx = 0
        miny = 0
        maxx = 5
        maxy = 5
        for point in self.pointlist:
            if point.x < minx:
                minx = point.x
            if point.x > maxx:
                maxx = point.x
            if point.y < miny:
                miny = point.y
            if point.y > maxy:
                maxy = point.y
        self.image = pygame.Surface((maxx, maxy))
        pygame.draw.circle(self.image, (255,0,0), (2,2), 2)
        self.image.convert_alpha()  
        
           

class Ball():
    
    group = []
    number = 0
    maxage = 400
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, screen, startpoint=Vec2d(5,5), move=Vec2d(1,0), radius = 50, color=(0,0,255), bossnumber=0):
        """create a (black) surface and paint a blue ball on it"""
        self.number = Ball.number
        Ball.number += 1
        #Ball.group[self.number] = self
        Ball.group.append(self)
        self.radius = radius
        self.color = color
        self.bossnumber = bossnumber # 
        self.screen = screen
        self.startpoint = Vec2d(startpoint.x, startpoint.y) # make a copy of the startpoint vector
        self.move = move
        self.age = 0
        # create a rectangular surface for the ball 100x100
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        #pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        width = 1
        pygame.draw.line(self.surface, self.color, (50,50),
                    (50+self.move.x * 10, 50+self.move.y*10),width)
        self.startpoint.x -= 50
        self.startpoint.y -= 50
        self.surface.set_colorkey((0,0,0)) # make black transparent
        self.surface = self.surface.convert_alpha() # for faster blitting. 
        
    #def blit(self, background):
        #"""blit the Ball on the background"""
        #background.blit(self.surface, ( self.x, self.y))
        
    def draw(self):
        self.screen.blit(self.surface, (self.startpoint.x, self.startpoint.y))
        self.startpoint += self.move
        self.age += 1
        

        

class PygView(object):
  
    width = 0
    height = 0
  
    def __init__(self, width=1440, height=850, fps=30, visualmode = False):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        pygame.display.set_caption("vectorGame | Press ESC to quit")
        PygView.width = width    # also self.width 
        PygView.height = height  # also self.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.text_rectangle = ""
        self.canwin = True
        self.hpp1 = False
        self.hpp2 = False
        self.hpp3 = False
        self.hpp4 = False
        self.hpp5 = False
        self.hpp6 = False
        self.hpp7 = False
        self.hpp8 = False
        self.hpp9 = False
        self.visual_mode = visualmode
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.purple = (255, 0, 255)
        self.light_blue = (0, 255, 255)
        self.blue = (0, 0, 255)
        with open("data/plane_file.txt", "r") as self.plane_file:
            self.active_plane = random.choice(self.plane_file.read().split(","))
        with open("data/colour_file.txt", "r") as self.colour_file:
            self.active_colour = random.choice(self.colour_file.read().split(","))
        with open("data/plane_file2.txt", "r") as self.plane_file2:
            self.active_plane2 = random.choice(self.plane_file2.read().split(","))
        with open("data/colour_file2.txt", "r") as self.colour_file2:
            self.active_colour2 = random.choice(self.colour_file2.read().split(","))

    def paint(self):
        """painting ships on the surface"""
        
        # --- Player1 Planes ---
        
        if "standard" in self.active_plane:
            self.player1 = Shape(self.screen, Vec2d(100, 80),
                                           (
                                            Vec2d(0, 0),
                                            Vec2d(-25, 25),
                                            Vec2d(25, 0),
                                            Vec2d(-25, -25),
                                            Vec2d(0, 0)))
            self.player1.draw()

        elif "rectangle" in self.active_plane:
            self.rectangle_plane = Shape(self.screen, Vec2d(100, 80), 
                                                  (
                                                   Vec2d(-25, -25), 
                                                   Vec2d(25, -25), 
                                                   Vec2d(25, -10), 
                                                   Vec2d(0, 0),
                                                   Vec2d(25, 10),
                                                   Vec2d(25, 25),
                                                   Vec2d(-25, 25),
                                                   Vec2d(-25, -25)))
            self.rectangle_plane.draw()
        
        elif "diamond" in self.active_plane:
            self.diamond_plane = Shape(self.screen, Vec2d(100, 80), 
                                                  (
                                                   Vec2d(-5, -15), 
                                                   Vec2d(-5, 15), 
                                                   Vec2d(0, 25), 
                                                   Vec2d(25, 0),
                                                   Vec2d(0, -25),
                                                   Vec2d(-5, -15)))
            self.diamond_plane.draw()
            
        elif "space_shuttle" in self.active_plane:
            self.space_shuttle_plane = Shape(self.screen, Vec2d(100, 80), 
                                                  (
                                                   Vec2d(-25, -25), 
                                                   Vec2d(-25, 25), 
                                                   Vec2d(25, 10), 
                                                   Vec2d(25, -10),
                                                   Vec2d(-25, -25)))
            self.space_shuttle_plane.draw()
        
        elif "dagger" in self.active_plane:
            self.dagger_plane = Shape(self.screen, Vec2d(100, 80), 
                                                  (
                                                   Vec2d(-25, -5), 
                                                   Vec2d(-25, 5), 
                                                   Vec2d(-5, 5), 
                                                   Vec2d(0, 15),
                                                   Vec2d(5, 5),
                                                   Vec2d(25, 0),
                                                   Vec2d(5, -5),
                                                   Vec2d(0, -15),
                                                   Vec2d(-5, -5),
                                                   Vec2d(-25, -5)))
            self.dagger_plane.draw()
            
        elif "rocket" in self.active_plane:
            self.rocket_plane = Shape(self.screen, Vec2d(100, 80), 
                                                  (
                                                   Vec2d(-25, -5), 
                                                   Vec2d(-25, 5), 
                                                   Vec2d(-15, 5), 
                                                   Vec2d(-15, 15),
                                                   Vec2d(-5, 15),
                                                   Vec2d(5, 5),
                                                   Vec2d(15, 5),
                                                   Vec2d(25, 0),
                                                   Vec2d(15, -5),
                                                   Vec2d(5, -5),
                                                   Vec2d(-5, -15),
                                                   Vec2d(-15, -15),
                                                   Vec2d(-15, -5),
                                                   Vec2d(-25, -5)))
            self.rocket_plane.draw()
        
        # --- Player2 Planes ---
        
        if "standard" in self.active_plane2:
            self.player2 = Shape(self.screen, Vec2d(self.width-100, self.height-100),
                                           (
                                            Vec2d(0, 0),
                                            Vec2d(-25, 25),
                                            Vec2d(75, 0),
                                            Vec2d(-25, -25),
                                            Vec2d(0, 0)))
            self.player2.rotate(180)
            self.player2.draw()
        
        elif "pacman" in self.active_plane2:
            self.pacman_plane = Shape(self.screen, Vec2d(self.width-100, self.height-100), 
                                                  (
                                                   Vec2d(-25, -15), 
                                                   Vec2d(-25, 15), 
                                                   Vec2d(-15, 25), 
                                                   Vec2d(15, 25),
                                                   Vec2d(25, 15),
                                                   Vec2d(25, 10),
                                                   Vec2d(5, 0),
                                                   Vec2d(25, -10),
                                                   Vec2d(25, -15),
                                                   Vec2d(15, -25),
                                                   Vec2d(-15, -25),
                                                   Vec2d(-25, -15)))
            self.pacman_plane.rotate(180)
            self.pacman_plane.draw()
        
        elif "arrow" in self.active_plane2:
            self.arrow_plane = Shape(self.screen, Vec2d(self.width-100, self.height-100), 
                                                  (
                                                   Vec2d(5, -5), 
                                                   Vec2d(-25, -5), 
                                                   Vec2d(-5, 0), 
                                                   Vec2d(-25, 5),
                                                   Vec2d(5, 5),
                                                   Vec2d(25, 0),
                                                   Vec2d(5, -5)))
            self.arrow_plane.rotate(180)
            self.arrow_plane.draw()
         
    def run(self):
        """The mainloop
        """
        self.paint() 
        running = True
        while running:
            # --------- update time -------------            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            if self.visual_mode is False:
                if "standard" in self.active_plane:
                    text_player1 = "Player1: HP: {}".format(self.player1.hitpoints)
                    self.draw_text(text_player1, x=50, y=30, color=(200,20,0))
                elif "rectangle" in self.active_plane:
                    self.text_rectangle = "Player1: HP: {}".format(self.rectangle_plane.hitpoints)
                    self.draw_text(self.text_rectangle, x=50, y=30, color=(200,20,0))
                elif "diamond" in self.active_plane:
                    self.text_diamond = "Player1: HP: {}".format(self.diamond_plane.hitpoints)
                    self.draw_text(self.text_diamond, x=50, y=30, color=(200,20,0))
                elif "space_shuttle" in self.active_plane:
                    self.text_space_shuttle = "Player1: HP: {}".format(self.space_shuttle_plane.hitpoints)
                    self.draw_text(self.text_space_shuttle, x=50, y=30, color=(200,20,0))
                elif "dagger" in self.active_plane:
                    self.text_dagger = "Player1: HP: {}".format(self.dagger_plane.hitpoints)
                    self.draw_text(self.text_dagger, x=50, y=30, color=(200,20,0))
                elif "rocket" in self.active_plane:
                    self.text_rocket = "Player1: HP: {}".format(self.rocket_plane.hitpoints)
                    self.draw_text(self.text_rocket, x=50, y=30, color=(200,20,0))
                    
                if "standard" in self.active_plane2:
                    text_player2 = "Player2: HP: {}".format(self.player2.hitpoints)
                    self.draw_text(text_player2, x=self.width-300, y=30, color=(0,20,200))
                elif "pacman" in self.active_plane2:
                    text_pacman = "Player2: HP: {}".format(self.pacman_plane.hitpoints)
                    self.draw_text(text_pacman, x=self.width-300, y=30, color=(0,20,200))
                elif "arrow" in self.active_plane2:
                    text_arrow = "Player2: HP: {}".format(self.arrow_plane.hitpoints)
                    self.draw_text(text_arrow, x=self.width-300, y=30, color=(0,20,200))
            text_time = "FPS: {:4.3}".format(self.clock.get_fps(), self.playtime)
            self.draw_text(text_time, x = self.width//2-200, y=30, color=(100,0,100))
            
            
            # ---- joystick handler ------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                    x = j.get_axis(0)
                    y = j.get_axis(1)
                    x2 = j.get_axis(2) # daniel black stick 4 alina red: 2
                    y2 = j.get_axis(3)
                    buttons = j.get_numbuttons()
                    for b in range(buttons):
                        pushed = j.get_button( b )
                        if pushed and b == 0:                # button 0: X, button 1: A, button 2: B, button 3: Y
                            print("button 0 was pressed.")
                        elif pushed and b == 1:
                            print("button 1 was pressed.")
                            if "standard" in self.active_plane:
                                if "green" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.player1.startpoint-c, move, color=self.green, bossnumber=self.player1.number)
                                if "yellow" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.player1.startpoint-c, move, color=self.yellow, bossnumber=self.player1.number)
                                if "red" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.player1.startpoint-c, move, color=self.red, bossnumber=self.player1.number)
                            elif "rectangle" in self.active_plane:
                                if "green" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.rectangle_plane.startpoint-c, move, color=self.green, bossnumber=self.rectangle_plane.number)                      
                                if "yellow" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.rectangle_plane.startpoint-c, move, color=self.yellow, bossnumber=self.rectangle_plane.number)                      
                                if "red" in self.active_colour:    
                                    move = c * -speedfactor # + self.p
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.green, bossnumber=self.diamond_plane.number)                      
                                if "yellow" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.yellow, bossnumber=self.diamond_plane.number)                      
                                if "red" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.red, bossnumber=self.diamond_plane.number)                      
                            elif "space_shuttle" in self.active_plane:
                                if "green" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.green, bossnumber=self.space_shuttle_plane.number)                      
                                if "yellow" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.yellow, bossnumber=self.space_shuttle_plane.number)                      
                                if "red" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.red, bossnumber=self.space_shuttle_plane.number)                      
                            elif "dagger" in self.active_plane:
                                if "green" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.green, bossnumber=self.rocket_plane.number)                      
                                if "yellow" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.yellow, bossnumber=self.rocket_plane.number)                      
                                if "red" in self.active_colour:
                                    move = c * -speedfactor # + self.player1.move
                                    Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.red, bossnumber=self.rocket_plane.number)                      

                    if x < -0.3:
                        if "standard" in self.active_plane:
                            self.player1.rotate(-5 * -x * 1.5)
                        elif "rectangle" in self.active_plane:
                            self.rectangle_plane.rotate(-5 * -x * 1.5)
                        elif "diamond" in self.active_plane:
                            self.diamond_plane.rotate(-5 * -x * 1.5)
                        elif "space_shuttle" in self.active_plane:
                            self.space_shuttle_plane.rotate(-5 * -x * 1.5)
                        elif "dagger" in self.active_plane:
                            self.dagger_plane.rotate(-5 * -x * 1.5)
                        elif "rocket" in self.active_plane:
                            self.rocket_plane.rotate(-5 * -x * 1.5)
                    if x > 0.3:
                        if "standard" in self.active_plane:
                            self.player1.rotate(5 * x * 1.5)
                        elif "rectangle" in self.active_plane:
                            self.rectangle_plane.rotate(5 * x * 1.5)
                        elif "diamond" in self.active_plane:
                            self.diamond_plane.rotate(5 * x * 1.5)
                        elif "space_shuttle" in self.active_plane:
                            self.space_shuttle_plane.rotate(5 * x * 1.5)
                        elif "dagger" in self.active_plane:
                            self.dagger_plane.rotate(5 * x * 1.5)
                        elif "rocket" in self.active_plane:
                            self.rocket_plane.rotate(5 * x * 1.5)
                    if y < -0.1:
                        if "standard" in self.active_plane:
                            self.player1.forward(150)
                        elif "rectangle" in self.active_plane:
                            self.rectangle_plane.forward(150)
                        elif "diamond" in self.active_plane:
                            self.diamond_plane.forward(150)
                        elif "space_shuttle" in self.active_plane:
                            self.space_shuttle_plane.forward(150)
                        elif "dagger" in self.active_plane:
                            self.dagger_plane.forward(150)
                        elif "rocket" in self.active_plane:
                            self.rocket_plane.forward(150)
                    if y > 0.3:
                        if "standard" in self.active_plane:
                            self.player1.forward(-75)
                        elif "rectangle" in self.active_plane:
                            self.rectangle_plane.forward(-75)
                        elif "diamond" in self.active_plane:
                            self.diamond_plane.forward(-75)
                        elif "space_shuttle" in self.active_plane:
                            self.space_shuttle_plane.forward(-75)
                        elif "dagger" in self.active_plane:
                            self.dagger_plane.forward(-75)
                        elif "rocket" in self.active_plane:
                            self.rocket_plane.forward(-75)
                    #self.snowman1.dx = seconds * self.snowman1.speed * x
                    #self.snowman1.dy = seconds * self.snowman1.speed * y
                if number == 1:
                    x = j.get_axis(0)
                    y = j.get_axis(1)
                    buttons = j.get_numbuttons()
                    for b in range(buttons):
                        pushed = j.get_button( b )
                        if pushed and b == 1:
                            if "standard" in self.active_plane2:  
                                if "purple" in self.active_colour2:                                           
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.player2.startpoint-d,  move, color=self.purple, bossnumber=self.player2.number)  
                                elif "light_blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.player2.startpoint-d,  move, color=self.light_blue, bossnumber=self.player2.number)  
                                elif "blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.player2.startpoint-d,  move, color=self.blue, bossnumber=self.player2.number)  
                            elif "pacman" in self.active_plane2:
                                if "purple" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.purple, bossnumber=self.pacman_plane.number)   
                                elif "light_blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.light_blue, bossnumber=self.pacman_plane.number)
                                elif "blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.blue, bossnumber=self.pacman_plane.number)
                            elif "arrow" in self.active_plane2:
                                if "purple" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.purple, bossnumber=self.arrow_plane.number)   
                                elif "light_blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.light_blue, bossnumber=self.arrow_plane.number)
                                elif "blue" in self.active_colour2:
                                    move = d * -speedfactor 
                                    Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.blue, bossnumber=self.arrow_plane.number)
                    if x < -0.3:
                        if "standard" in self.active_plane2:
                            self.player2.rotate(-5 * -x * 1.5)
                        if "pacman" in self.active_plane2:
                            self.pacman_plane.rotate(-5 * -x * 1.5)
                        if "arrow" in self.active_plane2:
                            self.arrow_plane.rotate(-5 * -x * 1.5)
                    if x > 0.3:
                        if "standard" in self.active_plane2:
                            self.player2.rotate(5 * x * 1.5)
                        if "pacman" in self.active_plane2:
                            self.pacman_plane.rotate(5 * x * 1.5)
                        if "arrow" in self.active_plane2:
                            self.arrow_plane.rotate(5 * x * 1.5)
                    if y < -0.3:
                        if "standard" in self.active_plane2:
                            self.player2.forward(150)
                        elif "pacman" in self.active_plane2:
                            self.pacman_plane.forward(150)
                        elif "arrow" in self.active_plane2:
                            self.arrow_plane.forward(150)
                    if y > 0.3:
                        if "standard" in self.active_plane2:
                            self.player2.forward(-50)
                        if "pacman" in self.active_plane2:
                            self.pacman_plane.forward(-50)
                        if "arrow" in self.active_plane2:
                            self.arrow_plane.forward(-50)
            
            # ------------ event handler: keys pressed and released -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False 
                    elif event.key == pygame.K_f:
                        self.fullscreen = True
            # --------- pressed key handler --------------            
            pressed = pygame.key.get_pressed()            
            #self.player1.move = Vec2d(0,0)
            if pressed[pygame.K_w]:
                if "standard" in self.active_plane:
                    self.player1.forward(150)
                elif "rectangle" in self.active_plane:
                    self.rectangle_plane.forward(150)
                elif "diamond" in self.active_plane:
                    self.diamond_plane.forward(150)
                elif "space_shuttle" in self.active_plane:
                    self.space_shuttle_plane.forward(150)
                elif "dagger" in self.active_plane:
                    self.dagger_plane.forward(150)
                elif "rocket" in self.active_plane:
                    self.rocket_plane.forward(150)
            if pressed[pygame.K_s]:
                if "standard" in self.active_plane:
                    self.player1.forward(-50)
                elif "rectangle" in self.active_plane:
                    self.rectangle_plane.forward(-50)
                elif "diamond" in self.active_plane:
                    self.diamond_plane.forward(-50)
                elif "space_shuttle" in self.active_plane:
                    self.space_shuttle_plane.forward(-50)
                elif "dagger" in self.active_plane:
                    self.dagger_plane.forward(-50)
                elif "rocket" in self.active_plane:
                    self.rocket_plane.forward(-50)
            if pressed[pygame.K_a]:
                if "standard" in self.active_plane:
                    self.player1.rotate(-5)
                elif "rectangle" in self.active_plane:
                    self.rectangle_plane.rotate(-5)
                elif "diamond" in self.active_plane:
                    self.diamond_plane.rotate(-5)
                elif "space_shuttle" in self.active_plane:
                    self.space_shuttle_plane.rotate(-5)
                elif "dagger" in self.active_plane:
                    self.dagger_plane.rotate(-5)
                elif "rocket" in self.active_plane:
                    self.rocket_plane.rotate(-5)
            if pressed[pygame.K_d]:
                if "standard" in self.active_plane:
                    self.player1.rotate(5)
                elif "rectangle" in self.active_plane:
                    self.rectangle_plane.rotate(5)
                elif "diamond" in self.active_plane:
                    self.diamond_plane.rotate(5)
                elif "space_shuttle" in self.active_plane:
                    self.space_shuttle_plane.rotate(5)
                elif "dagger" in self.active_plane:
                    self.dagger_plane.rotate(5)
                elif "rocket" in self.active_plane:
                    self.rocket_plane.rotate(5)
           
                
            #if pressed[pygame.K_t]:
            #    self.player1.zoom += 0.25
            #if pressed[pygame.K_f]:
            #    self.player1.zoom -= 0.25
            #-------- player2 ---------
            #self.player2.move = Vec2d(0,0)
            if pressed[pygame.K_UP]:
                if "standard" in self.active_plane2:
                    self.player2.forward(150)
                elif "pacman" in self.active_plane2:
                    self.pacman_plane.forward(150)
                elif "arrow" in self.active_plane2:
                    self.arrow_plane.forward(150)
            if pressed[pygame.K_DOWN]:
                if "standard" in self.active_plane2:
                    self.player2.forward(-50)
                if "pacman" in self.active_plane2:
                    self.pacman_plane.forward(-50)
                if "arrow" in self.active_plane2:
                    self.arrow_plane.forward(-50)
            if pressed[pygame.K_LEFT]:
                if "standard" in self.active_plane2:
                    self.player2.rotate(-5)
                if "pacman" in self.active_plane2:
                    self.pacman_plane.rotate(-5)
                if "arrow" in self.active_plane2:
                    self.arrow_plane.rotate(-5)
            if pressed[pygame.K_RIGHT]:
                if "standard" in self.active_plane2:
                    self.player2.rotate(5)
                if "pacman" in self.active_plane2:
                    self.pacman_plane.rotate(5)
                if "arrow" in self.active_plane2:
                    self.arrow_plane.rotate(5)
            
            #if pressed[pygame.K_PLUS]:
            #    self.player2.zoom += 0.25
            #if pressed[pygame.K_MINUS]:
            #    self.player2.zoom -= 0.25
            # ----------update ships ------
            
            # --- Player1 Update() ---
            
            if "standard" in self.active_plane:
                self.player1.update(seconds)
            elif "rectangle" in self.active_plane:
                self.rectangle_plane.update(seconds)
            elif "diamond" in self.active_plane:
                self.diamond_plane.update(seconds)
            elif "space_shuttle" in self.active_plane:
                self.space_shuttle_plane.update(seconds)
            elif "dagger" in self.active_plane:
                self.dagger_plane.update(seconds)
            elif "rocket" in self.active_plane:
                self.rocket_plane.update(seconds)
            
            # --- Player2 Update() ---
            
            if "standard" in self.active_plane2:
                self.player2.update(seconds)
            elif "pacman" in self.active_plane2:
                self.pacman_plane.update(seconds)
            elif "arrow" in self.active_plane2:
                self.arrow_plane.update(seconds)
            
            # ----------draw ships ----------------
            
            # --- Player1 Draw() ---
            
            if "standard" in self.active_plane:
                self.player1.draw()
            elif "rectangle" in self.active_plane:
                self.rectangle_plane.draw()
            elif "diamond" in self.active_plane:
                self.diamond_plane.draw()
            elif "space_shuttle" in self.active_plane:
                self.space_shuttle_plane.draw()
            elif "dagger" in self.active_plane:
                self.dagger_plane.draw()
            elif "rocket" in self.active_plane:
                self.rocket_plane.draw()
                
            # --- Player 2 Draw() ---
            
            if "standard" in self.active_plane2:
                self.player2.draw()
            elif "pacman" in self.active_plane2:
                self.pacman_plane.draw() 
            elif "arrow" in self.active_plane2:
                self.arrow_plane.draw()
            
            # -----draw balls-----
            for b in Ball.group:
                b.draw()
            # ---- delete old balls ----
            
            Ball.group = [b for b in Ball.group if b.age < Ball.maxage]
            
            # ----- game over detection -----
            
            # --- Player1 ---
            if self.visual_mode is False:
                if "standard" in self.active_plane:
                    if self.player1.hitpoints <= 0:
                        self.hpp1 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                            
                elif "rectangle" in self.active_plane:
                    if self.rectangle_plane.hitpoints <= 0:
                        self.hpp3 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                
                elif "diamond" in self.active_plane:
                    if self.diamond_plane.hitpoints <= 0:
                        self.hpp4 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                
                elif "space_shuttle" in self.active_plane:
                    if self.space_shuttle_plane.hitpoints <= 0:
                        self.hpp5 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                
                elif "dagger" in self.active_plane:
                    if self.dagger_plane.hitpoints <= 0:
                        self.hpp6 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                            
                elif "rocket" in self.active_plane:
                    if self.rocket_plane.hitpoints <= 0:
                        self.hpp7 = True
                        if self.canwin is not False:
                            text_gameover = "Player2 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(0,20,200), size=50)
                            self.canwin = False
                            return 100
                
                # --- Player2 ---
                
                if "standard" in self.active_plane2:
                    if self.player2.hitpoints <= 0:
                        self.hpp2 = True
                        if self.canwin is not False:
                            text_gameover = "Player1 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(200,20,0), size=50)
                            self.can_win = False
                            return 100
                elif "pacman" in self.active_plane2:
                    if self.pacman_plane.hitpoints <= 0:
                        self.hpp8 = True
                        if self.canwin is not False:
                            text_gameover = "Player1 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(200,20,0), size=50)
                            self.can_win = False
                            return 100
                elif "arrow" in self.active_plane2:
                    if self.arrow_plane.hitpoints <= 0:
                        self.hpp9 = True
                        if self.canwin is not False:
                            text_gameover = "Player1 has won the game!"
                            self.draw_text(text_gameover, x=370, y=425, color=(200,20,0), size=50)
                            self.can_win = False
                            return 100
                
                # ----- collision detection -----
                critical_distance = 20
                for b in Ball.group:
                    
                    # --- Player1 ---
                    
                    if "standard" in self.active_plane:
                        if b.bossnumber != self.player1.number:
                            if (b.startpoint - self.player1.startpoint).get_length() < critical_distance:
                                if self.hpp1 is False:
                                    self.player1.hitpoints -= 1
                    elif "rectangle" in self.active_plane:
                        if b.bossnumber != self.rectangle_plane.number:
                            if (b.startpoint - self.rectangle_plane.startpoint).get_length() < critical_distance:
                                if self.hpp3 is False:
                                    self.rectangle_plane.hitpoints -= 1
                    elif "diamond" in self.active_plane:
                        if b.bossnumber != self.diamond_plane.number:
                            if (b.startpoint - self.diamond_plane.startpoint).get_length() < critical_distance:
                                if self.hpp4 is False:
                                    self.diamond_plane.hitpoints -= 1
                    elif "space_shuttle" in self.active_plane:
                        if b.bossnumber != self.space_shuttle_plane.number:
                            if (b.startpoint - self.space_shuttle_plane.startpoint).get_length() < critical_distance:
                                if self.hpp5 is False:
                                    self.space_shuttle_plane.hitpoints -= 1
                    elif "dagger" in self.active_plane:
                        if b.bossnumber != self.dagger_plane.number:
                            if (b.startpoint - self.dagger_plane.startpoint).get_length() < critical_distance:
                                if self.hpp6 is False:
                                    self.dagger_plane.hitpoints -= 1
                    elif "rocket" in self.active_plane:
                        if b.bossnumber != self.rocket_plane.number:
                            if (b.startpoint - self.rocket_plane.startpoint).get_length() < critical_distance:
                                if self.hpp7 is False:
                                    self.rocket_plane.hitpoints -= 1
                                    
                    # --- Player2 ---
                    
                    if "standard" in self.active_plane2:
                        if b.bossnumber != self.player2.number:
                            if (b.startpoint - self.player2.startpoint).get_length() < critical_distance:
                                if self.hpp2 is False:
                                    self.player2.hitpoints -= 1
                    elif "pacman" in self.active_plane2:
                        if b.bossnumber != self.pacman_plane.number:
                            if (b.startpoint - self.pacman_plane.startpoint).get_length() < critical_distance:
                                if self.hpp8 is False:
                                    self.pacman_plane.hitpoints -= 1
                    elif "arrow" in self.active_plane2:
                        if b.bossnumber != self.arrow_plane.number:
                            if (b.startpoint - self.arrow_plane.startpoint).get_length() < critical_distance:
                                if self.hpp9 is False:
                                    self.arrow_plane.hitpoints -= 1
            
            # -------- draw cannons -----------
            
            # --- Player1 ---
            
            if "standard" in self.active_plane:
                if "standard" in self.active_plane2:
                    d =  self.player2.startpoint - self.player1.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player1.startpoint.x,
                                                            self.player1.startpoint.y),
                                                            (self.player1.startpoint.x + d.x,
                                                            self.player1.startpoint.y + d.y),
                                                            8)
                elif "pacman" in self.active_plane2:         
                    d =  self.pacman_plane.startpoint - self.player1.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player1.startpoint.x,
                                                            self.player1.startpoint.y),
                                                            (self.player1.startpoint.x + d.x,
                                                            self.player1.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:         
                    d =  self.arrow_plane.startpoint - self.player1.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player1.startpoint.x,
                                                            self.player1.startpoint.y),
                                                            (self.player1.startpoint.x + d.x,
                                                            self.player1.startpoint.y + d.y),
                                                            8)
                 
            elif "rectangle" in self.active_plane:           
                if "standard" in self.active_plane2: 
                    d =  self.player2.startpoint - self.rectangle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rectangle_plane.startpoint.x,
                                                            self.rectangle_plane.startpoint.y),
                                                            (self.rectangle_plane.startpoint.x + d.x,
                                                            self.rectangle_plane.startpoint.y + d.y),
                                                            8)
                
                elif "pacman" in self.active_plane2:
                    d =  self.pacman_plane.startpoint - self.rectangle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rectangle_plane.startpoint.x,
                                                            self.rectangle_plane.startpoint.y),
                                                            (self.rectangle_plane.startpoint.x + d.x,
                                                            self.rectangle_plane.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:
                    d =  self.arrow_plane.startpoint - self.rectangle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rectangle_plane.startpoint.x,
                                                            self.rectangle_plane.startpoint.y),
                                                            (self.rectangle_plane.startpoint.x + d.x,
                                                            self.rectangle_plane.startpoint.y + d.y),
                                                            8)
            
            elif "diamond" in self.active_plane:      
                if "standard" in self.active_plane2:      
                    d =  self.player2.startpoint - self.diamond_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.diamond_plane.startpoint.x,
                                                            self.diamond_plane.startpoint.y),
                                                            (self.diamond_plane.startpoint.x + d.x,
                                                            self.diamond_plane.startpoint.y + d.y),
                                                            8)
                elif "pacman" in self.active_plane2:
                    d =  self.pacman_plane.startpoint - self.diamond_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.diamond_plane.startpoint.x,
                                                            self.diamond_plane.startpoint.y),
                                                            (self.diamond_plane.startpoint.x + d.x,
                                                            self.diamond_plane.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:
                    d =  self.arrow_plane.startpoint - self.diamond_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.diamond_plane.startpoint.x,
                                                            self.diamond_plane.startpoint.y),
                                                            (self.diamond_plane.startpoint.x + d.x,
                                                            self.diamond_plane.startpoint.y + d.y),
                                                            8)
         
            elif "space_shuttle" in self.active_plane:
                if "standard" in self.active_plane2:            
                    d =  self.player2.startpoint - self.space_shuttle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.space_shuttle_plane.startpoint.x,
                                                            self.space_shuttle_plane.startpoint.y),
                                                            (self.space_shuttle_plane.startpoint.x + d.x,
                                                            self.space_shuttle_plane.startpoint.y + d.y),
                                                            8)
                elif "pacman" in self.active_plane2:
                    d =  self.pacman_plane.startpoint - self.space_shuttle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.space_shuttle_plane.startpoint.x,
                                                            self.space_shuttle_plane.startpoint.y),
                                                            (self.space_shuttle_plane.startpoint.x + d.x,
                                                            self.space_shuttle_plane.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:
                    d =  self.arrow_plane.startpoint - self.space_shuttle_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.space_shuttle_plane.startpoint.x,
                                                            self.space_shuttle_plane.startpoint.y),
                                                            (self.space_shuttle_plane.startpoint.x + d.x,
                                                            self.space_shuttle_plane.startpoint.y + d.y),
                                                            8)
     
            elif "dagger" in self.active_plane:    
                if "standard" in self.active_plane2:
                    d =  self.player2.startpoint - self.dagger_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.dagger_plane.startpoint.x,
                                                            self.dagger_plane.startpoint.y),
                                                            (self.dagger_plane.startpoint.x + d.x,
                                                            self.dagger_plane.startpoint.y + d.y),
                                                            8)
                elif "pacman" in self.active_plane2:
                    d =  self.pacman_plane.startpoint - self.dagger_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.dagger_plane.startpoint.x,
                                                            self.dagger_plane.startpoint.y),
                                                            (self.dagger_plane.startpoint.x + d.x,
                                                            self.dagger_plane.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:
                    d =  self.arrow_plane.startpoint - self.dagger_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.dagger_plane.startpoint.x,
                                                            self.dagger_plane.startpoint.y),
                                                            (self.dagger_plane.startpoint.x + d.x,
                                                            self.dagger_plane.startpoint.y + d.y),
                                                            8)

            elif "rocket" in self.active_plane:         
                if "standard" in self.active_plane2:   
                    d =  self.player2.startpoint - self.rocket_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rocket_plane.startpoint.x,
                                                            self.rocket_plane.startpoint.y),
                                                            (self.rocket_plane.startpoint.x + d.x,
                                                            self.rocket_plane.startpoint.y + d.y),
                                                            8)
                elif "pacman" in self.active_plane2:
                    d =  self.pacman_plane.startpoint - self.rocket_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rocket_plane.startpoint.x,
                                                            self.rocket_plane.startpoint.y),
                                                            (self.rocket_plane.startpoint.x + d.x,
                                                            self.rocket_plane.startpoint.y + d.y),
                                                            8)
                elif "arrow" in self.active_plane2:
                    d =  self.arrow_plane.startpoint - self.rocket_plane.startpoint 
                    d = d.normalized()
                    d *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.rocket_plane.startpoint.x,
                                                            self.rocket_plane.startpoint.y),
                                                            (self.rocket_plane.startpoint.x + d.x,
                                                            self.rocket_plane.startpoint.y + d.y),
                                                            8)
            
            # --- Player2 ---
            
            if "standard" in self.active_plane2:
                if "standard" in self.active_plane:
                    c =  self.player1.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
                elif "rectangle" in self.active_plane:  
                    c =  self.rectangle_plane.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
                elif "diamond" in self.active_plane:
                    c =  self.diamond_plane.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
                elif "space_shuttle" in self.active_plane:
                    c =  self.space_shuttle_plane.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
                elif "dagger" in self.active_plane:
                    c =  self.dagger_plane.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
                elif "rocket" in self.active_plane:
                    c =  self.rocket_plane.startpoint - self.player2.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.player2.startpoint.x,
                                                            self.player2.startpoint.y),
                                                            (self.player2.startpoint.x + c.x,
                                                            self.player2.startpoint.y + c.y),
                                                            8)
            
            if "pacman" in self.active_plane2:
                if "standard" in self.active_plane:
                    c =  self.player1.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                elif "rectangle" in self.active_plane:  
                    c =  self.rectangle_plane.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                elif "diamond" in self.active_plane:
                    c =  self.diamond_plane.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                elif "space_shuttle" in self.active_plane:
                    c =  self.space_shuttle_plane.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                elif "dagger" in self.active_plane:
                    c =  self.dagger_plane.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                elif "rocket" in self.active_plane:
                    c =  self.rocket_plane.startpoint - self.pacman_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.pacman_plane.startpoint.x,
                                                            self.pacman_plane.startpoint.y),
                                                            (self.pacman_plane.startpoint.x + c.x,
                                                            self.pacman_plane.startpoint.y + c.y),
                                                            8)
                                                            
            if "arrow" in self.active_plane2:
                if "standard" in self.active_plane:
                    c =  self.player1.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
                elif "rectangle" in self.active_plane:  
                    c =  self.rectangle_plane.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
                elif "diamond" in self.active_plane:
                    c =  self.diamond_plane.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
                elif "space_shuttle" in self.active_plane:
                    c =  self.space_shuttle_plane.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
                elif "dagger" in self.active_plane:
                    c =  self.dagger_plane.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
                elif "rocket" in self.active_plane:
                    c =  self.rocket_plane.startpoint - self.arrow_plane.startpoint 
                    c = c.normalized()
                    c *= 35
                    pygame.draw.line(self.screen, (0,0,0), (self.arrow_plane.startpoint.x,
                                                            self.arrow_plane.startpoint.y),
                                                            (self.arrow_plane.startpoint.x + c.x,
                                                            self.arrow_plane.startpoint.y + c.y),
                                                            8)
            
                                                            
            # --------- (auto)fire -------
            #c *= 0.05
            #d *= 0.05
            speedfactor = 0.05
            if pressed[pygame.K_LCTRL]:
                if "standard" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.player1.startpoint-c, move, color=self.green, bossnumber=self.player1.number)
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.player1.startpoint-c, move, color=self.yellow, bossnumber=self.player1.number)
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.player1.startpoint-c, move, color=self.red, bossnumber=self.player1.number)
                elif "rectangle" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rectangle_plane.startpoint-c, move, color=self.green, bossnumber=self.rectangle_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rectangle_plane.startpoint-c, move, color=self.yellow, bossnumber=self.rectangle_plane.number)                      
                    if "red" in self.active_colour:    
                        move = c * -speedfactor # + self.p
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.green, bossnumber=self.diamond_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.yellow, bossnumber=self.diamond_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.red, bossnumber=self.diamond_plane.number)                      
                elif "space_shuttle" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.green, bossnumber=self.space_shuttle_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.yellow, bossnumber=self.space_shuttle_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.red, bossnumber=self.space_shuttle_plane.number)                      
                elif "dagger" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.green, bossnumber=self.rocket_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.yellow, bossnumber=self.rocket_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.red, bossnumber=self.rocket_plane.number)                      
                elif "diamond" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.green, bossnumber=self.diamond_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.yellow, bossnumber=self.diamond_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.diamond_plane.startpoint-c, move, color=self.red, bossnumber=self.diamond_plane.number)                      
                elif "space_shuttle" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.green, bossnumber=self.space_shuttle_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.yellow, bossnumber=self.space_shuttle_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.space_shuttle_plane.startpoint-c, move, color=self.red, bossnumber=self.space_shuttle_plane.number)                      
                elif "dagger" in self.active_plane:
                    if "green" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.green, bossnumber=self.rocket_plane.number)                      
                    if "yellow" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.yellow, bossnumber=self.rocket_plane.number)                      
                    if "red" in self.active_colour:
                        move = c * -speedfactor # + self.player1.move
                        Ball(self.screen, self.rocket_plane.startpoint-c, move, color=self.red, bossnumber=self.rocket_plane.number)                                       



            
            if pressed[pygame.K_RCTRL]:  
                if "standard" in self.active_plane2:  
                    if "purple" in self.active_colour2:                                           
                        move = d * -speedfactor 
                        Ball(self.screen, self.player2.startpoint-d,  move, color=self.purple, bossnumber=self.player2.number)  
                    elif "light_blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.player2.startpoint-d,  move, color=self.light_blue, bossnumber=self.player2.number)  
                    elif "blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.player2.startpoint-d,  move, color=self.blue, bossnumber=self.player2.number)  
                elif "pacman" in self.active_plane2:
                    if "purple" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.purple, bossnumber=self.pacman_plane.number)   
                    elif "light_blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.light_blue, bossnumber=self.pacman_plane.number)
                    elif "blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.pacman_plane.startpoint-d,  move, color=self.blue, bossnumber=self.pacman_plane.number)
                elif "arrow" in self.active_plane2:
                    if "purple" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.purple, bossnumber=self.arrow_plane.number)   
                    elif "light_blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.light_blue, bossnumber=self.arrow_plane.number)
                    elif "blue" in self.active_colour2:
                        move = d * -speedfactor 
                        Ball(self.screen, self.arrow_plane.startpoint-d,  move, color=self.blue, bossnumber=self.arrow_plane.number)
            
            # ---------- update screen ----------- 
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()


    def draw_text(self, text, x=50, y=150, color=(0,0,0), size = 24):
        self.font = pygame.font.SysFont('mono', size, bold=True)
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))

if __name__ == '__main__':
    PygView().run()

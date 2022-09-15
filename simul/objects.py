from pymunk.body import Body
from pymunk.shapes import Circle as cr,Poly
from pymunk._types import Vec2d


class Rectangel:
    def __init__(self,
                 position: Vec2d,
                 w: int,
                 h: int,
                 mass: float = 20,
                 friction: float = 0,is_dynamic: bool = True):
        if is_dynamic:
            self.body = Body()
        else:
            self.body = Body(body_type=Body.KINEMATIC)
        self.body.position = position
        self.shape = Poly.create_box(self.body,(w,h))
        if not isinstance(mass,(int,float)):
            raise TypeError('Not valid type')
        self.shape.mass = mass
        if not isinstance(friction,(int,float)):
            raise TypeError("Not valid type")
        self.shape.friction = friction

class Circle:
    def __init__(self,
                 ):
        self.body = Body()

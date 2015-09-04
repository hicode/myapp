#!/usr/bin/python

from TurtleWorld import *

import Lumpy

if __name__ == '__main__':
    lumpy = Lumpy.Lumpy()
    print Interpreter
    lumpy.opaque_class(Interpreter)
    lumpy.make_reference()
    
    world = TurtleWorld()
    bob = Turtle(world)
    
    lumpy.object_diagram()
    lumpy.class_diagram()


"""
Noodle

Copyright: Will Adams (www.highsamples.com)
Written for CINEMA 4D R19

Name-US: Noodle
Description-US: A mathematical knot spline generator.
"""

import os
import math
import sys
import c4d
import random

from c4d import plugins, utils, bitmaps, gui

# PLugin ID received from plugincafe.com and assigned to extralush
PLUGIN_ID = 1040675

DT_OBJECT = "DataObject"
DT_LIST = "DataListObject"
DT_LISTITEM = "DataListItemObject"


# Empty Path Data Object
class PathData():
    pass

# Data Object for storing input parameters
class DataObject():
    def __init__(self, data):
        self.type = DT_OBJECT
        self.value = data[0] #Current value
        self.changed = data[0] #Changed value used to determine if there is a change
        self.valueType = data[1] #Value type in case it needs to be cast
        self.udid = data[2] #The user data id associated with the object

# Data List Object for storing list input parameters
class DataListObject():
    def __init__(self, data):
        self.type = DT_LIST
        self.value = data[0] #Current selected index of the list
        self.changed = data[0] #Changed index of the list
        self.items = data[1] #List of DataListItemObjects
        self.udid = data[2] #The user data id associated with the object
        self.selected = self.items[data[0]] #The current selected list item

# Data List Item Object for storing the information of list item including the function to call when selecting it
class DataListItemObject():
    def __init__(self, data):
        self.type = DT_LISTITEM
        self.index = data[0] #Index of the item in the list
        self.title = data[1] #Title of the item
        self.value = data[3] #Value of the item
        self.draw = data[2] #Draw function used when creating the spline
        self.data = data[4] #Any additional data

class TorusA():

    @staticmethod
    def params():
        
        # Determines which parameters to show / hide.
        # True means it is hidden.
        p = {
            'p' : False,
            'q' : False,
            'm' : True,
            'n' : True,
            'r' : False,
            's' : False,
            'signChange' : True,
            'interlacing' : False,
            'autoSolve' : True
        }

        return p

    @staticmethod
    def formula(path):

        sv = path['showValues'].value
        p = str(path['p'].value) if sv else 'p'
        q1 = str(path['q'].value.x) if sv else 'q1'
        q2 = str(path['q'].value.y) if sv else 'q2'
        q3 = str(path['q'].value.z) if sv else 'q3'
        m1 = str(path['m'].value.x) if sv else 'm1'
        m2 = str(path['m'].value.y) if sv else 'm2'
        n1 = str(path['n'].value.x) if sv else 'n1'
        n2 = str(path['n'].value.y) if sv else 'n2'
        n3 = str(path['n'].value.z) if sv else 'n3'
        r1 = str(path['r'].value.x) if sv else 'r1'
        r2 = str(path['r'].value.y) if sv else 'r2'
        s1 = str(path['s'].value.x) if sv else 's1'
        s2 = str(path['s'].value.y) if sv else 's2'
        inter = path['interlacing'].value
        sc = "-" if path['signChange'].value else "+"


        x = "x = cos("+p+" * t) * (1 + "+r1+" * cos("+q1+" * t))"
        y = "y = sin("+p+" * t) * (1 + "+r1+" * cos("+q1+" * t))"

        if inter :
            z = "z = "+s1+" * sin(("+p+" - 1) * "+q1+" * t)"
        else :
            z = "z = "+r1+" * sin("+q1+" * t)"

        n = "\n"

        return x + n + y + n + z

    @staticmethod
    def draw(path):
        points = []
        
        pc = path['pointCount'].value
        sx = path['size'].value.x
        sy = path['size'].value.y
        sz = path['size'].value.z
        p = path['p'].value
        q1 = path['q'].value.x
        q2 = path['q'].value.y
        q3 = path['q'].value.z
        m1 = path['m'].value.x
        m2 = path['m'].value.y
        n1 = path['n'].value.x
        n2 = path['n'].value.y
        n3 = path['n'].value.z
        r1 = path['r'].value.x
        r2 = path['r'].value.y
        s1 = path['s'].value.x
        s2 = path['s'].value.y
        sc = 1 if path['signChange'].value else - 1
        inter = path['interlacing'].value
        
        splineLength = 2.0 * math.pi
        segment = 1.0/float(pc)

        for i in range(0, pc):
            t = splineLength * segment * i
            point = c4d.Vector(0,0,0)

            point[0] = float(math.cos(p * t) * (1 + r1 * math.cos(q1 * t))) / splineLength * 2.0 * sx
            point[1] = float(math.sin(p * t) * (1 + r1 * math.cos(q1 * t))) / splineLength * 2.0 * sy

            if inter :
                point[2] = float(s1 * math.sin((p - 1) * q1 * t)) / splineLength * 2.0 * sz
            else :
                point[2] = float(r1 * math.sin(q1 * t)) / splineLength * 2.0 * sz
            
            points.append(point)
        
        return points

class TorusB():

    @staticmethod
    def params():
        
        # Determines which parameters to show / hide.
        # True means it is hidden.
        p = {
            'p' : False,
            'q' : False,
            'm' : False,
            'n' : False,
            'r' : False,
            's' : False,
            'signChange' : False,
            'interlacing' : True,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def formula(path):

        sv = path['showValues'].value
        p = str(path['p'].value) if sv else 'p'
        q1 = str(path['q'].value.x) if sv else 'q1'
        q2 = str(path['q'].value.y) if sv else 'q2'
        q3 = str(path['q'].value.z) if sv else 'q3'
        m1 = str(path['m'].value.x) if sv else 'm1'
        m2 = str(path['m'].value.y) if sv else 'm2'
        n1 = str(path['n'].value.x) if sv else 'n1'
        n2 = str(path['n'].value.y) if sv else 'n2'
        n3 = str(path['n'].value.z) if sv else 'n3'
        r1 = str(path['r'].value.x) if sv else 'r1'
        r2 = str(path['r'].value.y) if sv else 'r2'
        s1 = str(path['s'].value.x) if sv else 's1'
        s2 = str(path['s'].value.y) if sv else 's2'
        inter = path['interlacing'].value
        sc = "-" if path['signChange'].value else "+"

        x = "x = "+m1+" * cos("+p+" * t) "+sc+" "+n1+" * cos("+q1+" * t) "+sc+" "+n2+" * cos("+q2+" * t)"
        y = "y = "+m2+" * sin("+p+" * t) + "+n1+" * sin("+q1+" * t) + "+n2+" * sin("+q2+" * t)"
        z = "z = "+s1+" * sin("+r1+" * t) + "+s2+" * sin("+r2+" * t)"
        n = "\n"

        return x + n + y + n + z

    @staticmethod
    def draw(path):
        points = []
        
        pc = path['pointCount'].value
        sx = path['size'].value.x
        sy = path['size'].value.y
        sz = path['size'].value.z
        p = path['p'].value
        q1 = path['q'].value.x
        q2 = path['q'].value.y
        q3 = path['q'].value.z
        m1 = path['m'].value.x
        m2 = path['m'].value.y
        n1 = path['n'].value.x
        n2 = path['n'].value.y
        n3 = path['n'].value.z
        r1 = path['r'].value.x
        r2 = path['r'].value.y
        s1 = path['s'].value.x
        s2 = path['s'].value.y
        sc = 1 if not path['signChange'].value else -1
        inter = path['interlacing'].value
        
        splineLength = 2.0 * math.pi
        segment = 1.0/float(pc)

        for i in range(0, pc):
            t = splineLength * segment * i
            point = c4d.Vector(0,0,0)
            
            point[0] = float(m1 * math.cos(p * t) + sc * n1 * math.cos(q1 * t) + sc * n2 * math.cos(q2 * t)) / splineLength * sx
            point[1] = float(m2 * math.sin(p * t) + n1 * math.sin(q1 * t) + n2 * math.sin(q2 * t)) / splineLength * sy
            point[2] = float(s1 * math.sin(r1 * t) + s2 * math.sin(r2 * t)) / splineLength * sz
            
            points.append(point)
        
        return points


class TorusC():

    @staticmethod
    def params():
        
        # Determines which parameters to show / hide.
        # True means it is hidden.
        p = {
            'p' : False,
            'q' : False,
            'm' : False,
            'n' : False,
            'r' : False,
            's' : False,
            'signChange' : False,
            'interlacing' : True,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def formula(path):

        sv = path['showValues'].value
        p = str(path['p'].value) if sv else 'p'
        q1 = str(path['q'].value.x) if sv else 'q1'
        q2 = str(path['q'].value.y) if sv else 'q2'
        q3 = str(path['q'].value.z) if sv else 'q3'
        m1 = str(path['m'].value.x) if sv else 'm1'
        m2 = str(path['m'].value.y) if sv else 'm2'
        n1 = str(path['n'].value.x) if sv else 'n1'
        n2 = str(path['n'].value.y) if sv else 'n2'
        n3 = str(path['n'].value.z) if sv else 'n3'
        r1 = str(path['r'].value.x) if sv else 'r1'
        r2 = str(path['r'].value.y) if sv else 'r2'
        s1 = str(path['s'].value.x) if sv else 's1'
        s2 = str(path['s'].value.y) if sv else 's2'
        inter = path['interlacing'].value
        sc = "-" if path['signChange'].value else "+"

        x = "x = "+m1+" * cos("+p+" * t) * (1 + "+n1+" * cos("+q1+" * t) "+sc+" "+n2+" * cos("+q2+" * t) "+sc+" "+n3+" * cos("+q3+" * t))"
        y = "y = "+m2+" * sin("+p+" * t) * (1 + "+n1+" * cos("+q1+" * t) + "+n2+" * cos("+q2+" * t) + "+n3+" * cos("+q3+" * t))"
        z = "z = "+s1+" * sin("+r1+" * t) + "+s2+" * sin("+r2+" * t)"
        n = "\n"

        return x + n + y + n + z

    @staticmethod
    def draw(path, signChange=False, interlace=False):
        points = []
        
        pc = path['pointCount'].value
        sx = path['size'].value.x
        sy = path['size'].value.y
        sz = path['size'].value.z
        p = path['p'].value
        q1 = path['q'].value.x
        q2 = path['q'].value.y
        q3 = path['q'].value.z
        m1 = path['m'].value.x
        m2 = path['m'].value.y
        n1 = path['n'].value.x
        n2 = path['n'].value.y
        n3 = path['n'].value.z
        r1 = path['r'].value.x
        r2 = path['r'].value.y
        s1 = path['s'].value.x
        s2 = path['s'].value.y
        sc = float(1.0) if not path['signChange'].value else float(-1.0)
        inter = path['interlacing'].value
        
        splineLength = 2.0 * math.pi
        segment = 1.0/float(pc)

        for i in range(0, pc):
            t = splineLength * segment * i
            point = c4d.Vector(0,0,0)

            point[0] = (m1 * math.cos(p * t) * (1.0 + n1 * math.cos(q1 * t) + (sc * n2 * math.cos(q2 * t)) + (sc * n3 * math.cos(q3 * t)))) / splineLength * sx
            point[1] = (m2 * math.sin(p * t) * (1.0 + n1 * math.cos(q1 * t) + n2 * math.cos(q2 * t) + n3 * math.cos(q3 * t))) / splineLength * sy
            point[2] = (s1 * math.sin(r1 * t) + s2 * math.sin(r2 * t)) / splineLength * sz
            
            points.append(point)
        
        return points

class Presets():

    @staticmethod
    def TorusAKnot23():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_A,
            'pointCount' : 32,
            'p' : 2.0,
            'q' : c4d.Vector(3.0, 0.0, 0.0),
            'm' : c4d.Vector(2.0, 0.0, 0.0),
            'r' : c4d.Vector(0.55, 0.0, 0.0),
            's' : c4d.Vector(1.0, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False
        }

        return p

    @staticmethod
    def TorusAKnot32():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_A,
            'pointCount' : 32,
            'p' : 3.0,
            'q' : c4d.Vector(2.0, 0.0, 0.0),
            'm' : c4d.Vector(2.0, 0.0, 0.0),
            'r' : c4d.Vector(0.55, 0.0, 0.0),
            's' : c4d.Vector(1.0, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False
        }

        return p

    @staticmethod
    def TorusAKnot37():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_A,
            'pointCount' : 64,
            'p' : 3.0,
            'q' : c4d.Vector(7.0, 0.0, 0.0),
            'm' : c4d.Vector(2.0, 0.0, 0.0),
            'r' : c4d.Vector(0.55, 0.0, 0.0),
            's' : c4d.Vector(1.0, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False
        }

        return p

    @staticmethod
    def TorusAKnot94():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_A,
            'pointCount' : 64,
            'p' : 9.0,
            'q' : c4d.Vector(4.0, 0.0, 0.0),
            'm' : c4d.Vector(2.0, 0.0, 0.0),
            'r' : c4d.Vector(0.55, 0.0, 0.0),
            's' : c4d.Vector(1.0, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False
        }

        return p

    @staticmethod
    def TorusBTrefoil():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 32,
            'p' : 1.0,
            'q' : c4d.Vector(2.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(2, 0.0, 0.0),
            'r' : c4d.Vector(-3.0, 0.0, 0.0),
            's' : c4d.Vector(1.0, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False,
            'signChange' : True,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBStarA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(-5.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.2, 0.0, 0.0),
            'r' : c4d.Vector(7.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 50.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBStarB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(-7.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.25, 0.0, 0.0),
            'r' : c4d.Vector(9.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 50.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBStarC():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(-3.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.45, 0.0, 0.0),
            'r' : c4d.Vector(5.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 50.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBStarD():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 3.0,
            'q' : c4d.Vector(-2.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.45, 0.0, 0.0),
            'r' : c4d.Vector(5.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBStarE():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 4.0,
            'q' : c4d.Vector(-1.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.45, 0.0, 0.0),
            'r' : c4d.Vector(5.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBFig8A():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(3.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(1.5, 0.0, 0.0),
            'r' : c4d.Vector(2.0, 0.0, 0.0),
            's' : c4d.Vector(0.2, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBFig8B():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 3.0,
            'q' : c4d.Vector(5.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(1.25, 0.0, 0.0),
            'r' : c4d.Vector(4.0, 0.0, 0.0),
            's' : c4d.Vector(0.5, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBFig8C():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(3.0, 5.0, 0.0),
            'm' : c4d.Vector(1.5, 1.0, 0.0),
            'n' : c4d.Vector(0.35, -0.9, 0.0),
            'r' : c4d.Vector(4.0, 2.0, 0.0),
            's' : c4d.Vector(0.1, -0.1, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 200.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBCircA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(5.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.75, 0.0, 0.0),
            'r' : c4d.Vector(6.0, 0.0, 0.0),
            's' : c4d.Vector(0.4, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBCircB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(7.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.67, 0.0, 0.0),
            'r' : c4d.Vector(10.0, 5.0, 0.0),
            's' : c4d.Vector(0.2, -0.1, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBCircC():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 4.0,
            'q' : c4d.Vector(7.0, 0.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.875, 0.0, 0.0),
            'r' : c4d.Vector(12.0, 3.0, 0.0),
            's' : c4d.Vector(0.35, -0.15, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBPairA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(-1.0, -3.0, 0.0),
            'm' : c4d.Vector(0.45, 0.45, 0.0),
            'n' : c4d.Vector(0.25, -0.45, 0.0),
            'r' : c4d.Vector(5.0, 0.0, 0.0),
            's' : c4d.Vector(0.2, 0.0, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBPairB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(-1.0, -3.0, 0.0),
            'm' : c4d.Vector(0.45, 0.45, 0.0),
            'n' : c4d.Vector(0.25, -0.45, 0.0),
            'r' : c4d.Vector(4.0, 2.0, 0.0),
            's' : c4d.Vector(0.25, 0.185, 0.0),
            'size' : c4d.Vector(200.0, 200.0, 100.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBCompoundA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(-2.0, -5.0, 0.0),
            'm' : c4d.Vector(0.59, 0.59, 0.0),
            'n' : c4d.Vector(0.3, -0.45, 0.0),
            'r' : c4d.Vector(9.0, 6.0, 0.0),
            's' : c4d.Vector(0.1, 0.25, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusBCompoundB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_B,
            'pointCount' : 64,
            'p' : 1.0,
            'q' : c4d.Vector(-3.0, 9.0, 0.0),
            'm' : c4d.Vector(0.6, 0.6, 0.0),
            'n' : c4d.Vector(0.25, -0.26, 0.0),
            'r' : c4d.Vector(16.0, 4.0, 0.0),
            's' : c4d.Vector(0.12, -0.06, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCFlowerA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(5.0, 10.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.6, 0.75, 0.0),
            'r' : c4d.Vector(5.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCFlowerB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(3.0, 9.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.45, 0.4, 0.0),
            'r' : c4d.Vector(9.0, 0.0, 0.0),
            's' : c4d.Vector(0.2, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCFlowerC():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 128,
            'p' : 2.0,
            'q' : c4d.Vector(3.0, 9.0, 15.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.15, 0.35, -0.4),
            'r' : c4d.Vector(15.0, 0.0, 0.0),
            's' : c4d.Vector(0.25, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCStarA():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 128,
            'p' : 3.0,
            'q' : c4d.Vector(5.0, 10.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.3, 0.5, 0.0),
            'r' : c4d.Vector(10.0, 0.0, 0.0),
            's' : c4d.Vector(0.2, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCStarB():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 128,
            'p' : 3.0,
            'q' : c4d.Vector(4.0, 16.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.35, 0.25, 0.0),
            'r' : c4d.Vector(20.0, 0.0, 0.0),
            's' : c4d.Vector(0.2, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCStarC():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 128,
            'p' : 4.0,
            'q' : c4d.Vector(5.0, 20.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.5, 0.4, 0.0),
            'r' : c4d.Vector(15.0, 0.0, 0.0),
            's' : c4d.Vector(0.35, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p

    @staticmethod
    def TorusCStarD():
        p = {
            'knotType' : c4d.NOODLE_TYPE_TORUS_C,
            'pointCount' : 64,
            'p' : 2.0,
            'q' : c4d.Vector(7.0, 9.0, 0.0),
            'm' : c4d.Vector(1.0, 1.0, 0.0),
            'n' : c4d.Vector(0.4, 0.485, 0.0),
            'r' : c4d.Vector(9.0, 0.0, 0.0),
            's' : c4d.Vector(0.3, 0.0, 0.0),
            'interlacing' : False,
            'signChange' : False,
            'autoSolve' : False
        }

        return p



class Noodle(c4d.plugins.ObjectData):
    
    ###
    ### Local variables used in class:
    ###
    ###     isDirty     - Whether this object has changed and needs to be updated.
    ###     isPreset    - Whether the object is currently using a preset. Set back to false if any value changes.
    ###     path        - Stores of the information of the knot path. 
    ###
    ###


    ###
    ### Called all the damn time. No real idea what it is for. Not like a constructor call.
    ###
    def __init__(self):
        self.SetOptimizeCache(False)


    def Init(self, op):
        
        self.isDirty = True
        self.isPreset = False

        if not hasattr(self, "path"):
            self.createPathData(op)

        return True

    ###
    ### GetContour is called when the spline is redrawn. Create a new spline object, set its points, and return the object.
    ###
    def GetContour(self, op, doc, lod, bt):

        # Update path data information and check for chagnes.
        self.updateKnot(op)

        # Create a new spline object that will be used as the spline drawn.
        spline = c4d.SplineObject(self.path['pointCount'].value, c4d.SPLINETYPE_CUBIC)

        # Whether or not the spline is closed.
        spline[c4d.SPLINEOBJECT_CLOSED] = self.path['closeSpline'].value

        # Draws the point vectors of the knot based on formula and parameters. Returns an array of vectors.
        points = self.path['knotType'].selected.draw(self.path)
        
        # Sets the points on the spline, creating the line.
        spline.SetAllPoints(points)

        # Weird spline type toggle hack to calculate the tangents on the curve.
        # Currently not working for Bezier spline type.
        spline[c4d.SPLINEOBJECT_TYPE] = 0
        spline[c4d.SPLINEOBJECT_TYPE] = self.path['splineType'].selected.index
        
        # Let C4D know shit changed.
        #c4d.EventAdd()

        # Return the new spline object to be drawn.
        return spline

    ###
    ### Overrides the description get method for each of the description elements on the object.
    ### Using this funtion to set input parameters to hidden or shown based on formula selected.
    ###
    def GetDDescription(self, node, description, flags):

        data = node.GetDataInstance()
        if data is None:
            return False


        # Before adding dynamic parameters, load the parameters from the description resource
        if not description.LoadDescription(node.GetType()):
            return False

        # Check to see if path data exists yet
        if not hasattr(self, "path"):
            return False

        # Get description single ID
        singleID = description.GetSingleDescID()
        
        # Check to see if flags are not none.
        if self.path and flags is not c4d.DESCFLAGS_DESC_0 :
            
            # Get the selected knot type
            self.updateKnot(node, True)

            selected = self.path['knotType'].selected
            params = selected.data['p']

            # Loop over current formula parameters and enable disable each.
            for p in params :
                # Get the userdata id of the current data object
                udid = self.path[p].udid
                
                # Get an instance of the Description object
                desc = description.GetParameter(udid)
                
                # Set the Show / Hide value on the Description object
                desc.SetLong(c4d.DESC_HIDE, params[p])
                
                # Replace Description with the new modified Description
                description.SetParameter(udid, desc, c4d.NOODLE_GROUP_KNOT_PROPS)
        
        
        # After parameters have been loaded and added successfully, return True and DESCFLAGS_DESC_LOADED with the input flags
        return (True, flags | c4d.DESCFLAGS_DESC_LOADED)

    ###
    ### Overrides enabling get call allowing to show whether an input value is enabled or disabled.
    ###
    def GetDEnabling(self, node, id, t_data, flags, itemdesc):

        # Used for enabling and disabling input fields. For now, setting it to just disable the fourier preset.
        if id[0].id == c4d.NOODLE_FORMULA_VIEW :
            return False

        if id[0].id == c4d.NOODLE_VAR_R or id[0].id == c4d.NOODLE_VAR_S :

            knotType = self.path['knotType'].value
            
            if knotType == c4d.NOODLE_TYPE_TORUS_B or knotType == c4d.NOODLE_TYPE_TORUS_C :
                return not bool(self.path['autoSolve'].value)

        return True

    ###
    ### Creates all the path data objects.
    ###
    def createPathData(self, op):

        # Creating data objects for the Knot Type dropdown.
        knotItems = [
            DataListItemObject([0, 'Torus A', TorusA.draw, c4d.NOODLE_TYPE_TORUS_A, {'p':TorusA.params(),'f':TorusA.formula}]),
            DataListItemObject([1, 'Torus B', TorusB.draw, c4d.NOODLE_TYPE_TORUS_B, {'p':TorusB.params(),'f':TorusB.formula}]),
            DataListItemObject([2, 'Torus C', TorusC.draw, c4d.NOODLE_TYPE_TORUS_C, {'p':TorusC.params(),'f':TorusC.formula}])
        ]
        
        # Creating data objects for the Presets dropdown.
        presetItems = [
            DataListItemObject([0, 'No Preset', None, c4d.NOODLE_CUSTOM_PRESET, {}]),
            DataListItemObject([0, 'Torus A - 2,3', None, c4d.NOODLE_PRESET_A_KNOT_23, Presets.TorusAKnot23()]),
            DataListItemObject([0, 'Torus A - 3,2', None, c4d.NOODLE_PRESET_A_KNOT_32, Presets.TorusAKnot32()]),
            DataListItemObject([0, 'Torus A - 3,7', None, c4d.NOODLE_PRESET_A_KNOT_37, Presets.TorusAKnot37()]),
            DataListItemObject([0, 'Torus A - 4,9', None, c4d.NOODLE_PRESET_A_KNOT_94, Presets.TorusAKnot94()]),
            DataListItemObject([0, 'Torus B - Trefoil', None, c4d.NOODLE_PRESET_B_TREFOIL, Presets.TorusBTrefoil()]),
            DataListItemObject([0, 'Torus B - Star 1', None, c4d.NOODLE_PRESET_B_STAR_A, Presets.TorusBStarA()]),
            DataListItemObject([0, 'Torus B - Star 2', None, c4d.NOODLE_PRESET_B_STAR_B, Presets.TorusBStarB()]),
            DataListItemObject([0, 'Torus B - Star 3', None, c4d.NOODLE_PRESET_B_STAR_C, Presets.TorusBStarC()]),
            DataListItemObject([0, 'Torus B - Star 4', None, c4d.NOODLE_PRESET_B_STAR_D, Presets.TorusBStarD()]),
            DataListItemObject([0, 'Torus B - Star 5', None, c4d.NOODLE_PRESET_B_STAR_E, Presets.TorusBStarE()]),
            DataListItemObject([0, 'Torus B - Figure Eight 1', None, c4d.NOODLE_PRESET_B_FIG8_A, Presets.TorusBFig8A()]),
            DataListItemObject([0, 'Torus B - Figure Eight 2', None, c4d.NOODLE_PRESET_B_FIG8_B, Presets.TorusBFig8B()]),
            DataListItemObject([0, 'Torus B - Figure Eight 3', None, c4d.NOODLE_PRESET_B_FIG8_C, Presets.TorusBFig8C()]),
            DataListItemObject([0, 'Torus B - Circulating 1', None, c4d.NOODLE_PRESET_B_CIRC_A, Presets.TorusBCircA()]),
            DataListItemObject([0, 'Torus B - Circulating 2', None, c4d.NOODLE_PRESET_B_CIRC_B, Presets.TorusBCircB()]),
            DataListItemObject([0, 'Torus B - Circulating 3', None, c4d.NOODLE_PRESET_B_CIRC_C, Presets.TorusBCircC()]),
            DataListItemObject([0, 'Torus B - Knot Pair 1', None, c4d.NOODLE_PRESET_B_PAIR_A, Presets.TorusBPairA()]),
            DataListItemObject([0, 'Torus B - Knot Pair 2', None, c4d.NOODLE_PRESET_B_PAIR_B, Presets.TorusBPairB()]),
            DataListItemObject([0, 'Torus B - Compound 1', None, c4d.NOODLE_PRESET_B_COMP_A, Presets.TorusBCompoundA()]),
            DataListItemObject([0, 'Torus B - Compound 2', None, c4d.NOODLE_PRESET_B_COMP_B, Presets.TorusBCompoundB()]),
            DataListItemObject([0, 'Torus C - Fleur 1', None, c4d.NOODLE_PRESET_C_FLEUR_A, Presets.TorusCFlowerA()]),
            DataListItemObject([0, 'Torus C - Fleur 2', None, c4d.NOODLE_PRESET_C_FLEUR_B, Presets.TorusCFlowerB()]),
            DataListItemObject([0, 'Torus C - Fleur 3', None, c4d.NOODLE_PRESET_C_FLEUR_C, Presets.TorusCFlowerC()]),
            DataListItemObject([0, 'Torus C - Star 1', None, c4d.NOODLE_PRESET_C_STAR_A, Presets.TorusCStarA()]),
            DataListItemObject([0, 'Torus C - Star 2', None, c4d.NOODLE_PRESET_C_STAR_B, Presets.TorusCStarB()]),
            DataListItemObject([0, 'Torus C - Star 3', None, c4d.NOODLE_PRESET_C_STAR_C, Presets.TorusCStarC()]),
            DataListItemObject([0, 'Torus C - Star 4', None, c4d.NOODLE_PRESET_C_STAR_D, Presets.TorusCStarD()])
        ]

        # Assigning index values programmatically
        for i in range(0, len(presetItems)) :
            presetItems[i].index = i


        # Creating data objects for the Spline Type dropdown.
        # TODO: Probably should just use the existing spline object resource base (ospline). Look to change in future.
        splineType = [
            DataListItemObject([0, 'Linear', None, c4d.NOODLE_SPLINE_TYPE_LINEAR, {}]),
            DataListItemObject([1, 'Cubic', None, c4d.NOODLE_SPLINE_TYPE_CUBIC, {}]),
            DataListItemObject([2, 'Akami', None, c4d.NOODLE_SPLINE_TYPE_AKIMA, {}]),
            DataListItemObject([3, 'B-Spline', None, c4d.NOODLE_SPLINE_TYPE_BSPLINE, {}]),
            DataListItemObject([4, 'Bezier', None, c4d.NOODLE_SPLINE_TYPE_BEZIER, {}])
        ]

        # Setting path data, the backbone of the plugin.
        self.path = {
            'presets' : DataListObject([0, presetItems, c4d.NOODLE_PRESETS]),
            'knotType' : DataListObject([0, knotItems, c4d.NOODLE_TYPE]),
            'pointCount' : DataObject([10, int, c4d.NOODLE_POINT_COUNT]),
            'size' : DataObject([c4d.Vector(200.0,200.0,200.0), c4d.Vector, c4d.NOODLE_SIZE]),
            'p' : DataObject([1.0, float, c4d.NOODLE_VAR_P]),
            'q' : DataObject([c4d.Vector(0.0,0.0,0.0), c4d.Vector, c4d.NOODLE_VAR_Q]),
            'm' : DataObject([c4d.Vector(0.0,0.0,0.0), float, c4d.NOODLE_VAR_M]),
            'n' : DataObject([c4d.Vector(0.0,0.0,0.0), c4d.Vector, c4d.NOODLE_VAR_N]),
            'r' : DataObject([c4d.Vector(0.0,0.0,0.0), c4d.Vector, c4d.NOODLE_VAR_R]),
            's' : DataObject([c4d.Vector(0.0,0.0,0.0), c4d.Vector, c4d.NOODLE_VAR_S]),
            'signChange' : DataObject([False, bool, c4d.NOODLE_SIGN_CHANGE]),
            'interlacing' : DataObject([False, bool, c4d.NOODLE_INTERLACING]),
            'autoSolve' : DataObject([False, bool, c4d.NOODLE_AUTO_SOLVE]),
            'showValues' : DataObject([True, bool, c4d.NOODLE_FORMULA_SHOW_VALUES]),
            'splineType' : DataListObject([0, splineType, c4d.NOODLE_SPLINE_TYPE]),
            'closeSpline' : DataObject([True, bool, c4d.NOODLE_SPLINE_CLOSED])
        }

        self.setDefaultValues(op, self.path)

        # Select random preset
        presetIndex = random.randint(0, len(presetItems))
        # Set self.path['preset'].value = presetItems[presetIndex]


    ###
    ### Setting default values for the inputs.
    ###
    def setDefaultValues(self, op, path):
        
        op[c4d.NOODLE_TYPE] = c4d.NOODLE_TYPE_TORUS_A
        op[c4d.NOODLE_PRESETS] = c4d.NOODLE_CUSTOM_PRESET
        op[c4d.NOODLE_POINT_COUNT] = 32
        op[c4d.NOODLE_SIZE] = c4d.Vector(200.0, 200.0, 200.0)
        op[c4d.NOODLE_VAR_P] = 2.0
        op[c4d.NOODLE_VAR_Q] = c4d.Vector(3.0, 0.0, 0.0)
        op[c4d.NOODLE_VAR_M] = c4d.Vector(1.0, 0.0, 0.0)
        op[c4d.NOODLE_VAR_N] = c4d.Vector(1.0, 0.0, 0.0)
        op[c4d.NOODLE_VAR_R] = c4d.Vector(0.5, 0.0, 0.0)
        op[c4d.NOODLE_VAR_S] = c4d.Vector(1.0, 0.0, 0.0)
        op[c4d.NOODLE_SIGN_CHANGE] = False
        op[c4d.NOODLE_INTERLACING] = False
        op[c4d.NOODLE_AUTO_SOLVE] = False
        op[c4d.NOODLE_SPLINE_TYPE] = c4d.NOODLE_SPLINE_TYPE_CUBIC
        op[c4d.NOODLE_SPLINE_CLOSED] = True

        self.updateKnot(op)


    ###
    ### Updates the interface if needed, used for setting preset values. 
    ###
    def updateInterface(self, op, pd):

        # Update the formula to match the formula type.
        if pd.udid == c4d.NOODLE_TYPE:
            #print "noodle type change"
            pass

        # If the preset has been changed, adjust the input values to the preset values.
        if pd.udid == c4d.NOODLE_PRESETS:
            params = pd.selected.data
            
            # Loop over the list of values in the preset and set the corresponding input values
            for p in params :
                pid = self.path[p].udid
                op[pid] = params[p]
            
            # Determine whether a preset is currently being used.
            if pd.selected.value is not c4d.NOODLE_CUSTOM_PRESET:
                self.isPreset = True
            else :
                self.isPreset = False

            c4d.EventAdd()
    
    ###
    ### Calculates R and S for TorusB and TorusC formula types.
    ###
    def calculateAutoSolve(self, op):

        # If formula type is B, add together the P and Q1 and set S1 to 1
        if self.path['knotType'].value == c4d.NOODLE_TYPE_TORUS_B :
            p = float(self.path['p'].value)
            q1 = float(self.path['q'].value.x)
            op[c4d.NOODLE_VAR_R] = c4d.Vector(float(math.fabs(p)+math.fabs(q1)), 0.0, 0.0)
            op[c4d.NOODLE_VAR_S] = c4d.Vector(1.0, 0.0, 0.0)

        # If formula type is C, set R1 to Q1 and and S1 to 1
        if self.path['knotType'].value == c4d.NOODLE_TYPE_TORUS_C :
            q1 = float(self.path['q'].value.x)
            op[c4d.NOODLE_VAR_R] = c4d.Vector(q1, 0.0, 0.0)
            op[c4d.NOODLE_VAR_S] = c4d.Vector(1.0, 0.0, 0.0)

    ###
    ### Looks for changes in the values and updates the path data.
    ### If we need to update any input values, look for the changes and update the interface accordingly.
    ###
    def updateKnot(self, op, final=False):
        
        # Check to see if an input field has changed.
        inputChange = False

        # Check to see if a preset selection has changed.
        presetChange = False

        # Loops over objects in the path data object
        for data in self.path:
            # Stores the current object in the loop
            pd = self.path[data]

            # Stores the new value that is taken from the associated input.
            pd.changed = op[pd.udid]

            # Checks to see if there has been a change from the current value.
            if pd.changed != pd.value:

                # Flags the whole object as dirty.
                self.isDirty = True
                inputChange = True

                # Updates the current value to the changed value.
                pd.value = pd.changed

                # Checks to see if the object that has changed is a dropdown list.
                if pd.type == DT_LIST:
                    
                    if pd.udid == c4d.NOODLE_PRESETS:
                        presetChange = True

                    # Loops over all of the items in the dropdown to see which was selected.
                    for i in range(0, len(pd.items)) :

                        # If the selected item matches the current item in the loop
                        if pd.value == pd.items[i].value :

                            # Store the selected item in the list object for easy access.
                            pd.selected = pd.items[pd.items[i].index]

                    # Update the interface with the dropdown change.
                    self.updateInterface(op, pd)

        if self.isDirty :

            # Lets the object know it is now up to date.
            self.isDirty = False

            # Update formula view
            op[c4d.NOODLE_FORMULA_VIEW] = self.path['knotType'].selected.data['f'](self.path)

            if self.path['autoSolve'].value and not final:
                self.calculateAutoSolve(op)

            self.updateKnot(op, True)

        # Check if input has changed and a preset exists, also check if this is the last time this loop is called.
        if inputChange is True and presetChange is False and not final:
            op[c4d.NOODLE_PRESETS] = c4d.NOODLE_CUSTOM_PRESET



if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    icon = bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(dir, "res", "noodle.tif"))
    success = plugins.RegisterObjectPlugin(
        id=PLUGIN_ID,
        str="Noodle",
        g=Noodle,
        description="Onoodle",
        icon=icon,
        info=c4d.OBJECT_GENERATOR|c4d.OBJECT_ISSPLINE)
    if success :
        print "Noodle Plugin V0.6 initialized."

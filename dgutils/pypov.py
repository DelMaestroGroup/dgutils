import sys, os

from math import *

import subprocess 
from .colors import hex_to_rgb
import numpy as np

# -----------------------------------------------------------------------------------
def sweep(start,end,num_points,rad,color='#6bff2b',transmit=0.8):
    ''' Return a sphere_sweep object.'''

    # bond color
    bond_color = hex_to_rgb(color)

    # generate the points
    v = np.array(end) - np.array(start)
    dv = v/num_points
    midpoint = start + 0.5*dv

    min_rad = 0.1*rad
    max_rad = 2.0*(rad-min_rad)/num_points

    path = []
    rads = []
    for n in range(num_points+1):
        path.append(list(start + dv*n))
        rads.append(max_rad*np.abs(n-0.5*num_points)+min_rad)

    sweep = 'sphere_sweep {\n linear_spline\n%d,\n' % len(path)
    for n in range(num_points+1):
        x,y,z = path[n]
        sweep +=  '<%f,%f,%f>, %f\n' % (*path[n],rads[n])
    sweep += 'texture {finish {ambient 1}\n pigment { color rgb <%f,%f,%f>\n transmit %f\n} }\n' % (*bond_color,transmit)
    sweep += '}\n\n'

    return sweep

# -----------------------------------------------------------------------------------
def sweep_from_path(path,rad,color='#6bff2b',transmit=0.8):
    ''' Return a sphere_sweep object for the given path.'''

    # bond color
    bond_color = hex_to_rgb(color)

    if not isinstance(rad,(list,)):
        rad = rad*np.ones(len(path))

    sweep = 'sphere_sweep {\n linear_spline\n%d,\n' % len(path)
    for n in range(len(path)):
        x,y,z = path[n]
        sweep +=  '<%f,%f,%f>, %f\n' % (*path[n],rad[n])
    sweep += 'texture {finish {ambient 1}\n pigment { color rgb <%f,%f,%f>\n transmit %f\n} }\n' % (*bond_color,transmit)
    sweep += '}\n\n'

    return sweep

# ----------------------------------------------------------------------------
def linear(r1,r2):
    ''' Return a function that performs a linear interpolation between two
    points. '''
    m = (r1[1]-r2[1])/(r1[0]-r2[0])
    b = r1[1] - m*r1[0]

    return lambda x: m*x + b


# ----------------------------------------------------------------------------
def generate_linear_path(start,end,num_points):
    '''Generate a linear path of num_points between start and end. '''

    # generate the points
    v = np.array(end) - np.array(start)
    dv = v/(num_points-1)

    path = []
    for n in range(num_points):
        path.append(list(start + dv*n))
    return path

# -----------------------------------------------------------------------------------
def pov_run(pov_file,width=1024,height=1,res="low"):
    
    low_res = ["-p"]
    
    if height == 1:
        height = int(3*width/4.0)
   
    if res == "high":
        pov_opts = ["-p","+H%d"%height,"+W%d"%width,"+Q11","+UA"]
    else:
        pov_opts = ["-p"]

    HOME = os.environ['HOME']
    povcmd = f'{HOME}/local/bin/povray' 
    povopts = f'{HOME}/.povray/3.7/povray.ini'

    # render the povray files
    subprocess.call([povcmd,povopts] + pov_opts + [pov_file])

# -----------------------------------------------------------------------------------
class File:
  def __init__(self,fnam="out.pov",*items):
    self.file = open(fnam,"w")
    self.__indent = 0
    self.writeln("#version %3.1f;" % 3.7)
    self.writeln("global_settings { assumed_gamma 1}")
    self.write(*items)
  def include(self,name):
    self.writeln( '#include "%s"'%name )
    self.writeln()
  def indent(self):
    self.__indent += 1
  def dedent(self):
    self.__indent -= 1
    assert self.__indent >= 0
  def block_begin(self):
    self.writeln( "{" )
    self.indent()
  def block_end(self):
    self.dedent()
    self.writeln( "}" )
    if self.__indent == 0:
      # blank line if this is a top level end
      self.writeln( )
  def write(self,*items):
    for item in items:
      if type(item) == str:
        self.include(item)
      else:
        item.write(self)
  def writeln(self,s=""):
    #print "  "*self.__indent+s
    self.file.write("  "*self.__indent+s+os.linesep)
  def close(self):
      self.file.close()

# -----------------------------------------------------------------------------------
class Vector:
  def __init__(self,*args):
    if len(args) == 1:
      self.v = args[0]
    else:
      self.v = args
  def __str__(self):
    return "<%s>"%(", ".join([str(x)for x in self.v]))
  def __repr__(self):
    return "Vector(%s)"%self.v
  def __mul__(self,other):
    return Vector( [r*other for r in self.v] )
  def __rmul__(self,other):
    return Vector( [r*other for r in self.v] )

# -----------------------------------------------------------------------------------
class Item:
  def __init__(self,name,args=[],opts=[],**kwargs):
    self.name = name
    args=list(args)
    for i in range(len(args)):
      if type(args[i]) == tuple or type(args[i]) == list:
        args[i] = Vector(args[i])
    self.args = args
    self.opts = opts
    self.kwargs=kwargs
  def append(self, item):
    self.opts.append( item )
  def write(self, file):
    file.writeln( self.name )
    file.block_begin()
    if self.args:
      file.writeln( ", ".join([str(arg) for arg in self.args]) )
    for opt in self.opts:
      if hasattr(opt,"write"):
        opt.write(file)
      else:
        file.writeln( str(opt) )
    for key,val in self.kwargs.items():
      if type(val)==tuple or type(val)==list:
        # AGD added on 2017-10-09 to deal with rgbt tuples
        # there is probably a better way to do this
        rgbt = False
        if len(val) == 4: 
            rgbt = True
        val = Vector(*val)
        if key == "color" and rgbt:
            key += " rgbt"
        file.writeln( "%s %s"%(key,val) )
      else:
        file.writeln( "%s %s"%(key,val) )
    file.block_end()
  def __setattr__(self,name,val):
    self.__dict__[name]=val
    if name not in ["kwargs","args","opts","name"]:
      self.__dict__["kwargs"][name]=val
  def __setitem__(self,i,val):
    if i < len(self.args):
      self.args[i] = val
    else:
      i += len(args)
      if i < len(self.opts):
        self.opts[i] = val
  def __getitem__(self,i,val):
    if i < len(self.args):
      return self.args[i]
    else:
      i += len(args)
      if i < len(self.opts):
        return self.opts[i]

# -----------------------------------------------------------------------------------
class FunctionItem:
  def __init__(self,name,args="",opts=[],**kwargs):
    self.name = name
    self.args = args
    self.opts = opts
    self.kwargs=kwargs
  def append(self, item):
    self.opts.append( item )
  def write(self, file):
    file.writeln( self.name )
    file.block_begin()
    if self.args:
      file.writeln( self.args )
    for opt in self.opts:
      if hasattr(opt,"write"):
        opt.write(file)
      else:
        file.writeln( str(opt) )
    for key,val in self.kwargs.items():
      if type(val)==tuple or type(val)==list:
        val = Vector(*val)
        file.writeln( "%s %s"%(key,val) )
      else:
        file.writeln( "%s %s"%(key,val) )
    file.block_end()
  def __setattr__(self,name,val):
    self.__dict__[name]=val
    if name not in ["kwargs","args","opts","name"]:
      self.__dict__["kwargs"][name]=val

# -----------------------------------------------------------------------------------
class Texture(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"texture",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Pigment(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"pigment",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Finish(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"finish",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Normal(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"normal",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Camera(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"camera",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class LightSource(Item):
  def __init__(self,v,*opts,**kwargs):
    Item.__init__(self,"light_source",(Vector(v),),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Background(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"background",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Box(Item):
  def __init__(self,v1,v2,*opts,**kwargs):
    Item.__init__(self,"box",(v1,v2),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Cylinder(Item):
  def __init__(self,v1,v2,r,*opts,**kwargs):
    " opts: open "
    Item.__init__(self,"cylinder",(v1,v2,r),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Plane(Item):
  def __init__(self,v,r,*opts,**kwargs):
    Item.__init__(self,"plane",(v,r),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Torus(Item):
  def __init__(self,r1,r2,*opts,**kwargs):
    Item.__init__(self,"torus",(r1,r2),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Cone(Item):
  def __init__(self,v1,r1,v2,r2,*opts,**kwargs):
    " opts: open "
    Item.__init__(self,"cone", (v1,r1,v2,r2),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Sphere(Item):
  def __init__(self,v,r,*opts,**kwargs):
    Item.__init__(self,"sphere",(v,r),opts,**kwargs)

# class Lathe(Item):
#   def __init__(self,v,r,*opts,**kwargs):
#     Item.__init__(self,"sphere",(v,r),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Union(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"union",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Intersection(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"intersection",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Difference(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"difference",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Merge(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"merge",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Object(Item):
  def __init__(self, *opts, **kwargs):
      Item.__init__(self, "object", (), opts, **kwargs)

# -----------------------------------------------------------------------------------
class Isosurface(Item):
  def __init__(self,*opts,**kwargs):
    Item.__init__(self,"isosurface",(),opts,**kwargs)

# -----------------------------------------------------------------------------------
class Function(FunctionItem):
    def __init__(self, f, *opts, **kwargs):
        FunctionItem.__init__(self, "function", (f),opts,**kwargs)


# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
x = Vector(1,0,0)
y = Vector(0,1,0)
z = Vector(0,0,1)
white = Texture(Pigment(color=(1,1,1)))

def tutorial31():
  " from the povray tutorial sec. 3.1"
  file=File("demo.pov","colors.inc","stones.inc")
  cam = Camera(location=(0,2,-3),look_at=(0,1,2))
  sphere = Sphere( (0,1,2), 2, Texture(Pigment(color="Yellow")))
  light = LightSource( (2,4,-3), color="White")
  file.write( cam, sphere, light )

def spiral():
  " Fibonacci spiral "
  gamma = (sqrt(5)-1)/2
  file = File()
  Camera(location=(0,0,-128), look_at=(0,0,0)).write(file)
  LightSource((100,100,-100), color=(1,1,1)).write(file)
  LightSource((150,150,-100), color=(0,0,0.3)).write(file)
  LightSource((-150,150,-100), color=(0,0.3,0)).write(file)
  LightSource((150,-150,-100), color=(0.3,0,0)).write(file)
  theta = 0.0
  for i in range(200):
    r = i * 0.5
    color = 1,1,1
    v = [ r*sin(theta), r*cos(theta), 0 ]
    Sphere( v, 0.7*sqrt(i),
      Texture(
        Finish(
          ambient = 0.0,
          diffuse = 0.0,
          reflection = 0.85,
          specular = 1
        ),
        Pigment(color=color))
    ).write(file)
    theta += gamma * 2 * pi

from manimlib.imports import *

class ClockOrganization(VGroup):
  CONFIG = {
    "numbers" : 4,
    "radius" : 3.1,
    "color" : WHITE
  }

  def __init__(self, **kwargs):
    digest_config(self, kwargs, locals())
    self.generate_nodes()
    VGroup.__init__(self, *self.node_list,**kwargs)

  def generate_nodes(self):
    self.node_list = []
    for i in range(self.numbers):
      mobject = VMobject()
      number = TexMobject(str(i+1))
      circle = Circle(radius=0.4,color=self.color)
      mobject.add(number)
      mobject.add(circle)
      mobject.move_to(
        self.radius * np.cos((-TAU / self.numbers) * i + 17*TAU / 84) * RIGHT
        + self.radius * np.sin((-TAU / self.numbers) * i + 17*TAU / 84) * UP
      )
      self.node_list.append(mobject)

  def select_node(self, node):
    selected_node = self.node_list[node]
    selected_node.scale(1.2)
    selected_node.set_color(RED)

  def deselect_node(self, selected_node):
    node = self.node_list[selected_node]
    node.scale(0.8)
    node.set_color(self.color)

class Testing3(Scene):
  def construct(self):
    test = ClockOrganization(numbers=21)
    self.play(Write(test), run_time=1.5)
    animation_steps=[]
    for i in range(10):
      thing = test.deepcopy()
      thing.select_node((19+i)%test.numbers-1)
      animation_steps.append(thing)
    self.play(Transform(test, animation_steps[0]))
    self.wait(2)
    for i in range(1,10):
      self.play(Transform(test, animation_steps[i]),run_time=0.3)
    self.wait()
import pyglet
from pyglet import shapes
from pyglet.window import key
from enum import Enum
import classes


window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

keys = key.KeyStateHandler()
window.push_handlers(keys)

greenScreen = pyglet.shapes.Rectangle(0, 0, 1000, 1000, color = (57, 255, 51), batch = batch)

###  TARGET
target = shapes.Circle(y=500, x=500, radius=10, color =(50, 0, 255), batch = batch)

### JOINTS
joint1 = classes.joint(batch, 0, target, distanceFromCenter=0, radius=5)
joint2 = classes.joint(batch, distanceMax=40, linked_to=joint1.joint, distanceFromCenter=0, radius=15)
joint3 = classes.joint(batch, distanceMax=40, linked_to=joint2.joint, distanceFromCenter=0, radius=20)
joint4 = classes.joint(batch, distanceMax=40, linked_to=joint3.joint, distanceFromCenter=0, radius=17)
joint5 = classes.joint(batch, distanceMax=40, linked_to=joint4.joint, distanceFromCenter=0, radius=15)
joint6 = classes.joint(batch, distanceMax=40, linked_to=joint5.joint, distanceFromCenter=0, radius=10)
joint7 = classes.joint(batch, distanceMax=40, linked_to=joint6.joint, distanceFromCenter=0, radius=10)

all_joints = [joint1, joint2, joint3, joint4, joint5, joint6, joint7]
bonner = classes.boner(all_joints)

articulation1 = classes.articulation(bonner, batch, whereIndexFrom=1, distanceFromCenter=100)
articulation2 = classes.articulation(bonner, batch, whereIndexFrom=3, distanceFromCenter=90)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        #target.y = y
        #target.x = x
        pass

# important
@window.event
def on_mouse_motion(x, y, dx, dy):
    target.y = y
    target.x = x

# dont change
@window.event
def on_draw():
    window.clear()
    batch.draw()

def update(dt):
    for joint in bonner.all_joints:
        joint.update_osco()
    articulation1.update_osco()
    articulation2.update_osco()


pyglet.clock.schedule_interval(update, 1/60.1)
pyglet.app.run()
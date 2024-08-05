from pyglet import shapes
import utils

class joint():
    def __init__(self, batch, distanceMax, linked_to, distanceFromCenter, radius):
        x = linked_to.x + distanceFromCenter
        y = linked_to.y

        if distanceMax != 0:
            y -= distanceMax

        self.joint = shapes.Circle(x=x, y=y, radius=radius, color =(50, 0, 255), batch = batch)
        self.actual_bone = shapes.Line(x=0, y=0, x2=0, y2=0, width=4, color=(200, 20, 20), batch=batch)
        self.linked = linked_to
        self.maxDistance = distanceMax
        self.distanceFromCenter = distanceFromCenter
        self.locked = False
        self.targetCoords = [0, 0]

    def update_osco(self):        
        vector = utils.normalize(utils.vector(self.joint, self.linked))
        if self.distanceFromCenter != 0:
            # switched
            if self.locked == False:
                vector = [-vector[1] * self.distanceFromCenter / 2, vector[0] * self.distanceFromCenter / 2]
                #self.joint.x = vector[0] + self.linked.x
                #self.joint.y = vector[1] + self.linked.y

                self.targetCoords[0] = vector[0] + self.linked.x
                self.targetCoords[1] = vector[1] + self.linked.y

                self.locked = True
        else:
            #self.joint.x = (vector[0] * self.maxDistance) + self.linked.x
            #self.joint.y = (vector[1] * self.maxDistance) + self.linked.y

            self.targetCoords[0] = (vector[0] * self.maxDistance) + self.linked.x
            self.targetCoords[1] = (vector[1] * self.maxDistance) + self.linked.y
        
        xtarget = (self.joint.x + self.targetCoords[0]) / 2
        ytarget = (self.joint.y + self.targetCoords[1]) / 2

        self.joint.x = xtarget
        self.joint.y = ytarget

        # ray
        self.actual_bone.x = self.joint.x
        self.actual_bone.y = self.joint.y
        self.actual_bone.x2 = self.linked.x
        self.actual_bone.y2 = self.linked.y



class boner():
    def __init__(self, joints) -> None:
        self.all_joints = joints

class articulation():
    def __init__(self, boner, batch, whereIndexFrom, distanceFromCenter) -> None:
        self.bonner = boner
        self.anchor = boner.all_joints[whereIndexFrom]
        self.arm1 = joint(batch, 100, self.anchor.joint, distanceFromCenter, radius=7)
        self.arm2 = joint(batch, 100, self.anchor.joint, -distanceFromCenter, radius=7)
        self.distanceFromCenter = distanceFromCenter

        self.pointToGetAwayFrom1 = shapes.Circle(x=self.arm1.joint.x, y=self.arm1.joint.y,
                                                radius=2, color =(50, 255, 0), batch = batch)
        self.pointToGetAwayFrom2 = shapes.Circle(x=self.arm2.joint.x, y=self.arm2.joint.y,
                                                radius=2, color =(50, 255, 0), batch = batch)
        boner.all_joints.append(self.arm1)
        boner.all_joints.append(self.arm2)

    def update_osco(self):
        distance1 = utils.distanceBetween2Points(self.pointToGetAwayFrom1, self.arm1.linked)
        if distance1 > self.distanceFromCenter:
            self.arm1.locked = False
            self.pointToGetAwayFrom1.x=self.arm1.joint.x
            self.pointToGetAwayFrom1.y=self.arm1.joint.y

        distance2 = utils.distanceBetween2Points(self.pointToGetAwayFrom2, self.arm2.linked)
        if distance2 > self.distanceFromCenter:
            self.arm2.locked = False
            self.pointToGetAwayFrom2.x=self.arm2.joint.x
            self.pointToGetAwayFrom2.y=self.arm2.joint.y

class boneIks():
    def __init__(self, joint: shapes.Circle, ending: shapes.Circle, batch) -> None:
        self.realBone = shapes.Line(x=joint.x, y=joint.y, x2=ending.x, y2=ending.y, batch=batch)
        self.joint = joint
        self.end = ending
    
    def update_osco(self):
        self.realBone.x = self.joint.x
        self.realBone.y = self.joint.y
        self.realBone.x2 = self.end.x
        self.realBone.y2 = self.end.y
        
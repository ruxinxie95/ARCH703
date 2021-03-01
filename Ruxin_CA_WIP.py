
#GAME OF LIGE 2D/3D
#Original code by Ezio Blasetti


#ARCH703_Virtual Engagement by Glenn Wilcox
#Ruxin Xie
#WIP WEEK 7
#Added Bone structure def addComponentMesh and subD

import rhinoscriptsyntax as rs
import random as rnd  
import Rhino.Geometry as rg
from scriptcontext import doc



class generateArray():
    def __init__(self, INTX, INTY, STRSTACK):
        self.intX = INTX
        self.intY = INTY
        self.strStack = STRSTACK
        self.ptMTX = {}
        self.valMTX = {}
        self.meshMTX = {}



        self.arrayValues()
        self.render(0)


    def applyGOL(self):
        newValues = {}

        for i in range(self.intX):
            for j in range(self.intY):
                sum = self.sumNeighbors(i, j)

                if self.valMTX[(i, j)] == 1:
                    if sum < 2:
                        newValues[(i,j)] = 0
                    elif sum > 3:
                        newValues[(i, j)] = 0
                    else:
                        newValues[(i, j)] = 1
                else:
                    if sum == 3:
                        newValues[(i, j)] = 1
                    else:
                        newValues[(i, j)] = 0

        self.valMTX = newValues

        return newValues


    def sumNeighbors(self, i, j):
        iplus1 = i + 1
        iminus1 = i - 1
        jplus1 = j + 1 
        jminus1 = j - 1

        if i == 0:
            iminus1 = self.intX - 1
        if i == self.intX - 1:
            iplus1 = 0
        if j == 0:
            jminus1 = self.intY - 1
        if j == self.intY - 1:
            jplus1 = 0
        
        sum = 0
        sum = sum + self.valMTX[(iminus1, jminus1)]
        sum = sum + self.valMTX[(i, jminus1)]
        sum = sum + self.valMTX[(iplus1, jminus1)]
        sum = sum + self.valMTX[(iminus1, j)]
        sum = sum + self.valMTX[(iplus1, j)]
        sum = sum + self.valMTX[(iminus1, jplus1)]
        sum = sum + self.valMTX[(i, jminus1)]
        sum = sum + self.valMTX[(iplus1, jplus1)]

        return sum

    def update(self, VALUES):
        for i in range(self.intX - 1):
            for j in range(self.intY - 1):
                self.colorObject(self.meshMTX[(i, j)], VALUES[(i, j)])

    def arrayValues(self):
        for i in range(self.intX):
            for j in range(self.intY):
                x = i
                y = j
                z = 0

                self.ptMTX[(i, j)] = (x, y, z)
                if rnd.randint(0, 1) == 0 :
                    self.valMTX[(i, j)] = 0

                else:
                    self.valMTX[(i, j)] = 1

    def render(self, z):
        rs.EnableRedraw(False)
        if self.strStack == "no":
            for i in range(self.intX):
                for j in range(self.intY):
                    if i > 0 and j> 0:
                        arrPoints = [self.ptMTX[(i, j)], self.ptMTX[(i-1, j)], self.ptMTX[(i-1, j-1)], self.ptMTX[(i, j-1)]]
                        self.meshMTX[(i-1, j-1)] = self.addMeshQuad(arrPoints)

            for i in range(self.intX - 1):
                for j in range(self.intY - 1):
                    self.colorObject(self.meshMTX[(i,j)], self.valMTX[(i, j)])
        else:
            for i in range(self.intX):
                for j in range(self.intY):
                    if i > 0 and j > 0 and self.valMTX[(i, j)] == 1:
                        arrPoints = [self.ptMTX[(i, j)], self.ptMTX[(i-1, j)], self.ptMTX[(i-1, j-1)], self.ptMTX[(i, j-1)]]
                        # self.addMeshBox(arrPoints, z)
                        self.addComponentMesh(arrPoints, z)
        rs.EnableRedraw(True)



    def addMeshQuad(self, ARRPOINTS):
        arrFaceVertices = []
        arrFaceVertices.append([0, 1, 2, 3])
        return rs.AddMesh(ARRPOINTS, arrFaceVertices)

    def colorObject(self, mesh, value):
        color = [value * 255, value * 255, value * 255]
        rs.ObjectColor(mesh, color)

        mat_index = rs.ObjectMaterialIndex(mesh)
        if mat_index == -1:
            mat_index = rs.AddMaterialToObject(mesh)
            rs.MaterialColor(mat_index, color)

    def addMeshBox(self, arrPts, z):

        arrVertices = []
        arrVertices.append([arrPts[0][0], arrPts[0][1], arrPts[0][2]+z])
        arrVertices.append([arrPts[1][0], arrPts[1][1], arrPts[1][2]+z])
        arrVertices.append([arrPts[2][0], arrPts[2][1], arrPts[2][2]+z])
        arrVertices.append([arrPts[3][0], arrPts[3][1], arrPts[3][2]+z])

        arrVertices.append([arrPts[0][0], arrPts[0][1], arrPts[0][2]+z+1])
        arrVertices.append([arrPts[1][0], arrPts[1][1], arrPts[1][2]+z+1])
        arrVertices.append([arrPts[2][0], arrPts[2][1], arrPts[2][2]+z+1])
        arrVertices.append([arrPts[3][0], arrPts[3][1], arrPts[3][2]+z+1])

        arrFaceVertices = []
        arrFaceVertices.append([0,3,2,1])
        arrFaceVertices.append([4,5,6,7])
        arrFaceVertices.append([0,4,7,3])
        arrFaceVertices.append([3,7,6,2])
        arrFaceVertices.append([2,6,5,1])
        arrFaceVertices.append([1,5,4,0])

        rs.AddMesh(arrVertices, arrFaceVertices)
    
    def addComponentMesh(self, arrPts, z):
        #Input bone structure scale factor
        factor = 0.3
        factorSide = 0.15

        #Find the bounding box vertices
        arrVertices = []
        innerPts = []

        arrVertices.append([arrPts[0][0], arrPts[0][1], arrPts[0][2]+z])
        arrVertices.append([arrPts[1][0], arrPts[1][1], arrPts[1][2]+z])
        arrVertices.append([arrPts[2][0], arrPts[2][1], arrPts[2][2]+z])
        arrVertices.append([arrPts[3][0], arrPts[3][1], arrPts[3][2]+z])

        arrVertices.append([arrPts[0][0], arrPts[0][1], arrPts[0][2]+z+1])
        arrVertices.append([arrPts[1][0], arrPts[1][1], arrPts[1][2]+z+1])
        arrVertices.append([arrPts[2][0], arrPts[2][1], arrPts[2][2]+z+1])
        arrVertices.append([arrPts[3][0], arrPts[3][1], arrPts[3][2]+z+1])
        
        pt00 = arrVertices[0]
        pt01 = arrVertices[1]
        pt02 = arrVertices[2]
        pt03 = arrVertices[3]
        pt04 = arrVertices[4]
        pt05 = arrVertices[5]
        pt06 = arrVertices[6]
        pt07 = arrVertices[7]

        pts = [pt00, pt01, pt02, pt03, pt04, pt05, pt06, pt07]

        #find bouding box center
        centroid = ((pt00[0] + pt06[0])/2, (pt00[1] + pt06[1])/2, (pt00[2] + pt06[2])/2)
        rs.AddPoint(centroid)

        #Generate inner vertices
        for i in range(len(pts)):

            innerPt = self.weightPt( centroid, pts[i], factor)
            innerPts.append(innerPt)

        sidePtIndex = [[0,4,7,3], [1,5,4,0], [2,6,5,1], [3,7,6,2], [7,4,5,6], [3,2,1,0]]

        meshes = []
        for i in range(6):
            
            side = sidePtIndex[i]
            arrsidePts = [pts[side[0]], pts[side[1]], pts[side[2]], pts[side[3]]]
            newarrsidePts = self.sideScale(arrsidePts, factorSide)
            arrinnerPts = [innerPts[side[0]], innerPts[side[1]], innerPts[side[2]], innerPts[side[3]]]

            #combine inner and side pt vertices 
            arrVertices = newarrsidePts + arrinnerPts

            # create mesh face vertices
            arrFaceVertices = []
            arrFaceVertices.append([0,4,7,3])
            arrFaceVertices.append([3,7,6,2])
            arrFaceVertices.append([2,6,5,1])
            arrFaceVertices.append([1,5,4,0])


            mesh = rs.AddMesh(arrVertices, arrFaceVertices)
            meshes.append(mesh)
            # rs.DeleteObject(mesh)
        joinedMesh = rs.JoinMeshes(meshes, True)
        meshObj = rs.coercemesh(joinedMesh)

        sub = rg.SubD.CreateFromMesh(meshObj)
        doc.Objects.AddSubD(sub)
        doc.Views.Redraw()
        rs.DeleteObject(joinedMesh)


    def sideScale(self, SIDEPTS, FACTORSIDE):
        sideNewPt = []
        midPt = ((SIDEPTS[0][0] + SIDEPTS[2][0])/2, (SIDEPTS[0][1] + SIDEPTS[2][1])/2,(SIDEPTS[0][2] + SIDEPTS[2][2])/2)

        for pt in SIDEPTS:
            scaledPt = self.weightPt(midPt, pt, FACTORSIDE)
            sideNewPt.append(scaledPt)
            
        return sideNewPt
    
    def weightPt(self, pt01, pt02, weight):
        #The bigger the weight is, the closer it is to the pt02
        pt = None
        newPt = (pt01[0] + (pt02[0] - pt01[0]) * weight, pt01[1] + (pt02[1] - pt01[1]) * weight, pt01[2] + (pt02[2] - pt01[2]) * weight)
        return newPt



def main():
    intX = rs.GetInteger("how many in x", 8)
    intY = rs.GetInteger("how many in y", 8)
    intGen = rs.GetInteger("how many generations", 15)
    strStack = rs.GetString("should I stack the generations", "yes", ["yes", "no"])

    if intX is not None:
        obj = generateArray(intX, intY, strStack)
        for i in range(intGen):
            rs.EnableRedraw(False)
            if strStack == 'no':
                values = obj.applyGOL()
                obj.update(values)
            else:
                obj.applyGOL()
                obj.render(i+1)



main()
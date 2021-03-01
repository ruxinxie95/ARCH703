import rhinoscriptsyntax as rs  
import random as rnd

class generateArray(object):
    def __init__(self, INTX, INTY):
        self.intX = INTX
        self.intY = INTY
        self.ptMTX = {}
        self.valMTX= {}
        self.meshMTX = {}

        self.pointMatrix()
        self.render()

    def pointMatrix(self):
        for i in range(self.intX):
            for j in range(self.intY):
                x = i
                y = j
                z = 0

                self.ptMTX[(i, j)] = (x , y , z)
                if rnd.randint(0,1) == 0:
                    self.valMTX[(i, j)] = 0
                else:
                    self.valMTX[(i, j)] = 1
    
    def render(self):
        for i in range(self.intX):
            for j in range(self.intY):
                if i > 0 and j > 0:
                    arrPoints = [self.ptMTX[(i, j)], self.ptMTX[(i-1, j)], self.ptMTX[(i-1, j-1)], self.ptMTX[(i, j-1)]]
                    self.meshMTX[(i-1, j-1)] = self.addMeshQuad(arrPoints)
                    # ??? why i-1, j-1
        for i in range(self.intX - 1):
            for j in range(self.intY - 1):
                self.colorObject(self.meshMTX[(i, j)], self.valMTX[(i, j)])

    def addMeshQuad(self, ARRPOINTS):
        arrVertices = [(0, 1, 2, 3)]
        return rs.AddMesh(ARRPOINTS, arrVertices)

    def colorObject(self, mesh, value):
        color = [value * 255, value * 255, value * 255]
        rs.ObjectColor(mesh, color)
        mat_index = rs.ObjectMaterialIndex(mesh)
        # if mat_index==-1: 
        #     mat_index = rs.AddMaterialToObject(mesh)

        rs.MaterialColor(mat_index, color)
                

def main():
    intX = rs.GetInteger("how many in x", 30)
    intY = rs.GetInteger("how many in y", 30)
    rs.EnableRedraw(False)
    obj = generateArray(intX, intY)
    rs.EnableRedraw(True)

main()
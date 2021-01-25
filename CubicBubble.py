"""This program creates the minimal surface (soap bubbles) inside of the cubic frame. """



import rhinoscriptsyntax as rs 
import random as rd 



def SurfacePoints(SRF, INTU, INTV,ATTR):

    """Generate the points on the base surface"""

    backPt = {}
    frontPt = {}

    thickFactor = 5

    Udomain = rs.SurfaceDomain(SRF, 0)
    Vdomain = rs.SurfaceDomain(SRF, 1)

    stepU = (Udomain[1] - Udomain[0])/INTU
    stepV = (Vdomain[1] - Vdomain[0])/INTV

    #Plotting points of the cubic frame on a surface
    count = 0
    for i in range(INTU + 1):
        for j in range(INTV + 1):
            
            if i == 0 or j == 0 or i == INTU or j == INTV:
                u = Udomain[0] + i * stepU
                v = Vdomain[0] + j * stepV 
            
            else:

                u = Udomain[0] + i * stepU + rd.random()*2
                v = Vdomain[0] + j * stepV + rd.random()*2


            pt = rs.EvaluateSurface(SRF, u, v)

            # rs.AddTextDot((i,j), pt)
            # rs.AddPoint(pt)

            backPt[(i, j)] = pt
            
            #Generate the normal direction points
            VectNorm = rs.SurfaceNormal(SRF, (u, v))
            VectNorm = rs.VectorScale(VectNorm, thickFactor)
            ptFront = rs.PointAdd(VectNorm, pt)

            # rs.AddTextDot((i,j), ptFront)
            # rs.AddPoint(ptFront)
            
            frontPt[(i, j)] = ptFront
            count += 1

    CenterCubic(ATTR, backPt, frontPt, INTU, INTV)

def CenterCubic(ATTR, backPt, frontPt, INTU, INTV):
    dist = []
    centerScale = []
    center = []

    #Find the centroid point and calculate distance to attractor point
    for i in range(INTU + 1):
        for j in range(INTV + 1):
            if i > 0 and j > 0:

                c = Centroid(backPt[(i, j)], frontPt[(i-1, j-1)])

                rs.AddPoint(c)
                d = rs.Distance(ATTR, c)
                dist.append(d)
                center.append(c)

    #Use Remap() funtion to generate scale factor for centroid cubic side
    for i in range(len(dist)):
        Scale = Remap(dist[i], min(dist), max(dist), 0.1, 0.6)
        centerScale.append((Scale, Scale, Scale))
        
            
    #Generate center cubic surfaces
    count = 0
    for i in range(INTU + 1):
        for j in range(INTV + 1):
            if i > 0 and j > 0:
                
                # srf01 = rs.AddSrfPt([backPt[(i, j)], backPt[(i-1, j)], backPt[(i-1, j-1)], backPt[(i, j-1)]])
                # innersrf01 = rs.ScaleObject(srf01, center[count], centerScale[count])

                # srf02 = rs.AddSrfPt((frontPt[(i, j)], frontPt[(i-1, j)], frontPt[(i-1, j-1)], frontPt[(i, j-1)]))
                # innersrf02 = rs.ScaleObject(srf02, center[count], centerScale[count])

                srf03 = rs.AddSrfPt((backPt[(i-1, j)], backPt[(i-1, j-1)], frontPt[(i-1, j-1)], frontPt[(i-1, j)]))
                innersrf03 = rs.ScaleObject(srf03, center[count], centerScale[count])

                srf04 = rs.AddSrfPt((backPt[(i, j)], frontPt[(i, j)], frontPt[(i, j-1)], backPt[(i, j-1)]))
                innersrf04 = rs.ScaleObject(srf04, center[count], centerScale[count])

                srf05 = rs.AddSrfPt((backPt[(i, j)], backPt[(i-1, j)], frontPt[(i-1, j)], frontPt[(i, j)]))
                innersrf05 = rs.ScaleObject(srf05, center[count], centerScale[count])

                srf06 = rs.AddSrfPt((backPt[(i, j-1)], backPt[(i-1, j-1)], frontPt[(i-1, j-1)], frontPt[(i, j-1)]))
                innersrf06 = rs.ScaleObject(srf06, center[count], centerScale[count])

                #Generate loft surfaces
                crv01 = rs.AddPolyline((backPt[(i, j)], backPt[(i-1, j)], backPt[(i-1, j-1)], backPt[(i, j-1)], backPt[(i, j)]))
                innercrv01 = rs.ScaleObject(crv01, center[count], centerScale[count],True)
                loftSrf01 = rs.AddLoftSrf([crv01, innercrv01])

                crv02 = rs.AddPolyline((frontPt[(i, j)], frontPt[(i-1, j)], frontPt[(i-1, j-1)], frontPt[(i, j-1)], frontPt[(i, j)]))          
                innercrv02 = rs.ScaleObject(crv02, center[count], centerScale[count],True)
                loftSrf02 = rs.AddLoftSrf([crv02, innercrv02])

                rs.DeleteObjects((crv01, crv02,innercrv01, innercrv02))

                #Join all surfaces together
                module = rs.JoinSurfaces([innersrf03, innersrf04, innersrf05, innersrf06,loftSrf01,loftSrf02],True)

                # Add Color and Material
                color = (int(255/INTU*i), int(255-(255/INTU)*j), int(255- 55/INTU*j))

                rs.ObjectColor(module, color)
                mat_index = rs.AddMaterialToObject(module)
                rs.MaterialColor(mat_index, color)

                count += 1
                

def Remap(oldVal, oldMin, oldMax, newMin, newMax):
    newVal = None
    newVal = ((oldVal - oldMin)/(oldMax-oldMin)) * (newMax-newMin) + newMin
    return newVal

def Centroid(PT01, PT02):
    pt = None
    pt = ((PT02[0] + PT01[0])/2, (PT02[1] + PT01[1])/2, (PT02[2] + PT01[2])/2)
    return pt


def main():

    srf = rs.GetObject("Please select a surface ", rs.filter.surface)
    if srf is None: return
    
    attr = rs.GetPoint("Select attract point" )
    if not attr:
        return

    intu = rs.GetInteger("Enter U interval", 10)
    intv = rs.GetInteger("Enter V interval", 6)

    rs.EnableRedraw(False)
    SurfacePoints(srf, intu, intv,attr)
    rs.HideObject(srf)
    rs.EnableRedraw(True)


main()

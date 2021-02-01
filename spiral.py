import rhinoscriptsyntax as rs

def SpiralRecursion(CRVGUID):
    if rs.CurveLength(CRVGUID) > 0.1:

        crvGUID = CRVGUID
        startPt = rs.CurveStartPoint(crvGUID)
        endPt = rs.CurveEndPoint(crvGUID)
        translation = endPt - startPt

        newLine = rs.CopyObject(crvGUID, translation)
        rs.RotateObject(newLine, endPt, 30, False)
        endPt_new = rs.CurveEndPoint(newLine)
        endPt_loaded = MidPtLoaded(endPt, endPt_new, 5, 6)
        
        newLine = rs.AddLine(endPt, endPt_loaded)

        SpiralRecursion(newLine)

def MidPtLoaded(aP1, aP2, load1, load2):

    MidPtLoaded = None
    MidPtLoaded = [(aP1[0] * load1 + aP2[0] * load2)/(load1 + load2),(aP1[1] * load1 + aP2[1] * load2)/(load1 + load2), (aP1[2] * load1 + aP2[2] * load2)/(load1 + load2)]
    return MidPtLoaded



    

def main():
    crvGUID = rs.GetObject("select the start curve", rs.filter.curve)
    SpiralRecursion(crvGUID)
main()
import rhinoscriptsyntax as rs

def addBranch(STRCRV, scale, angle, count):

    #create SECOND branch by copying FIRST
    #find startPt of STRCRV 
    startPt = rs.CurveStartPoint(STRCRV)
    
    #find endPt of STRCRV
    endPt = rs.CurveEndPoint(STRCRV)

    #calculate translation
    translation = endPt - startPt

    #copy STRCRV to create strLine01
    strLine01 = rs.CopyObject(STRCRV, translation)

    #scale SECOND branch strLine01 -  scale factor
    rs.ScaleObject(strLine01, endPt, scale)

    #rotate SECOND branch - angle
    rs.RotateObject(strLine01, endPt, angle)

    #create THIRD branch by mirroring SECOND - strLine02

    #recursively call function using SECOND and THIRD branches
    # if (count < 5):     
    #     addBranch(StrLine01, (0.75, 0.75, 0.75), 25, count + 1 )
    #     addBranch(StrLine02, (0.75, 0.75, 0.75), 25, count + 1 )




def main():
    strCRV = rs.GetObject('select line to branching', rs.filter.curve)

    addBranch(strCRV,(0.75, 0.75, 0.75), 25, 0)

main()

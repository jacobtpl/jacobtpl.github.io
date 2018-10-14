import numpy as np
import cv2
import sys
import landmark
import triangulation

# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = [];
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst

def avgpoint(p1, p2, alpha):
    return ((1 - alpha) * p1[0] + alpha * p2[0], (1 - alpha) * p1[1] + alpha * p2[1])

# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(imgFrom, imgTo, tris, t, numFaces, alpha) :

    # Find bounding rectangle for each triangle
    rBound = []
    for tri in tris:
        rBound.append(cv2.boundingRect(np.float32([tri])))

    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    trisRect = []
    tRect = []

    for i in range(numFaces):
        tr = []
        for j in range(3):
            tr.append(((tris[i][j][0] - rBound[i][0]),(tris[i][j][1] - rBound[i][1])))
        trisRect.append(tr)

    tRect = []
    for j in range(3):
        tRect.append(((t[j][0] - r[0],t[j][1] - r[1])))

    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # # Apply warpImage to small rectangular patches
    # img1Rect = imgOrig[rBound[0][1]:rBound[0][1] + rBound[0][3], rBound[0][0]:rBound[0][0] + rBound[0][2]]
    # img2Rect = imgOrig[rBound[1][1]:rBound[1][1] + rBound[1][3], rBound[1][0]:rBound[1][0] + rBound[1][2]]

    # Apply warpImage to small rectangular patches
    imgRect = []
    for rb in rBound:
        imgRect.append(imgFrom[rb[1]:rb[1] + rb[3], rb[0]:rb[0] + rb[2]])

    size = (r[2], r[3])
    # warpImage1 = applyAffineTransform(imgRect[0], trisRect[0], tRect, size)
    # warpImage2 = applyAffineTransform(imgRect[1], trisRect[1], tRect, size)

    warpImage = []
    for i in range(numFaces):
        warpImage.append(applyAffineTransform(imgRect[i], trisRect[i], tRect, size))
    
    # Alpha blend rectangular patches
    imgRectBlended = np.zeros((r[3], r[2], 3), dtype = np.float32)
    for w in warpImage:
        imgRectBlended = imgRectBlended + alpha * w

    # Copy triangular region of the rectangular patch to the output image
    imgTo[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = imgTo[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRectBlended * mask


def get_image(filename):
    imgOrig = cv2.imread(filename);

    points = np.float32(landmark.get_face_landmarks(imgOrig))

    numFaces = len(points)
    alpha = 1.0/numFaces

    # Allocate space for final output
    imgFinal = np.zeros(imgOrig.shape, dtype = imgOrig.dtype)

    # Generate triangulation
    triangles = []
    for i in range(numFaces):
        triangles.append(triangulation.get_triangulation(imgOrig, points[i]))

    for i in range(numFaces):
        for t in triangles[i]:
            x = t[0]
            y = t[1]
            z = t[2]
            tri = []
            for j in range(numFaces):
                if j==i:
                    triTo = [points[j][x],points[j][y],points[j][z]]
                else:
                    tri.append([points[j][x],points[j][y],points[j][z]])

            # Morph one triangle at a time.
            morphTriangle(imgOrig, imgFinal, tri, triTo, numFaces-1, 1/(numFaces-1))


    def inrange(x, y, r, c):
        if x<0 or x>=r or y<0 or y>=c:
            return False
        else:
            return True

    BLUR = 15
    r = imgFinal.shape[0]
    c = imgFinal.shape[1]

    weight = np.zeros((r, c), dtype=np.float32)
    ps = np.zeros((r+BLUR+1, c+BLUR+1), dtype=int)

    def filled(x1, y1, x2, y2):
        ret = ps[x2][y2]
        if x1>0:
            ret -= ps[x1-1][y2]
        if y1>0:
            ret -= ps[x2][y1-1]
        if x1>0 and y1>0:
            ret += ps[x1-1][y1-1]
        return ret

    def count(x1, y1, x2, y2):
        if x1<0:
            x1=0
        if y1<0:
            y1=0
        return (y2-y1+1)*(x2-x1+1)

    for i in range(r):
        for j in range(c):
            if imgFinal[i][j][0]!=0 or imgFinal[i][j][1]!=0 or imgFinal[i][j][2]!=0:
                ps[i][j]=1
            if i>0:
                ps[i][j] += ps[i-1][j]
            if j>0:
                ps[i][j] += ps[i][j-1]  
            if i>0 and j>0:
                ps[i][j] -= ps[i-1][j-1]  

    print("prefix table done")


    for i in range(r):
        for j in range(c):
            if imgFinal[i][j][0]!=0 or imgFinal[i][j][1]!=0 or imgFinal[i][j][2]!=0:
                w = filled(i-BLUR,j-BLUR,i+BLUR,j+BLUR)/count(i-BLUR,j-BLUR,i+BLUR,j+BLUR)
                weight[i][j] = max(0, w*2 - 1)

    print("computed weights")

    for i in range(r):
        for j in range(c):
            imgFinal[i][j] = (1-weight[i][j])*imgOrig[i][j] + weight[i][j]*imgFinal[i][j]
            # imgFinal[i][j] = [int(255*weight[i][j]),int(255*weight[i][j]),int(255*weight[i][j])]

    # Display Result
    cv2.imwrite( "output.jpg", np.uint8(imgFinal) );


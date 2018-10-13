import numpy as np
import cv2
import sys
import landmark
import triangulation as tri

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
# def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

#     # Find bounding rectangle for each triangle
#     r1 = cv2.boundingRect(np.float32([t1]))
#     r2 = cv2.boundingRect(np.float32([t2]))


#     # Offset points by left top corner of the respective rectangles
#     t1Rect = []
#     t2Rect = []


#     for i in range(0, 3):
#         t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
#         t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


#     # Get mask by filling triangle
#     mask = np.zeros((r1[3], r1[2], 3), dtype = np.float32)
#     cv2.fillConvexPoly(mask, np.int32(t1Rect), (1.0, 1.0, 1.0), 16, 0);

#     # Apply warpImage to small rectangular patches
#     img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
#     img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

#     size = (r1[2], r1[3])
#     warpImage1 = img1Rect
#     warpImage2 = applyAffineTransform(img2Rect, t2Rect, t1Rect, size)

#     # Alpha blend rectangular patches
#     imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

#     # Copy triangular region of the rectangular patch to the output image
#     img1[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img1[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in range(3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask


filename1 = 'dylan_nospecs.jpg'
filename2 = 'jacob.jpg'
alpha = 0.7

# Read images
img1 = cv2.imread(filename1);
img2 = cv2.imread(filename2);

# Read array of corresponding points
points1 = np.float32(landmark.get_face_landmarks(img1)[0])
points2 = np.float32(landmark.get_face_landmarks(img2)[0])

print(len(points1))
print(len(points2))

# Allocate space for final output
imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

t1 = tri.get_triangulation(img1, points1.astype(int))
t2 = tri.get_triangulation(img2, points2.astype(int))

# tri1 = []
# tri2 = []



# for i in range(min(len(t1),len(t2))):
#     tri1.append([(t1[i][0], t1[i][1]), (t1[i][2], t1[i][3]), (t1[i][4], t1[i][5])])
#     tri2.append([(t2[i][0], t2[i][1]), (t2[i][2], t2[i][3]), (t2[i][4], t2[i][5])])

# for i in range(min(len(t1),len(t2))):
#     morphTriangle(img1, img2, imgMorph, tri1[i], tri2[i], tri1[i], alpha)

for t in t1:
    x = t[0]
    y = t[1]
    z = t[2]
    t1 = [points1[x], points1[y], points1[z]]
    t2 = [points2[x], points2[y], points2[z]]

    # Morph one triangle at a time.
    morphTriangle(img1, img2, imgMorph, t1, t2, t1, alpha)
# Display Result
cv2.imshow("Morphed Face", np.uint8(imgMorph))
cv2.waitKey(0)
#!/usr/bin/python
 
import cv2
import numpy as np
import random
 
# Check if a point is inside a rectangle
def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True
 
# Draw a point
def draw_point(img, p, color ) :
    cv2.circle( img, p, 2, color)
 
 
# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :
 
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])
 
    for t in triangleList :
        print(t)
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
         
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
         
            cv2.line(img, pt1, pt2, delaunay_color, 1)
            cv2.line(img, pt2, pt3, delaunay_color, 1)
            cv2.line(img, pt3, pt1, delaunay_color, 1)
 
 
# Draw voronoi diagram
def draw_voronoi(img, subdiv) :
 
    ( facets, centers) = subdiv.getVoronoiFacetList([])
 
    for i in range(0,len(facets)) :
        ifacet_arr = []
        for f in facets[i] :
            ifacet_arr.append(f)
         
        ifacet = np.array(ifacet_arr, np.int)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
 
        cv2.fillConvexPoly(img, ifacet, color);
        ifacets = np.array([ifacet])
        cv2.polylines(img, ifacets, True, (0, 0, 0), 1)
        cv2.circle(img, (centers[i][0], centers[i][1]), 3, (0, 0, 0))
 
 
if __name__ == '__main__':
 
    # Define window names
    win_delaunay = "Delaunay Triangulation"
    win_voronoi = "Voronoi Diagram"
    win_tempImg = "Temp Img"
 
    # Turn on animation while drawing triangles
    animate = True
     
    # Define colors for drawing.
    delaunay_color = (255,255,255)
    points_color = (0, 0, 255)
 
    # Read in the image.
    img = cv2.imread("img2.jpg");
    # Keep a copy around
    img_orig = img.copy();
     
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
     
    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect);

    FACES = 2;
    points = [];
    subdiv = [];


    for i in range(FACES):
        # Create an array of points.
        points.append([]);
        subdiv.append(cv2.Subdiv2D(rect));
         
        # Read in the points from a text file
        with open("points"+str(i)+".txt") as file :
            for line in file :
                x, y = line.split()
                points[i].append((int(x), int(y)))
        for p in points[i] :
            subdiv[i].insert(p)

    for i in range(FACES):
        triangleList = subdiv[i].getTriangleList();
        for t in triangleList:
            pt1 = (int(t[0]),int(t[1]))
            pt2 = (int(t[2]),int(t[3]))
            pt3 = (int(t[4]),int(t[5]))
            dstBox = [min(int(t[0]),int(t[2]),int(t[4])), min(int(t[1]),int(t[3]),int(t[5])),max(int(t[0]),int(t[2]),int(t[4])), max(int(t[1]),int(t[3]),int(t[5]))]
            if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3) :

                dstTri = np.float32([[t[0],t[1]], [t[2],t[3]], [t[4],t[5]]]);
                for j in range (FACES):
                    if j != i:
                        index1 = points[i].index(pt1)
                        index2 = points[i].index(pt2)
                        index3 = points[i].index(pt3)
                        s0 = points[j][index1][0];
                        s1 = points[j][index1][1];
                        s2 = points[j][index2][0];
                        s3 = points[j][index2][1];
                        s4 = points[j][index3][0];
                        s5 = points[j][index3][1];
                        srcBox = [min(s0,s2,s4), min(s1,s3,s5),max(s0,s2,s4), max(s1,s3,s5)]

                        src = img_orig[srcBox[0]:srcBox[2], srcBox[1]:srcBox[3]]
                        cv2.imshow(win_tempImg, src)

                        srcTri = np.float32([[s0,s1], [s2,s3], [s4,s5]]);
                        transform = cv2.getAffineTransform(srcTri, dstTri);
                        #dstbox = cv2.warpAffine(src, transform, [dstBox[2]-dstBox[0]+1, dstBox[3]-dstBox[1]+1]);


                        







    
 
    # Insert points into subdiv
    
        # Show animation
        if animate :
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay( img_copy, subdiv[i], (255, 255, 255) );
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)
 
    # Draw delaunay triangles
    draw_delaunay( img, subdiv[i], (255, 255, 255) );
 
    # Draw points
    for p in points[i] :
        draw_point(img, p, (0,0,255))
 
    # Allocate space for Voronoi Diagram
    img_voronoi = np.zeros(img.shape, dtype = img.dtype)
 
    # Draw Voronoi diagram
    draw_voronoi(img_voronoi,subdiv[i])
 
    # Show results
    cv2.imshow(win_delaunay,img)
    cv2.imshow(win_voronoi,img_voronoi)
    cv2.waitKey(0)

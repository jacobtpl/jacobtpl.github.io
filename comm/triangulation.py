import numpy as np
import cv2
import sys

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

def index_of(vals, val):
	for i in range(len(vals)):
		if vals[i][0] == val[0] and vals[i][1] == val[1]:
			return i
	return -1

def get_triangulation(image, points):
	# Rectangle to be used with Subdiv2D
	size = image.shape
	rect = (0, 0, size[1], size[0])
	print(rect)
	# Create an instance of Subdiv2D
	subdiv = cv2.Subdiv2D(rect);

	for p in points:
		print(p)
		subdiv.insert((p[0],p[1]))

	# draw_delaunay(image, subdiv, (255, 0, 0))
	triangle_list = subdiv.getTriangleList().astype(int)
	
	output_list = []
	for t in triangle_list:
		x = index_of(points, (t[0], t[1]))
		y = index_of(points, (t[2], t[3]))
		z = index_of(points, (t[4], t[5]))

		if x!=-1 and y!=-1 and z!=-1:
			output_list.append([x,y,z])

	output_list.sort()
	print(len(output_list))
	print(output_list)
	return output_list
import math 
import copy

from random import randrange

# A class to represent a Point in 2D plane 
class Point(): 
	def __init__(self, x, y): 
		self.x = x 
		self.y = y 

# A utility function to find the 
# distance between two points 
def dist(p1, p2): 
	return math.sqrt((p1.x - p2.x) *
					(p1.x - p2.x) +
					(p1.y - p2.y) *
					(p1.y - p2.y)) 

# A Brute Force method to return the 
# smallest distance between two points 
# in P[] of size n 
# Time complexity: O(n ^ 2)
def getClosestUsingBruteForce(P): 
    n = len(P)    
	
    min_val = float('inf') 
    for i in range(n): 
        for j in range(i + 1, n): 
            if dist(P[i], P[j]) < min_val: 
                min_val = dist(P[i], P[j]) 

    return min_val 

# A utility function to find the 
# distance beween the closest points of 
# strip of given size. All points in 
# strip[] are sorted accordint to 
# y coordinate. They all have an upper 
# bound on minimum distance as d. 
# Note that this method seems to be 
# a O(n^2) method, but it's a O(n) 
# method as the inner loop runs at most 6 times 
def stripClosest(strip, size, d): 
	
	# Initialize the minimum distance as d 
	min_val = d 

	
	# Pick all points one by one and 
	# try the next points till the difference 
	# between y coordinates is smaller than d. 
	# This is a proven fact that this loop 
	# runs at most 6 times 
	for i in range(size): 
		j = i + 1
		while j < size and (strip[j].y -
							strip[i].y) < min_val: 
			min_val = dist(strip[i], strip[j]) 
			j += 1

	return min_val 

# A recursive function to find the 
# smallest distance. The array P contains 
# all points sorted according to x coordinate 
def closestUtil(P, Q, n): 
	
	# If there are 2 or 3 points, 
	# then use brute force 
	if n <= 3: 
		return getClosestUsingBruteForce(P) 

	# Find the middle point 
	mid = n // 2
	midPoint = P[mid] 

	# Consider the vertical line passing 
	# through the middle point calculate 
	# the smallest distance dl on left 
	# of middle point and dr on right side 
	dl = closestUtil(P[:mid], Q, mid) 
	dr = closestUtil(P[mid:], Q, n - mid) 

	# Find the smaller of two distances 
	d = min(dl, dr) 

	# Build an array strip[] that contains 
	# points close (closer than d) 
	# to the line passing through the middle point 
	strip = [] 
	for i in range(n): 
		if abs(Q[i].x - midPoint.x) < d: 
			strip.append(Q[i]) 

	# Find the closest points in strip. 
	# Return the minimum of d and closest 
	# distance is strip[] 
	return min(d, stripClosest(strip, len(strip), d)) 

# The main function that finds 
# the smallest distance. 
# This method mainly uses closestUtil() 
def getClosestDivideConquer(P):     
    P.sort(key = lambda point: point.x) 
    Q = copy.deepcopy(P) 
    Q.sort(key = lambda point: point.y)	 

    # Use recursive function closestUtil() 
    # to find the smallest distance 
    n = len(P)
    return closestUtil(P, Q, n) 


def euclidean_distance_sqr(point1, point2):
    """
    >>> euclidean_distance_sqr([1,2],[2,4])
    5
    """
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def column_based_sort(array, column=0):
    """
    >>> column_based_sort([(5, 1), (4, 2), (3, 0)], 1)
    [(3, 0), (5, 1), (4, 2)]
    """
    return sorted(array, key=lambda x: x[column])


def dis_between_closest_pair(points, points_counts, min_dis=float("inf")):
    """
    brute force approach to find distance between closest pair points
    Parameters :
    points, points_count, min_dis (list(tuple(int, int)), int, int)
    Returns :
    min_dis (float):  distance between closest pair of points
    >>> dis_between_closest_pair([[1,2],[2,4],[5,7],[8,9],[11,0]],5)
    5
    """

    for i in range(points_counts - 1):
        for j in range(i + 1, points_counts):
            current_dis = euclidean_distance_sqr(points[i], points[j])
            if current_dis < min_dis:
                min_dis = current_dis
    return min_dis


def dis_between_closest_in_strip(points, points_counts, min_dis=float("inf")):
    """
    closest pair of points in strip
    Parameters :
    points, points_count, min_dis (list(tuple(int, int)), int, int)
    Returns :
    min_dis (float):  distance btw closest pair of points in the strip (< min_dis)
    >>> dis_between_closest_in_strip([[1,2],[2,4],[5,7],[8,9],[11,0]],5)
    85
    """

    for i in range(min(6, points_counts - 1), points_counts):
        for j in range(max(0, i - 6), i):
            current_dis = euclidean_distance_sqr(points[i], points[j])
            if current_dis < min_dis:
                min_dis = current_dis
    return min_dis


def closest_pair_of_points_sqr(points_sorted_on_x, points_sorted_on_y, points_counts):
    """divide and conquer approach
    Parameters :
    points, points_count (list(tuple(int, int)), int)
    Returns :
    (float):  distance btw closest pair of points
    >>> closest_pair_of_points_sqr([(1, 2), (3, 4)], [(5, 6), (7, 8)], 2)
    8
    """

    # base case
    if points_counts <= 3:
        return dis_between_closest_pair(points_sorted_on_x, points_counts)

    # recursion
    mid = points_counts // 2
    closest_in_left = closest_pair_of_points_sqr(
        points_sorted_on_x, points_sorted_on_y[:mid], mid
    )
    closest_in_right = closest_pair_of_points_sqr(
        points_sorted_on_y, points_sorted_on_y[mid:], points_counts - mid
    )
    closest_pair_dis = min(closest_in_left, closest_in_right)

    """
    cross_strip contains the points, whose Xcoords are at a
    distance(< closest_pair_dis) from mid's Xcoord
    """

    cross_strip = []
    for point in points_sorted_on_x:
        if abs(point[0] - points_sorted_on_x[mid][0]) < closest_pair_dis:
            cross_strip.append(point)

    closest_in_strip = dis_between_closest_in_strip(
        cross_strip, len(cross_strip), closest_pair_dis
    )
    return min(closest_pair_dis, closest_in_strip)


def closest_pair_of_points(points, points_counts):
    """
    >>> closest_pair_of_points([(2, 3), (12, 30)], len([(2, 3), (12, 30)]))
    28.792360097775937
    """
    points_sorted_on_x = column_based_sort(points, column=0)
    points_sorted_on_y = column_based_sort(points, column=1)
    return (
        closest_pair_of_points_sqr(
            points_sorted_on_x, points_sorted_on_y, points_counts
        )
    ) ** 0.5

def generateRandomPointsAndSaveIt(n):
    file = open("Points.txt", "w+") 

    for i in range(n):
        x = randrange(10 * n)
        y = randrange(10 * n)

        file.write(str(x) + " " + str(y) + '\n')

    file.close()

def readPointArray():
    file = open("Points.txt", "r") 

    lines = file.readlines()

    file.close()

    points = []
    for li in lines:
       array = li.split(" ")
       x = int(array[0])
       y = int(array[1])

       points.append(Point(x, y))

    return points


def readPointArray1():
    file = open("Points.txt", "r") 

    lines = file.readlines()

    file.close()

    points = []
    for li in lines:
       array = li.split(" ")
       x = int(array[0])
       y = int(array[1])

       points.append((x, y))

    return points

n = 100

# generateRandomPointsAndSaveIt(n)

points = readPointArray()
points1 = readPointArray1()

n = len(points) 

print("The smallest distance based on Direct method  is", getClosestUsingBruteForce(points))
print("The smallest distance based on Direct method1  is", dis_between_closest_pair(points1, len(points1)) ** 0.5)
print("The smallest distance based on Divide and Conquer  is", getClosestDivideConquer(points))
print("The smallest distance based on Divide and Conquer1  is", closest_pair_of_points(points1, len(points1)))

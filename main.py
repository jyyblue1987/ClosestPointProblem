import time
from random import randrange

def dist(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def sort_based_index(array, column=0):
    return sorted(array, key=lambda x: x[column])


# brute force approach to find distance between closest pair points
def dis_using_direct_method(points, n, min_dis=float("inf")):
    for i in range(n - 1):
        for j in range(i + 1, n):
            current_dis = dist(points[i], points[j])
            if current_dis < min_dis:
                min_dis = current_dis
    return min_dis

# closest pair of points in strip
# Note that this method seems to be  
# a O(n^2) method, but it's a O(n)  
# method as the inner loop runs at most 6 times 
def strip_closest(points, n, min_dis=float("inf")):
    for i in range(min(6, n - 1), n):
        for j in range(max(0, i - 6), i):
            current_dis = dist(points[i], points[j])
            if current_dis < min_dis:
                min_dis = current_dis

    min_val = min_dis

    # for i in range(n): 
    #     j = i + 1
    #     while j < n and (points[j][0]- points[i][0]) < min_val: 
    #         min_val = dist(points[i], points[j])
    #         j += 1


    return min_val

# T(n)
def closest_util(s_on_x, s_on_y, n):
    # base case
    if n <= 3:
        return dis_using_direct_method(s_on_x, n)

    # recursion
    mid = n // 2
    dl = closest_util( s_on_x, s_on_y[:mid], mid) # T(n/2)
    dr = closest_util( s_on_y, s_on_y[mid:], n - mid) # T(n/2)
    d = min(dl, dr)

    strip = [] # O(n)
    for point in s_on_x:
        if abs(point[0] - s_on_x[mid][0]) < d:
            strip.append(point)

    d_strip = strip_closest(
        strip, len(strip), d
    )
    return min(d, d_strip)


def dis_using_divide_conquer(points, n):
    s_on_x = sort_based_index(points, column=0) # O(N*log(N))
    s_on_y = sort_based_index(points, column=1) # O(N*log(N))
    return (
        closest_util(
            s_on_x, s_on_y, n
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

       points.append((x, y))

    return points

n = 100
generateRandomPointsAndSaveIt(n)

points = readPointArray()
n = len(points) 

start = time.time()
dis = dis_using_direct_method(points, len(points)) ** 0.5
end = time.time()
print("The smallest distance based on Direct method  is", dis, "Running Time = ", (end - start), 's')

start = time.time()
dis = dis_using_divide_conquer(points, len(points))
end = time.time()
print("The smallest distance based on Divide and Conquer  is", dis, "Running Time = ", (end - start), 's')

# Time Complexity Let Time complexity of above algorithm be T(n). 
# Let us assume that we use a O(nLogn) sorting algorithm. 
# The above algorithm divides all points in two sets and recursively calls for two sets. 
# After dividing, it finds the strip in O(n) time, sorts the strip in O(nLogn) time and 
# finally finds the closest points in strip in O(n) time. So T(n) can expressed as follows
# T(n) = 2T(n/2) + O(n) + O(nLogn) + O(n)
# T(n) = 2T(n/2) + O(nLogn)
# T(n) = T(n x Logn x Logn)
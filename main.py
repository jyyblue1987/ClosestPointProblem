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
def dis_between_closest_in_strip(points, n, min_dis=float("inf")):
    for i in range(min(6, n - 1), n):
        for j in range(max(0, i - 6), i):
            current_dis = dist(points[i], points[j])
            if current_dis < min_dis:
                min_dis = current_dis

    return min_dis


def closest_util(points_sorted_on_x, points_sorted_on_y, n):
    # base case
    if n <= 3:
        return dis_using_direct_method(points_sorted_on_x, n)

    # recursion
    mid = n // 2
    closest_in_left = closest_util(
        points_sorted_on_x, points_sorted_on_y[:mid], mid
    )
    closest_in_right = closest_util(
        points_sorted_on_y, points_sorted_on_y[mid:], n - mid
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


def dis_using_divide_conquer(points, n):
    points_sorted_on_x = sort_based_index(points, column=0)
    points_sorted_on_y = sort_based_index(points, column=1)
    return (
        closest_util(
            points_sorted_on_x, points_sorted_on_y, n
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

# n = 100
# generateRandomPointsAndSaveIt(n)

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


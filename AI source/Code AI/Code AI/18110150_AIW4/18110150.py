#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from queue import PriorityQueue
import cv2 as cv # Open CV dùng để vẽ bảng đồ
import numpy as np

class peak(object):
    def __init__(self, th_poly, x, y):
        self.peak = [x, y]
        self.th_poly = th_poly

    def distance(self, p2):
        x1, y1 = self.peak[0], self.peak[1]
        x2, y2 = p2.peak[0], p2.peak[1]
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def __eq__(self, value):
        return self.peak == value.peak # and self.th_poly == value.th_poly

    def __str__(self):
        x, y, th = self.peak[0], self.peak[1], self.th_poly
        if th == None:
            return '(%d, %d)' % (x, y)
        return '(%d, %d, Polygon : %s)' % (x, y,str(th))

class polygon(object):
    def __init__(self, num_peak, list_peak):
        self.num_peak = num_peak
        self.list_peak = list_peak

def draw_poly(img, list_peak, name):
    pts = np.array(list_peak, np.int32)
    pts = pts.reshape((-1,1,2))
    cv.polylines(img, [pts], True, (0,0,0), 2)
    p = (list_peak[-1][0], list_peak[-1][1])
    cv.putText(img, name, p, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    return img

def draw_map(poly_main, start, goal, name):
    img = np.ones((560,820,3), np.uint8) * 255

    xs , ys = start.peak[0], start.peak[1]
    xg, yg = goal.peak[0], goal.peak[1]
    cv.putText(img, 'S', (xs, ys - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    cv.circle(img, (xs, ys), 5, (0,0,0), -1)
    cv.putText(img, 'G', (xg, yg - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    cv.circle(img, (xg, yg) , 5, (0,0,0), -1)

    for p in poly_main:
        temp = p.list_peak
        list_peak = [item.peak for item in temp]
        img = draw_poly(img, list_peak, str(temp[-1].th_poly))

    # img = img[::-1,:]
    cv.imwrite(name + '.jpg', img)
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return img

def draw_result(map, path, name):
    cost = 0
    for i in range(len(path) - 1):
        cost += path[i].distance(path[i + 1])
        p1 = (path[i].peak[0], path[i].peak[1])
        p2 = (path[i + 1].peak[0], path[i + 1].peak[1])
        cv.line(map, p1, p2, (255, 0, 0), 2)
    rows, cols = map.shape[0], map.shape[1]
    cv.putText(map, 'Path Cost: %3f' %(cost),(5, rows - 10), 
    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    cv.imwrite(name + '.jpg', map)
    cv.imshow(name, map)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return map

def line_equa(p , pline1, pline2):
    x1, y1 = pline1.peak[0], pline1.peak[1]
    x2, y2 = pline2.peak[0], pline2.peak[1]
    x, y = p.peak
    return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)

def check_see(P, A, B, Q):
    # kiểm tra Q có thấy được từ P qua canh AB
    d11 = line_equa(Q, P, A)
    d12 = line_equa(B, P, A)

    d21 = line_equa(Q, P, B)
    d22 = line_equa(A, P, B)

    d31 = line_equa(Q, A, B)
    d32 = line_equa(P, A, B)

    if d11 * d12 >= 0 and d21 * d22 >= 0 and d31 * d32 < 0:
        return False
    return True

def find(list, x):
    # Tìm kiếm 1 đỉnh x trong list các đỉnh
    for i in range(len(list)):
        if list[i] == x:
            return i
    return -1

def set_obserable(s, polys):
    '''
    Dùng để tìm các điểm có thể nhìn thấy từ s 
    '''
    # Nếu s là 1 đỉnh của poly thì không xét đỉnh đó
    is_s_in_poly = s.th_poly

    list_peaks = [] # tất cả các đỉnh bao gồm cả đích
    num_peaks = 0
    for poly in polys:
        num_peak, list_peak = poly.num_peak, poly.list_peak
        if list_peak[0].th_poly == is_s_in_poly:
            # Nếu s là 1 đỉnh của poly thì không xét đỉnh đó
            find_s = -1
            # Loại bỏ đỉnh trùng với s
            list_peak_temp = []
            for temp_p in list_peak:
                if temp_p != s:
                    list_peak_temp.append(temp_p)
                    num_peaks += 1
            continue
        list_peaks += list_peak
        num_peaks += num_peak

    left = [p for p in list_peaks]
    # xét 1 poly, trừ đích cuối cùng
    for i_poly in range(len(polys)):
        if polys[i_poly].num_peak == 1:
            # Không xét đỉnh đích trong danh sách polys
            continue
        i = 0
        delete = []
        num_peak = polys[i_poly].num_peak # số đỉnh của poly
        if polys[i_poly].list_peak[0].th_poly == is_s_in_poly:
            # Không xét đỉnh trùng với s
            find_s = find(polys[i_poly].list_peak, s)
            same_s = polys[i_poly].list_peak.pop(find_s)
            num_peak -= 1
        num_peak_left = len(left) # số đỉnh còn lại
        # duyệt từng đỉnh của poly đang xét
        while i < num_peak:
            if polys[i_poly].list_peak[i] == s:
                continue
            next = 0 if i == num_peak - 1 else i + 1
            # duyệt từng đỉnh còn lại
            for p in left:
                # Có thể thấy được từ s hay không?
                if p == polys[i_poly].list_peak[i] or p == polys[i_poly].list_peak[next]:
                    # không xét các đỉnh là cạnh đang xét
                    continue
                if not check_see(s, polys[i_poly].list_peak[i], polys[i_poly].list_peak[next], p):
                    temp = find(left, p)
                    if temp not in delete:
                        delete.append(temp)
            i += 1
        if  is_s_in_poly == polys[i_poly].list_peak[0].th_poly:
            if find_s != -1:
                polys[i_poly].list_peak.insert(find_s, same_s)
        # Xóa các đỉnh không nhìn thấy
        left = [left[i] for i in range(num_peak_left) if i not in delete]
    
        #thêm vào lại các đỉnh trong poly có thể thấy từ s
    return left

class node(object):
    def __init__(self, state = None, parent = None):
        self.state = state
        self.parent = parent
    
    def generate_node(self, polys):
        res = []
        temp = set_obserable(self.state, polys)
        for i in range(len(temp)):
            temp1 = node(temp[i], self)
            res.append(temp1)
        return res

    def trackPath(self):
        res = [self.state]
        path = self.parent
        while path:
            res.append(path.state)
            path = path.parent
        res = res[::-1]
        return res

    def __eq__(self, value):
        return self.state == value.state

class A_star_node(object):
    def __init__(self, state = None, parent = None, h = 0, g = 0):
        self.state = state
        self.parent = parent
        self.h = h
        self.g = g
        self.f = self.g + self.h

    def generate_node(self, polys, goal):
        res = []
        temp = set_obserable(self.state, polys)
        for i in range(len(temp)):
            temp1 = A_star_node(temp[i], self, 
            h= get_h(temp[i], goal), g= self.g + get_g(temp[i], self.state))
            res.append(temp1)
        return res

    def trackPath(self):
        res = [self.state]
        path = self.parent
        while path:
            res.append(path.state)
            path = path.parent
        res = res[::-1]
        return res

    def __str__(self):
        return '(%s, %f, %f, %f)' % (self.state, self.f, self.g, self.h)

    def __lt__(self, value):
        return self.f < value.f

    def __le__(self, value):
        return self.f <= value.self

    def __gt__(self, value):
        return self.f > value.self
    
    def __ge__(self, value):
        return self.f >= value.self

    def __eq__(self, value):
        return self.state == value.state and self.f == value.f

def A_star_search(polys, start, goal):
    OPEN = PriorityQueue()
    CLOSE = []
    initial_state = A_star_node(state= start, 
    parent=None, g= 0, h= get_h(start, goal))
    OPEN.put(initial_state)
    while True:
        if OPEN.empty():
            return False, 'No way Exception'
        current = OPEN.get()
        CLOSE.append(current)
        if current.state == goal:
            return True, current.trackPath()
        temp = current.generate_node(polys, goal)
        for n in temp:
            if n not in CLOSE:
                OPEN.put(n)

def searhPath(polys, start, goal, searh_algorithm):
    # Thực hiện thuật toán BFS hoặc DFS
    init_node = node(state= start)
    # Thêm goal vào polys để tìm đường ở vị trí cuối cùng
    polys.append(polygon(1, [goal]))

    if searh_algorithm == "A_star":
        return A_star_search(polys, start, goal)

    L = [init_node]# stack, or queue
    index = -1 if searh_algorithm == "BFS" else 0

    expanded = []
    
    while True:
        if L == []:
            return False, "No Way Exception"
        current = L.pop(index)
        expanded.append(current)
        if current.state == goal:
            return True, current.trackPath()
        temp = current.generate_node(polys)
        for n in temp:
            if n not in expanded:
                L.append(n)

def get_h(s, goal):
    return s.distance(goal)

def get_g(a, b):
    return a.distance(b)

if __name__ == "__main__":
    # Đọc file
    file = open('input.txt', 'r')
    inp = file.read().splitlines()
    inp = [[int(num) for num in list.split()] for list in inp]
    file.close()
    info = inp[0] 
    poly = inp[1:]

    num_poly = info[0] # số đa giác
    start = peak(None, info[1], info[2]) # Bắt đầu
    goal = peak(None, info[3], info[4]) # Đích
        
    poly = [(p[0], p[1:]) for p in poly]
    poly_main = [] # Danh sách các đa giác

    th_poly = 1
    for p in poly:
        temp = [peak(th_poly, p[1][i], p[1][i+1]) for i in range(0, len(p[1]) - 1, 2)]
        poly_main.append(polygon(p[0], temp))
        th_poly += 1

    # Có thể dùng BFS, DFS, A_star
    #searh_algorithm = "DFS"
    #searh_algorithm = "BFS"
    searh_algorithm = "A_star"

    # Vẽ bảng đồ
    map = draw_map(poly_main, start, goal, "Map")

    # Tìm đường đi
    found, path = searhPath(poly_main, start, goal, searh_algorithm)

    #Viết kết quả lên file
    output = open('Output ' + searh_algorithm + '.txt', 'w')
    cost = 0
    for i in range(len(path)):
        if i < len(path) - 1:
            cost += path[i].distance(path[i + 1])
        output.write('%s\n'%path[i])
    output.write('Path cost: %f'%(cost))
    output.close()

    # Vẽ Đường đi
    draw_result(map, path, "Result " + searh_algorithm)


import re
import Queue as Q

class state(object):
    def __init__(self):
        self.fn = -1
        self.gn = -1
        self.hn = -1
        self.pos = []
        self.police_left = -1
        self.next_row = -1
        return         
    
    def __cmp__(self, other):
        return cmp(self.fn, other.fn)
    
    def clone_pos(self):
        out = []
        for i in range(len(self.pos)):
            out.append(self.pos[i])
        return out
    
    def output_st(self):
        print "fn: ",self.fn
        print "gn: ",self.gn
        print "hn: ",self.hn
        print "pos: ",self.pos
        print "next_row: ",self.next_row
    
def input_function():
    with open("input.txt") as fi:
        n = int(fi.readline())
        p = int(fi.readline())
        s = int(fi.readline())
        intersection = []
        for i in range(n):
            new = []
            for j in range(n):
                new.append(0)
            intersection.append(new)
        for line in fi:
            x, y = re.split(',|\n', line)[:2]
            x = int(x)
            y = int(y)
            intersection[y][x] += 1
        return n,p,s,intersection 

def current_map(intersections, pos):
    tem = clone(intersection, n)
    for t in pos:
        for i in range(n):
            x = t[0]
            y = t[1]
            tem[i][y] = -1
            tem[x][i] = -1
            if x-i >= 0 and y+i < n:
                tem[x-i][y+i] = -1
            if x+i < n and y+i < n:
                tem[x+i][y+i] = -1
            if x-i >= 0 and y-i >= 0:
                tem[x-i][y-i] = -1
            if x+i < n and y-i >= 0:
                tem[x+i][y-i] = -1
    return tem
    
def count_hn(cur, pos, next_row):
    if(p-len(pos) > n - next_row):
        return 0
    s = []
    for i in range(next_row, n):
        x = cur[i][0]
        for j in range(n):
            if(cur[i][j] > x):
                x = cur[i][j]
        s.append(x)
    s.sort(reverse = True)
    h = 0
    for i in range(p-len(pos)):
        h += s[i]
    return h
    
def check(intersection):
    for i in range(n):
        for j in range(n):
            print ("{:02d}".format(intersection[i][j])),
        print(" ")

def clone(intersection, n):
    out = []
    for i in range(n):
        new = []
        for j in range(n):
            new.append(intersection[i][j])
        out.append(new)
    return out

def A_search(n, p, s, intersection):
    frontier = Q.PriorityQueue()
    #initial
    #don't choose in first roll
    #print("intial")
    st = state()
    st.gn = 0
    st.hn = count_hn(intersection, st.pos, 1)
    st.fn = -st.gn + -st.hn
    st.next_row = 1
    #st.output_st()
    frontier.put(st)
    for j in range(n):
        st = state()
        st.pos.append([0,j])
        st.gn = intersection[0][j]
        cur = current_map(intersection, st.pos)
        st.hn = count_hn(cur, st.pos, 1)
        st.fn = -st.gn + -st.hn
        st.next_row = 1
        #st.output_st()
        frontier.put(st)
    #print("while")
    while not frontier.empty():
        front = frontier.get()
        #print("front")
        #front.output_st()
        #print "p: ",p," len:", len(front.pos)
        if p-len(front.pos) == 0:
            return front
        cur = current_map(intersection, front.pos)
        #print("expand")
        i = front.next_row
        if(p-len(front.pos) > n - front.next_row):
            continue
        st = state()
        st.pos = front.clone_pos()
        st.gn = front.gn
        st.hn = count_hn(cur, front.pos, i+1)
        st.fn = -st.gn + -st.hn
        st.next_row = i + 1
        #st.output_st()
        #print("h_map")
        #check(cur)
        frontier.put(st)
        for j in range(n):
            if cur[i][j] == -1:
                continue
            st = state()
            st.pos = front.clone_pos()
            st.pos.append([i,j])
            st.gn = front.gn + cur[i][j]
            h_map = current_map(cur, st.pos)
            st.hn = count_hn(h_map, st.pos, i)
            st.fn = -st.gn + -st.hn
            st.next_row = i + 1
            #st.output_st()
            #print("h_map")
            #check(h_map)
            frontier.put(st)
        #print("expand_fin")
                    
    
n,p,s,intersection = input_function()
#check(intersection)
ans = A_search(n,p,s,intersection)
#check(intersection)
#print ans.pos
#print "ans: ",-ans.fn
with open("output.txt", "w") as fo:
    fo.write(str(-ans.fn) + "\n")

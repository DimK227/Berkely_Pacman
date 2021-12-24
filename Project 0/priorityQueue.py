import heapq

#priority queue using heap (with heapq)

class PriorityQueue:
    def __init__(self):
        self.heap = []
                                    #Initiate the priority queue
        self.count = 0
    def push(self,item, priority):     #This method iserts an item with its priority in the priority queue
        if item in (element[1] for element in self.heap):   #if the item already exists in queue do nothing. Just return false
            return False
        else:                                               #Else insert it and increase the count. Return true
            heapq.heappush(self.heap,(priority,item))
            self.count += 1
            return True
    def pop(self):                                          #This method returns the element with the minimum priority
        self.count -=1                                      #Decrease by one the count
        return heapq.heappop(self.heap)
    def isEmpty(self):                                      #This method checks if a queue is empty
        return self.count==0
    def update(self,item,priority):                         #This method updates the priority of an item (if the given on is smaller)
        f=0
        cnt=-1;
        for x in self.heap:
            cnt+=1
            if x[1]==item :                                #if you find the item
                f=1
                if x[0] > priority:                        #If the given priority is smaller
                    self.heap[cnt]=(priority,item)         #Replace it
        if f==0:                                           #If the item does not exist
            heapq.heappush(self.heap,(priority,item))      #Insert it
    def PQSort(self,list):                                 #This method takes a list of unsorted numbers and sorts it using the priority queue
        sorted_list = []
        pq = PriorityQueue()
        for i in list:
            pq.push(i,i)                                    #Inserts all the items of the list to the new queue
        for x in range(pq.count):
            y = pq.pop()                                    #Take one by one the smaller items
            sorted_list.append(y[1])                        #Insert only the item and not the priority
        return sorted_list

q = PriorityQueue()

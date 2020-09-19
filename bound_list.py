class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class UnorderedList:

    def __init__(self):
        self.head = None
        self.link = None

    def isEmpty(self):
        return self.head is None

    def add(self, item):
        if self.link is None:
            temp = Node(item)
            temp.setNext(self.head)
            self.head = temp
            self.link = temp
        else:
            temp = Node(item)
            temp.setNext(self.head)
            self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.getNext()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous is None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    def pop(self, ind=-1):
        pop_data = self.head
        previous = None
        place = 0
        if ind == -1:
            while pop_data is not None:
                previous = pop_data
                pop_data = pop_data.getNext()
            previous.setNext(pop_data)
            pop_data = previous
        else:
            while place < ind:
                previous = pop_data
                pop_data = pop_data.getNext()
                place += 1
            previous.next = pop_data.getNext()
        return pop_data.getData()

    def append(self, item):
        temp = Node(item)
        current = self.head
        previous = None
        while current is not None:
            previous = current
            current = current.getNext()
        previous.setNext(temp)
        temp.setNext(current)

    def insert(self, pos, item):
        if pos == 0:
            self.add(item)
        else:
            temp = Node(item)
            insert_data = self.head
            previous = None
            place = 0
            while place < pos:
                previous = insert_data
                insert_data = insert_data.getNext()
                place += 1
            previous.next = temp
            temp.next = insert_data

    def index(self, item):
        current = self.head
        count = 0
        while current.getData() != item:
            current = current.getNext()
            count += 1
        return count

    def list(self):
        current = self.head
        lst = []
        while current is not None:
            lst.append(current.getData())
            current = current.getNext()
        return lst


if __name__ == '__main__':
    mylist = UnorderedList()
    mylist.add(31)
    mylist.add(77)
    mylist.add(17)
    mylist.add(93)
    mylist.add(26)
    mylist.add(54)
    print(mylist.list())
    print(mylist.pop())
    print(mylist.list())
    mylist.insert(0, 500)
    print(mylist.list())
    print(mylist.index(26))
    mylist.append(100)
    print(mylist.list())


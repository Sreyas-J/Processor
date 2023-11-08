from collections import deque

queue = deque()

# Enqueue
queue.append(1)
queue.append(2)

# Dequeue
item = queue.popleft()
print(queue)

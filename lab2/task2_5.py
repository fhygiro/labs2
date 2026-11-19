import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, end):
    rows, columns = len(maze), len(maze[0])
    queue = [(0, start)]
    g_score = {start: 0}
    came_from = {}
    direct = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while queue:
        _, current = heapq.heappop(queue)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in direct:
            neighbor = (current[0] + dx, current[1] + dy)
            x, y = neighbor

            if not (0 <= x < rows and 0 <= y < columns):
                continue

            if maze[x][y] == 1:
                continue

            g = g_score[current] + 1

            if neighbor not in g_score or g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = g
                f = g + heuristic(neighbor, end)
                heapq.heappush(queue, (f, neighbor))

    return []

n = int(input('Кол-во строк: '))
print('Введите матрицу:')
maze = [list(map(int, input().split())) for _ in range(n)]
start = tuple(map(int, input('Начало: ').split()))
end = tuple(map(int, input('Конец: ').split()))

result = astar(maze, start, end)

if result:
    print(*result, sep=' -> ')
else:
    print('Путь не найден') 
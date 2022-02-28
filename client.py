import json
import sys

import socketio

if len(sys.argv) != 2:
    print("Usage: python3 temp_client.py <player_id>")
    exit(1)

sio = socketio.Client()

if sys.argv[1] == "1":
    PLAYER_ID = 'player1'
    PLAYER_PASSWORD = 'player1'
else:
    PLAYER_ID = 'player2'
    PLAYER_PASSWORD = 'player2'
PLAYER_ROOM = 'gameRoom'


@sio.event
def connect():
    print("I'm connected!")


counter = 1

visited = []
stack = []


def bfs(state):
    queue = []
    neighbour_list = state["movegen"]["Gamora"]["neighbour_cells"]
    print(neighbour_list)
    for i in range(len(neighbour_list)):
        for j in range(len(neighbour_list[i])):
            neighbour_coordinates = neighbour_list[i][j]["coordinates"]
            is_powerStone_present = neighbour_list[i][j]["is_powerStone_present"]
            queue.append((neighbour_coordinates, is_powerStone_present))
    if state["movegen"]["Gamora"]["current_cell"]["coordinates"] not in visited:
        visited.append(state["movegen"]["Gamora"]["current_cell"]["coordinates"])

    queue = sorted(queue, key=lambda x: x[1], reverse=True)
    print("Queue:", queue)

    cell = None
    while queue:
        cell = queue.pop(0)
        if cell[0] not in visited:
            break
    print("Visited: ", visited)
    print("next possible Cell: ", cell)
    print("Stack: ", stack)
    print("current cell: ", state["movegen"]["Gamora"]["current_cell"]["coordinates"])
    if cell:
        print(cell[0] in visited)
    if not cell or cell[0] in visited:  # if all cells queue are in visited, then return parent cell
        if len(stack):
            cell = stack.pop()
            print("Next Cell1: ", cell)

            return cell
        else:
            print("None")
            return None


    else:  # if not, then add cell to visited and stack and return cell
        if state["movegen"]["Gamora"]["current_cell"]["coordinates"] not in stack:
            stack.append(
                state["movegen"]["Gamora"]["current_cell"]["coordinates"])
        print("Next Cell2: ", cell[0])
        return cell[0]


@sio.event
def action(state):
    fi = open('state.json', 'w')
    fi.write(json.dumps(state))
    fi.close()
    # cells = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # cell = random.choice(cells)
    # guardians = ["Gamora", "Drax", "Rocket", "Groot", "StarLord"]
    # guardian = random.choice(guardians)
    # coordinates = state['movegen'][guardian]['current_cell']['coordinates']
    # coordinates = coordinates.strip('(').strip(')').split(', ')
    #
    # new_cell = (int(coordinates[0]) + int(cell[0]), int(coordinates[1]) + cell[1])
    #
    # action_type = ['MOVE', 'ATTACK']
    # action_selected = random.choice(action_type)
    #
    # print(action_selected, guardian, new_cell)

    cell = bfs(state)
    if not cell:
        print("No more moves")
        return None
    # print("State: ",state)

    action = {
        "action_type": 'MOVE',
        "troop": 'Gamora',
        'target': cell,
        'player_id': PLAYER_ID,
        'round_no': state['round_no']
    }
    print("Sending action:", action)
    sio.emit('action', action)


@sio.event
def connected(data):
    print("Response:", data)


sio.connect('http://127.0.0.1:5000',
            {"auth": json.dumps({'player_id': PLAYER_ID, 'password': PLAYER_PASSWORD, 'room': PLAYER_ROOM})})

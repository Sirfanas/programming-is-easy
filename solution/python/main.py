# coding: utf-8

# forward declaration
class Node:
    pass
class Link:
    pass


"""
    Structures
"""
class Node:
    name: str
    flag: bool
    links: list[Link]

class Link:
    source: Node
    destination: Node

class Graph:
    start: Node
    stop: Node

class Player:
    name: str
    current_room: Node


"""
    Node
"""
def node_create(name: str) -> Node:
    n: Node = Node()
    n.name = name
    n.flag = False
    n.links = list()
    return n

def node_add_portal(node_src: Node, node_dst: Node):
    node_src.links.append(link_create(node_src, node_dst))

def node_to_str(node: Node):
    res: str = f"{{name: {node.name}, links: {[n.destination.name for n in node.links]}}}"
    return res

def node_display(node: Node, delta: int=0):
    if node.flag:
        return
    tabs: str = delta * "\t"
    node.flag = True
    print(tabs + node_to_str(node))
    for link in node.links:
        if not link.destination.flag:
            node_display(link.destination, delta + 1)
    node.flag = False

def node_read_portal_indice(node: Node) -> int:
    n_link: int = len(node.links)
    indice = n_link + 1
    while indice < 1 or indice > n_link:
        print(f"Choose a portal indice (between 1 - {n_link})")
        buf = input()
        try:
            indice = int(buf)
        except:
            print("You should try typing an integer value")
    return indice - 1

"""
    Link
"""
def link_create(src: Node, dst: Node) -> Link:
    l: Link = Link()
    l.source = src
    l.destination = dst
    return l


"""
    Graph
"""
def graph_create(start: Node, stop: Node) -> Graph:
    g: Graph = Graph()
    g.start = start
    g.stop = stop
    return g

def graph_display(graph: Graph):
    node_display(graph.start)

def graph_create_dungeon() -> Graph:
    start = node_create("Départ")
    room_a = node_create("Salle A")
    room_b = node_create("Salle B")
    room_c = node_create("Salle C")
    room_d = node_create("Salle D")
    stop = node_create("Fin")

    dungeon = graph_create(start, stop)

    node_add_portal(start, room_a)
    node_add_portal(room_a, room_b)
    node_add_portal(start, room_b)

    node_add_portal(room_b, room_c)
    node_add_portal(room_b, room_d)

    node_add_portal(room_c, room_a)

    node_add_portal(room_c, stop)
    node_add_portal(room_d, stop)

    graph_display(dungeon)
    return dungeon

"""
    Player
"""
def player_create(name: str) -> Player:
    p: Player = Player()
    p.name = name
    p.current_room = None
    return p

def player_set_current_room(player: Player, room: Node):
    player.current_room = room

def player_to_str(player: Player) -> str:
    res = f"Player '{player.name}', currently at '{player.current_room.name}'."
    return res

def player_travel_portal(player: Player, portal_indice: int):
    player_set_current_room(player, player.current_room.links[portal_indice].destination)

def player_display(player: Player):
    print(player_to_str(player))

def player_display_current_room(player: Player):
    print(f"Currently in room '{player.current_room.name}'")
    i: int = 1
    for link in player.current_room.links:
        print(f"\t{i}: {link.destination.name}")
        i += 1


if __name__ == "__main__":
    print("Type your name:")
    pname = input()

    player: Player = player_create(pname)

    dungeon = graph_create_dungeon()
    player_set_current_room(player, dungeon.start)

    player_display(player)

    while player.current_room != dungeon.stop:
        player_display_current_room(player)
        print("Choose a portal:")
        portal_indice = node_read_portal_indice(player.current_room)
        player_travel_portal(player, portal_indice)

    print("You're out ! GG ^^")

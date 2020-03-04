from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import randint, shuffle
Room.objects.all().delete()
adj = ["Adorable", "Happy", "Charming", "Cute", "Lovely", "Pleasant", "Pretty", "Tropical", "Peaceful", "Safe", "Nostalgic", "Dainty", "Endearing", "Precious", "Amiable", "Welcoming", "Cordial", "Neighborly", "Local", "Familiar", "Placid", "Harmonious", "Gentle"]
nouns = [
    ["Fountain", "You feel the healing effects of the fountain and steel yourself for battle."], 
    ["Ancient", "The ancient lives here. It must be protected at all costs."], 
    ["Tower", "A tower sits here. It now defends the long abandoned lands only from ghosts."], 
    ["Forest Lane", "Trees cover the sun as you walk, guided by a path."], 
    ["River", "You come upon a river crossing. The waters are shallow enough to wade across."], 
    ["Secret Shop", "A wily storekeeper is hiding here in the wilderness. He invites you to peruse his wares."], 
    ["Pit", "You wander into a pit. Tall black rocks extend up around you. You wonder if beast are nearby."], 
    ["Jungle", "Beasts stay here, but seem aware of danger and stay in their dens. Maybe it's you they're scared of!"], 
    ["Dire Citadel", "A towering, rocky citadel extends from the top of a cliff. Stairs are carved into the mountainside leading up to it."], 
    ["Abandoned Town", "A broken clocktower stands over an abandoned town. No citizens remain."],
    ["Camp", "You find a camp. A tent is standing here, and the coals of the campfire are still hot."],
    ["City", "You come upon a city. As you approach the guards yell 'Stop! You may not enter!`"],
    ["Temple", "You find an abandoned temple. An altar to some forgotten god sits in the center, lit under a skylight."],
    ["Road", "You're on a dirt road. Your mind wanders to hikes as a child."],
    ["Manor", "You are outside of a great manor. You hear giggling and commotion inside, but the doors are locked."],
    ["Stream", "You stand above an enchanted stream. Faeries flit about above the babbling waters."],
    ["Apple Store", "A badly-bearded beta male approaches you and begins to sell you an iPhone. When he sees the outdated Apple hardware in your hand, he retreats in fear."],
    ["Chapel", "A chapel is here. You stop and pray to the one true god."],
    ["DNC", "You are outside the Democratic National Convention. You hear rioting as Bernie is once again robbed of the nomination."],
    ["Timeless Whirlpool", "You see a whirlpool. As you stand and watch it, it neither slows nor speeds up."],
    ["Treasure Room", "Treasures surround you. When you attempt to lift them, you find them too heavy to lift."],
    ["Clearing", "The trees and rocks clear aside and you find yourself in a plesant meadow. Birds fly silently overhead."],
    ["Cave", "You enter a small cave. The walls are cramped and the ceiling forces you to stoop over. You hope you don't have to defend yourself here."]
    ]
shuffle(adj)
shuffle(nouns)
rooms = []
descriptions = []
# **************************************************************************
all_rooms = Room.objects.all()
counter = 0
for r in all_rooms:
    r.title = rooms[counter]
    r.description = descriptions[counter]
    r.save()
    counter += 1

# **************************************************************************
for i in range(len(adj)):
    for j in range(len(adj)):
        rooms.append(adj[i] + " " + nouns[j][0])
# **************************************************************************

for i in range(len(adj)):
    for j in range(len(adj)): 
        descriptions.append(f"{nouns[j][1]} You feel {adj[i].lower()} here.")
# **************************************************************************
class World:
    def __init__(self):
        self.grid = None
        self.width = 23
        self.height = 23
    def is_in_grid(self, direction, x, y):
        if direction == 'w':
            return self.grid[y][x - 1]
        elif direction == 'n':
            return self.grid[y + 1][x]
        elif direction == 'e':
            return self.grid[y][x + 1]
        elif direction == 's':
            return self.grid[y - 1][x]
    def is_out_of_bounds(self, direction, x, y):
        if direction == 'w':
            return (x - 1) < 0
        elif direction == 'n':
            return (y + 1) >= self.height
        elif direction == 'e':
            return (x + 1) >= self.width
        elif direction == 's':
            return (y - 1) < 0
    def generate_rooms(self):
        # Initialize the grid
        self.grid = [None] * self.height
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * self.width
        # start from middle of the bottom row
        seed_x = self.width // 2
        seed_y = self.height // 2
        x = seed_x
        y = seed_y
        room_count = 0
        # seed the first room
        seed_room = Room(title=rooms[0], description=descriptions[0], x=x, y=y)
        seed_room.save()
        self.grid[y][x] = seed_room
        room_count += 1
        # start players in seed room
        players = Player.objects.all()
        for p in players:
            p.currentRoom=seed_room.id
            p.save()
        # While there are rooms to be created...
        while room_count < 100:
            print(room_count)
            # never travel south
            directions = ['w', 'n', 'e', 's']
            prev_direction = None
            # start at the seed room
            previous_room = seed_room.id
            # reset x and y coordinates
            x = seed_x
            y = seed_y
            # find a random direction
            direction = directions[randint(0, 3)]
            can_move = True
            # traverse rooms...
            while can_move == True:
                # if no room in grid
                print(room_count)
                if not self.is_out_of_bounds(direction, x, y) and self.is_in_grid(direction, x, y) is None:
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1
                    elif direction == 's':
                        y -= 1
                    # Create a room in the given direction
                    room = Room(title=rooms[room_count], description=descriptions[room_count], x=x, y=y)
                    # save room 
                    room.save()
                    # Save the room in the World grid
                    self.grid[y][x] = room
                    # Connect the new room to the previous room
                    # previous_room.connectRooms(room, direction)
                    Room.objects.get(id=previous_room).connectRooms(room, direction)
                    # Update iteration variables
                    room_count += 1
                    can_move = False
                # if room in grid and prev room is connected to target room,
                # elif previous_room.getRoomInDirection(direction) != 0:
                elif getattr(Room.objects.get(id=previous_room), f"{direction}_to") != 0:
                    # move to that room
                    # previous_room = getattr(previous_room, f"{direction}_to")
                    previous_room = getattr(Room.objects.get(id=previous_room), f"{direction}_to")
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1
                    elif direction == 's':
                        y -= 1
                    # find a new random direction
                    prev_direction = direction
                    if prev_direction == 'e':
                        directions = ['n', 'e', 's']
                    elif prev_direction == 'w':
                        directions = ['s', 'n', 'w']
                    elif prev_direction == 'n':
                        directions = ['e', 'w', 'n']
                    elif prev_direction == 's':
                        directions = ['w', 's', 'e']
                    direction = directions[randint(0, 2)]
                # if room is outside bounds OR if room in grid and prev room not connected to target room
                elif self.is_out_of_bounds(direction, x, y) or getattr(Room.objects.get(id=previous_room), f"{direction}_to") == 0:
                    # if no directions available
                    if directions == None:
                        can_move = False
                    # try again in available directions
                    elif len(directions) == 4:
                        if prev_direction == 'e':
                            directions = ['n', 'e', 's']
                            direction = 'n'
                        elif prev_direction == 'w':
                            directions = ['s', 'n', 'w']
                            direction = 's'
                        elif prev_direction == 'n':
                            directions = ['e', 'w', 'n']
                            direction = 'e'
                        elif prev_direction == 's':
                            directions = ['w', 's', 'e']
                            direction = 'w'
                    elif len(directions) == 3:
                        if prev_direction == 'e':
                            directions = ['e', 's']
                            direction = 'e'
                        elif prev_direction == 'w':
                            directions = ['n', 'w']
                            direction = 'n'
                        elif prev_direction == 'n':
                            directions = ['w', 'n']
                            direction = 'w'
                        elif prev_direction == 's':
                            directions = ['s', 'e']
                            direction = 's'
                    elif len(directions) == 2:
                        if prev_direction == 'e':
                            direction = 's'
                        elif prev_direction == 'w':
                            direction = 'w'
                        elif prev_direction == 'n':
                            direction = 'n'
                        elif prev_direction == 's':
                            direction = 'e'
                        directions = None
# **************************************************************************
World().generate_rooms()
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('957774'), key=config('e21ba1b1e7a9aec5b48a'), secret=config('f87a598fe73967a57c2b'), cluster=config('us3'))
# initiate and subscribe to pusher channel?

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    world = Room.objects.all()
    worldRooms = []
    for r in world:
        worldRooms.append({'id': r.id, 'x': r.x, 'y': r.y, 'title': r.title, "n_to": r.n_to, "s_to": r.s_to, "e_to": r.e_to, "w_to": r.w_to})
        
        
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'world': worldRooms, 'name':player.user.username, "id" : room.id, "x": room.x, "y": room.y, "n_to": room.n_to, "s_to": room.s_to, "e_to": room.e_to, "w_to": room.w_to, 'title':room.title, 'description':room.description, 'players':players}, safe=True)

@csrf_exempt
@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    rooms_res = []
    res = {}
    res_dict = {}
    for r in rooms:
        res[r.key] = {'dbid': r.id, 'key': r.key, 'title':r.title, 'description':r.description, 'n_to':r.n_to, 's_to': r.s_to,'e_to':r.e_to,"w_to": r.w_to,"x": r.x, "y": r.y,}
    res_dict['rooms'] = res
    return JsonResponse(res_dict)

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
<<<<<<< HEAD
=======

>>>>>>> 70ed8fbd1efaceecc051b256ff9ae95c51417537
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
<<<<<<< HEAD
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
=======
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, "id" : nextRoom.id, "x": nextRoom.x, "y": nextRoom.y, 'n_to':nextRoom.n_to, 's_to': nextRoom.s_to,'e_to':nextRoom.e_to,"w_to": nextRoom.w_to, 'players':players, 'error_msg':""}, safe=True)

>>>>>>> 70ed8fbd1efaceecc051b256ff9ae95c51417537
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, "id" : room.id, "x": room.x, "y": room.y, 'n_to':room.n_to, 's_to': room.s_to, 'e_to':room.e_to, "w_to": room.w_to, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)

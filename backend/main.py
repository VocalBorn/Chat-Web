room_users = {}  # 紀錄每個房間有哪些使用者 { room: [username1, username2, ...] }
user_sid_map = {}  # 紀錄 sid 對應的 username { sid: username }

@sio.event
async def join(sid, data):
    username = data["username"]
    room = data["room"]
    
    await sio.enter_room(sid, room)
    user_sid_map[sid] = username
    
    if room not in room_users:
        room_users[room] = []
    room_users[room].append(username)
    
    await sio.emit("room_users", room_users[room], room=room)

@sio.event
async def disconnect(sid):
    username = user_sid_map.get(sid)
    if username:
        for room in sio.rooms(sid):
            if room in room_users and username in room_users[room]:
                room_users[room].remove(username)
                await sio.emit("room_users", room_users[room], room=room)
    
    user_sid_map.pop(sid, None)

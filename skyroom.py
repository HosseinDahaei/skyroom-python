import json

import requests



class APIException(Exception):
    pass


class HTTPException(Exception):
    pass


class SkyroomAPI(object):
    def __init__(self, apikey, **request_kwargs):
        self.host = 'www.skyroom.online'
        self.apikey = apikey
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }
        self.request_kwargs = request_kwargs

    def __repr__(self):
        return "skyroom.SkyroomAPI({!r})".format(self.apikey)

    def __str__(self):
        return "skyroom.SkyroomAPI({!s})".format(self.apikey)

    def _request(self, action, params=None):
        url = 'https://' + self.host + '/skyroom/api/' + self.apikey
        data = {
            'action': action
        }
        if params:
            data['params'] = params
        try:
            content_data = requests.post(url, headers=self.headers, auth=None, json=data, **self.request_kwargs).content
            try:
                response = json.loads(content_data.decode("utf-8"))
                if (response['ok'] == True):
                    response = response['result']
                else:
                    raise APIException(
                        (f'APIException[error_code: {response["error_code"]}]: {response["error_message"]}')
                    )
            except ValueError as e:
                raise HTTPException(e)
            return response
        except requests.exceptions.RequestException as e:
            raise HTTPException(e)

    # 1.Service Management

    def getServices(self, params=None):
        return self._request('getServices', params)

    # 2.Rooms Management

    def getRooms(self):
        """Get list of rooms."""
        return self._request('getRooms')

    def countRooms(self):
        """Get room count."""
        return self._request('countRooms')

    def getRoom(self, room_id=None, name=None, params=None):
        """Get room by ID or name."""
        if params is None:
            params = {}
            if room_id is not None:
                params['room_id'] = room_id
            if name is not None:
                params['name'] = name
        return self._request('getRoom', params)

    def getRoomUrl(self, room_id=None, language=None, params=None):
        """Get room URL by room_id and optional language."""
        if params is None:
            params = {}
            if room_id is not None:
                params['room_id'] = room_id
            if language is not None:
                params['language'] = language
        return self._request('getRoomUrl', params)

    def createRoom(self, name, title, guest_login=False, op_login_first=True, max_users=0, guest_limit=0,
                   status=1, service_id=None, description=None, session_duration=None, time_limit=None, params=None):
        """Create a new room."""
        if params is None:
            params = {
                'name': name,
                'title': title,
                'guest_login': guest_login,
                'op_login_first': op_login_first,
                'max_users': max_users,
                'guest_limit': guest_limit,
                'status': status,
            }
            if service_id is not None:
                params['service_id'] = service_id
            if description is not None:
                params['description'] = description
            if session_duration is not None:
                params['session_duration'] = session_duration
            if time_limit is not None:
                params['time_limit'] = time_limit
        return self._request('createRoom', params)

    def updateRoom(self, room_id, title=None, description=None, status=None, guest_login=None,
                   guest_limit=None, op_login_first=None, max_users=None, session_duration=None,
                   time_limit=None, service_id=None, params=None):
        """Update room attributes."""
        if params is None:
            params = {'room_id': room_id}
            for key, value in {
                'title': title,
                'description': description,
                'status': status,
                'guest_login': guest_login,
                'guest_limit': guest_limit,
                'op_login_first': op_login_first,
                'max_users': max_users,
                'session_duration': session_duration,
                'time_limit': time_limit,
                'service_id': service_id,
            }.items():
                if value is not None:
                    params[key] = value
        return self._request('updateRoom', params)

    def deleteRoom(self, room_id=None, params=None):
        """Delete room by ID."""
        if params is None:
            params = {'room_id': room_id}
        return self._request('deleteRoom', params)

    def getRoomUsers(self, room_id=None, params=None):
        """List users in room."""
        if params is None:
            params = {'room_id': room_id}
        return self._request('getRoomUsers', params)

    def addRoomUsers(self, room_id=None, users=None, params=None):
        """Add users to room.

        users: list of dicts [{'user_id': ..., 'access': ...}] or user IDs as numbers
        """
        if params is None:
            params = {'room_id': room_id, 'users': users}
        return self._request('addRoomUsers', params)

    def removeRoomUsers(self, room_id=None, users=None, params=None):
        """Remove user access from room."""
        if params is None:
            params = {'room_id': room_id, 'users': users}
        return self._request('removeRoomUsers', params)

    def updateRoomUser(self, room_id, user_id=None, access=None, params=None):
        """Change a user's room access."""
        if params is None:
            params = {'room_id': room_id}
            if user_id is not None:
                params['user_id'] = user_id
            if access is not None:
                params['access'] = access
        return self._request('updateRoomUser', params)

    # 3. Users Management

    def getUsers(self):
        """List all users."""
        return self._request('getUsers')

    def countUsers(self):
        """Count users."""
        return self._request('countUsers')

    def getUser(self, user_id=None, username=None, params=None):
        """Get user by ID or username."""
        if params is None:
            params = {}
            if user_id is not None:
                params['user_id'] = user_id
            if username is not None:
                params['username'] = username
        return self._request('getUser', params)

    def createUser(self, username, password, nickname, status=1, is_public=False,
                   email=None, fname=None, lname=None, gender=None, concurrent=None,
                   time_limit=None, expiry_date=None, params=None):
        """Create a user."""
        if params is None:
            params = {
                'username': username,
                'password': password,
                'nickname': nickname,
                'status': status,
                'is_public': is_public,
            }
            if email is not None:
                params['email'] = email
            if fname is not None:
                params['fname'] = fname
            if lname is not None:
                params['lname'] = lname
            if gender is not None:
                params['gender'] = gender
            if concurrent is not None:
                params['concurrent'] = concurrent
            if time_limit is not None:
                params['time_limit'] = time_limit
            if expiry_date is not None:
                params['expiry_date'] = expiry_date
        return self._request('createUser', params)

    def updateUser(self, user_id, password=None, nickname=None, email=None, fname=None,
                   lname=None, gender=None, status=None, is_public=None, concurrent=None,
                   time_limit=None, expiry_date=None, params=None):
        """Update user details."""
        if params is None:
            params = {'user_id': user_id}
            for key, value in {
                'password': password,
                'nickname': nickname,
                'email': email,
                'fname': fname,
                'lname': lname,
                'gender': gender,
                'status': status,
                'is_public': is_public,
                'concurrent': concurrent,
                'time_limit': time_limit,
                'expiry_date': expiry_date,
            }.items():
                if value is not None:
                    params[key] = value
        return self._request('updateUser', params)

    def deleteUser(self, user_id=None, params=None):
        """Delete a single user by ID."""
        if params is None:
            params = {'user_id': user_id}
        return self._request('deleteUser', params)

    def getUserRooms(self, user_id=None, params=None):
        """Get rooms assigned to a user."""
        if params is None:
            params = {'user_id': user_id}
        return self._request('getUserRooms', params)

    def addUserRooms(self, user_id=None, rooms=None, params=None):
        """Add room access for user."""
        if params is None:
            params = {'user_id': user_id, 'rooms': rooms}
        return self._request('addUserRooms', params)

    def removeUserRooms(self, user_id=None, rooms=None, params=None):
        """Remove room access from user."""
        if params is None:
            params = {'user_id': user_id, 'rooms': rooms}
        return self._request('removeUserRooms', params)

    def deleteUsers(self, users=None, params=None):
        """Delete multiple users by IDs."""
        if params is None:
            params = {'users': users}
        return self._request('deleteUsers', params)

    def createLoginUrl(self, room_id, user_id, nickname, access=1, concurrent=1,
                       language='fa', ttl=3600, params=None):
        """Create direct login URL (room login token)."""
        if params is None:
            params = {
                'room_id': room_id,
                'user_id': user_id,
                'nickname': nickname,
                'access': access,
                'concurrent': concurrent,
                'language': language,
                'ttl': ttl,
            }
        return self._request('createLoginUrl', params)

    def getLoginUrl(self, *args, **kwargs):
        """Alias of createLoginUrl for backward compatibility."""
        return self.createLoginUrl(*args, **kwargs)

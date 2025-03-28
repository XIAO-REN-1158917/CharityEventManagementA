from voteapp.model.enums import Role, Status


class User:
    def __init__(
        self,
        id,
        username,
        password_hash,
        email,
        first_name,
        last_name,
        location,
        description,
        avatar,
        role,
        status,
    ):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.description = description
        self.avatar = avatar

        if isinstance(role, Role):
            self.role = role
        else:
            try:
                self.role = Role[role.upper()]
            except KeyError:
                raise ValueError(f"Invalid role: {role}")

        if isinstance(status, Status):
            self.status = status
        else:
            try:
                self.status = Status[status.upper()]
            except KeyError:
                raise ValueError(f"Invalid status: {status}")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "location": self.location,
            "description": self.description,
            "avatar": self.avatar,
            "role": self.role.value,
            "status": self.status.value,
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data["id"],
            username=data["username"],
            password_hash=data["password_hash"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            location=data["location"],
            description=data["description"],
            avatar=data["avatar"],
            role=data["role"],
            status=data["status"],
        )

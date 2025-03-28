from voteapp.dao.base_dao import BaseDAO
from voteapp.model import User
from voteapp.model import enums
from voteapp.utils.hash_utils import get_password_hash
from voteapp.model.enums import Role, Status


class UserDao(BaseDAO):
    def __init__(self) -> None:
        super().__init__()

    def authenticate_user(self, user_name, password):
        query = (
            r"select id, username, password_hash, email, first_name, last_name, location, description, avatar, role, status"
            " from users where username = %s and password_hash = %s"
        )

        result = self.execute_query(query, (user_name, get_password_hash(password)))
        if len(result) > 0:
            user = User(
                result[0][0],
                result[0][1],
                result[0][2],
                result[0][3],
                result[0][4],
                result[0][5],
                result[0][6],
                result[0][7],
                result[0][8],
                result[0][9],
                result[0][10],
            )
            if user.status == enums.Status.ACTIVE:
                return user, ""
            else:
                return None, "Your account has been deactivated. Please contact an admin."
        else:
            return None, "Invalid username or password, please try again!"

    def register(self, user: User):
        query = "select * from users where username = %s"
        result = self.execute_query(query, (user.username,))
        if len(result) > 0:
            return False, "User name '" + user.username + "' already exists."

        query = (
            "insert into users (username, password_hash, email, first_name, last_name, description, location, avatar, role, status)"
            " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        self.execute_non_query(
            query,
            (
                user.username,
                user.password_hash,
                user.email,
                user.first_name,
                user.last_name,
                user.description,
                user.location,
                user.avatar,
                user.role.value,
                user.status.value,
            ),
        )
        return (
            True,
            "User '" + user.username + "' registered successfully, please log in.",
        )

    # update by nan
    def search_voters(self, search_criteria):
        query = """
            SELECT id, username, email, first_name, last_name, location, description, avatar, role, status 
            FROM users 
            WHERE (username LIKE %s OR email LIKE %s OR first_name LIKE %s OR last_name LIKE %s)
            AND role = %s
        """
        like_criteria = f"%{search_criteria}%"
        result = self.execute_query(
            query,
            (
                like_criteria,
                like_criteria,
                like_criteria,
                like_criteria,
                Role.VOTER.value,
            ),
        )

        return [
            User(
                id=row[0],
                username=row[1],
                password_hash=None,
                email=row[2],
                first_name=row[3],
                last_name=row[4],
                location=row[5],
                description=row[6],
                avatar=row[7],
                role=row[8],
                status=row[9],
            )
            for row in result
        ]

    def get_voter_by_id(self, voter_id):
        query = """
            SELECT id, username, password_hash, email, first_name, last_name, location, description, avatar, role, status
            FROM users
            WHERE id = %s
        """
        result = self.execute_query(query, (voter_id,))

        if result:
            return User(
                id=result[0][0],
                username=result[0][1],
                password_hash=result[0][2],
                email=result[0][3],
                first_name=result[0][4],
                last_name=result[0][5],
                location=result[0][6],
                description=result[0][7],
                avatar=result[0][8],
                role=result[0][9],
                status=result[0][10],
            )
        return None

    def set_voter_status(self, voter_id, status):
        query = "UPDATE users SET status = %s WHERE id = %s"
        self.execute_non_query(query, (status, voter_id))

    def find_by_email(self, email):
        query = "select id, username, password_hash, email, first_name, last_name, location, description, avatar, role, status from users where email = %s"
        result = self.execute_query(query, (email,))
        if result:
            user_data = result[0]
            return User(
                id=user_data[0],
                username=user_data[1],
                password_hash=user_data[2],
                email=user_data[3],
                first_name=user_data[4],
                last_name=user_data[5],
                location=user_data[6],
                description=user_data[7],
                avatar=user_data[8],
                role=enums.Role(user_data[9]), 
                status=enums.Status(user_data[10])
            )
        return None
    
    def find_by_id(self, user_id):
        query = "select id, username, password_hash, email, first_name, last_name, location, description, avatar, role, status from users where id = %s"
        result = self.execute_query(query, (user_id,))
        if result:
            user_data = result[0]
            return User(
                id=user_data[0],
                username=user_data[1],
                password_hash=user_data[2],
                email=user_data[3],
                first_name=user_data[4],
                last_name=user_data[5],
                location=user_data[6],
                description=user_data[7],
                avatar=user_data[8],
                role=enums.Role(user_data[9]),  # Ensure enums.Role and enums.Status are correct
                status=enums.Status(user_data[10])
            )
        return None
    
    def update_user(self, user: User):
        query = (
            "update users set username = %s, password_hash = %s, email = %s, first_name = %s, last_name = %s, "
            "location = %s, description = %s, avatar = %s, role = %s, status = %s where id = %s"
        )
        self.execute_non_query(
            query,
            (
                user.username,
                user.password_hash,
                user.email,
                user.first_name,
                user.last_name,
                user.location,
                user.description,
                user.avatar,
                user.role.value,
                user.status.value,
                user.id,
            ),
        )
                                                                            
    def search_backend_user(self, username, first_name, last_name, exclude_user=None) -> list[User]:
        query = """
            SELECT id, username, email, first_name, last_name, role, status 
            FROM users 
            WHERE (role = 'admin' or role = 'scrutineer')
            """
        conditions = []
        parameters = []
        if username != "":
            conditions.append("username like %s")
            parameters.append(f"{username}%")

        if first_name != "":
            conditions.append("first_name like %s")
            parameters.append(f"%{first_name}%")

        if last_name != "":
            conditions.append("last_name like %s")
            parameters.append(f"%{last_name}%")

        if exclude_user:
            conditions.append("id != %s")
            parameters.append(exclude_user)

        sql = self.build_query(query, conditions)

        result = self.execute_query(sql, parameters)

        user_list = []
        for row in result:
            user = User(
                row[0],
                row[1],
                None,
                row[2],
                row[3],
                row[4],
                None,
                None,
                None,
                row[5],
                row[6],
            )
            user_list.append(user)

        return user_list
    
    def update_role(self, user_id, role: enums.Role):
        query = "UPDATE users SET role = %s WHERE id = %s"
        self.execute_non_query(query, (role.value, user_id))

    def update_status(self, user_id, status: enums.Status):
        query = "UPDATE users SET status = %s WHERE id = %s"
        self.execute_non_query(query, (status.value, user_id))
        
    def backend_user_add(self):
        # Generate unique username, email, and other default values
        last_user = self.execute_query("SELECT MAX(id) FROM users", ())[0][0] or 0
        username = f"backend_user_{last_user + 1}"
        email = f"{username}@example.com"
        password_hash = get_password_hash("backenduser1pass")
        first_name = "firstname"
        last_name = "lastname"
        location = "location"
        description = "n/a"
        avatar = "default.png"
        role = Role.SCRUTINEER.value
        status = Status.INACTIVE.value

        query = (
            "INSERT INTO users (username, password_hash, email, first_name, last_name, description, location, avatar, role, status)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        try:
            self.execute_non_query(
                query,
                (username, password_hash, email, first_name, last_name, description, location, avatar, role, status)
            )
            return True, f"Backend user '{username}' created successfully."
        except Exception as e:
            return False, f"Failed to create backend user: {str(e)}"
        
    def update_backend_user(self, user_id, username=None, email=None, first_name=None, last_name=None, location=None, description=None):
        query = "UPDATE users SET "
        params = []

        if username is not None:
            query += "username = %s, "
            params.append(username)
        if email is not None:
            query += "email = %s, "
            params.append(email)
        if first_name is not None:
            query += "first_name = %s, "
            params.append(first_name)
        if last_name is not None:
            query += "last_name = %s, "
            params.append(last_name)
        if location is not None:
            query += "location = %s, "
            params.append(location)
        if description is not None:
            query += "description = %s, "
            params.append(description)

        query = query.rstrip(', ')
        query += " WHERE id = %s"
        params.append(user_id)

        self.execute_non_query(query, params)

    def find_by_username(self, username):
        query = """
            SELECT id, username, password_hash, email, first_name, last_name, location, description, avatar, role, status 
            FROM users 
            WHERE username = %s
        """
        result = self.execute_query(query, (username,))
        if result:
            user_data = result[0]
            return User(
                id=user_data[0],
                username=user_data[1],
                password_hash=user_data[2],
                email=user_data[3],
                first_name=user_data[4],
                last_name=user_data[5],
                location=user_data[6],
                description=user_data[7],
                avatar=user_data[8],
                role=enums.Role(user_data[9]),  
                status=enums.Status(user_data[10])
            )
        return None

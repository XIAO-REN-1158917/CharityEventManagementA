from voteapp.dao.base_dao import BaseDAO
from voteapp.model.competitor import Competitor
from typing import List


class CompetitorDAO(BaseDAO):

    def __init__(self) -> None:
        super().__init__()

    def add_competitor(self, name: str, description: str, image: str) -> None:
        query = "INSERT INTO competitors (name, description, image) VALUES (%s, %s, %s)"
        self.execute_non_query(query, (name, description, image))

    def edit_competitor(self, id: int, name: str, description: str, image: str) -> None:
        query = "UPDATE competitors SET name = %s, description = %s, image = %s WHERE id = %s"
        self.execute_non_query(query, (name, description, image, id))

    def delete_competitor(self, id: int) -> None:
        query = "DELETE FROM competitors WHERE id = %s"
        self.execute_non_query(query, (id,))

    def search_competitor(self, keyword: str) -> List[Competitor]:
        query = "SELECT * FROM competitors WHERE name LIKE %s OR description LIKE %s"
        result = self.execute_query(query, (f"%{keyword}%", f"%{keyword}%"))
        competitors = []
        for row in result:
            competitor = Competitor(
                id=row[0], name=row[1], description=row[2], image=row[3]
            )
            competitors.append(competitor)
        return competitors

    def get_competitor_by_id(self, id: int) -> Competitor:
        query = "SELECT * FROM competitors WHERE id = %s"
        result = self.execute_query(query, (id,))
        if result:
            row = result[0]
            return Competitor(id=row[0], name=row[1], description=row[2], image=row[3])
        return None

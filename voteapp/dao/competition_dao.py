from voteapp.dao.base_dao import BaseDAO
from voteapp.model.competition import CompetitionResult
from voteapp.model.competition import Competition
from voteapp.model.competitor import Competitor
from voteapp.model.competitor import CompetitionCompetitor
from typing import Tuple, List
from datetime import datetime


class CompetitionDao(BaseDAO):

    def __init__(self) -> None:
        super().__init__()

    def current_competition(self, status) -> List[Competition]:
        """
        Returns a list of current competitions with the given status,
        each with their associated competitors.
        """
        query = "SELECT * FROM competitions WHERE status = %s"
        current_competition = []
        result = self.execute_query(query, (status,))
        for row in result:
            competition = Competition(
                row[0],
                row[1],
                row[2].strftime("%d-%m-%Y %H:%M:%S"),
                row[3].strftime("%d-%m-%Y %H:%M:%S"),
                row[4],
            )
            competition.competitors = self.current_competitor(competition.id)
            current_competition.append(competition)

        return current_competition

    def current_competitor(self, competition_id) -> List[Competitor]:
        query = """
            SELECT c.id, c.name, c.description, c.image
            FROM competitors c
            INNER JOIN competition_competitors cc ON c.id = cc.competitor_id
            WHERE cc.competition_id = %s
        """
        current_competitor = []
        result = self.execute_query(query, (competition_id,))
        for row in result:
            competitor = Competitor(row[0], row[1], row[2], row[3])
            current_competitor.append(competitor)

        return current_competitor

    def get_competition_competitor_id(self, competition_id, competitor_id):
        query = """
            SELECT id FROM competition_competitors
            WHERE competition_id = %s AND competitor_id = %s
        """
        result = self.execute_query(query, (competition_id, competitor_id))
        if result:
            return result[0][0]
        return None

    def get_competitor_details(self, competitor_id) -> CompetitionCompetitor:
        """
        Returns a tuple of (CompetitionCompetitor, Competitor) for the given competitor ID.
        """
        query = """
            SELECT cc.competition_id, c.id, c.name, c.description, c.image, cc.vote_count, cc.vote_ratio, cc.is_winner
            FROM competitors c
            INNER JOIN competition_competitors cc ON c.id = cc.competitor_id
            WHERE c.id = %s
        """
        result = self.execute_query(query, (competitor_id,))
        if result:
            row = result[0]
            competitor = Competitor(
                id=row[1],
                name=row[2],
                description=row[3],
                image=row[4],
            )
            competition_competitor = CompetitionCompetitor(
                competition_id=row[0],
                competitor_id=row[1],
                vote_count=row[5],
                vote_ratio=row[6],
                is_winner=row[7],
            )
            return competition_competitor, competitor
        return None, None

    # def all_finalized_competition_results(self) -> list:
    #     """
    #     Fetches the results for all finalized competitions, including the total votes
    #     and winner information.
    #     """
    #     query = """SELECT c.id AS competition_id, c.name AS competition_name, comp.name AS competitor_name,
    #                 (SELECT SUM(cc2.vote_count) FROM competition_competitors cc2 WHERE cc2.competition_id = c.id) AS total_votes,
    #                 ROUND((cc.vote_count / (SELECT SUM(cc2.vote_count) FROM competition_competitors cc2
    #                 WHERE cc2.competition_id = c.id)) * 100, 1) AS winner_votes_proportion
    #                 FROM competition_competitors cc JOIN competitions c ON cc.competition_id = c.id
    #                 JOIN competitors comp ON cc.competitor_id = comp.id WHERE c.status = 'published'
    #                 AND cc.is_winner = 1 ORDER BY c.voting_end_date DESC, c.name, cc.vote_count DESC;"""

    #     results = self.execute_query(query)

    #     competition_results = []
    #     for row in results:
    #         competitionresult = CompetitionResult(
    #             row[0], row[1], row[2], row[3], row[4]
    #         )
    #         competition_results.append(competitionresult)

    #     return competition_results

    # Refactor: move vote calculation logic from SQL to Python for better efficiency and readability

    def all_finalized_competition_results(self) -> list:
        """
        Fetches the results for all finalized (published) competitions,
        including the total votes and winner information.
        Calculates vote percentage in Python instead of SQL for better control.
        """
        # Step 1: Get all published competitions
        competition_query = "SELECT id, name FROM competitions WHERE status = 'published'"
        competition_rows = self.execute_query(competition_query)

        competition_results = []

        for comp_id, comp_name in competition_rows:
            # Step 2: Get all competitors for this competition who are marked as winners
            winner_query = """
                SELECT comp.name, cc.vote_count
                FROM competition_competitors cc
                JOIN competitors comp ON cc.competitor_id = comp.id
                WHERE cc.competition_id = %s AND cc.is_winner = 1
            """
            winner_rows = self.execute_query(winner_query, (comp_id,))

            # Step 3: Get total vote count for this competition
            total_votes_query = """
                SELECT SUM(vote_count)
                FROM competition_competitors
                WHERE competition_id = %s
            """
            total_votes_result = self.execute_query(
                total_votes_query, (comp_id,))
            total_votes = total_votes_result[0][0] if total_votes_result and total_votes_result[0][0] else 0

            # Step 4: Build result objects
            for competitor_name, vote_count in winner_rows:
                if total_votes == 0:
                    vote_ratio = 0.0
                else:
                    vote_ratio = round((vote_count / total_votes) * 100, 1)

                result = CompetitionResult(
                    competition_id=comp_id,
                    competition_name=comp_name,
                    competitor_name=competitor_name,
                    total_votes=total_votes,
                    winner_votes_proportion=vote_ratio
                )
                competition_results.append(result)

        return competition_results

    # def competition_details(self, competition_id):
    #     """Fetches the detailed results for a specific competition, including
    #     competitors and their vote counts.
    #     """
    #     query = """SELECT comp.id AS competitor_id, comp.name AS competitor_name, cc.vote_count AS total_votes,
    #         ROUND ((cc.vote_count / (SELECT SUM(vote_count) FROM competition_competitors
    #         WHERE competition_id = %s)) * 100, 1) AS vote_percentage, comp.image AS image
    #         FROM competition_competitors cc
    #         JOIN competitors comp ON cc.competitor_id = comp.id WHERE cc.competition_id = %s
    #         ORDER BY cc.vote_count DESC"""

    #     results = self.execute_query(query, (competition_id, competition_id))

    #     competition_details = []
    #     max_votes = 0
    #     for row in results:
    #         detail = {
    #             "competitor_id": row[0],
    #             "competitor_name": row[1],
    #             "total_votes": row[2],
    #             "vote_percentage": row[3],
    #             "image": row[4],
    #         }
    #         competition_details.append(detail)
    #         if row[2] > max_votes:
    #             max_votes = row[2]

    #     for detail in competition_details:
    #         detail["is_winner"] = detail["total_votes"] == max_votes

    #     return competition_details

    def competition_details(self, competition_id):
        """
        Fetches detailed results for a specific competition, including:
        - Each competitor's vote count
        - Vote percentage (calculated in Python)
        - Whether the competitor is the winner
        """
        # Step 1: Query all competitors and their vote counts in the competition
        query = """
            SELECT comp.id AS competitor_id, comp.name AS competitor_name, 
                cc.vote_count AS total_votes, comp.image AS image
            FROM competition_competitors cc
            JOIN competitors comp ON cc.competitor_id = comp.id 
            WHERE cc.competition_id = %s
            ORDER BY cc.vote_count DESC
        """
        results = self.execute_query(query, (competition_id,))

        competition_details = []
        total_votes = sum(row[2] for row in results) if results else 0
        max_votes = max((row[2] for row in results), default=0)

        for row in results:
            vote_count = row[2]
            vote_percentage = round((vote_count / total_votes)
                                    * 100, 1) if total_votes > 0 else 0.0
            detail = {
                "competitor_id": row[0],
                "competitor_name": row[1],
                "total_votes": vote_count,
                "vote_percentage": vote_percentage,
                "image": row[3],
                "is_winner": vote_count == max_votes
            }
            competition_details.append(detail)

        return competition_details

    def competition_name(self, competition_id):
        """Fetches the competition name by ID."""
        query = "SELECT name FROM competitions WHERE id = %s"
        result = self.execute_query(query, (competition_id,))

        if result:
            return result[0][0]  # Return the name of the competition

    def search_competitions(self, status) -> List[Competition]:
        if status == "all":
            query = "SELECT id, name, voting_start_date, voting_end_date, status FROM competitions where 'all' = %s order by status"
        else:
            query = "SELECT id, name, voting_start_date, voting_end_date, status FROM competitions WHERE status = %s order by status"
        current_competition = []
        result = self.execute_query(query, (status,))
        for row in result:
            competition = Competition(
                row[0],
                row[1],
                row[2].strftime("%d-%m-%Y"),
                row[3].strftime("%d-%m-%Y"),
                row[4],
            )
            current_competition.append(competition)

        return current_competition

    def add_competition(self, name, voting_start_date, voting_end_date):
        query = (
            "insert into competitions(name,voting_start_date, voting_end_date, status)"
            " values(%s,%s,%s,%s)"
        )
        self.execute_non_query(
            query, (name, voting_start_date, voting_end_date, "pending")
        )

    def del_competition(self, id):
        queries_and_params = [
            ("DELETE FROM competition_competitors WHERE competition_id = %s", (id,)),
            ("DELETE FROM competitions WHERE id = %s", (id,)),
        ]
        self.execute_transaction(queries_and_params)

    def get_competition_by_id(self, id) -> Competition:
        query = "SELECT id, name, voting_start_date, voting_end_date, status FROM competitions where id =%s "
        row = self.execute_query(query, (id,))
        competition = Competition(
            row[0][0],
            row[0][1],
            row[0][2],
            row[0][3],
            row[0][4],
        )
        return competition

    def edit_competition(self, id, name, voting_start_date, voting_end_date):
        query = "update competitions set name=%s, voting_start_date=%s, voting_end_date=%s where id = %s"
        self.execute_non_query(
            query, (name, voting_start_date, voting_end_date, id))

    def launch_competition(self, id):
        """
        Launches a competition if no other ongoing competition exists.
        Returns a tuple (success: bool, message: str).
        """
        query = "select * from competitions where status = 'ongoing'"
        result = self.execute_query(query)
        if len(result) > 0:
            return (
                False,
                "An onging competition already exists, so you cannot launch another one.",
            )
        else:
            query = "update competitions set status='ongoing' where id =%s"
            self.execute_non_query(query, (id,))
            competition = self.get_competition_by_id(id)
            return True, "Competition %s has been successfully launched." % (
                competition.name
            )

    # new dao
    def add_competitor_to_competition(
        self,
        competition_id: int,
        competitor_id: int,
        vote_count: int = 0,
        vote_ratio: int = 0,
        is_winner: int = 0,
    ) -> None:
        query = """
        INSERT INTO competition_competitors (competition_id, competitor_id, vote_count, vote_ratio, is_winner)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_non_query(
            query, (competition_id, competitor_id,
                    vote_count, vote_ratio, is_winner)
        )

    def get_competitors_by_competition(
        self, competition_id: int
    ) -> List[dict[str, any]]:
        query = """
        SELECT competitors.id, competitors.name
        FROM competition_competitors
        JOIN competitors ON competition_competitors.competitor_id = competitors.id
        WHERE competition_competitors.competition_id = %s
        """
        results = self.execute_query(query, (competition_id,))
        competitors = [{"id": row[0], "name": row[1]} for row in results]
        return competitors

    def get_competition_id_by_name(self, competition_name: str) -> int:
        query = "SELECT id FROM competitions WHERE name = %s"
        result = self.execute_query(query, (competition_name,))
        if result:
            return result[0][0]
        return None

    def get_competition_staus(self, competition_id: int):
        query = "SELECT status FROM competitions WHERE id = %s"
        result = self.execute_query(query, (competition_id,))
        if result:
            return result[0][0]
        return None

    def delete_competitor_from_competition(
        self, competition_id: int, competitor_id: int
    ) -> None:
        query = """DELETE FROM competition_competitors
                WHERE competition_id = %s AND competitor_id = %s
            """
        self.execute_non_query(query, (competition_id, competitor_id))

    def update_status_for_expired_competitions(self):
        """
        Automatically sets the status of competitions to 'ended' if their voting_end_date has passed.
        """
        current_date = datetime.now().date()
        sql = """
            UPDATE competitions
            SET status = 'ended'
            WHERE status = 'ongoing' AND voting_end_date < %s
        """
        try:
            self.execute_non_query(sql, (current_date,))
        except Exception as e:
            print(f"更新比赛状态时发生错误: {e}")

    def ongoing_or_ended_competition(self):
        query = """SELECT id, name AS competition_name, voting_start_date, voting_end_date, 
                status AS competition_status FROM competitions WHERE status IN ('ongoing', 'ended')
                ORDER BY status, name;"""
        result = self.execute_query(query)
        competitions = [
            {
                "id": row[0],
                "competition_name": row[1],
                "voting_start_date": row[2].strftime("%d/%m/%Y") if row[2] else "",
                "voting_end_date": row[3].strftime("%d/%m/%Y") if row[3] else "",
                "competition_status": row[4],
            }
            for row in result
        ]
        return competitions

    def finalize_competition(self, competition_id: int) -> None:
        query = "UPDATE competitions SET status = 'published' WHERE id = %s AND status = 'ended'"
        self.execute_non_query(query, (competition_id,))

    def latest_competition(self) -> int:
        query = """
        SELECT id, name
        FROM competitions 
        WHERE status = 'published' 
        ORDER BY voting_end_date DESC 
        LIMIT 1
        """
        print("Executing query to find latest published competition")
        result = self.execute_query(query)
        print(f"Query result: {result}")
        if result:
            return result[0][0], result[0][1]
        return None

    def champ_in_competition(self, competition_id: int) -> tuple:
        query = """
        SELECT competitors.name, competitors.image, competition_competitors.vote_count
        FROM competition_competitors 
        JOIN competitors ON competition_competitors.competitor_id = competitors.id
        WHERE competition_competitors.competition_id = %s
        ORDER BY competition_competitors.vote_count DESC 
        LIMIT 1
        """
        result = self.execute_query(query, (competition_id,))
        if result:
            return result[0][0], result[0][1], result[0][2]
        return None, None, None

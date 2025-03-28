from voteapp.dao.base_dao import BaseDAO
from voteapp.model.vote import Vote
from voteapp.model.enums import VoteStatus
from datetime import datetime


class VoteDao(BaseDAO):

    def __init__(self) -> None:
        super().__init__()

    def record_vote(self, competition_competitor_id, voter_id, voting_ip):
        query = """
            SELECT * FROM votes 
            WHERE competition_competitor_id = %s AND voter_id = %s
        """
        result = self.execute_query(query, (competition_competitor_id, voter_id))
        if result:
            return False, "You have already voted in this competition."

        query = """
            INSERT INTO votes (competition_competitor_id, voter_id, voting_time, voting_ip, status)
            VALUES (%s, %s, NOW(), %s, %s)
        """
        self.execute_non_query(
            query,
            (
                competition_competitor_id,
                voter_id,
                voting_ip,
                VoteStatus.VALID.value,
            ),
        )
        return True, "Vote recorded successfully."

    def has_voted(self, competition_id, voter_id):
        query = """
            SELECT v.id FROM votes v
            INNER JOIN competition_competitors cc ON v.competition_competitor_id = cc.id
            WHERE cc.competition_id = %s AND v.voter_id = %s
        """
        result = self.execute_query(query, (competition_id, voter_id))
        return len(result) > 0

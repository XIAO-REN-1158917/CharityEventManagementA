from voteapp.dao.base_dao import BaseDAO
from typing import Tuple, List
from datetime import datetime, timedelta


class ScrutineeringDAO(BaseDAO):

    def summary_votes(self):
        query = (
            f"select a.name,a.voting_start_date,a.voting_end_date, DATE_FORMAT(c.voting_time,'%d-%m-%Y'),count(*)"
            " from competitions a "
            " inner join competition_competitors b on a.id = b.competition_id"
            " inner join votes c on b.id = c.competition_competitor_id"
            " where a.status = 'ongoing'"
            f" group by a.name,a.voting_start_date,a.voting_end_date,DATE_FORMAT(c.voting_time,'%d-%m-%Y')"
            f" order by DATE_FORMAT(c.voting_time,'%d-%m-%Y')"
        )
        return self.execute_query(query)

    def generate_date_range(self, start_date, end_date):
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime("%d-%m-%Y"))
            current_date += timedelta(days=1)
        return dates

    def unusual_votes(self, competition_id, ip):
        sql = """
            select a.status, a.id as competition_id, a.name as competition_name,
            c.id as vote_id, d.username as voter, c.voting_time, c.voting_ip,
            b.competitor_id, e.name as competitor_name,c.status as vote_status
            from competitions a
            inner join competition_competitors b on a.id = b.competition_id
            inner join votes c on b.id = c.competition_competitor_id
            inner join users d on c.voter_id = d.id
            inner join competitors e on b.competitor_id = e.id
            where a.status in ("ongoing", "ended")
            """

        conditions = []
        parameter = []
        if competition_id != "":
            conditions.append("a.id = %s")
            parameter.append(competition_id)
        if ip != "":
            conditions.append("c.voting_ip like %s")
            parameter.append(f"%{ip}%")

        sql = self.build_query(sql, conditions) + " order by a.status,a.id,d.id"
        result = self.execute_query(sql, parameter)
        votes = [
            {
                "status": row[0],
                "competition_id": row[1],
                "competition_name": row[2],
                "vote_id": row[3],
                "voter": row[4],
                "voting_time": row[5].strftime("%d-%m-%Y %H:%M"),
                "voting_ip": row[6],
                "competitor_id": row[7],
                "competitor_name": row[8],
                "vote_status": row[9],
            }
            for row in result
        ]
        return votes

    def invalidate(self, ids):
        parms = ",".join(map(str, ids))
        sql = f"update votes set status = 'invalid' where id in({parms})"
        self.execute_non_query(sql)

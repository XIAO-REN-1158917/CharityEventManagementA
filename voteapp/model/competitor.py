class Competitor:
    def __init__(
        self,
        id,
        name,
        description,
        image,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.image = image

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
        }

    @staticmethod
    def from_dict(data):
        return Competitor(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            image=data["image"],
        )
    

class CompetitionCompetitor:
    def __init__(
        self,
        competition_id,
        competitor_id,
        vote_count,
        vote_ratio,
        is_winner,
    ):
        self.competition_id = competition_id
        self.competitor_id = competitor_id
        self.vote_count = vote_count
        self.vote_ratio = vote_ratio
        self.is_winner = is_winner

    def to_dict(self):
        return {
            "competition_id": self.competition_id,
            "competitor_id": self.competitor_id,
            "vote_count": self.vote_count,
            "vote_ratio": self.vote_ratio,
            "is_winner" : self.is_winner,
        }

    @staticmethod
    def from_dict(data):
        return CompetitionCompetitor(
            competition_id=data["competition_id"],
            competitor_id=data["competitor_id"],
            vote_count=data["vote_count"],
            vote_ratio=data["vote_ratio"],
            is_winner=data["is_winner"]
        )
from models import Recommendation


class RecommendationEngine:

    def __init__(self, searcher, evaluator):
        self.searcher = searcher
        self.evaluator = evaluator

    def recommend(self, profile, limit=5):

        repositories = self.searcher.search_repositories(
            profile,
            limit=20
        )

        evaluations = []

        for repository in repositories:

            evaluation = self.evaluator.evaluate(
                repository,
                profile
            )

            evaluations.append(evaluation)

        evaluations.sort(
            key=lambda item: item.overall_score,
            reverse=True
        )

        recommendations = []

        for evaluation in evaluations[:limit]:

            recommendations.append(
                Recommendation(
                    repository=evaluation.repository,
                    match_percentage=round(
                        evaluation.overall_score,
                        1
                    ),
                    reasons=evaluation.reasons,
                    concerns=[]
                )
            )

        return recommendations
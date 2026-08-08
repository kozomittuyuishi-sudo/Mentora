from models import RepositoryEvaluation


class RepositoryEvaluator:

    def evaluate(self, repository, profile):

        documentation = self._documentation_score(repository)
        activity = self._activity_score(repository)
        setup = self._setup_score(repository)
        contribution = self._contribution_score(repository)
        architecture = self._architecture_score(repository)
        learning_value = self._learning_value(repository, profile)
        goal_alignment = self._goal_alignment(repository, profile)
        technology_match = self._technology_match(repository, profile)

        overall = (
            documentation * 0.15
            + activity * 0.10
            + setup * 0.15
            + contribution * 0.15
            + architecture * 0.10
            + learning_value * 0.15
            + goal_alignment * 0.10
            + technology_match * 0.10
        )

        reasons = self._generate_reasons(
            repository,
            profile,
            documentation,
            activity,
            setup,
            contribution,
            learning_value,
            goal_alignment,
            technology_match
        )

        return RepositoryEvaluation(
            repository=repository,
            documentation=documentation,
            activity=activity,
            setup=setup,
            contribution=contribution,
            architecture=architecture,
            learning_value=learning_value,
            goal_alignment=goal_alignment,
            technology_match=technology_match,
            overall_score=round(overall, 2),
            reasons=reasons
        )

    def _documentation_score(self, repo):

        score = 30

        if repo.has_readme:
            score += 40

        if repo.has_license:
            score += 10

        if repo.has_contributing:
            score += 20

        return min(score, 100)

    def _activity_score(self, repo):

        score = 40

        if repo.stars > 100:
            score += 15

        if repo.stars > 1000:
            score += 15

        if repo.updated_at:
            score += 30

        return min(score, 100)

    def _setup_score(self, repo):

        score = 70

        if repo.size_kb > 50000:
            score -= 30

        elif repo.size_kb > 20000:
            score -= 15

        return max(score, 10)

    def _contribution_score(self, repo):

        score = 30

        if repo.has_contributing:
            score += 40

        if repo.open_issues > 0:
            score += 20

        if repo.open_issues > 10:
            score += 10

        return min(score, 100)

    def _architecture_score(self, repo):

        # Initial heuristic.
        # This will later be replaced by actual repository analysis.

        if repo.size_kb < 10000:
            return 90

        if repo.size_kb < 50000:
            return 70

        return 45

    def _learning_value(self, repo, profile):

        score = 50

        if repo.description:
            score += 20

        if repo.topics:
            score += 20

        if repo.has_readme:
            score += 10

        return min(score, 100)

    def _goal_alignment(self, repo, profile):

        goal = profile.goal.lower()

        if goal == "contribute":
            return self._contribution_score(repo)

        if goal == "learn":
            return self._learning_value(repo, profile)

        if goal == "build":
            return 75 if repo.description else 50

        return 60

    def _technology_match(self, repo, profile):

        if not repo.language:
            return 30

        for language in profile.languages:
            if language.lower() == repo.language.lower():
                return 100

        return 40

    def _generate_reasons(
        self,
        repo,
        profile,
        documentation,
        activity,
        setup,
        contribution,
        learning_value,
        goal_alignment,
        technology_match
    ):

        reasons = []

        if technology_match >= 90:
            reasons.append(
                f"Matches your {repo.language} experience."
            )

        if documentation >= 80:
            reasons.append(
                "Has strong basic documentation signals."
            )

        if contribution >= 70:
            reasons.append(
                "Looks suitable for exploring contributions."
            )

        if setup >= 70:
            reasons.append(
                "Repository size suggests a relatively manageable setup."
            )

        if learning_value >= 70:
            reasons.append(
                "Contains useful learning signals such as documentation and topics."
            )

        return reasons
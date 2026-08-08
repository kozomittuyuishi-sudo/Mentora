from user_profiler import UserProfiler
from github_search import GitHubSearcher
from repository_evaluator import RepositoryEvaluator
from recommendation_engine import RecommendationEngine


def main():

    profiler = UserProfiler()

    profile = profiler.create_profile(
        experience_level="beginner",
        languages=["Python"],
        interests=["machine learning"],
        goal="learn",
        available_hours_per_day=1,
        learning_style="building"
    )

    searcher = GitHubSearcher()

    evaluator = RepositoryEvaluator()

    engine = RecommendationEngine(
        searcher,
        evaluator
    )

    recommendations = engine.recommend(
        profile,
        limit=5
    )

    print("\nMentora Recommendations")
    print("=" * 60)

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        repo = recommendation.repository

        print(
            f"\n{index}. {repo.full_name}"
        )

        print(
            f"Match: {recommendation.match_percentage}%"
        )

        print(
            f"Language: {repo.language}"
        )

        print(
            f"Stars: {repo.stars:,}"
        )

        print(
            f"Description: {repo.description}"
        )

        print("\nWhy Mentora recommends it:")

        for reason in recommendation.reasons:
            print(f"  ✓ {reason}")

        print(f"\n{repo.url}")


if __name__ == "__main__":
    main()
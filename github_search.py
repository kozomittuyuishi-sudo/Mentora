import os

from dotenv import load_dotenv
from github import Github, Auth
from github.GithubException import GithubException

from models import Repository


load_dotenv()


class GitHubSearcher:

    def __init__(self, token=None):

        token = token or os.getenv("GITHUB_TOKEN")

        if not token:
            raise ValueError(
                "GITHUB_TOKEN is missing. "
                "Add it to the .env file."
            )

        auth = Auth.Token(token)

        self.github = Github(auth=auth)

    def search_repositories(self, profile, limit=20):

        query_parts = []

        # Language preference
        for language in profile.languages:
            query_parts.append(
                f"language:{language}"
            )

        # Interest / topic preference
        for interest in profile.interests:
            query_parts.append(
                interest
            )

        # Don't search with an empty query
        if not query_parts:
            query = "stars:>100"
        else:
            query = " ".join(query_parts)

        print(f"\nGitHub search query: {query}")

        try:

            results = self.github.search_repositories(
                query=query,
                sort="stars",
                order="desc"
            )

            repositories = []

            for repo in results[:limit]:

                repositories.append(
                    Repository(
                        name=repo.name,
                        full_name=repo.full_name,
                        url=repo.html_url,
                        description=repo.description or "",
                        language=repo.language or "Unknown",
                        stars=repo.stargazers_count,
                        forks=repo.forks_count,
                        open_issues=repo.open_issues_count,

                        # IMPORTANT:
                        # Don't call get_topics(),
                        # get_readme(), etc. here.
                        topics=[],

                        has_readme=False,
                        has_license=repo.license is not None,
                        has_contributing=False,

                        size_kb=repo.size,
                        updated_at=str(repo.updated_at),
                    )
                )

            return repositories

        except GithubException as error:

            print(
                f"\nGitHub API error: {error}"
            )

            return []
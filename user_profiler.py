from models import UserProfile


class UserProfiler:

    def create_profile(
        self,
        experience_level,
        languages,
        interests,
        goal,
        available_hours_per_day,
        learning_style="building"
    ):
        return UserProfile(
            experience_level=experience_level,
            languages=languages,
            interests=interests,
            goal=goal,
            available_hours_per_day=available_hours_per_day,
            learning_style=learning_style
        )
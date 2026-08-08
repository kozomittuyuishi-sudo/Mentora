from pathlib import Path


class RepositoryAnalyzer:

    def analyze(self, repository_path):

        path = Path(repository_path)

        files = []
        folders = set()
        extensions = {}

        for item in path.rglob("*"):

            if not item.is_file():
                continue

            # Ignore Git internals
            if ".git" in item.parts:
                continue

            files.append(str(item.relative_to(path)))

            folders.add(
                str(item.parent.relative_to(path))
            )

            extension = item.suffix.lower()

            if extension:
                extensions[extension] = (
                    extensions.get(extension, 0) + 1
                )

        return {
            "name": path.name,
            "file_count": len(files),
            "folder_count": len(folders),
            "files": files,
            "extensions": extensions,
        }
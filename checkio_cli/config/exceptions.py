class ConfigVerificationException(Exception):
    def __init__(self, file_path, name, description):
        self.name = name
        self.file_path = file_path
        self.description = description

    def __str__(self):
        return 'Config Error in {file_path}:{name} {description}'.format(
            name=self.name,
            file_path=self.file_path,
            description=self.description
        )

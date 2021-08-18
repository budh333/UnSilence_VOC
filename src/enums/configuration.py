from enums.argument_enum import ArgumentEnum

class Configuration(ArgumentEnum):
    BERT = 'bert'

    @staticmethod
    def get_friendly_name(configuration) -> str:
        if configuration == Configuration.BERT:
            return 'BERT'

        return None
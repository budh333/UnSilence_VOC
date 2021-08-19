from enums.argument_enum import ArgumentEnum

class Configuration(ArgumentEnum):
    BiLSTMCRF = 'bi_lstm_crf'

    @staticmethod
    def get_friendly_name(configuration) -> str:
        if configuration == Configuration.BiLSTMCRF:
            return 'bi_lstm_crf'

        return None
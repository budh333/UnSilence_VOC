from enums.configuration import Configuration
from enums.challenge import Challenge

from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.arguments.pretrained_arguments_service import PretrainedArgumentsService


def get_arguments_service(arguments_service: ArgumentsServiceBase):
    result = 'base'
    challenge = arguments_service.challenge

    if challenge == Challenge.NamedEntityRecognition:
        result = 'ner'

    return result


def get_optimizer(arguments_service: ArgumentsServiceBase):
    if arguments_service.evaluate or arguments_service.run_experiments:
        return 'base'

    result = 'base'
    challenge = arguments_service.challenge
    configuration = arguments_service.configuration
    if challenge == Challenge.NamedEntityRecognition:
        if configuration == Configuration.BiLSTMCRF:
            result = 'adam'

    return result


def get_loss_function(arguments_service: ArgumentsServiceBase):
    loss_function = None
    challenge = arguments_service.challenge
    configuration = arguments_service.configuration

    if challenge == Challenge.NamedEntityRecognition:
        if configuration == Configuration.BiLSTMCRF:
            return 'ner'

    return loss_function

def get_model_type(arguments_service: ArgumentsServiceBase):

    run_experiments = arguments_service.run_experiments
    configuration = arguments_service.configuration

    model = None

    if run_experiments:
        model = 'eval'
    else:
        model = str(configuration.value).replace('-', '_')

    return model

def get_evaluation_service(arguments_service: ArgumentsServiceBase):
    result = 'base'
    if arguments_service.configuration == Configuration.BiLSTMCRF:
        result = 'ner'

    return result


def get_process_service(arguments_service: ArgumentsServiceBase):
    result = None

    challenge = arguments_service.challenge

    if challenge == Challenge.NamedEntityRecognition:
        result = 'ner'

    return result


def get_tokenize_service(arguments_service: ArgumentsServiceBase) -> str:
    pretrained_model_type = None
    if isinstance(arguments_service, PretrainedArgumentsService):
        pretrained_model_type = arguments_service.pretrained_model

    if pretrained_model_type is None:
        configuration = arguments_service.configuration
        return str(configuration.value).replace('-', '_')

    return pretrained_model_type.value


def get_experiment_service(arguments_service: ArgumentsServiceBase):

    run_experiments = arguments_service.run_experiments

    if not run_experiments:
        return 'none'

    return 'named_entity_recognition'

def include_train_service(arguments_service: ArgumentsServiceBase):
    if arguments_service.run_experiments or arguments_service.evaluate:
        return 'exclude'

    return 'include'

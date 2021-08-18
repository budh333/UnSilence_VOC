from enums.argument_enum import ArgumentEnum

class PretrainedModel(ArgumentEnum):
    BERT = 'bert'
    ALBERT = 'albert'
    XLNet = 'xlnet'
    BART = 'bart'
    CamemBERT = 'camembert'
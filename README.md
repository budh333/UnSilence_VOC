# UnSilencing the VOC Testaments

Colonial archives are at the center of increased interest from a variety of perspectives, as they contain traces of historically marginalized people. Unfortunately, like most archives, they remain difficult to access due to significant persisting barriers. We focus here on one of them: the biases to be found in historical findings aids, such as indexes of person names, which remain in use to this day. In colonial archives, indexes can perpetrate silences by omitting to include mentions of historically marginalized persons. In order to overcome such limitation and pluralize the scope of existing finding aids, we propose using automated entity recognition. To this end, we contribute a fit-for-purpose annotation typology and apply it on the colonial archive of the Dutch East India Company (VOC). **We release a corpus of nearly 70,000 annotations as a shared task, for which we provide strong baselines using state-of-the-art neural network models.**

# Description of the VOC Testaments

The VOC wills in the National Archives are a small part of a much larger collection of wills that ever existed. Every VOC employee was obliged to have a will drawn up (this could be done in Amsterdam, on the ships or in the VOC establishments). This was a form of efficient personnel policy so that after the death of an employee it was clear what should be done with the bequest. 

The collection in which we work is largely built up in the VOC establishments, in particular Batavia. A copy of each will was sent to the VOC headquarters in Amsterdam. After the disintegration of the VOC at the end of the 18th century, part of these copy wills have been preserved and probably only much later merged into volumes (in Dutch: banden) that are now in the custody of the National Archives. In the 19th century, archivists produced an index to these testaments indexing the name of the male testator. A few years ago these testaments were digitized and can be accessed online but the 19th century index was still the main tool to be used to access the wills.  

This project is concerned with [testaments of those employed by the VOC](https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/voc-oost-indische-testamenten) now with the National Archives. These handwritten wills were recorded in Dutch in the XVII and XVIII century. These wills have been recently automatically transcribed using handwritten text recognition (HTR) technology, therefore the transcriptions might contain errors. 

# Data

The corpus consists of 2183 unique pages, plus 307 duplicated ones (for calculating the Inter-Annotator Agreement), resulting in a total of 2490 pages.
Total number of annotations is 68,416 of which 32,203 at the entitiy level (47%) abd 36,213 at the attribute level (53%). 

Total number of annotated tokens is 79,715 more details given in table below: 


## Annotation Schema
Please refer to the documentation of the annotation schema [here](data/README.md)

## Data Statement
Please refer to the data statement of the annotated dataset here (coming soon)

# Code

Please refer to the separate documentation of our Entity Recognition model implementation [here](src/code_documentation.md)

# Description of the VOC Testaments

The VOC wills in the National Archives are a small part of a much larger collection of wills that ever existed. Every VOC employee was obliged to have a will drawn up (this could be done in Amsterdam, on the ships or in the VOC establishments). This was a form of efficient personnel policy so that after the death of an employee it was clear what should be done with the bequest. 

The collection in which we work is largely built up in the VOC establishments, in particular Batavia. A copy of each will was sent to the VOC headquarters in Amsterdam. After the disintegration of the VOC at the end of the 18th century, part of these copy wills have been preserved and probably only much later merged into volumes (in Dutch: banden) that are now in the custody of the National Archives. In the 19th century, archivists produced an index to these testaments indexing the name of the male testator. A few years ago these testaments were digitized and can be accessed online but the 19th century index was still the main tool to be used to access the wills.  

This project is concerned with [testaments of those employed by the VOC](https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/voc-oost-indische-testamenten) now with the National Archives. These handwritten wills were recorded in Dutch in the XVII and XVIII century. These wills have been recently automatically transcribed using handwritten text recognition (HTR) technology, therefore the transcriptions might contain errors. 


# Annotation Typology

To 'unsilence' colonial archives by broadening access, more inclusive finding aids are required, encompassing all persons mentioned in the archive with emphasis on marginalized ones. Existing generic typologies for named entity recognition and classification tasks mainly focus on the high-level 'universal' or 'ubiquitous' triad *Person*, *Organization* and *Location*. **Our custom typology extends the universal triad to encompass all mentions of entities, both named and unnamed, and further qualifies them by gender, legal status, notarial roles and other relevant attributes**. 
<figure>
  <img src="../images/AnnotationTypology.png" width="700" height="300">
  <figcaption>
  <strong>Figure 1: </strong> Proposed Annotation Typology
  </figcaption>
</figure>

&nbsp;

Our custom typology separates the name of an entity (always tagged separately as Proper Name) from a generic reference to an entity type (Person, Place or Organization). We introduce this distinction primarily because marginalized persons are frequently mentioned in the VOC testaments, and in colonial archives more generally, without name. Instead they are referred to by a variety of terms such as “slaaf” [slave], “leiffeigenen” [serf] and “inlandse burger” [formerly enslaved persons or descendants of freed slaves]. 

For more details on each entity and attributes in the proposed annotation typology, continue reading [here](../data/AnnotationTypology.md).

# Data

The corpus consists of 2193 unique pages, plus 307 duplicated ones (for calculating the Inter-Annotator Agreement), resulting in a total of 2500 pages.
Total number of annotations is 68,429 of which 32,203 at the entity level (47%) and 36,213 at the attribute level (53%). 

**Entity Type**|**Number of Annotations**|**Percentage over Total (%)**|
-------------- | ----------------------- | ----------------------- |
Person         | 11,715                  | 36.4                    | 
Place          | 4,510                   | 14.0                    |
Organization   | 1,080                   | 3.4                     |
Proper Name    | 14,898                  | 46.2                    |
**Total**      | **33,203**              | **100**                 |


Total number of annotated tokens is 79,715 more details given in table below:

**Entity Type**|**Number of Tokens**     |**Average per Annotation**|
-------------- | ----------------------- | ------------------------ |
Person         | 32,644                  | 2.8                      | 
Place          | 10,115                  | 2.2                      |
Organization   | 4,641                   | 4.3                      |
Proper Name    | 32,397                  | 2.1                      |
**Total**      | **79,715**              | **2.7**                  |

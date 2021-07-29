# UnSilencing the VOC Testaments

## Description of the Documents
The VOC wills in the National Archives are a small part of a much larger collection of wills that ever existed. Every VOC employee was obliged to have a will drawn up (this could be done in Amsterdam, on the ships or in the VOC establishments). This was a form of efficient personnel policy so that after the death of an employee it was clear what should be done with the bequest. 

The collection in which we work is largely built up in the VOC establishments, in particular Batavia. A copy of each will was sent to the VOC headquarters in Amsterdam. After the disintegration of the VOC at the end of the 18th century, part of these copy wills have been preserved and probably only much later merged into volumes (in Dutch: banden) that are now in the custody of the National Archives. In the 19th century, archivists produced an index to these testaments indexing the name of the male testator. A few years ago these testaments were digitized and can be accessed online but the 19th century index was still the main tool to be used to access the wills.  

## Data
This project is concerned with [testaments of those employed by the VOC](https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/voc-oost-indische-testamenten) now with the National Archives. These handwritten wills were recorded in Dutch in the XVII and XVIII century. These wills have been recently automatically transcribed using handwritten text recognition (HTR) technology, therefore the transcriptions might contain errors. Part of the transcriptions (**percentage of total**) were annotated using the brat rapid annotation tool (BRAT). 

## Annotation Schema
The BRAT annotation tool was used for the task of collaborative annotations. While performing annotations on BRAT, the annotators compared the transcribed documents with the actual scans which can be found on the website of the Nationaal Archief due to the errors in the transcription. Find below an explanation ofthe annotation schema. 

### Person
This entity category refers to persons. It may refer to both individuals as well as groups of people. When tagging a piece of text as a “Person”, title of the person is included as well when available. In case only the title is mentioned, mark that as a person as well.

Persons have three kinds of attributes: **Gender**, **Role** and **Legal Status**

#### Gender
* Man
* Woman
* Group
* Unspecified

In general we are interested in tagging persons with the mentioned proper name. If the name is followed or led by an identifier which reveals their gender, we shall mark the identifier and the name. Consider these examples:

![woman](images/person_slavinneclara.png)
![man](images/person_man.png)
<img src="images/person_Group.png" width=21% height=21.25%>

The exception is made only in the case of enslaved or formerly enslaved persons — such references to persons are tagged even when not followed by proper name. This is because such persons are often mentioned without name in these documents — a silencing mechanism — and are of particular interest for this research. For example:

![slave](images/person_nonname.png)

When the leading identifier is not mentioned and only the name of a person is mentioned, gender is left as unspecified. 

<img src="images/person_unspecifiedgender.png" width=33% height=33%>

However, in a situation where a leading identifier does mark the gender of a person, we continue tagging them with that gender elsewhere on the page even when it occurs without the leading identifier. For instance consider the two mentions of “Jan Hendrik van der Laan”:

<img src="images/JanHendrik.png" width=45% height=45%>

#### Legal Status

* Enslaved
* Freed
* Unspecified

When legal status of the person is specified, that is annotated as an attribute to the person otherwise legal status is marked as unspecified. Consider these examples:

<img src="images/person_enslaved.png" width=17% height=15%> <img src="images/person_unspecleg.png" width=18% height=15%>


#### Role

* Notary
* Acting_Notary
* Testator
* Beneficiary
* Testator_Beneficiary
* Witness
* Other

When role of the person in the testament is one of the six stated roles, it is annotated and otherwise annotated as other.

<img src="images/person_notary.png" width=20% height=20%> 
<img src="images/person_witness.png" width=50% height=50%>


### ProperName
Proper names apply for places, organizations and persons. 

<img src="images/propername_notary.png" width=20% height=20%> 

### Place 

Consider these examples:

<img src="images/propernames_place.png" width=7.5% height=7.5%> <img src="images/place.png" width=60% height=60%> 

### Organization 
Organizations refer to companies, schools, universities but also the branches of the church. In case the proper name of the organization is mentioned, that is annotated as well. 

Organizations have an attribute: **beneficiary** depending on whether the testator decides to leave money to the organization.

Consider this frequent example:

<img src="images/org_place.png" width=50% height=50%> 


### Noteworthy
 
When annotators encounter a fragment of text that reveals some interesting information, it is tagged under this entity. Additionally a comment may be left under the “Note” section of any annotation. For instance the note left for the noteworthy annotation may state the correct spelling, and why the annotator found the phrase noteworthy.

<img src="images/noteworthy.png" width=50% height=50%> 





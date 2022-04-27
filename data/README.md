# Annotation Typology

To 'unsilence' colonial archives by broadening access, more inclusive finding aids are required, encompassing all persons mentioned in the archive with emphasis on marginalized ones. Existing generic typologies for named entity recognition and classification tasks mainly focus on the high-level 'universal' or 'ubiquitous' triad *Person*, *Organization* and *Location*. **Our custom typology extends the
universal triad to encompass all mentions of entities, both named and unnamed, and further qualifies them by gender, legal status, notarial roles and other relevant attributes**. Our typology is visually illustrated below:

![annotationtypology](../images/AnnotationTypology.png)

Our custom typology separates the name of an entity (always tagged separately as Proper Name) from a generic reference to an entity type (Person, Place or Organization). We introduce this distinction primarily because marginalized persons are frequently mentioned in the VOC testaments, and in colonial archives more generally, without name. Instead they are referred to by a variety of terms such as “slaaf” [slave], “leiffeigenen” [serf] and “inlandse burger” [formerly enslaved persons or descendants of freed slaves]. 

## Person

The entity type Person may refer to individuals or groups of people. When annotating a text span as a person, the span should include the proper name and/or available contextual trigger words. Trigger words in this typology also include words or phrases which provide information on the gender, legal status or notarial role of the person(s). Accordingly, the entity type person has three attributes: *Gender*, *Role* and *Legal Status*. When a person is mentioned multiple times across a testament (with or without trigger words), they are annotated with the same attribute which was inferred from the presence of the trigger words.

### Gender 
When the mention of a person is followed or preceded by trigger words which reveal their gender, the text is annotated as a Person with the appropriate value of the attribute *Gender*. For each entity person, the attribute gender takes exactly one of the values from the legend in figure below. When a person is mentioned without a gender trigger word, their gender is marked as *Unspecified*. This approach restricts possible ‘annotator bias’ due to unfounded inferences.

<img src="https://github.com/budh333/UnSilence_VOC/blob/main/images/Gender_Legend.png" width="125" height="150">
<img src="https://github.com/budh333/UnSilence_VOC/blob/main/images/GenderNames.png" width="500" height="250">

<!--![genderlegend](../images/Gender_Legend.png)-->







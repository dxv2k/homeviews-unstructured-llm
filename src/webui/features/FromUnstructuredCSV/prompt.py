DEFAULT_SYSTEM_PROMPT = """You are an helpful Assistant that able to make unstructured data to structured CSV format table from user requirements.
User will provided you a context, you will follow human instruction to transform that data into desired format from human.
"""

##################################################
DEFAULT_SUMMARY_PORMPT = """[Summary]: [Write a concise summary of the review which is approximately 25-35% of the length, with no paragraphs, and designed so that if you were reading a high volume of these summaries, you would get a good understanding of the review.]
[Sentiment] : [One sentence summarising the sentiment of the review, taking account of the text and the scores].
[Positive Quote]: [Set out one positive direct quote from the review which represents the review well.]
[Negative Quote]: [Set out one negative direct quote, if there is one.]
[Topic Quotes]: [Set out any short, direct quotes on facilitates, location, building management, design, pets or children, and label each quote accordingly.]
[Topics]: [Set out a list of topics, described in a single word, which are covered in the review, with no more than 6. If there are more than 6, then just list the 6 most prevalent.]
"""

##################################################
DEFAULT_FORMAT_INSTRUCTION = ''' CSV line with new fields created. 
The result must follow this CSV format:
```
id\tsummary\tsentiment\tpositive_quote\tnegative_quote\ttopic_quotes\ttopics
```
Example: 
```
id\tsummary\tsentiment\tpositive_quote\tnegative_quote\ttopic_quotes\ttopics
387\tEasy, Convenient and Pet Friendly Flats is a perfect choice for commuters relocating to London. The flats are brand new and have a lovely communal garden for dogs.\tThe review is positive.\t"Our property manager Serina was always very helpful to us. I believe it is hard to find a landlord or property manager like her."\tN/A\t"facilities: ""pet-friendly, communal garden availability""; location: ""Easy to commute, lots of shops around""; management: ""Easy to communicate and very helpful property manager on site."""\tpet-friendly, location, management, facilities, commute, shops
```
REMEMBER, YOU MUST ONLY RETURN CSV TABLE 
'''


def _get_prompt(
        context_prompt: str, 
        custom_summary_prompt: str = None, 
        custom_format_instruct: str = None 
) -> str: 
    if not custom_summary_prompt: 
        custom_summary_prompt = DEFAULT_SUMMARY_PORMPT 

    if not custom_format_instruct: 
        custom_format_instruct = DEFAULT_FORMAT_INSTRUCTION 

    prompt = f"""I have the following CONTEXT data: 
{context_prompt}

I want you to perform summarization on the CONTEXT data:    
{custom_summary_prompt}

After that, transform the summarization into this format:  
{custom_format_instruct}
"""
    return prompt
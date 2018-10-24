import os, json, re
from pandas import DataFrame

def getFileContent(name: str, congress_number: int) -> str:
    '''Reading the file content for a congress member

    @param name: Name of the congress member
    @param congress_number: The number of congress to look in
    '''
    with open(os.path.join('..\\data', str(congress_number), str(name)), 'r') as f:
        content = json.load(f)

    return content['revisions'][0]['*']

def isCongressMember(name: str, members) -> bool:
    '''Check in the name is a congress member

    @param name: Name of a potential congress member
    @param members: Known members of the congress
    '''
    name = re.sub(r'\ ', '_', name)
    return name in members

def findLinks(content: str) -> list:
    '''Find links in a text

    @param content: The text to search for links in
    '''
    for link in re.findall(r'\[\[(.*?)\]\]', content):
        yield re.sub(r'\|.*', '', link)

def getCongressConnections(name: str, congress_number: int, members) -> list:
    '''Get all the connections for a given congress member

    @param name: Name of the congress member
    @param congress_number: The number of the congress to look at
    '''
    content = getFileContent(re.sub('_', ' ', name), congress_number)
    links = findLinks(content)
    for x in links:
        if isCongressMember(x, members):
            yield x

def getEdges(congress_number: int, members: list) -> list:
    '''Get all the edges in a given congress

    @param congress_number: The number of the congress to get the edges for
    '''
    for member in members:
        cleaned_member = re.sub(r'_', ' ', member)
        for connection in getCongressConnections(member, congress_number, members):
            yield cleaned_member, connection

def getNodes(congress_number: int, members: list, df: DataFrame) -> list:
    '''Get all the nodes for a given congress with their state and party as attribute

    @param congress_number: The number of the congress
    '''
    for member in members:
        row = df.loc[df['WikiPageName'] == member].reset_index()

        party = str(row.at[0, 'Party'])
        if party == 'Republican': color ='red'
        else: color = 'blue'
        attributes = {
            'state': row.at[0, 'State'],
            'party': party,
            'node_color': color
        }
        member = re.sub(r'_', ' ', member)

        yield (member, attributes)

def getMembers(df: DataFrame) -> list:
    '''Get all the members from a given congress stored as pandas
    '''
    return df.groupby('WikiPageName')['WikiPageName'].groups
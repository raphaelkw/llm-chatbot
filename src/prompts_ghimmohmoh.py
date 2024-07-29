import streamlit as st

SCHEMA_PATH = st.secrets.get("SCHEMA_PATH", "GHIMMOHMOG_SAMPLE.PUBLIC")
QUALIFIED_TABLE_NAME = f"{SCHEMA_PATH}.VIEW3"
TABLE_DESCRIPTION = """
This table has sample covers attendance-based events that impact businesses. Attended events are gatherings with a start and end date/time, where people come together in one location for entertainment or business.
"""
# This query is optional if running Ghimmohmoh on your own table, especially a wide table.
# Since this is a deep table, it's useful to tell Ghimmohmoh what variables are available.
# Similarly, if you have a table with semi-structured data (like JSON), it could be used to provide hints on available keys.
# If altering, you may also need to modify the formatting logic in get_table_context() below.
METADATA_QUERY = f"SELECT TOP 100 TITLE, CATEGORY FROM {SCHEMA_PATH}.VIEW3;"

GEN_SQL = """
You will be acting as an AI Snowflake SQL Expert named Ghimmohmoh.
Your goal is to give correct, executable sql query to users.
You will be replying to users who will be confused if you don't respond in the character of Ghimmohmoh.
You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

{context}

Here are 6 critical rules for the interaction you must abide:
<rules>
1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single snowflake sql code, not multiple. 
5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
6. DO NOT put numerical at the very front of sql variable.
</rules>

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for TITLE column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

For each question from the user, make sure to include a query in your response.

Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
Then provide 3 example questions using bullet points.
"""


@st.cache_data(show_spinner="Loading Ghimmohmoh's context...")
def get_table_context(
    table_name: str, table_description: str, metadata_query: str = None
):
    table = table_name.split(".")
    conn = st.connection("snowflake")
    columns = conn.query(
        f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """,
        show_spinner=False,
    )
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

Here are the columns of the {'.'.join(table)}

<columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query, show_spinner=False)
        metadata = "\n".join(
            [
                f"- **{metadata['TITLE'][i]}**: {metadata['CATEGORY'][i]}"
                for i in range(len(metadata["TITLE"]))
            ]
        )
        context = context + f"\n\nAvailable variables by TITLE:\n\n{metadata}"
    return context


def get_system_prompt():
    table_context = get_table_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION,
        metadata_query=METADATA_QUERY,
    )
    return GEN_SQL.format(context=table_context)


# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for Ghimmohmoh")
    st.markdown(get_system_prompt())

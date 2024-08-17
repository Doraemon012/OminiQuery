from prompts import TEXT2SQL_PROMPT



class Text2SQL:
    def __init__(self, schema, cohere_client):
        self.schema = schema
        self.co = cohere_client
    
    def gen_sql(self, database_schema, requirement, relevant_tables):
        """
        The function `gen_sql` generates SQL queries based on a given database schema, requirement, and
        relevant tables using a text-to-SQL model.
        
        :param database_schema: The `database_schema` parameter typically refers to the structure or
        layout of a database, including tables, columns, relationships, and constraints. It provides the
        necessary information for generating SQL queries based on the specific database design
        :param requirement: The `requirement` parameter in the `gen_sql` method represents the specific
        requirement or query for which you want to generate SQL code. This requirement could be a query
        to retrieve specific data from the database, perform an update operation, or any other SQL
        operation you need to execute
        :param relevant_tables: The `relevant_tables` parameter in the `gen_sql` function is used to
        specify which tables in the `database_schema` are relevant to the SQL generation process based
        on the given `requirement`. This parameter helps the function focus on the necessary tables when
        generating the SQL query
        :return: The `gen_sql` method returns the generated SQL query based on the provided
        `database_schema`, `requirement`, and `relevant_tables`. If the SQL generation is successful, it
        returns the generated SQL query as a string. If there is an error during SQL generation
        (indicated by the string "BeyondError"), it prints an error message and returns `None`.
        """
        # Get the model response
        sql =  self.co.generate(
            prompt=TEXT2SQL_PROMPT.format(
                database_schema=database_schema,
                requirement=requirement,
                relevant_tables=relevant_tables,
                db_type='MySQL' # TODO: Can be changed to other DB types
                ),
            model="command", 
            max_tokens=5000,
            temperature=0.1,
            frequency_penalty=0,
            presence_penalty=0,

        ).generations[0].text.strip()
        
        # Can not generate SQL
        if sql == "BeyondError":
            print(f"Error on generating sql for [{requirement}]")
            return None
        
        return sql

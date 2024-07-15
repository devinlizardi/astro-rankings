import pyodbc
import logging
import os

# Database connection strings with parameters from environment variables
db_configs = {
    'NA': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("NA_DB_SERVER")};DATABASE={os.getenv("NA_DB_DATABASE")};UID={os.getenv("NA_DB_UID")};PWD={os.getenv("NA_DB_PASSWORD")}',
    'EU': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("EU_DB_SERVER")};DATABASE={os.getenv("EU_DB_DATABASE")};UID={os.getenv("EU_DB_UID")};PWD={os.getenv("EU_DB_PASSWORD")}',
    'UAE': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("NA_DB_SERVER")};DATABASE={os.getenv("NA_DB_DATABASE")};UID={os.getenv("NA_DB_UID")};PWD={os.getenv("NA_DB_PASSWORD")}',
    'TH': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("TH_DB_SERVER")};DATABASE={os.getenv("TH_DB_DATABASE")};UID={os.getenv("TH_DB_UID")};PWD={os.getenv("TH_DB_PASSWORD")}'
}

# Queries
queries = {
    'default': """
    SELECT 
        Rank,
        szID1,
        szID2,
        Value1,
        'https://static.latale.com/static/v3/web/img/character/character_' + 
        CASE 
            WHEN szID2 = 15 THEN '78'
            ELSE CAST(szID2 AS VARCHAR(10)) 
        END + 
        '.png' AS CharacterImageURL
    FROM 
        tbluRanking
    WHERE 
        Rank BETWEEN 1 AND 26;
    """,
    'UAE': """
    SELECT 
        Rank,
        szID1,
        szID2,
        Value1,
        'https://static.latale.com/static/v3/web/img/character/character_' + 
        CASE 
            WHEN szID2 = 15 THEN '78'
            ELSE CAST(szID2 AS VARCHAR(10)) 
        END + 
        '.png' AS CharacterImageURL
    FROM 
        tbluRanking_UAE
    WHERE 
        Rank BETWEEN 1 AND 26;
    """,
    'before': """
    SELECT 
        Rank,
        szID1,
        szID2,
        Value1,
        'https://static.latale.com/static/v3/web/img/character/character_' + 
        CASE 
            WHEN szID2 = 15 THEN '78'
            ELSE CAST(szID2 AS VARCHAR(10)) 
        END + 
        '.png' AS CharacterImageURL
    FROM 
        tbluRanking_before
    WHERE 
        Rank BETWEEN 1 AND 26;
    """,
    'UAE_before': """
    SELECT 
        Rank,
        szID1,
        szID2,
        Value1,
        'https://static.latale.com/static/v3/web/img/character/character_' + 
        CASE 
            WHEN szID2 = 15 THEN '78'
            ELSE CAST(szID2 AS VARCHAR(10)) 
        END + 
        '.png' AS CharacterImageURL
    FROM 
        tbluRanking_UAE_before
    WHERE 
        Rank BETWEEN 1 AND 26;
    """
}

def fetch_rankings(db_config, query):
    try:
        logging.debug(f"Connecting with config: {db_config}")
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()
        logging.debug(f"Executing query: {query}")
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
        logging.debug(f"Fetched results: {results}")
        return results
    except pyodbc.Error as e:
        logging.error(f"Error fetching rankings for config {db_config}: {e}")
        return []

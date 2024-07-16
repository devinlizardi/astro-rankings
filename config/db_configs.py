import pyodbc
import logging
import os
from typing import Optional
from dataclasses import dataclass
from enum import IntEnum

DATABASE_DRIVER = 'ODBC Driver 17 for SQL Server'

if DATABASE_DRIVER not in pyodbc.drivers():
    raise ValueError(f'Database driver {DATABASE_DRIVER} is not installed on this machine')


class DbConfig:
    prefix: str
    server: str
    database: str
    uid: str
    pwd: str

    def __init__(self, prefix: str, server: Optional[str] = None, database: Optional[str] = None,
                 uid: Optional[str] = None, pwd: Optional[str] = None, *, use_env: bool = False) -> None:
        self.prefix = prefix

        if use_env:
            self.server = os.getenv(f'{prefix}_DB_SERVER')
            self.database = os.getenv(f'{prefix}_DB_DATABASE')
            self.uid = os.getenv(f'{prefix}_DB_UID')
            self.pwd = os.getenv(f'{prefix}_DB_PASSWORD')

        if server is not None:
            self.server = server

        if database is not None:
            self.database = database

        if uid is not None:
            self.uid = uid

        if pwd is not None:
            self.pwd = pwd

    def __str__(self) -> str:
        return f'DRIVER={{{DATABASE_DRIVER}}};SERVER={self.server};DATABASE={self.database};UID={self.uid};PWD={self.pwd}'


# Database connection configurations with parameters from environment variables
db_configs: dict[str, DbConfig] = {
    'NA': DbConfig(prefix='NA', use_env=True),
    'EU': DbConfig(prefix='EU', use_env=True),
    'UAE': DbConfig(prefix='NA', use_env=True),
    'TH': DbConfig(prefix='TH', use_env=True),
}

# Queries
queries = {
    'default': """
    SELECT 
        Rank,
        uiID1,
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
        Rank BETWEEN 1 AND 25;
    """,
    'UAE': """
    SELECT 
        Rank,
        uiID1,
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
        Rank BETWEEN 1 AND 25;
    """,
    'before': """
    SELECT 
        Rank,
        uiID1,
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
        Rank BETWEEN 1 AND 25;
    """,
    'UAE_before': """
    SELECT 
        Rank,
        uiID1,
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
        Rank BETWEEN 1 AND 25;
    """
}


class MovementType(IntEnum):
    UNCHANGED = 0
    UP = 1
    DOWN = -1


@dataclass
class FetchedRanking:
    Rank: int
    uiID1: int
    szID1: int
    szID2: int
    Value1: int
    CharacterImageURL: str
    MovementType: Optional[MovementType] = None


def fetch_rankings(db_config: DbConfig, query: str) -> list[FetchedRanking]:
    try:
        logging.debug(f"Connecting with config: {db_config}")
        conn = pyodbc.connect(str(db_config))
        cursor = conn.cursor()
        logging.debug(f"Executing query: {query}")
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(FetchedRanking(**dict(zip(columns, row))))
        conn.close()
        logging.debug(f"Fetched results: {results}")
        return results
    except pyodbc.Error as e:
        logging.error(f"Error fetching rankings for config {db_config}: {e}")
        return []

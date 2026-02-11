import sqlite3


def query_dict(db_path: str, word: str) -> str:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT translation FROM stardict WHERE sw = ? LIMIT 1"
        row = cursor.execute(sql, (word,)).fetchone()
        if row:
            return dict(row).get('translation', "")
        return ""

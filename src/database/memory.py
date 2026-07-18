import sqlite3
from src.core.config import DATABASE_PATH
class MemoryManager:
    """
    Sigma AI مرکزی Memory Manager

    مستقبل میں یہی کلاس:
    - Chat Memory
    - User Memory
    - Long-Term Memory
    - Task Memory
    - AI Learning
    - Context History
    - Conversation Recall

    سب کچھ Handle کرے گی۔
    """

    def __init__(self):
        self.db_path = DATABASE_PATH 
    import sqlite3
from src.core.config import DATABASE_PATH


class MemoryManager:
    """
    Sigma AI Memory Manager
    Conversation Recall System
    """

    def __init__(self):
        self.db_path = DATABASE_PATH
        self.initialize_database()

    def initialize_database(self):
        """Create database if it does not exist."""

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        connection.commit()
        connection.close()

    def save_memory(self, category: str, content: str):
        """
        Save a memory into database.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories(category, content)
            VALUES (?, ?)
            """,
            (category, content)
        )

        connection.commit()
        connection.close()

    def get_memories(self, category: str = None):
        """
        Retrieve memories from database.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if category:
            cursor.execute(
                """
                SELECT category, content, created_at
                FROM memories
                WHERE category = ?
                ORDER BY id DESC
                """,
                (category,)
            )
        else:
            cursor.execute(
                """
                SELECT category, content, created_at
                FROM memories
                ORDER BY id DESC
                """
            )

        data = cursor.fetchall()
        connection.close()

        return data

    def get_conversation_history(self, limit: int = 20):
        """
        Return latest conversation history.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT category, content, created_at
            FROM memories
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        data = cursor.fetchall()

        connection.close()

        return list(reversed(data))

    def delete_all_memories(self):
        """
        Delete all memories.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM memories")

        connection.commit()
        connection.close()

    def memory_count(self):
        """
        Return total memory count.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM memories")

        count = cursor.fetchone()[0]

        connection.close()

        return count

    def latest_memory(self):
        """
        Return latest saved memory.
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, content, created_at
            FROM memories
            ORDER BY id DESC
            LIMIT 1
        """)

        memory = cursor.fetchone()

        connection.close()

        return memory
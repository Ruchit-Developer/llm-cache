import sqlite3
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SmartCache:
    def __init__(self, db_path: str = "llm_cache.db"):
        """Initializes the SQLite caching engine."""
        self.db_path = db_path
        self._boot_database()

    def _boot_database(self):
        """Creates the high-speed local database if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    prompt_hash TEXT PRIMARY KEY,
                    response TEXT NOT NULL
                )
            """)
            conn.commit()

    def _generate_hash(self, text: str) -> str:
        """Converts a long prompt into a fast, searchable SHA-256 hash."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def check_cache(self, prompt: str):
        """Checks if the exact prompt has been asked before."""
        prompt_hash = self._generate_hash(prompt)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT response FROM api_cache WHERE prompt_hash = ?", (prompt_hash,))
            result = cursor.fetchone()
            
            if result:
                logging.info("CACHE HIT: Returning instant response (Cost: $0.00).")
                return result[0]
                
        logging.info("CACHE MISS: Prompt not found. Routing to LLM Provider...")
        return None

    def save_to_cache(self, prompt: str, response: str):
        """Saves the expensive LLM response to local memory."""
        prompt_hash = self._generate_hash(prompt)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO api_cache (prompt_hash, response)
                VALUES (?, ?)
            """, (prompt_hash, response))
            conn.commit()
            logging.info("CACHE SAVED: Response stored in local memory.")

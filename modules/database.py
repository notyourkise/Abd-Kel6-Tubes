import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import streamlit as st
from config.settings import DB_CONFIG
import numpy as np

def convert_params(params):
    """Convert numpy types to Python types for psycopg2"""
    if params is None:
        return None
    
    if isinstance(params, (list, tuple)):
        return tuple(
            int(p) if isinstance(p, (np.integer, np.int64)) else 
            float(p) if isinstance(p, (np.floating, np.float64)) else 
            p for p in params
        )
    return params

class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            return True
        except psycopg2.Error as e:
            st.error(f"❌ Database connection failed: {str(e)}")
            return False

    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except:
            pass

    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results as DataFrame"""
        try:
            if self.conn is None or self.conn.closed:
                self.connect()
            
            # Convert numpy types to Python types
            params = convert_params(params)
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
            else:
                df = pd.DataFrame()
            return df
        except psycopg2.Error as e:
            try:
                self.conn.rollback()
            except:
                pass
            st.warning(f"⚠️ Query error: {str(e)[:100]}")
            return pd.DataFrame()
        except Exception as e:
            st.warning(f"⚠️ Unexpected error: {str(e)[:100]}")
            return pd.DataFrame()

    def execute_insert_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            if self.conn is None or self.conn.closed:
                self.connect()
            
            # Convert numpy types to Python types
            params = convert_params(params)
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            try:
                self.conn.rollback()
            except:
                pass
            st.error(f"❌ Update failed: {str(e)[:100]}")
            return False
        except Exception as e:
            try:
                self.conn.rollback()
            except:
                pass
            st.error(f"❌ Unexpected error: {str(e)[:100]}")
            return False

    def get_all_students(self):
        """Get all students"""
        query = "SELECT * FROM student ORDER BY id_student"
        return self.execute_query(query)

    def get_student_by_id(self, student_id):
        """Get student by ID"""
        query = "SELECT * FROM student WHERE id_student = %s"
        return self.execute_query(query, (student_id,))

    def get_student_with_details(self, student_id):
        """Get student with all related information"""
        query = """
        SELECT 
            s.*, 
            sh.study_hours_per_week, sh.prefers_group_study, sh.has_private_tutor,
            es.math_score, es.reading_score, es.writing_score
        FROM student s
        LEFT JOIN study_habits sh ON s.id_student = sh.id_student
        LEFT JOIN exam_scores es ON s.id_student = es.id_student
        WHERE s.id_student = %s
        """
        return self.execute_query(query, (student_id,))

@st.cache_resource
def get_db_connection():
    """Get cached database connection"""
    db = DatabaseConnection()
    if db.connect():
        return db
    return None

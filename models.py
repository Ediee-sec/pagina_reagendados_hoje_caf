from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from sqlalchemy import text

db = SQLAlchemy()

def get_data_as_dataframe(limit=None, offset=None):
    query_str = "SELECT * FROM reagendados_hoje"
    if limit is not None and offset is not None:
        query_str += f" LIMIT {limit} OFFSET {offset}"
    query = text(query_str)
    result = db.session.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df.columns = df.columns.str.lower()
    if 'data_agendamento' in df.columns:
        df['data_agendamento'] = pd.to_datetime(df['data_agendamento'], errors='coerce').dt.date
    df = df.reset_index(drop=False)
    df = df.rename(columns={'index': 'id'})
    df['id'] = df['id'] + 1
    return df

def get_total_data_count():
    query = text("SELECT COUNT(*) FROM reagendados_hoje")
    result = db.session.execute(query)
    return result.scalar_one()

class Data(db.Model):
    __tablename__ = 'reagendados_hoje'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    curso = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    data_agendamento = db.Column(db.Date)
    total = db.Column(db.Float)
    status_pendencia = db.Column(db.String(50))



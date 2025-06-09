from flask import Blueprint, render_template, request, send_file, jsonify
from models import db, get_data_as_dataframe, get_total_data_count
import io
import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
from datetime import date
import math

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = 30 # 30 linhas por página
    offset = (page - 1) * per_page

    # Obter dados como DataFrame (com paginação)
    df = get_data_as_dataframe(limit=per_page, offset=offset)
    
    # Obter o total de registros sem paginação para calcular o total de páginas
    total_registros = get_total_data_count()
    total_pages = math.ceil(total_registros / per_page)

    # Calcular estatísticas antes de filtrar/ordenar (agora baseado no df completo)
    df_full = get_data_as_dataframe() # Obter o DataFrame completo para cálculos de estatísticas

    agendamentos_hoje_count = 0
    if not df_full.empty and 'data_agendamento' in df_full.columns:
        df_full['data_agendamento'] = pd.to_datetime(df_full['data_agendamento'], errors='coerce')
        today = date.today()
        agendamentos_hoje_count = df_full[df_full['data_agendamento'].dt.date == today].shape[0]

    pendencias_count = 0
    if not df_full.empty and 'status_pendencia' in df_full.columns:
        pendencias_count = df_full[df_full['status_pendencia'].str.contains('Pendente', na=False, case=False)].shape[0]

    # Filter (aplicado ao df paginado)
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    if filter_column and filter_value:
        if filter_column in df.columns:
            df = df[df[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]

    # Sort (aplicado ao df paginado)
    sort_by = request.args.get('sort_by', 'nome')
    sort_order = request.args.get('sort_order', 'asc')
    if sort_by in df.columns:
        if df[sort_by].dtype == 'object': # For strings, use case-insensitive sort
            df = df.sort_values(by=sort_by, key=lambda col: col.str.lower(), ascending=(sort_order == 'asc'))
        else:
            df = df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Converter DataFrame para lista de dicionários
    data = df.to_dict('records')

    if data:
        print("Keys of the first data row:", data[0].keys())
    else:
        print("No data to display.")
    
    return render_template('index.html', 
                         data=data, 
                         sort_by=sort_by, 
                         sort_order=sort_order, 
                         filter_column=filter_column, 
                         filter_value=filter_value,
                         total_registros=total_registros,
                         agendamentos_hoje_count=agendamentos_hoje_count,
                         pendencias_count=pendencias_count,
                         page=page,
                         total_pages=total_pages,
                         per_page=per_page)

@main.route('/download/<file_format>')
def download_data(file_format):
    # Obter dados como DataFrame
    df = get_data_as_dataframe()
    
    # Aplicar os mesmos filtros da rota index
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    if filter_column and filter_value:
        if filter_column in df.columns:
            df = df[df[filter_column].str.contains(filter_value, case=False, na=False)]

    sort_by = request.args.get('sort_by', 'nome')
    sort_order = request.args.get('sort_order', 'asc')
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    if file_format == 'csv':
        output = io.BytesIO()
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='reagendados_hoje.csv')

    elif file_format == 'xlsx':
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='reagendados_hoje.xlsx')

    elif file_format == 'json':
        return jsonify(df.to_dict('records'))

    elif file_format == 'pdf':
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        
        # Create table data
        table_data = [df.columns.tolist()]  # Headers
        table_data.extend(df.values.tolist())  # Data
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        # Build PDF
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("Relatório - Reagendados Hoje", styles['Title'])
        elements.append(title)
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        
        return send_file(output, mimetype='application/pdf', as_attachment=True, download_name='reagendados_hoje.pdf')

    return "Invalid file format", 400


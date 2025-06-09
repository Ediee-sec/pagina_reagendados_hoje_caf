# Dashboard de Reagendamentos

Este projeto é um dashboard web que exibe e gerencia os dados de reagendamentos do sistema CAF. Ele consome os dados gerados pelo projeto [reagendamento_caf](https://github.com/Ediee-sec/reagendamento_caf), que é responsável por preencher a tabela `reagendados_hoje` no banco de dados.

## Funcionalidades

- Visualização de reagendamentos em formato de tabela
- Filtros por coluna
- Ordenação por qualquer coluna
- Paginação dos resultados
- Estatísticas de:
  - Total de registros
  - Agendamentos do dia
  - Itens pendentes
- Exportação de dados em múltiplos formatos:
  - CSV
  - Excel (XLSX)
  - JSON
  - PDF

## Tecnologias Utilizadas

- **Backend**:
  - Python 3.11
  - Flask
  - SQLAlchemy
  - Pandas
  - ReportLab (para geração de PDFs)

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5

## Estrutura do Banco de Dados

A tabela `reagendados_hoje` possui os seguintes campos:
- `id`: Identificador único
- `nome`: Nome do paciente
- `curso`: Curso do paciente
- `telefone`: Número de telefone
- `data_agendamento`: Data do agendamento
- `total`: Valor total
- `status_pendencia`: Status da pendência

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
export POSTGRES_HOST="seu_host"
export POSTGRES_PORT="sua_porta"
export POSTGRES_DB="seu_banco"
export POSTGRES_USER="seu_usuario"
export POSTGRES_PASSWORD="sua_senha"
```

4. Execute a aplicação:
```bash
python app.py
```

## Deploy

O projeto está configurado para deploy no Railway. O arquivo `Procfile` já está configurado para usar o Gunicorn como servidor WSGI.

## Integração com o Sistema CAF

Este dashboard é parte de um ecossistema maior que inclui:
1. [reagendamento_caf](https://github.com/Ediee-sec/reagendamento_caf): Responsável por preencher a tabela `reagendados_hoje`
2. Este dashboard: Responsável por visualizar e gerenciar os dados

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 
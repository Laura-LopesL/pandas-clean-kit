# pandas-clean-kit

Pequeno pipeline de limpeza de dados em Python com Pandas.

O projeto lê um arquivo CSV, normaliza nomes de colunas, remove registros duplicados, converte colunas numéricas e exporta o resultado para Parquet.

## Funcionalidades

- Normalização de nomes de colunas
- Remoção de duplicatas
- Conversão de colunas numéricas
- Identificação de valores ausentes
- Relatório simples de qualidade dos dados
- Exportação para Parquet
- Testes automatizados com `unittest`
- Contagem de erros de conversão numérica

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python app.py --in raw.csv --out cleaned.parquet
```

Exemplo de entrada:

```csv
Product,Amount,Price
A,10,2.5
A,10,2.5
B,invalid,4.0
```

Exemplo de saída no terminal:

Exemplo de saída no terminal:

```text
Rows read: 3
Duplicates removed: 1
Missing values: 0
Numeric conversion errors: 1
Rows exported: 2
Saved to: cleaned.parquet
```

## Estrutura

- `app.py`: interface de linha de comando
- `cleaner.py`: funções de limpeza e transformação
- `tests/test_cleaner.py`: testes automatizados
- `requirements.txt`: dependências do projeto

## Testes

```bash
python -m unittest discover -s tests -v
```
import os
import pandas as pd

# ------------------------------------------------------------------------------
# ETAPA 1 — IMPORTAÇÃO E CONFIGURAÇÕES INICIAIS
# ------------------------------------------------------------------------------

# Define o caminho do arquivo
pasta_base = r"C:\PUCPR"
#pasta_base = r"F:\PUCPR\2025\EAD-4D\IA nos negócios\Database"
nome_arquivo = "log.csv"
caminho_arquivo = os.path.join(pasta_base, nome_arquivo)

# Importa os dados
df = pd.read_csv(caminho_arquivo, sep=";")

# Formata a exibição de números decimais no pandas (sem notação científica)
pd.set_option("display.float_format", "{:.2f}".format)

# ------------------------------------------------------------------------------
# ETAPA 2 — VISÃO GERAL DOS DADOS
# ------------------------------------------------------------------------------

# Exibe as primeiras linhas
print("Primeiras linhas da base de dados:")
print(df.head())

# Estrutura geral da base
print("\nInformações gerais sobre os dados:")
print(df.info())

# Contagem de valores ausentes por coluna
print("\nValores ausentes por coluna:")
print(df.isnull().sum())

# Tipos de dados por categoria
tipos = df.dtypes.value_counts()
print("\nDistribuição dos tipos de dados:")
print(tipos)

# ------------------------------------------------------------------------------
# ETAPA 3 — TRATAMENTO DE DADOS MONETÁRIOS E TEMPORAIS
# ------------------------------------------------------------------------------

# Conversão de colunas monetárias (de string para float)
colunas_monetarias = [
    "custo_unitario", "custo_total", "valor_unitario", "sub_total",
    "desconto_aplicado", "valor_frete", "valor_total",
    "lucro_unitario", "lucro_total", "margem_lucro_fixada",
    "percentual_desconto_aplicado", "margem_lucro_real"
]

for col in colunas_monetarias:
    if df[col].dtype == object:
        df[col] = df[col].str.replace(",", ".").astype(float)

# Conversão da coluna de data
df["data_pedido"] = pd.to_datetime(df["data_pedido"], format="%d/%m/%Y")

# Extração de informações úteis da data
df["ano"] = df["data_pedido"].dt.year
df["mes"] = df["data_pedido"].dt.month

# ------------------------------------------------------------------------------
# ETAPA 4 — VERIFICAÇÕES DE QUALIDADE DOS DADOS
# ------------------------------------------------------------------------------

# Checagem de registros duplicados
print("\nRegistros duplicados na base:", df.duplicated().sum())

# Percentual de valores faltantes por coluna
faltantes = df.isnull().mean().sort_values(ascending=False) * 100
print("\nPercentual de valores ausentes por coluna:")
print(faltantes)

# Conversão de campos booleanos para 0/1 (se necessário)
df["cliente_reincidente"] = df["cliente_reincidente"].astype(int)

# Verifica cardinalidade das variáveis categóricas
categóricas = df.select_dtypes(include="object").nunique().sort_values()
print("\nCardinalidade das variáveis categóricas:")
print(categóricas)

# ------------------------------------------------------------------------------
# ETAPA 5 — RESUMO POR CANAL DE VENDA (VISÃO EMPRESARIAL)
# ------------------------------------------------------------------------------

# Geração de uma tabela resumo por canal de venda
resumo_canal = df.groupby("canal_venda").agg({
    "valor_total": "sum",
    "lucro_total": "sum",
    "id_pedido": "count"
}).rename(columns={"id_pedido": "qtd_pedidos"}).sort_values("valor_total", ascending=False)

print("\nResumo por canal de venda (valor, lucro e quantidade de pedidos):")
print(resumo_canal)










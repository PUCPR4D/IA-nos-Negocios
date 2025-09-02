import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==============================================================================
# ETAPA 1 — IMPORTAÇÃO, ORGANIZAÇÃO E PRÉ-PROCESSAMENTO DE DADOS
# ==============================================================================

# Caminho do arquivo CSV
pasta_base = r"C:\PUCPR"
#pasta_base = r"F:\PUCPR\2025\EAD-4D\IA nos negócios\Database"
nome_arquivo = "log.csv"
caminho_arquivo = os.path.join(pasta_base, nome_arquivo)

# Importação
df = pd.read_csv(caminho_arquivo, sep=";")

# Configuração de exibição
pd.set_option("display.float_format", "{:.2f}".format)

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

# Conversão de datas e criação de colunas derivadas
df["data_pedido"] = pd.to_datetime(df["data_pedido"], format="%d/%m/%Y")
df["ano"] = df["data_pedido"].dt.year
df["mes"] = df["data_pedido"].dt.month

# Tratamento de campos booleanos
df["produto_entregue"] = df["produto_entregue"].fillna(False).astype(bool)
df["cliente_reincidente"] = df["cliente_reincidente"].astype(int)

# ==============================================================================
# ETAPA 2 — ANÁLISE DESCRITIVA E DIAGNÓSTICA DOS DADOS
# ==============================================================================

# Estatísticas descritivas
print("\nEstatísticas descritivas:")
print(df.describe())

# Frequência de variáveis categóricas
print("\nFrequência por tipo de produto:")
print(df['tipo_produto'].value_counts())

print("\nDistribuição da forma de pagamento:")
print(df['forma_pagamento'].value_counts(normalize=True))

print("\nStatus de entrega do produto:")
print(df['produto_entregue'].value_counts())

# Histograma de valor_total
df['valor_total'].hist(bins=30)
plt.title("Distribuição de Valor Total")
plt.xlabel("Valor Total")
plt.ylabel("Frequência")
plt.show()

# Boxplot de valor_total por região
sns.boxplot(x='regiao', y='valor_total', data=df)
plt.title("Boxplot de Valor Total por Região")
plt.xlabel("Região")
plt.ylabel("Valor Total")
plt.show()

# Contagem de pedidos por região
df['regiao'].value_counts().plot(kind='bar')
plt.title("Distribuição por Região")
plt.xlabel("Região")
plt.ylabel("Contagem")
plt.show()

# Correlação entre variáveis monetárias
correlacoes = df[colunas_monetarias].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlacoes, annot=True, cmap="coolwarm")
plt.title("Correlação entre Variáveis Monetárias")
plt.show()

# Tabela cruzada: sexo_cliente vs tipo_produto
tabela = pd.crosstab(df['sexo_cliente'], df['tipo_produto'], normalize='index')
plt.figure(figsize=(12, 6))
sns.heatmap(tabela, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("Distribuição de Tipo de Produto por Gênero do Cliente")
plt.xlabel("Tipo de Produto")
plt.ylabel("Gênero do Cliente")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Lucro total por tipo de produto
plt.figure(figsize=(12, 6))
sns.boxplot(x="tipo_produto", y="lucro_total", data=df)
plt.xticks(rotation=45)
plt.title("Lucro Total por Tipo de Produto")
plt.tight_layout()
plt.show()

# Quantidade de produtos vendidos por canal de venda
produtos_por_canal = df.groupby("canal_venda")["produto"].count().sort_values()
plt.figure(figsize=(10, 5))
sns.barplot(x=produtos_por_canal.index, y=produtos_por_canal.values)
plt.title("Quantidade de Produtos Vendidos por Canal de Venda")
plt.xlabel("Canal de Venda")
plt.ylabel("Número de Produtos Vendidos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Margem média por canal de venda
margem_media_canal = df.groupby("canal_venda")["margem_lucro_real"].mean().sort_values()
plt.figure(figsize=(10, 5))
sns.barplot(x=margem_media_canal.index, y=margem_media_canal.values)
plt.title("Média da Margem de Lucro por Canal de Venda")
plt.xlabel("Canal de Venda")
plt.ylabel("Margem de Lucro Média")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Evolução mensal do lucro total
lucro_mensal = df.groupby(["ano", "mes"])["lucro_total"].sum().reset_index()
lucro_mensal["periodo"] = lucro_mensal["ano"].astype(str) + "-" + lucro_mensal["mes"].astype(str)

plt.figure(figsize=(10, 5))
sns.lineplot(data=lucro_mensal, x="periodo", y="lucro_total", marker="o")
plt.title("Evolução Mensal do Lucro Total")
plt.xlabel("Período")
plt.ylabel("Lucro Total")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Comparativo: produto entregue x lucro médio
entregue_lucro = df.groupby("produto_entregue")["lucro_total"].mean()

plt.figure(figsize=(6, 4))
sns.barplot(x=entregue_lucro.index.map({True: "Entregue", False: "Não Entregue"}), y=entregue_lucro.values)
plt.title("Média de Lucro por Status de Entrega")
plt.ylabel("Lucro Médio")
plt.xlabel("Produto Entregue")
plt.tight_layout()
plt.show()

# Correlação cruzada entre variáveis-chave
correlacoes_chave = df[["valor_total", "lucro_total", "desconto_aplicado", "valor_frete", "avaliacao_cliente"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlacoes_chave, annot=True, cmap="RdBu", center=0)
plt.title("Correlação entre Indicadores de Negócio")
plt.tight_layout()
plt.show()

# Top 10 clientes por lucro gerado
top_clientes = df.groupby("id_cliente")["lucro_total"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_clientes.index.astype(str), y=top_clientes.values)
plt.title("Top 10 Clientes por Lucro Gerado")
plt.xlabel("ID do Cliente")
plt.ylabel("Lucro Total")
plt.tight_layout()
plt.show()

# Seleciona os registros do cliente 1513
df["avaliacao_cliente"] = pd.to_numeric(df["avaliacao_cliente"], errors="coerce")
cliente_1513 = df[df["id_cliente"] == 1513]


# Exibe resumo
print("Resumo do Cliente 1513")
print("-" * 30)
print(f"Total de pedidos: {cliente_1513.shape[0]}")
print(f"Lucro total gerado: R$ {cliente_1513['lucro_total'].sum():.2f}")
print(f"Valor total comprado: R$ {cliente_1513['valor_total'].sum():.2f}")
print(f"Avaliação média: {cliente_1513['avaliacao_cliente'].mean():.2f}")
print(f"Produtos mais comprados:\n{cliente_1513['tipo_produto'].value_counts().head()}")
print(f"Forma(s) de pagamento:\n{cliente_1513['forma_pagamento'].value_counts()}")

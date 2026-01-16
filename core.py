import json
import os
import sys
from datetime import datetime


# Lista que armazena todas as movimentações - Constantes
movimentacoes = []

# Dados em memória
def caminho_dados():
    base = os.getenv('APPDATA')
    pasta = os.path.join(base, 'FinancePy')

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    return os.path.join(pasta, 'dados.json')    

CAMINHO_DADOS = caminho_dados()
ARQUIVO_DADOS = CAMINHO_DADOS    

# ordenar movimentações por data (funções auxiliares)
def converter_data(data_str):
    try:
        return datetime.strptime(data_str, '%d/%m/%Y')
    except ValueError:
        return datetime.min

def ordenar_movimentacoes():
    movimentacoes.sort(
        key=lambda mov: converter_data(mov.get('data', '---'))
    )

def adicionar_receita(valor, descricao, data):
    """
    Adiciona uma receita ao sistema.
    """
    if not data:
        data = '---'

    movimentacoes.append({
        'tipo': 'receita',
        'valor': valor,
        'descricao': descricao,
        'data': data
    })
    ordenar_movimentacoes()
    salvar_dados()

def adicionar_despesa(valor, descricao, data):
    if not data:
        data = '---'
        
    """
    Adiciona uma despesa ao sistema.
    """
    movimentacoes.append({
        'tipo': 'despesa',
        'valor': valor,
        'descricao': descricao,
        'data': data
    })
    ordenar_movimentacoes()
    salvar_dados()

def calcular_saldo():
    """
    Calcula o saldo com base nas movimentações.
    """
    saldo = 0
    for mov in movimentacoes:
        if mov['tipo'] == 'receita':
            saldo += mov['valor']
        else:
            saldo -= mov['valor']

    return saldo            

"""Retorna todas as movimentações registradas."""

def listar_movimentacoes():
    for mov in movimentacoes:
         if 'data' not in mov or not mov['data']:
             mov['data'] = '---'
        
    movimentacoes.sort(
        key=lambda mov: converter_data(mov['data']),
        reverse=True
    )

    return movimentacoes
    
# Função de filtro
def filtrar_movimentacoes_por_mes_ano(mes=None, ano=None):
    resultado = []

    for mov in movimentacoes:
        data = mov.get('data', '---')

        if data == '---':
            continue

        try:
            data_obj = datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            continue

        if ano and data_obj.year != ano:
            continue

        resultado.append(mov)

    return resultado            


def carregar_dados():
    global movimentacoes

    if not os.path.exists(CAMINHO_DADOS):
        movimentacoes = []
        return
    
    with open(CAMINHO_DADOS, 'r', encoding='utf-8') as arquivo:
        movimentacoes = json.load(arquivo)
        ordenar_movimentacoes()

def salvar_dados():
    with open(CAMINHO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(movimentacoes, arquivo, ensure_ascii=False, indent=4)

# remover movimentação
def remover_movimentacao(indice):
    try:
        movimentacoes.pop(indice)
        salvar_dados()
    except IndexError:
        pass

def calcular_total_receitas():
    total = 0
    for mov in movimentacoes:
        if mov['tipo'] == 'receita':
            total += mov['valor']
    return total

def calcular_total_despesas():
    total = 0
    for mov in movimentacoes:
        if mov['tipo'] == 'despesa':
            total += mov['valor']
    return total


# Chamada automatica ao iniciar o programa
carregar_dados()



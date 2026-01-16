import tkinter as tk
from tkinter import messagebox
from core import (
    adicionar_receita,
    adicionar_despesa,
    calcular_saldo,
    listar_movimentacoes,
    ordenar_movimentacoes,
    salvar_dados,
    remover_movimentacao,
    calcular_total_receitas,
    calcular_total_despesas,
    filtrar_movimentacoes_por_mes_ano
)
from datetime import datetime


def iniciar_interface():
    # Janela principal
    janela = tk.Tk()
    fonte_titulo = ('Segoe UI', 18, 'bold')
    fonte_resumo = ('Segoe UI', 11, 'bold')
    fonte_padrao = ('Segoe UI', 10)
    fonte_lista = ('Consolas', 10)
    janela.title('FinancePy - Controle Financeiro')
    janela.geometry('620x660')
    janela.minsize(620, 660)
    indice_em_edicao = None

    # Titulo
    titulo = tk.Label(
        janela,
        text='FinancePy',
        font=fonte_titulo
    )
    titulo.pack(pady=10)

    def validar_data(data_str):
        if data_str == '' or data_str == '---':
            return '---'
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return data_str
        except ValueError:
            messagebox.showerror(
                'Erro',
                'Data inválida. Use o formato DD/MM/AAAA.'
            )
            return None
    
    # Frame resumo
    frame_resumo = tk.Frame(janela, bd=1, relief=tk.SOLID, bg='white')
    frame_resumo.pack(pady=10, padx=10, fill='x')

    # FRames de organização
    frame_campos = tk.Frame(janela)
    frame_campos.pack(pady=5)

    frame_filtro = tk.Frame(janela)
    frame_filtro.pack(pady=5)

    frame_botao_excluir = tk.Frame(janela)
    frame_botao_excluir.pack(pady=5)

    # Resumo de receitas e despesas
    label_receitas = tk.Label(
        frame_resumo,
        text='Receitas: R$ 0.00',
        font=fonte_resumo,
        fg='blue',
        bg='white'
    )
    label_receitas.pack(anchor='w')

    label_despesas = tk.Label(
        frame_resumo,
        text='Despesas: R$ 0.00',
        font=fonte_resumo,
        fg='red',
        bg='white'
    )
    label_despesas.pack(anchor='w')

    label_saldo_resumo = tk.Label(
        frame_resumo,
        text='Saldo: R$ 0.00',
        font=fonte_resumo,
        bg='white'
    )
    label_saldo_resumo.pack(anchor='w')
  
        
    # Função para atualizar saldos
    def atualizar_saldos():
        saldo = calcular_saldo()

        label_receitas.config(
            text=f'Receitas: R$ {calcular_total_receitas():.2f}'
        )
        
        label_despesas.config(
            text=f'Despesas: R$ {calcular_total_despesas():.2f}'
        )

        if saldo >=0:
            label_saldo_resumo.config(
                text=f'Saldo: R$ {saldo:.2f}',
                fg='green',
                font=('Arial', 10, 'bold')
            )
            resultado.config(
                text=f'Saldo: R$ {saldo:.2f}',
                fg='green',
                font=('Arial', 10)
            )
        else:
            label_saldo_resumo.config(
                text=f'Saldo: R$ {saldo:.2f}',
                fg='red',
                font=('Arial', 10, 'bold')
            )
            resultado.config(
                text=f'Saldo: R$ {saldo:.2f}',
                fg='red',
                font=('Arial', 10, 'bold')
            )    

    def filtrar_movimentacoes():
        mes = entrada_mes.get().strip()
        ano = entrada_ano.get().strip()

        lista_mov.delete(0, tk.END)

        for mov in listar_movimentacoes():
            data = mov.get('data', '---')

            if data == '---':
                continue

            try:
                data_obj = datetime.strptime(data, '%d/%m/%Y')
            except ValueError:
                continue

            if mes and data_obj.month != int(mes):
                continue    

            if ano and data_obj.year != int(ano):
                continue

            texto = f"{mov['tipo'].capitalize()} | R$ {mov['valor']:.2f} | {mov['descricao']} | {data}"
            lista_mov.insert(tk.END, texto)

    def calcular_resumo_mensal(mes, ano):
        total_receitas = 0
        total_despesas = 0

        for mov in listar_movimentacoes():
            data = mov.get('data')
            if not data or data == '---':
                continue

            try:
                data_obj = datetime.strptime(data, '%d/%m/%Y')
            except ValueError:
                continue

            if data_obj.month == mes and data_obj.year == ano:
                if mov['tipo'] == 'receita':
                    total_receitas += mov['valor']
                else:
                    total_despesas += mov['valor']

        saldo = total_receitas - total_despesas
        return total_receitas, total_despesas, saldo                


    def clicar_editar():
        nonlocal indice_em_edicao

        selecionado = lista_mov.curselection()

        if not selecionado:
            messagebox.showwarning(
                'Aviso',
                'Selecione uma movimentação para editar.'
            )
            return
        
        indice = selecionado[0]
        mov = listar_movimentacoes()[indice]

        entrada_valor.delete(0, tk.END)
        entrada_valor.insert(0, str(mov['valor']))

        entrada_desc.delete(0, tk.END)
        entrada_desc.insert(0, mov['descricao'])

        entrada_data.delete(0, tk.END)
        entrada_data.insert(0, mov.get('data', '---'))

     
        indice_em_edicao = indice

    def clicar_salvar_edicao():
        nonlocal indice_em_edicao

        if indice_em_edicao is None:
            messagebox.showwarning(
                'Aviso',
                'Nenhuma movimentação está em edição.'
            )
            return
        
        try:
            valor = float(entrada_valor.get())
            descricao = entrada_desc.get().strip()

            data = entrada_data.get().strip()

            
            if not descricao:
                messagebox.showerror(
                    'Erro',
                    'A descrição não pode estar vazia.'
                )
                return
            
            data_digitada = entrada_data.get().strip()
            data = validar_data(data_digitada)

            if data is None:
                return
            
            mov = listar_movimentacoes()[indice_em_edicao]
            mov['valor'] = valor
            mov['descricao'] = descricao
            mov['data'] = data

            ordenar_movimentacoes()
            salvar_dados()

            indice_em_edicao = None

            entrada_valor.delete(0, tk.END)
            entrada_desc.delete(0, tk.END)
            entrada_data.delete(0, tk.END)

            atualizar_lista()
            atualizar_saldos()

        except ValueError:
            messagebox.showerror(
                'Erro',
                'Digite um valor numérico válido.'
            )    

    # Frames campos
    tk.Label(frame_campos, text='Valor').pack(side=tk.LEFT, padx=5)
    entrada_valor = tk.Entry(frame_campos, width=10)
    entrada_valor.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_campos, text='Descrição').pack(side=tk.LEFT, padx=5)
    entrada_desc = tk.Entry(frame_campos, width=25)
    entrada_desc.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_campos, text='Data').pack(side=tk.LEFT, padx=5)
    entrada_data = tk.Entry(frame_campos, width=12)
    entrada_data.pack(side=tk.LEFT, padx=5)
    

    # Frames Filtros de mês e ano
    tk.Label(frame_filtro, text='Mês').pack(side=tk.LEFT, padx=5)
    entrada_mes = tk.Entry(frame_filtro, width=5)
    entrada_mes.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_filtro, text='Ano').pack(side=tk.LEFT, padx=5)
    entrada_ano = tk.Entry(frame_filtro, width=7)
    entrada_ano.pack(side=tk.LEFT, padx=5)

    # Resumo Mensal
    frame_resumo_mensal = tk.Frame(janela, bd=1, relief=tk.GROOVE)
    frame_resumo_mensal.pack(pady=10, padx=10, fill='x')

    label_mes_ano = tk.Label(frame_resumo_mensal, text='Resumo Mensal', font=('Segoe UI', 11, 'bold'))
    label_mes_ano.pack(anchor='w')

    label_receita_mes = tk.Label(frame_resumo_mensal, text='Receitas do mês: R$ 0.00')
    label_receita_mes.pack(anchor='w')
    label_despesa_mes = tk.Label(frame_resumo_mensal, text='Despesas do mês: R$ 0.00')
    label_despesa_mes.pack(anchor='w')

    label_saldo_mes = tk.Label(frame_resumo_mensal, text='Saldo do mês: R$ 0.00')
    label_saldo_mes.pack(anchor='w')

    # atualização automatica do resumo mensal ao filtrar
    def atualizar_resumo_mensal():
        hoje = datetime.now()
        mes = int(entrada_mes.get()) if entrada_mes.get().isdigit() else hoje.month
        ano = int(entrada_ano.get()) if entrada_ano.get().isdigit() else hoje.year

        resumo = calcular_resumo_mensal(mes, ano)

        if not resumo:
            receitas = despesas = saldo = 0
        else:
            receitas, despesas, saldo = resumo    

        label_mes_ano.config(text=f'Resumo Mensal - {mes:02d}/{ano}')
        label_receita_mes.config(text=f'Receitas do mês: R$ {receitas:.2f}')
        label_despesa_mes.config(text=f'Despesas do mês: R$ {despesas:.2f}')

        cor = 'green' if saldo >= 0 else 'red'
        label_saldo_mes.config(text=f'Saldo do mês: R$ {saldo:.2f}', fg=cor)

    # Função intermediaria
    def filtrar_e_atualizar():
        filtrar_movimentacoes()
        atualizar_resumo_mensal()

    # Botão filtrar
    botao_filtrar = tk.Button(
        frame_filtro,
        text='Filtrar',
        command=filtrar_e_atualizar
    )
    botao_filtrar.pack(side=tk.LEFT, padx=10)
 
    # Resultado do saldo
    resultado = tk.Label(janela, text='Saldo: 0')
    resultado.pack(pady=10)
    
    # Atualiza o saldo ao abrir
    atualizar_saldos()
    atualizar_resumo_mensal()


    # Funções auxiliares
    def atualizar_lista():
        lista_mov.delete(0, tk.END)

        for mov in listar_movimentacoes():
            data = mov.get('data', '---')
            texto = f"{mov['tipo'].capitalize()} | R$ {mov['valor']:.2f} | {mov['descricao']} | {data}"
            lista_mov.insert(tk.END, texto)

    # Criar lista (sem pack ainda)
    frame_lista = tk.Frame(janela)

    scrollbar = tk.Scrollbar(frame_lista)
    lista_mov = tk.Listbox(
        frame_lista,
        font=fonte_lista,
        fg='black',
        yscrollcommand=scrollbar.set,
        height=10          
    )
    scrollbar.config(command=lista_mov.yview)    

    # Atualiza lista ao abrir
    atualizar_lista()

    # Funções dos botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    def clicar_receita():
        try:
            valor = float(entrada_valor.get())
            descricao = entrada_desc.get()

            if not descricao:
                messagebox.showerror(
                    'Erro',
                    'A descricao não pode estar vazia'
                )
                return
            
            data_digitada = entrada_data.get().strip()
            data = validar_data(data_digitada)


            if data is None:
                return

            adicionar_receita(valor, descricao, data)
            atualizar_saldos()
            atualizar_lista()               

            
            if calcular_saldo() < 0:
                messagebox.showwarning('Atenção', 'Seu saldo está negativo!')   

            entrada_valor.delete(0, tk.END)
            entrada_desc.delete(0, tk.END)
            entrada_data.delete(0, tk.END)

           
        except ValueError:
            messagebox.showerror('Erro', 'Digite um valor numérico válido.')   
 

    def clicar_despesa():
        try:
            valor = float(entrada_valor.get())
            descricao = entrada_desc.get().strip()

            if not descricao:
                messagebox.showerror(
                    'Erro',
                    'A descricao não pode estar vazia'
                )
                return
            
            data_digitada = entrada_data.get().strip()
            data = validar_data(data_digitada)

            if data is None:
                return

            adicionar_despesa(valor, descricao, data)
            atualizar_saldos()
            atualizar_lista()


            if calcular_saldo() < 0:
                messagebox.showwarning('Atenção', 'Seu saldo está negativo!')

            entrada_valor.delete(0, tk.END)
            entrada_desc.delete(0, tk.END)
            entrada_data.delete(0, tk.END)

        
        except ValueError:
            messagebox.showerror('Erro', 'Digite um valor numérico válido.')    

    def clicar_excluir():
        selecionado = lista_mov.curselection()

        if not selecionado:
            messagebox.showwarning(
                'Aviso',
                'Selecione uma movimentação para excluir.'
            )
            return
        
        confirmar = messagebox.askyesno(
            'Confirmar exclusão',
            'Tem certeza que deseja excluir esta movimentação?'
        )

        if not confirmar:
            return
        
        indice = selecionado[0]

        remover_movimentacao(indice)
        atualizar_lista()       
        atualizar_saldos()
       

    # Frames dos botões principais
    frame_botoes_principais = tk.Frame(janela)
    frame_botoes_principais.pack(pady=5)

    botao_receita = tk.Button(
        frame_botoes_principais,
        text='Adicionar Receita',
        width=18,
        command=clicar_receita
    )
    botao_receita.pack(side=tk.LEFT, padx=5)

    botao_despesa = tk.Button(
        frame_botoes_principais,
        text='Adicionar Despesa',
        width=18,
        command=clicar_despesa
    )
    botao_despesa.pack(side=tk.LEFT, padx=5)

    botao_editar = tk.Button(
        frame_botoes_principais,
        text='Editar Movimentação',
        width=18,
        command=clicar_editar
    )
    botao_editar.pack(side=tk.LEFT, padx=5)

    botao_salvar = tk.Button(
        frame_botoes_principais,
        text='Salvar Edição',
        width=18,
        command=clicar_salvar_edicao
    )
    botao_salvar.pack(side=tk.LEFT, padx=5)

    # exibir lista
    frame_lista.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    lista_mov.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Botão excluir
    frame_excluir = tk.Frame(janela)
    frame_excluir.pack(pady=5)

    botao_excluir = tk.Button(
        frame_excluir,
        text='Excluir Movimentação',
        fg='red',
        command=clicar_excluir
    )
    botao_excluir.pack()

  
    #Loop principal
    janela.mainloop()    

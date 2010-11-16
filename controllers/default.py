# -*- coding: utf-8 -*- 
#from http import redirect
largura_grid = 900
largura_col = 150

def index():
    if auth.is_logged_in():
        usuario = db.auth_user[auth.user.id]
        if usuario.area_cliente:
            redirect(URL(r=request,c='cliente',f='index'))
        projetos = crud.select(db.projeto_consultoria,query=db.projeto_consultoria.encerrado==False,fields=['projeto_consultoria.id','projeto_consultoria.cliente'])
        atividades = crud.select(db.atividade,query=db.atividade.concluido<100)
        contas_pagar = crud.select(db.conta_a_pagar,query=db.conta_a_pagar.paga==False,orderby=db.conta_a_pagar.vencimento,
                                   fields=['conta_a_pagar.id','conta_a_pagar.fornecedor',
                                           'conta_a_pagar.vencimento'])
        contas_receber = crud.select(db.conta_a_receber,query=db.conta_a_receber.recebida==False,orderby=db.conta_a_receber.vencimento,
                                   fields=['conta_a_receber.id','conta_a_receber.cliente',
                                           'conta_a_receber.vencimento'])
        return dict(projetos=projetos,atividades=atividades,contas_pagar=contas_pagar,contas_receber=contas_receber)
    else:
        return dict(message='Benvindo a Intranet Anima!')

def cidades():
    from gluon.contrib import simplejson as sj
    rows = db(db.cidade.uf == request.vars.uf).select(db.cidade.id, db.cidade.nome).as_list()
    return sj.dumps(rows)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if len(request.args) > 0:
        if request.args[0] == 'profile':
            response.subtitle = 'Editar perfil de %s' % auth.user.first_name
        elif request.args[0] == 'change_password':
            response.subtitle = 'Trocar Senha'
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    #session.forget()
    return service()

def data():
    return dict(form=crud())

def menu():
    response.subtitle = 'Menu'
    response.view = 'todos_novo.html'
    form = crud.create(db.menu)
    grid = plugin_jqgrid(db.menu, col_width=largura_col, width=largura_grid)
    return dict(form=form,grid=grid)

def editar_menu():
    response.subtitle = 'Editar Menu'
    response.view = 'simple_form.html'
    form = crud.update(db.menu, request.args(0))
    return dict(form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def parceiro():
    response.subtitle = 'Parceiro'
    form = crud.create(db.parceiro)
    grid = plugin_jqgrid(db.parceiro, col_width=largura_col, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_parceiro():
    response.subtitle = 'Editar Parceiro'
    form = crud.update(db.parceiro, request.args(0), next=URL(r=request, c='default', f='parceiro'))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def contato():
    response.subtitle = 'Contato'
    response.view = 'todos_novo.html'
    db.auth_user.admin.readable=db.auth_user.admin.writable=False
    form = crud.create(db.auth_user)
    grid = plugin_jqgrid(db.auth_user, 'admin', False,width=largura_grid, col_width=largura_col)
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_contato():
    response.subtitle = 'Editar Contato'
    response.view = 'simple_form.html'
    db.auth_user.admin.writable=db.auth_user.admin.readable=False
    form = crud.update(db.auth_user, request.args(0)) 
    return dict(title='Editar Contato', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def grupo():
    response.subtitle = 'Grupo'
    response.view = 'todos_novo.html'
    form = crud.create(db.grupo)
    grid = plugin_jqgrid(db.grupo, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_grupo():
    response.subtitle = 'Editar Grupo'
    response.view = 'simple_form.html'
    form = crud.update(db.grupo, request.args(0), next=URL(r=request, c='default', f='grupo')) 
    return dict(title='Editar Grupo', form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def participacao():
    response.subtitle = 'Participação'
    response.view = 'todos_novo.html'
    form = crud.create(db.participacao)
    grid = plugin_jqgrid(db.participacao, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_participacao():
    response.subtitle = 'Editar Participação'
    response.view = 'simple_form.html'
    form = crud.update(db.participacao, request.args(0), next=URL(r=request, c='default', f='participacao')) 
    return dict(title='Editar Agrupamento', form=form)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def log():
    response.subtitle = 'Log'
    response.view = 'todos_novo.html'
    form = crud.create(db.log)
    grid = plugin_jqgrid(db.log, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def usuario():
    response.subtitle = 'Usuários'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_user)
    grid = plugin_jqgrid(db.auth_user, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def auth_group():
    response.subtitle = 'Grupos'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_group)
    grid = plugin_jqgrid(db.auth_group, width=largura_grid)  
    return dict(form=form, grid=grid)

def editar_auth_group():
    response.subtitle = 'Editar Grupo'
    response.view = 'simple_form.html'
    form = crud.update(db.auth_group, request.args(0))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def auth_membership():
    response.subtitle = 'Papéis'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_membership)
    grid = plugin_jqgrid(db.auth_membership, width=largura_grid)  
    return dict(form=form, grid=grid) 

#
# Fluxo de Caixa

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def movimento_caixa():
    response.subtitle = 'Entrada/Saída do Caixa'
    response.view = 'todos_novo.html'
    form = crud.create(db.caixa)
    grid = plugin_jqgrid(db.caixa, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento():
    response.subtitle = 'Editar Entrada/Saída'
    response.view = 'simple_form.html'
    form = crud.update(db.caixa, request.args(0), next=URL(r=request, c='default', f='entrada')) 
    return dict(form=form)


def transferencia():
    response.subtitle = 'Transferência entre Contas'
    form = SQLFORM.factory(Field('montante', 'decimal', requires=IS_NOT_EMPTY()),
                           Field('conta_origem', db.conta, requires=IS_IN_DB(db, 'conta.id', '%(nome)s')),
                           Field('conta_destino', db.conta, requires=IS_IN_DB(db, 'conta.id', '%(nome)s')),
                           Field('obs', 'string')
                           )
    if form.accepts(request.vars, session):
        db.caixa.insert(conta=request.vars.conta_destino,
                          valor=request.vars.montante,
                          movimento='Entrada',
                          documento='Trans: %s' % request.vars.obs)
        db.caixa.insert(conta=request.vars.conta_origem,
                        valor=request.vars.montante,
                        movimento='Saída',
                        documento='Trans: %s' % request.vars.obs)
        response.flash = 'Transferência efetuada com sucesso.'
    elif form.errors:
        response.flash = 'Há erros no formulário.'
    response.view = 'simple_form.html'
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def conta():
    response.subtitle = 'Conta (plano de contas)'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta)
    grid = plugin_jqgrid(db.conta, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta():
    response.subtitle = 'Editar Conta'
    response.view = 'simple_form.html'
    form = crud.update(db.banco, request.args(0), next=URL(r=request, c='default', f='conta')) 
    return dict(title='Editar Conta', form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def categoria_entrada_saida():
    response.subtitle = 'Categoria de Entrada e Saída'
    response.view = 'todos_novo.html'
    form = crud.create(db.categoria_entrada_saida)
    grid = plugin_jqgrid(db.categoria_entrada_saida, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_categoria_entrada_saida():
    response.subtitle = 'Editar Categoria de Entradas e Saídas'
    response.view = 'simple_form.html'
    form = crud.update(db.categoria_entrada_saida, request.args(0), next=URL(r=request, c='default', f='categoria_entrada_saida')) 
    return dict(title='Editar Categorias de Entrada e Saída', form=form)

def tipo_documento():
    response.subtitle = 'Tipo Documento'
    response.view = 'todos_novo.html'
    form = crud.create(db.tipo_documento)
    grid = plugin_jqgrid(db.tipo_documento, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_tipo_documento():
    response.subtitle = 'Editar Tipo de Documento'
    response.view = 'simple_form.html'
    form = crud.update(db.tipo_documento, request.args(0), next=URL(r=request, c='default', f='tipo_documento')) 
    return dict(title='Editar Tipo de Documento', form=form)

def conta_a_pagar():
    response.subtitle = 'Conta a Pagar'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta_a_pagar)
    grid = plugin_jqgrid(db.conta_a_pagar, width=largura_grid, col_width=largura_col)
    db.conta_a_pagar.paga.writable = False  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta_a_pagar():
    response.subtitle = 'Editar Conta a Pagar'
    response.view = 'simple_form.html'
    form = crud.update(db.conta_a_pagar, request.args(0), next=URL(r=request, c='default', f='conta_a_pagar')) 
    return dict(title='Editar Conta a Pagar', form=form)

def conta_a_receber():
    response.subtitle = 'Conta a Receber'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta_a_receber)
    grid = plugin_jqgrid(db.conta_a_receber, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta_a_receber():
    response.subtitle = 'Editar Conta a Receber'
    response.view = 'simple_form.html'
    form = crud.update(db.conta_a_receber, request.args(0), next=URL(r=request, c='default', f='conta_a_receber')) 
    return dict(title='Editar Conta a Receber', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def pagar_conta():
    response.subtitle = 'Pagar Conta (baixa)'
    if request.args:
        conta = crud.read(db.conta_a_pagar, request.args[0])
        form = SQLFORM.factory(
                               Field('valor_pago', 'decimal', default=db.conta_a_pagar[request.args[0]].valor),
                               Field('data_pagamento', 'date', default=request.now),
                               Field('pagar_com', db.conta, requires=IS_IN_DB(db, 'conta.id', '%(nome)s')))
        if form.accepts(request.vars, session):
            db(db.conta_a_pagar.id == request.args[0]).update(paga=True,
                                                            data_pagamento=request.vars.data_pagamento,
                                                            valor=request.valor)
            db.caixa.insert(conta=request.vars.pagar_com,
                            documento=db.conta_a_pagar[request.args[0]].id,
                            valor=request.vars.valor_pago,
                            movimento='Saída',
                            data=request.vars.data_pagamento)
            session.flash = 'A conta foi paga!'
            return redirect(URL(r=request, args=[]))
        elif form.errors:
            response.flash = 'Há erros no formulário.'
            
    else:
        conta = 'Selecione um conta para pagar:'
        form = ''
    grid = plugin_jqgrid(db.conta_a_pagar, 'paga', False)
    return dict(conta=conta, form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def receber_conta():
    response.subtitle = 'Receber Conta (baixa)'
    if request.args:
        conta = crud.read(db.conta_a_receber, request.args[0])
        form = SQLFORM.factory(
                               Field('valor_recebido', 'decimal', default=db.conta_a_receber[request.args[0]].valor),
                               Field('data_recebimento', 'date', default=request.now),
                               Field('receber_em', db.conta, requires=IS_IN_DB(db, 'conta.id', '%(nome)s')))
        if form.accepts(request.vars, session):
            db(db.conta_a_receber.id == request.args[0]).update(recebida=True,
                                                              data_recebimento=request.vars.data_recebimento,
                                                              valor=request.vars.valor)
            db.caixa.insert(conta=request.vars.receber_em,
                            documento=db.conta_a_receber[request.args[0]].id,
                            valor=request.vars.valor_recebido,
                            data=request.vars.data_recebimento)
            session.flash = 'Conta recebida!'
            return redirect(URL(r=request, args=[])) 
        elif form.errors:
            response.flash = 'Há erros no formulário.'
    else:
        conta = 'Selecione um conta para receber:'
        form = ''
    grid = plugin_jqgrid(db.conta_a_receber, 'recebida', False)
    return dict(conta=conta, form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def banco():
    response.subtitle = 'Banco'
    response.view = 'todos_novo.html'
    form = crud.create(db.banco)
    grid = plugin_jqgrid(db.banco, width=largura_grid)  
    return dict(form=form, grid=grid)

def editar_banco():
    response.subtitle = 'Editar Banco'
    response.view = 'simple_form.html'
    form = crud.update(db.banco, request.args(0), next=URL(r=request, c='default', f='banco')) 
    return dict(title='Editar Banco', form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def item_almoxarifado():
    response.subtitle = 'Item do Almoxarifado'
    response.view = 'todos_novo.html'
    form = crud.create(db.item_almoxarifado)
    grid = plugin_jqgrid(db.item_almoxarifado, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_item_almoxarifado():
    response.subtitle = 'Editar Item do Almoxarifado'
    response.view = 'simple_form.html'
    form = crud.update(db.item_almoxarifado, request.args(0), next=URL(r=request, c='default', f='item_almoxarifado')) 
    return dict(title='Editar Item do Almoxarifado', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def movimento_almoxarifado():
    response.subtitle = 'Movimento do Almoxarifado'
    response.view = 'todos_novo.html'
    form = crud.create(db.movimento_almoxarifado)
    grid = plugin_jqgrid(db.movimento_almoxarifado, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento_almoxarifado():
    response.subtitle = 'Editar Movimento do Almoxarifado'
    response.view = 'simple_form.html'
    form = crud.update(db.movimento_almoxarifado, request.args(0), next=URL(r=request, c='default', f='movimento_almoxarifado')) 
    return dict(title='Editar Almoxarifado', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def produto():
    response.subtitle = 'Produto'
    response.view = 'todos_novo.html'
    response.subtitle = 'Produto'
    form = crud.create(db.produto)
    grid = plugin_jqgrid(db.produto, width=largura_grid, col_width=200)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_produto():
    response.subtitle = 'Editar Produto'
    id = request.args(0)
    form = crud.update(db.produto, id, next=URL(r=request, c='default', f='produto'))
    entradas = db((db.movimento_estoque.produto == id) & 
                      (db.movimento_estoque.movimento == 'Entrada')).select(db.movimento_estoque.quantidade.sum())
    entradas_soma = 0
    if entradas[0]._extra[db.movimento_estoque.quantidade.sum()]:
        entradas_soma = entradas[0]._extra[db.movimento_estoque.quantidade.sum()]
    saidas = db((db.movimento_estoque.produto == id) & 
                      (db.movimento_estoque.movimento == 'Saída')).select(db.movimento_estoque.quantidade.sum())
    saidas_soma = 0
    if saidas[0]._extra[db.movimento_estoque.quantidade.sum()]:
        saidas_soma = saidas[0]._extra[db.movimento_estoque.quantidade.sum()]
    total_estoque = entradas_soma - saidas_soma 
    return dict(title='Editar Produto', form=form, total_estoque=total_estoque)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def movimento_estoque():
    response.subtitle = 'Movimento de Estoque'
    response.view = 'todos_novo.html'
    form = crud.create(db.movimento_estoque)
    grid = plugin_jqgrid(db.movimento_estoque, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento_estoque():
    response.subtitle = 'Editar Movimento de Estoque'
    response.view = 'simple_form.html'
    form = crud.update(db.movimento_estoque, request.args(0), next=URL(r=request, c='default', f='movimento_estoque')) 
    return dict(title='Editar Estoque', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )

def unidade():
    response.subtitle = 'Unidade'
    response.view = 'todos_novo.html'
    form = crud.create(db.unidade)
    grid = plugin_jqgrid(db.unidade, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_unidade():
    response.subtitle = 'Editar Unidade'
    response.view = 'simple_form.html'
    form = crud.update(db.unidade, request.args(0), next=URL(r=request, c='default', f='unidade')) 
    return dict(title='Editar Unidade', form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def funcionario():
    response.subtitle = 'Fucionário'
    response.view = 'todos_novo.html'
    form = crud.create(db.funcionario)
    grid = plugin_jqgrid(db.funcionario, width=largura_grid)  
    return dict(form=form, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_funcionario():
    response.subtitle = 'Editar Funcionário'
    response.view = 'simple_form.html'
    form = crud.update(db.funcionario, request.args(0), next=URL(r=request, c='default', f='funcionario')) 
    return dict(title='Editar Funcionário', form=form)


# relatórios
@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_fluxo_caixa_conta():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório Fluxo de Caixa por Conta'
    response.view = 'relatorio.html'
    
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('conta',db.conta,label='Conta', 
                                 requires=IS_IN_DB(db,'conta.id','%(nome)s')), 
                        submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_fluxo_caixa.pd')
    if request.extension=='pd' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        fluxo = db((db.caixa.data >= data_ini) & 
                   (db.caixa.data <= data_fim) &
                   (db.caixa.conta == request.vars.conta)).select(db.caixa.conta,
                                                       db.caixa.data,
                                                       db.caixa.documento,
                                                       db.caixa.movimento,
                                                       db.caixa.valor,
                                                       groupby=db.caixa.data|db.caixa.movimento)
        tbl = report.ReportTable(rows=fluxo,
                      grouping={'field':'caixa.data', 'function': lambda row: row.data.month},
                      sumary={'caixa.valor': lambda row,v: (v-row.valor,v+row.valor)[row.movimento=='Entrada'],
                              'caixa.movimento':lambda row,v: 'Subtotal:',
                              'caixa.id':lambda row,v: 'Movimentos:',
                              'caixa.conta':lambda row,v: v+1},
                     footer={'caixa.valor': lambda row,v: (v-row.valor,v+row.valor)[row.movimento=='Entrada'],
                             'caixa.movimento':lambda row,v: 'Total:',
                             'caixa.id':lambda row,v: 'Movimentos:',
                             'caixa.conta':lambda row,v: v+1},
                     col_widths=[15,11,50,10,10],   
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           return dict(form=form, rel=tbl.generate(),pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_fluxo_caixa():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório Fluxo de Caixa'
    response.view = 'relatorio.html'
    
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                                 submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_fluxo_caixa.pd',
                      submit_button='Enviar')
    if request.extension=='pd' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        fluxo = db((db.caixa.data >= data_ini) & 
                   (db.caixa.data <= data_fim)).select(db.caixa.conta,
                                                       db.caixa.data,
                                                       db.caixa.documento,
                                                       db.caixa.movimento,
                                                       db.caixa.valor,
                                                       groupby=db.caixa.data|db.caixa.movimento)
        tbl = report.ReportTable(rows=fluxo,
                      grouping={'field':'caixa.data', 'function': lambda row: row.data.month},
                      sumary={'caixa.valor': lambda row,v: (v-row.valor,v+row.valor)[row.movimento=='Entrada'],
                              'caixa.movimento':lambda row,v: 'Subtotal:',
                              'caixa.id':lambda row,v: 'Movimentos:',
                              'caixa.conta':lambda row,v: v+1},
                     footer={'caixa.valor': lambda row,v: (v-row.valor,v+row.valor)[row.movimento=='Entrada'],
                             'caixa.movimento':lambda row,v: 'Total:',
                             'caixa.id':lambda row,v: 'Movimentos:',
                             'caixa.conta':lambda row,v: v+1},
                     col_widths=[15,11,50,10,10],   
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           return dict(form=form, rel=tbl.generate(),pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_contas_pagar():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Contas a Pagar'
    response.view = 'relatorio.html'
    
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                                 submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_fluxo_caixa.pd')
    if request.extension=='pd' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        rel = db((db.conta_a_pagar.vencimento >= data_ini) & 
                   (db.conta_a_pagar.vencimento <= data_fim)).select(db.conta_a_pagar.fornecedor,
                                                       db.conta_a_pagar.vencimento,
                                                       db.conta_a_pagar.descricao,
                                                       db.conta_a_pagar.valor,
                                                       groupby=db.conta_a_pagar.vencimento|
                                                               db.conta_a_pagar.fornecedor)
        tbl = report.ReportTable(rows=rel,
                      grouping={'field':'conta_a_pagar.vencimento', 'function': lambda row: row.vencimento.month},
                      sumary={'conta_a_pagar.valor': lambda row,v: v+row.valor,
                             },
                     footer={'conta_a_pagar.valor': lambda row,v: v+row.valor,
                             },
                     col_widths=[25,25,25,25],   
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           return dict(form=form, rel=tbl.generate(),pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_contas_receber():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Contas a Receber'
    response.view = 'relatorio.html'
    
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                                 submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_fluxo_caixa.pd')
    if request.extension=='pd' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        rel = db((db.conta_a_receber.vencimento >= data_ini) & 
                   (db.conta_a_receber.vencimento <= data_fim)).select(db.conta_a_receber.cliente,
                                                       db.conta_a_receber.vencimento,
                                                       db.conta_a_receber.descricao,
                                                       db.conta_a_receber.valor,
                                                       groupby=db.conta_a_receber.vencimento|
                                                               db.conta_a_receber.cliente)
        tbl = report.ReportTable(rows=rel,
                      grouping={'field':'conta_a_receber.vencimento', 'function': lambda row: row.vencimento.month},
                      sumary={'conta_a_receber.valor': lambda row,v: v+row.valor,
                             },
                     footer={'conta_a_receber.valor': lambda row,v: v+row.valor,
                             },
                     col_widths=[25,25,25,25],   
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           return dict(form=form, rel=tbl.generate(),pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)
   
@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_status_almoxarifado():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Status do Almoxarifado'
    response.view = 'relatorio.html'
    
    rel = db(db.movimento_almoxarifado.item==db.item_almoxarifado.id).select(db.item_almoxarifado.descricao,
                                                                             db.movimento_almoxarifado.data,
                                                                             db.movimento_almoxarifado.movimento,
                                                                             db.movimento_almoxarifado.quantidade,
                                                                             )
    tbl = report.ReportTable(rows=rel,
                  grouping={'field':'item_almoxarifado.descricao', 'function': lambda row: row['item_almoxarifado'].descricao},
                  sumary={'movimento_almoxarifado.quantidade': lambda row,v: (v-row['movimento_almoxarifado'].quantidade,v+row['movimento_almoxarifado'].quantidade)[row['movimento_almoxarifado'].movimento=='Entrada'],
                          'item_almoxarifado.descricao': lambda row,v: row.item_almoxarifado.descricao,
                          'movimento_almoxarifado.data': lambda row,v: '-',
                          'movimento_almoxarifado.movimento': lambda row,v: '-',
                         },
                 footer={'movimento_almoxarifado.quantidade': lambda row,v: (v-row['movimento_almoxarifado'].quantidade,v+row['movimento_almoxarifado'].quantidade)[row['movimento_almoxarifado'].movimento=='Entrada'],
                         },
                 col_widths=[20,20,20,20,20],   
                 truncate=50              
                )
    pdf_link = A(TAG.button('PDF'),_href=URL(r=request,extension='pdf'))
    if request.extension=='pdf':
        pdf = Relatorio()
        pdf.add_page()
        pdf.write_html(tbl.generate().xml().decode('UTF-8'))
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
       rel = tbl.generate()
       rel = TABLE(tbl._header,tbl._summaries)
       return dict(form='',rel=rel,pdf_link=pdf_link)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_status_estoque():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Status do Estoque'
    response.view = 'relatorio.html'
    
    rel = db((db.movimento_estoque.produto==db.produto.id) &
              (db.produto.descontinuado==False)).select(db.produto.descricao,
                                                                             db.movimento_estoque.data,
                                                                             db.movimento_estoque.movimento,
                                                                             db.movimento_estoque.quantidade,
                                                                             )
    tbl = report.ReportTable(rows=rel,
                  grouping={'field':'produto.descricao', 'function': lambda row: row['produto'].descricao},
                  sumary={'movimento_estoque.quantidade': lambda row,v: (v-row['movimento_estoque'].quantidade,v+row['movimento_estoque'].quantidade)[row['movimento_estoque'].movimento=='Entrada'],
                          'produto.descricao': lambda row,v: row.produto.descricao,
                          'movimento_estoque.data': lambda row,v: '-',
                          'movimento_estoque.movimento': lambda row,v: '-',
                         },
                 footer={'movimento_estoque.quantidade': lambda row,v: (v-row['movimento_estoque'].quantidade,v+row['movimento_estoque'].quantidade)[row['movimento_estoque'].movimento=='Entrada'],
                         },
                 col_widths=[20,20,20,20,20],   
                 truncate=50              
                )
    pdf_link = A(TAG.button('PDF'),_href=URL(r=request,extension='pdf'))
    if request.extension=='pdf':
        pdf = Relatorio()
        pdf.add_page()
        pdf.write_html(tbl.generate().xml().decode('UTF-8'))
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
       rel = tbl.generate()
       rel = TABLE(tbl._header,tbl._summaries)
       return dict(form='',rel=rel,pdf_link=pdf_link)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def rel_extrato_estoque():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Extrato do Estoque'
    response.view = 'relatorio.html'
    
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                                 submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_fluxo_caixa.pd')
    if request.extension=='pdf' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        rel = db((db.movimento_estoque.data >= data_ini) & 
                 (db.movimento_estoque.data <= data_fim) &
                 (db.movimento_estoque.produto==db.produto.id)).select(db.produto.descricao,
                                                                       db.movimento_estoque.data,
                                                                       db.movimento_estoque.quantidade,
                                                                       db.movimento_estoque.movimento,
                                                                       db.movimento_estoque.preco,
                                                       )
        print rel
        tbl = report.ReportTable(rows=rel,
                      grouping={'field':'produto.descricao', 'function': lambda row: row.produto.descricao},
                      sumary={'movimento_estoque.movimento': lambda row,v: 'Lucro bruto',
                              'movimento_estoque.preco': lambda row,v: (v+row.movimento_estoque.preco*row.movimento_estoque.quantidade,v-row.movimento_estoque.preco*row.movimento_estoque.quantidade)[row.movimento_estoque.movimento=='Entrada']
                             },
                     footer={
                             },
                     col_widths=[20,20,20,20,20],   
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           rel = tbl.generate()
           #rel = TABLE(tbl._summaries)
           return dict(form=form, rel=rel,pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)

   
   

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def saldo():
    response.subtitle = 'Saldos'
    contas = db(db.conta.id > 0).select()
    saldos = []
    for conta in contas:
            entradas = db((db.caixa.conta == conta.id) and (db.caixa.movimento == 'Entrada')).select(db.caixa.valor.sum())
            if entradas[0]._extra[db.caixa.valor.sum()]:
                entradas_soma = entradas[0]._extra[db.caixa.valor.sum()]
            else:
                entradas_soma = 0
            saidas = db((db.caixa.conta == conta.id) and (db.caixa.movimento == 'Saída')).select(db.caixa.valor.sum())
            if saidas[0]._extra[db.caixa.valor.sum()]:
                saidas_soma = saidas[0]._extra[db.caixa.valor.sum()]
            else:
                saidas_soma = 0
            saldos.append([conta.nome, entradas_soma - saidas_soma])
    return dict(saldos=saldos)

#
# Consultoria
#

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def modelo_proposta():
    form = crud.create(db.modelo_proposta)
    grid = plugin_jqgrid(db.modelo_proposta, col_width=largura_col,width=largura_grid)
    campos = db.proposta.fields
    return dict(grid=grid, form=form, campos=campos)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_modelo_proposta():
    response.subtitle = 'Editando modelo de proposta'
    if len(request.args) == 0:
        session.flash = 'Selecione um modelo de proposta para editar.'
        return redirect(URL(r=request, f='modelo_proposta'))
    proposta = db.modelo_proposta[request.args[0]]
    if not proposta:
        session.flash = 'Selecione um modelo de proposta para editar.'
        return redirect(URL(r=request, f='modelo_proposta'))
    form = crud.update(db.modelo_proposta, request.args[0], next=URL(r=request, c='default', f='modelo_proposta'))
    campos = db.proposta.fields
    return dict(form=form,campos=campos)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def modelo_contrato():
    form = crud.create(db.modelo_contrato)
    grid = plugin_jqgrid(db.modelo_contrato, width=700)
    return dict(grid=grid, form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_modelo_contrato():
    if len(request.args) == 0:
        session.flash = 'Selecione um modelo de contrato para editar.'
        return redirect(URL(r=request, f='modelo_contrato'))
    contrato = db.modelo_contrato[request.args[0]]
    if not contrato:
        session.flash = 'Selecione um modelo de contrato para editar.'
        return redirect(URL(r=request, f='modelo_contrato'))
    form = crud.update(db.modelo_contrato, request.args[0], next=URL(r=request, c='default', f='modelo_contrato'))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def projeto():
    db.projeto_consultoria.diagnostico_alfa.writable = db.projeto_consultoria.diagnostico_alfa.readable= False
    db.projeto_consultoria.diagnostico_beta.writable = db.projeto_consultoria.diagnostico_beta.readable=False
    db.projeto_consultoria.diagnostico_gama.writable = db.projeto_consultoria.diagnostico_gama.readable=False
    db.projeto_consultoria.encerrado.writable = db.projeto_consultoria.encerrado.readable=False
    form = crud.create(db.projeto_consultoria)
    return dict(form=form, grid=plugin_jqgrid(db.projeto_consultoria,col_width=largura_col, width=largura_grid))

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_diag_alfa():
    form = crud.update(db.diagnostico_alfa, request.args(0), deletable=False)
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_diag_beta():
    form = crud.update(db.diagnostico_beta, request.args(0), deletable=False)
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_diag_gama():
    form = crud.update(db.diagnostico_gama, request.args(0), deletable=False)
#    form = SQLFORM(db.diagnostico_gama, record=request.args(0),fields=db.diagnostico_gama.fields, submit_button='Enviar' )
#    if form.accepts(request.vars,session):
#        response.headers['web2py-component-flash'] = 'Registro salvo.'
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def diag_gama_pontos():
    pontos = db(db.diagnostico_gama.id==request.args(0)).select(db.diagnostico_gama.lideranca_pontos,
                                                                db.diagnostico_gama.estrategia_planos_pontos,
                                                                db.diagnostico_gama.clientes_pontos,
                                                                db.diagnostico_gama.resp_social_pontos,
                                                                db.diagnostico_gama.info_conhecimento_pontos,
                                                                db.diagnostico_gama.pessoas_pontos,
                                                                db.diagnostico_gama.processo_pontos,
                                                                db.diagnostico_gama.resultados_pontos).first()
    return dict(pontos=pontos)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_projeto():
    if len(request.args) == 0:
        session.flash = 'Selecione um projeto para editar.'
        return redirect(URL(r=request, f='projeto'))
    
    #verifica se o projeto tem um diag. alfa e cria
    if db.projeto_consultoria[request.args(0)].diagnostico_alfa == None:
        alfa = db.diagnostico_alfa.insert()
        db.projeto_consultoria[request.args(0)].update_record(diagnostico_alfa=alfa)
        
    #verifica se o projeto tem um diag. alfa e cria
    if db.projeto_consultoria[request.args(0)].diagnostico_beta == None:
        beta = db.diagnostico_beta.insert()
        db.projeto_consultoria[request.args(0)].update_record(diagnostico_beta=beta)
    
    #verifica se o projeto tem um diag. gama e cria
    if db.projeto_consultoria[request.args(0)].diagnostico_gama == None:
        gama = db.diagnostico_gama.insert()
        db.projeto_consultoria[request.args(0)].update_record(diagnostico_gama=gama)
    
    projeto = db.projeto_consultoria[request.args[0]]
    response.subtitle = 'Projeto #%(id)s - Cliente:%(cliente)s' %{'id':request.args(0),'cliente':db.parceiro[projeto.cliente].nome}
    if not projeto:
        session.flash = 'Selecione um projeto para editar.'
        return redirect(URL(r=request, f='projeto'))
    propostas = plugin_jqgrid(db.proposta, 'projeto', projeto.id,col_width=largura_col, width=largura_grid)
    contratos = plugin_jqgrid(db.contrato, 'projeto', projeto.id,col_width=largura_col, width=largura_grid)
    planos = plugin_jqgrid(db.plano_acao,'projeto',projeto.id,col_width=largura_col, width=largura_grid)
    registros_info = plugin_jqgrid(db.registro_info,'projeto',projeto.id,col_width=largura_col, width=largura_grid)
    plan_estrategico = plugin_jqgrid(db.planejamento_estrategico,'projeto',projeto.id,col_width=largura_col, width=largura_grid)
    proposta = db(db.proposta.aprovada == True).select()
    proposta_aprovada = None
    contrato = None
    contrato_fechado = None
    if len(proposta) > 0:
        proposta_aprovada = proposta[0]
        contrato = db(db.contrato.proposta == proposta_aprovada.id).select()
        if len(contrato) > 0:
            contrato_fechado = contrato[0]
    db.projeto_consultoria.diagnostico_alfa.writable=db.projeto_consultoria.diagnostico_alfa.readable=False
    db.projeto_consultoria.diagnostico_beta.writable=db.projeto_consultoria.diagnostico_beta.readable=False
    db.projeto_consultoria.diagnostico_gama.writable=db.projeto_consultoria.diagnostico_gama.readable=False
    db.projeto_consultoria.cliente.writable=False
    form = crud.update(db.projeto_consultoria,projeto.id,deletable=False)
    return dict(projeto=projeto, propostas=propostas, contratos=contratos, proposta_aprovada=proposta_aprovada, contrato_fechado=contrato_fechado,planos=planos,registros_info=registros_info,plan_estrategico=plan_estrategico,form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_proposta():
    def aprovar(form):
        if form.vars.aprovada:
            db(db.proposta.aprovada == True).update(aprovada=False)
            db(db.proposta.id == request.args(0)).update(aprovada=True)
            response.flash = 'A proposta foi aprovada!'
    response.subtitle = 'Editando proposta %(id)s' %{'id':request.args(0)}
    proposta = db.proposta[request.args(0)]
    db.proposta.projeto.writable = False
    form = crud.update(db.proposta, proposta.id,
                     next=URL(r=request, c='default', f='editar_projeto', args=proposta.projeto),
                     onaccept=aprovar)
    return dict(form=form, proposta=proposta)
    
@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def novo_projeto():
    db.projeto_consultoria.contrato.writable = False
    db.projeto_consultoria.contrato.readable = False
    form = crud.create(db.projeto_consultoria, next=URL(r=request, f='projeto'))
    return dict(form=form)

        
@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def criar_proposta():
    if request.args:
        projeto = db.projeto_consultoria[request.args[0]]
    else:
        session.flash = 'Selecione um projeto para criar uma proposta.'
        return redirect(URL(r=request, f='projeto'))
    db.proposta.projeto.default = projeto.id
    db.proposta.projeto.writable = False
    form = crud.create(db.proposta, next='editar_proposta/[id]')
    return dict(projeto=projeto, form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master() or
               auth.has_membership(auth.id_group('cliente'))
               )
def visualizar_proposta():
    from gluon import template 
    proposta = db.proposta[request.args(0)]
    contrato = db(db.contrato.proposta==proposta.id).select().first()
    modelo_template = db.modelo_proposta[proposta.modelo].modelo
    try:
        rel = template.render(content=modelo_template,context=dict(proposta=proposta,contrato=contrato),delimiters=('[[',']]'))
    except Exception, e:
        session.flash = SPAN(P('Erro ao processar modelo. Confira a sintaxe.'),
                             P(proposta.as_dict()),
                             P(e))
        return redirect(URL(r=request,f='editar_projeto',args=proposta.projeto))
    return dict(rel=XML(rel))

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def visualizar_contrato():
    from gluon import template 
    contrato = db.contrato[request.args(0)]
    modelo_template = contrato.modelo.modelo
    try:
        rel = template.render(content=modelo_template,context=dict(contrato=contrato,extenso=extenso),delimiters=('[[',']]'))
    except Exception, e:
        session.flash = SPAN(P('Erro ao processar modelo. Confira a sintaxe.'),
                             P(contrato.as_dict()),
                             P(e))
        return redirect(URL(r=request,f='editar_projeto',args=contrato.projeto))
    return dict(rel=XML(rel))
    

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def criar_contrato():
    if request.args:
        projeto = db.projeto_consultoria[request.args[0]]
    else:
        session.flash = 'Selecione um projeto para criar um contrato.'
        return redirect(URL(r=request, f='projeto'))
    proposta_aprovada = db(db.proposta.aprovada == True).select()
    if len(proposta_aprovada) != 1:
        session.flash = 'Primeiro deve você ter uma proposta aprovada!'
        return redirect(URL(r=request, c='default', f='editar_projeto', args=request.args(0)))
    db.contrato.projeto.default = projeto.id
    db.contrato.projeto.writable = False
    db.contrato.proposta.default = proposta_aprovada[0].id
    db.contrato.proposta.writable = False
    form = crud.create(db.contrato, next=URL(r=request, c='default', f='editar_projeto', args=request.args(0)))
    return dict(projeto=projeto, form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_contrato():
    response.subtitle = 'Contrato'
    response.view = 'simple_form.html'
    db.contrato.projeto.writable = False
    db.contrato.proposta.writable = False
    contrato = db.contrato[request.args(0)]
    form = crud.update(db.contrato, contrato.id,
                     next=URL(r=request, c='default', f='editar_projeto', args=contrato.projeto),
                     )
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_cenario():
    db.cenario.proposta.writable = db.cenario.proposta.readable = False
    if request.args(1):
        form = crud.update(db.cenario,request.args(1),next=URL(r=request,args=request.args(0)))
    else:
        db.cenario.proposta.default = request.args(0)
        form = crud.create(db.cenario,next=URL(r=request,args=request.args(0)))
    db.cenario.id.represent = lambda id: A('Editar',_href=URL(r=request,args=[request.args(0),id]),cid='cen')
    cen= db(db.cenario.proposta==request.args(0)).select()
    cenario = SQLTABLE(cen,
                          headers={'cenario.id':'','cenario.item_cenario':'Item'},
                          columns=['cenario.id','cenario.item_cenario'],
                          truncate='30')
    return dict(form=form, cenario=cenario)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def categoria_cenario():
    form = crud.create(db.categoria_cenario)
    categorias = plugin_jqgrid(db.categoria_cenario, col_width=largura_col, width=largura_grid)
    return dict(form=form, grid=categorias)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_categoria_cenario():
    form = crud.update(db.categoria_cenario, request.args(0))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def item_cenario():
    db.item_cenario.categoria.default = request.args(0)
    db.item_cenario.categoria.writable = db.item_cenario.categoria.readable = False
    form_itens = crud.create(db.item_cenario)
    grid = plugin_jqgrid(db.item_cenario, 'categoria', request.args(0),col_width=largura_col, width=largura_grid)
    return dict(form=form_itens, grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def plano_acao():
    response.subtitle = 'Novo Plano de Ação'
    response.view = 'simple_form.html'
    db.plano_acao.projeto.default = request.args(0)
    db.plano_acao.projeto.writable = False
    form = crud.create(db.plano_acao,next='editar_plano_acao/[id]')
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_plano_acao():
    response.subtitle = 'Editar Plano de Ação'
    db.plano_acao.projeto.writable = False
    form = crud.update(db.plano_acao,request.args(0),next='editar_projeto/%i' % db.plano_acao[request.args(0)].projeto)
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_atividades():    
    db.atividade.plano_acao.writable = db.atividade.plano_acao.readable = False
    if request.args(1):
        form = crud.update(db.atividade,request.args(1),next=URL(r=request,args=request.args(0)))
    else:
        db.atividade.plano_acao.default = request.args(0)
        db.atividade.concluido.writable = db.atividade.concluido.readable = False
        form = crud.create(db.atividade)
    db.atividade.id.represent = lambda id: A('Editar',_href=URL(r=request,args=[request.args(0),id]),cid='atv')
    atv= db(db.atividade.plano_acao==request.args(0)).select()
    atividades = SQLTABLE(atv,
                          headers={'atividade.id':'','atividade.descricao':'Descrição','atividade.concluido':'Concluído'},
                          columns=['atividade.id','atividade.descricao','atividade.concluido'],
                          truncate='30')
    return dict(form=form,atividades=atividades)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def registro_info():
    response.subtitle = 'Registro de Informações'
    response.view = 'simple_form.html'
    db.registro_info.projeto.default = request.args(0)
    db.registro_info.projeto.writable = False
    db.registro_info.projeto.represent = lambda id: edicao(id,'/default/editar_projeto/')
    form = crud.create(db.registro_info,next=URL(r=request,f='editar_projeto',args=request.args(0)))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_registro_info():
    response.subtitle = 'Editar Registro de Informações'
    response.view = 'simple_form.html'
    db.registro_info.projeto.writable = False
    db.registro_info.projeto.represent = lambda id: edicao(id,'/default/editar_projeto/')
    form = crud.update(db.registro_info,request.args(0),next=URL(r=request,f='editar_projeto',args=db.registro_info[request.args(0)].projeto))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def planejamento_estrategico():
    response.subtitle = 'Planejamento Estratégico'
    response.view = 'simple_form.html'
    db.planejamento_estrategico.projeto.default = request.args(0)
    db.planejamento_estrategico.projeto.writable = False
    db.planejamento_estrategico.projeto.represent = lambda id: edicao(id,'/default/editar_projeto/')
    form = crud.create(db.planejamento_estrategico,next=URL(r=request,f='editar_projeto',args=request.args(0)))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_planejamento_estrategico():
    response.subtitle = 'Editar Planejamento Estratégico'
    response.view = 'simple_form.html'
    db.planejamento_estrategico.projeto.writable = False
    db.planejamento_estrategico.projeto.represent = lambda id: edicao(id,'/default/editar_projeto/')
    form = crud.update(db.planejamento_estrategico,request.args(0),next=URL(r=request,f='editar_projeto',args=db.planejamento_estrategico[request.args(0)].projeto))
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_setores():    
    db.setor.planejamento_estrategico.writable = False
    if request.args(1):
        form = crud.update(db.setor,request.args(1),next=URL(r=request,args=request.args(0)))
    else:
        db.setor.planejamento_estrategico.default = request.args(0)
        form = crud.create(db.setor)
    db.setor.id.represent = lambda id: A('Editar',_href=URL(r=request,args=[request.args(0),id]),cid='str')
    str= db(db.setor.planejamento_estrategico==request.args(0)).select()
    setores = SQLTABLE(str,
                          headers={'setor.id':'','setor.descricao':'Descrição','setor.atividades':'Atividades'},
                          columns=['setor.id','setor.descricao','setor.atividades'],
                          truncate='30')
    return dict(form=form,setores=setores)


    


def editor():
    return dict()
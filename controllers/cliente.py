# -*- coding: utf-8 -*-
#from http import redirect
largura_grid = 900
largura_col = 150

usuario = db(db.auth_user.id==auth.user.id).select().first()
projeto = None
if usuario.empresa:
    projeto = db((db.projeto_consultoria.cliente==usuario.empresa.id) &
                     (db.projeto_consultoria.encerrado==False)).select().first()

@auth.requires(usuario.area_cliente)
def index():
    if not usuario.empresa:
        response.flash = 'Você não está cadastrado em uma empresa no nosso sistema.'
        return dict(empresa=None,projeto='Nenhum',planos='Nenhum')
    elif not projeto:
        response.flash = 'Não há projeto em atividade.'
        return dict(empresa=usuario.empresa.nome,projeto='Nenhum',planos='Nenhum')
    else:
        db.plano_acao.id.represent = lambda id: edicao(id,'/cliente/plano/')
        db.plano_acao.projeto.represent = lambda id: id
        planos = db(db.plano_acao.quem==usuario.id)
        proposta = db((db.proposta.projeto==projeto.id) & (db.proposta.aprovada==True)).select().first()
        contrato = db(db.contrato.proposta==proposta.id).select().first()
        documentos = DIV()
        if usuario.visualiza_projeto:
            documentos.append(A(TAG.button('Proposta'),_href=URL(r=request,c='default',f='visualizar_proposta',args=proposta.id)))
            documentos.append(A(TAG.button('Contrato'),_href=URL(r=request,c='default',f='visualizar_contrato',args=contrato.id)))
            documentos.append(A(TAG.button('Diagnóstico Alfa'),_href=URL(r=request,c='cliente',f='visualizar_diag_alfa',args=projeto.diagnostico_alfa)))
            documentos.append(A(TAG.button('Diagnóstico Beta'),_href=URL(r=request,c='cliente',f='visualizar_diag_beta',args=projeto.diagnostico_beta)))
            documentos.append(A(TAG.button('Diagnóstico Gama'),_href=URL(r=request,c='cliente',f='visualizar_diag_gama',args=projeto.diagnostico_gama)))
            documentos.append(A(TAG.button('Pontos do Diagnóstico Gama'),_href=URL(r=request,c='cliente',f='visualizar_diag_gama_pontos',args=projeto.diagnostico_gama)))
            documentos.append(A(TAG.button('Registros de Informações'),_href=URL(r=request,c='cliente',f='registro_info')))
            documentos.append(A(TAG.button('Planejamento Estratégico'),_href=URL(r=request,c='cliente',f='planejamento',args=projeto.id)))
        else:
            documentos.append(SPAN('Você não tem permissão para visualizar documentos do projeto.'))
        return dict(empresa=usuario.empresa.nome,
                    projeto=documentos,
                    planos=crud.select(db.plano_acao,query=db.plano_acao.quem==usuario.id))

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_diag_alfa():
    response.view = 'simple_form.html'
    return dict(form=crud.read(db.diagnostico_alfa,request.args(0)))

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_diag_beta():
    response.view = 'simple_form.html'
    return dict(form=crud.read(db.diagnostico_beta,request.args(0)))

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_diag_gama():
    response.view = 'simple_form.html'
    return dict(form=crud.read(db.diagnostico_gama,request.args(0)))

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_diag_gama_pontos():
    response.view = 'simple_form.html'
    return dict(form=LOAD('default','diag_gama_pontos.html',args=[request.args(0)],ajax=False))

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def registro_info():
    response.view = 'simple_form.html'
    db.registro_info.id.represent = lambda id: visualizacao(id,'/cliente/visualizar_registro/')
    form = crud.select(db.registro_info)
    return dict(form=form)

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_registro():
    response.view = 'simple_form.html'
    form = crud.read(db.registro_info,request.args(0))
    return dict(form=form)

@auth.requires(usuario.area_cliente and usuario.visualiza_tarefas)
def plano():
    response.view = 'simple_form.html'
    db.atividade.id.represent = lambda id: visualizacao(id,'/cliente/atividade/')
    atividades = crud.select(db.atividade,db.atividade.plano_acao==request.args(0),orderby=db.atividade.data_limite)
    return dict(form=atividades)

@auth.requires(usuario.area_cliente and usuario.visualiza_tarefas)
def atividade():
    response.view = 'simple_form.html'
    db.atividade.plano_acao.writable=db.atividade.plano_acao.readable=False
    db.atividade.data_limite.writable=db.atividade.data_limite.readable=False
    db.atividade.descricao.writable=False
    form = crud.update(db.atividade,request.args(0),deletable=False)
    return dict(form=form)
    
    
@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def planejamento():
    response.view = 'simple_form.html'
    db.planejamento_estrategico.id.represent = lambda id: visualizacao(id,'/cliente/visualizar_planejamento/')
    planejamentos = crud.select(db.planejamento_estrategico,db.planejamento_estrategico.projeto==request.args(0))
    return dict(form=planejamentos)

@auth.requires(usuario.area_cliente and usuario.visualiza_projeto)
def visualizar_planejamento():
    response.view = 'simple_form.html'
    planejamento = crud.read(db.planejamento_estrategico,request.args(0))
    return dict(form=planejamento)



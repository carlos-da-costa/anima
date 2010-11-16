# -*- coding: utf-8 -*-

request.env.http_accept_language = 'pt-br'  

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    #db = DAL('mysql://anima_fimachi:am4ch1n3@bm12.webservidor.net/anima_fimachine')
    #db = DAL('mysql://root@127.0.0.1/anima_machine')

from gluon.tools import *
auth = Auth(globals(), db)                      # authentication/authorization
auth.settings.hmac_key = 'yawehyireh'

db.define_table('cidade',
    Field('nome', 'string', label='Cidade', required=True),
    Field('uf', 'string', label='UF', required=True),
    )
db.cidade.uf.requires = IS_IN_SET(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])

db.define_table('parceiro',
                Field('razao_social', 'string', required=True),
                Field('nome', 'string'),
                Field('cnpj', 'string',requires=IS_NULL_OR(IS_CNPJ())),
                Field('cpf', 'string',requires=IS_NULL_OR(IS_CPF())),
                Field('endereco', 'string'),
                Field('numero', 'string'),
                Field('uf', 'string'),
                Field('cidade', db.cidade),
                Field('complemento','string',default='-'),
                Field('bairro','string',default='-'),
                Field('e_cliente', 'boolean', default=False,represent=rep_sim_nao,label='É cliente'),
                Field('e_fornecedor', 'boolean', default=False,represent=rep_sim_nao,label='É fornecedor'),
                Field('fundacao', 'integer'))
db.parceiro.id.represent = lambda id: SPAN(A('%i editar' % id, _href=URL(r=request, c="default", f="editar_parceiro", args=id)))
db.parceiro.uf.requires = IS_IN_SET(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
db.parceiro.cidade.requires = IS_IN_DB(db,'cidade.id','%(nome)s')


# definir tabela de usuário customizada
auth_table = db.define_table(
  auth.settings.table_user_name,
    Field('first_name', length=128, default='', label='Nome'),
    Field('last_name', length=128, default='', label='Sobrenome'),
    Field('email', length=128, default='', unique=True, label='Email'),
    Field('password', 'password', length=256,
          readable=False, label='Senha'),
    Field('registration_key', length=128, default='',
          writable=False, readable=False),
    Field('cpf','string',requires=IS_NULL_OR(IS_CPF())),
    Field('rg','string',default='-'),
    Field('cargo', 'string'),
    Field('celular', 'string', required=True),
    Field('endereco', 'string', label='Endereço'),
    Field('numero', 'string'),
    Field('bairro','string',default='-'),
    Field('complemento','string',default='-'),
    Field('cidade', 'string'),
    Field('uf', 'string'),
    Field('empresa', db.parceiro),
    Field('admin','boolean',default=False,represent=rep_sim_nao),
    Field('area_cliente','boolean',default=False,label='Acessa Área do Cliente',represent=rep_sim_nao),
    Field('visualiza_projeto','boolean',default=False,represent=rep_sim_nao),
    Field('visualiza_tarefas','boolean',default=False,represent=rep_sim_nao),
    )
auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
auth_table.password.requires = CRYPT()
auth_table.email.requires = [
   IS_EMAIL(error_message=auth.messages.invalid_email),
   IS_NOT_IN_DB(db, auth_table.email)]
auth_table.empresa.requires = IS_NULL_OR(IS_IN_DB(db, 'parceiro.id', '%(razao_social)s'))
#auth_table.empresa.represent = lambda value: ('', db.parceiro[value].razao_social)[value]
auth_table.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_contato", args=id)))
auth.settings.table_user = auth_table

auth_group_table = db.define_table('auth_group',
                             Field('role',label='Papel'),
                             Field('description',label='Descrição'))
auth_group_table.id.represent = lambda id: edicao(id,'/default/editar_auth_group/','Editar')
auth.settings.table_group = auth_group_table

auth.define_tables()                         # creates all needed tables
crud = Crud(globals(), db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

def is_master():
  if auth.is_logged_in():
    return auth.user.admin
  else:
    return False

response.title = 'Anima'
response.subtitle = 'Bem vindo!'

db.define_table('funcionario',
                Field('usuario', db.auth_user),
                Field('nome', 'string'),
                Field('cpf', 'string'),
                Field('endereco', 'string'),
                Field('numero', 'string'),
                Field('uf', 'string'),
                Field('cidade', 'string'),
                Field('salario_atual', 'decimal(10,2)'),
                Field('vencimento_salario', 'integer'),
                Field('cargo', 'string'))
db.funcionario.usuario.requires = IS_NULL_OR(IS_IN_DB(db, 'auth_user.id', '%(first_name)s'))
db.funcionario.usuario.represent = lambda value: db.auth_user[value].first_name
db.funcionario.vencimento_salario.requires = IS_INT_IN_RANGE(1, 31)
db.funcionario.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_funcionario", args=id))) 

db.define_table('grupo',
                Field('nome', 'string', required=True),
                Field('observacao', 'text', label='Observação'))
db.grupo.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_grupo", args=id)))

# chamado de agrupamento na interface 
db.define_table('participacao',
                Field('contato', db.auth_user),
                Field('grupo', db.grupo))
db.participacao.grupo.requires = IS_IN_DB(db, 'grupo.id', '%(nome)s')
db.participacao.grupo.represent = lambda value: db.grupo[value].nome         
db.participacao.contato.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s')
db.participacao.contato.represent = lambda value: db.auth_user[value].first_name 
db.participacao.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_participacao", args=id)))

db.define_table('log',
               Field('acao', 'string'),
               Field('data', 'datetime'),
               Field('usuario', db.auth_user))
db.log.usuario.requires = IS_IN_DB(db, 'user.id', '%(first_name)')

#
# Fluxo de Caixa
#

# Conta
db.define_table('banco',
                Field('nome', 'string', required=True),
                Field('agencia', 'string', label='Agência'),
                Field('cidade', 'string'),
                Field('uf', 'string')
                )
db.banco.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_banco", args=id)))

db.define_table('conta',
                Field('nome', 'string', required=True),
                Field('numero', 'string'),
                Field('banco', db.banco),
                Field('obs', 'text'),
                )
db.conta.nome.requires = IS_NOT_EMPTY()
db.conta.banco.requires = IS_IN_DB(db, 'banco.id', '%(nome)s')
db.conta.banco.represent = lambda value: db.banco[value].nome 
db.conta.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_conta", args=id)))


# Tipo de documento: boleto, cheque, espécie, etc.
db.define_table('tipo_documento',
                Field('nome', 'string'),
                )
db.tipo_documento.requires = IS_NOT_EMPTY()
db.tipo_documento.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_tipo_documento", args=id)))

# Categorias de despesas ou 
db.define_table('categoria_entrada_saida',
                Field('nome', 'string', required=True),
                Field('entrada_saida', 'string', label='Entrada/Saída')
                )            
db.categoria_entrada_saida.nome.requires = IS_NOT_EMPTY()
db.categoria_entrada_saida.entrada_saida.requires = IS_IN_SET(['Entrada', 'Saída'])
db.categoria_entrada_saida.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_categoria_entrada_saida", args=id)))

db.define_table('conta_a_pagar',
                Field('fornecedor', db.parceiro),
                Field('valor', 'double', default=0),
                Field('vencimento', 'date', requires=data_br),
                Field('tipo_documento', db.tipo_documento, label='Tipo Doc.'),
                Field('data_pagamento', 'date', label='Data do Pagamento', writable=False, readable=False),
                Field('paga', 'boolean', default=False, writable=False,represent=rep_sim_nao),
                Field('categoria', db.categoria_entrada_saida),
                Field('descricao', 'text', label='Descrição'),
                )
db.conta_a_pagar.fornecedor.requires = IS_IN_DB(db(db.parceiro.e_fornecedor == 'True'), 'parceiro.id', '%(razao_social)s')
db.conta_a_pagar.fornecedor.represent = lambda value: db.parceiro[value].razao_social
db.conta_a_pagar.valor.requires = IS_NOT_EMPTY()
db.conta_a_pagar.tipo_documento.requires = IS_IN_DB(db, 'tipo_documento.id', '%(nome)s')
db.conta_a_pagar.tipo_documento.represent = lambda value: db.tipo_documento[value].nome
db.conta_a_pagar.paga.represent = rep_sim_nao
db.conta_a_pagar.categoria.requires = IS_IN_DB(db(db.categoria_entrada_saida.entrada_saida == 'Saída'), 'categoria_entrada_saida.id', '%(nome)s')
db.conta_a_pagar.categoria.represent = lambda value: db.categoria_entrada_saida[value].nome 
db.conta_a_pagar.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_conta_a_pagar", args=id)),
                                                A(' pagar', _href=URL(r=request, c="default", f="pagar_conta", args=id))) 

db.define_table('conta_a_receber',
                Field('cliente', db.parceiro),
                Field('valor', 'double', default=0),
                Field('vencimento', 'date',requires=data_br),
                Field('tipo_documento', db.tipo_documento, label='Tipo Doc.'),
                Field('data_recebimento', 'date', label='Data do Recebimento', readable=False, writable=False),
                Field('recebida', 'boolean', default=False, writable=False,represent=rep_sim_nao),
                Field('categoria', db.categoria_entrada_saida),
                Field('descricao', 'text', label='Descrição'),
                )
db.conta_a_receber.cliente.requires = IS_IN_DB(db(db.parceiro.e_cliente == True), 'parceiro.id', '%(razao_social)s')
db.conta_a_receber.cliente.represent = lambda value: db.parceiro[value].razao_social
db.conta_a_receber.valor.requires = IS_NOT_EMPTY()
db.conta_a_receber.tipo_documento.requires = IS_IN_DB(db, 'tipo_documento.id', '%(nome)s')
db.conta_a_receber.tipo_documento.represent = lambda value: db.tipo_documento[value].nome
db.conta_a_receber.recebida.represent = rep_sim_nao
db.conta_a_receber.categoria.requires = IS_IN_DB(db(db.categoria_entrada_saida.entrada_saida == 'Entrada'), 'categoria_entrada_saida.id', '%(nome)s')
db.conta_a_receber.categoria.represent = lambda value: db.categoria_entrada_saida[value].nome
db.conta_a_receber.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_conta_a_receber", args=id)),
                                                  A(' receber', _href=URL(r=request, c="default", f="pagar_conta", args=id)))

class Valor_Real:
        def valor_real(self):
            if self.movimento == 'Saída':
                return - abs(self.valor)
            else:
                return abs(self.valor)

db.define_table('caixa',
                Field('conta', db.conta),
                Field('data', 'date', label='Data Venc.'),
                Field('documento', 'string', label='Número Doc.', default=0),
                Field('movimento', 'string'),
                Field('valor', 'decimal(10,2)', default=0, requires=IS_DECIMAL_IN_RANGE(0, 999999)),
                )
db.caixa.conta.requires = IS_IN_DB(db, 'conta.id', '%(nome)s')
db.caixa.conta.represent = lambda value: db.conta[value].nome
db.caixa.data.requires = IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')
db.caixa.data.represent = lambda v: v.strftime('%d/%m/%Y')
db.caixa.movimento.requires = IS_IN_SET(['Entrada', 'Saída'])
db.caixa.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_saida", args=id)))
#db.caixa.virtualfields = Valor_Real


db.define_table('unidade',
                Field('sigla', 'string', required=True),
                Field('descricao', 'string'))
db.unidade.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_unidade", args=id)))

db.define_table('item_almoxarifado',
                Field('descricao', label='Descriação', required=True),
                Field('unidade', db.unidade)
                )
db.item_almoxarifado.unidade.requires = IS_IN_DB(db, 'unidade.id', '%(sigla)s')
db.item_almoxarifado.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_item_almoxarifado", args=id)))

db.define_table('movimento_almoxarifado',
                Field('item', db.item_almoxarifado),
                Field('quantidade', 'integer'),
                Field('movimento', 'string'),
                Field('data', 'date', default=request.now, writable=False),
                Field('marca', 'string')
                )
db.movimento_almoxarifado.item.requires = IS_IN_DB(db, 'item_almoxarifado.id', '%(descricao)s')
db.movimento_almoxarifado.item.represent = lambda value: db.item_almoxarifado[value].descricao 
db.movimento_almoxarifado.movimento.requires = IS_IN_SET(['Entrada', 'Saída'])
db.movimento_almoxarifado.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_movimento_almoxarifado", args=id)))

db.define_table('produto',
                Field('descricao', 'string'),
                Field('unidade', db.unidade),
                Field('descontinuado', 'boolean', default=False,represent=rep_sim_nao),
                Field('fornecedor', db.parceiro)
                )
db.produto.unidade.requires = IS_IN_DB(db, 'unidade.id', '%(sigla)s')
db.produto.descontinuado.represent = rep_sim_nao
db.produto.fornecedor.requires = IS_IN_DB(db(db.parceiro.e_fornecedor == True), 'parceiro.id', '%(razao_social)s')
db.produto.fornecedor.represent = lambda value: db.parceiro[value].razao_social 
db.produto.id.represent = lambda id: SPAN(A('%i editar' % id, _href=URL(r=request, c="default", f="editar_produto", args=id)))


db.define_table('movimento_estoque',
                Field('produto', db.produto),
                Field('quantidade', 'integer'),
                Field('data', 'date', default=request.now, writable=False),
                Field('movimento', 'string'),
                Field('preco', 'decimal(10,2)', label='Preço unitário', default=0),
                Field('marca', 'string'))
#class TotalVirtual:
#        def valor_total(self):
#            return self.movimento_estoque.quantidade*self.movimento_estoque.preco
#db.movimento_estoque.virtualfields.append(TotalVirtual())
db.movimento_estoque.produto.requires = IS_IN_DB(db(db.produto.descontinuado == False),
                                                 'produto.id', '%(descricao)s')
db.movimento_estoque.movimento.requires = IS_IN_SET(['Entrada', 'Saída'])
db.movimento_estoque.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_movimento_estoque", args=id)))




#
# Consultoria
#

#
# Diagnósticos
#

db.define_table('diagnostico_alfa',
                Field('data', 'date', default=request.now, label='Data'), #cabeçalho
                Field('contato_responsavel', db.auth_user, requires=IS_NULL_OR(IS_IN_DB(db, 'auth_user.id', '%(first_name)s'))),
                Field('data_inicio', 'date', label='Data Incial', default=request.now),
                Field('data_terminio', 'date', label='Data Final', default=request.now),
                Field('qualidade_produto', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Qualidade do produto'), # mercadológico
                Field('padronizacao_produto', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Padronização do produto'),
                Field('aceitacao_produto', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Aceitação do produto no mercado'),
                Field('transparencia_formacao_preco', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Transparência na formação do preço'),
                Field('canais_distribuicao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Canais de distribuição'),
                Field('politicas_promocionais_divulgacao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Políticas promocionais e de divulgação'),
                Field('propaganda_forca_venda', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Propagando e força de venda'),
                Field('pesquisa_mercado', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Pesquisa de mercado'),
                Field('controle_insumos_materia_prima', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Controle de insumos e matérias primas'), # produção e operações
                Field('capacidade_producao_suporte', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Capacidade de produção/suporte'),
                Field('capacidade_utilizacao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Capacidade de utilização'),
                Field('eficiencia_produttiva', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Eficiência ou produtividade'),
                Field('estrutura_custo_producao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Estrutura do custo de produção'),
                Field('controles_estoque_reposicao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Controle de estoque e reposição'),
                Field('instalacoes_equipamentos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Instalações e equipamentos'),
                Field('controle_equipamentos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Controle de qualidade'),
                Field('inovacao_processo_produtivo', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Inovação no processo produtivo'),
                Field('flexibilizacao_processo_produtivo', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Flexibilização da produção'),
                Field('coleta_dados_informacao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Coleta de dados e informações'), # sistema de informação gerencial
                Field('capacidade_armazenamento_dados', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Capacidade de armazanemanto de dados'),
                Field('qualidade_dados_informacao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Qualidade dos dados e informações'),
                Field('integracao_sistema_gerencial', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Integração do sistema gerencial'),
                Field('velocidade_resposta_sistema', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Velocidade de resposta do sistema'),
                Field('habilidade', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Habilidade'), # administração
                Field('experiencia', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Experiência'),
                Field('comprometimento_objetivos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Comprometimento com os objetivos'),
                Field('trabalho_equipe', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Trabalho em equipe'),
                Field('coordenacao_esforcos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Coordenação de esfoços'),
                Field('flexibilizacao_administrativa', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Flexibilização administrativa'),
                Field('procedimentos_administrativos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Procedimentos administrativos'),
                Field('operacionalizacao_procedimentos', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Operacionalização dos procedimentos'),
                Field('capacidade_tecnica_operativa', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Capacidade técnica operativa'), # recursos humanos
                Field('sistema_gestao_rh', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Sistema de gestão de recursos humanos'),
                Field('formalizacao_contratual', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Formalização contratual'),
                Field('rotatividade_pessoal', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Rotatividade de pessoal'),
                Field('motivacao_trabalhadores', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Motivacao dos trabalhadores'),
                Field('desenvolvimento_tecnico_profissional', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Desenvolvimento técnico profissional'),
                Field('sistema_qualificacao_profissional', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Sistema de qualificação profissional'),
                Field('estimulo_produtividade', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Estímulo a produtividade'),
                Field('sistema_recrutamento_selecao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Sistema de recrutamento e selecao'),
                Field('beneficios', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Benefícios'),
                Field('sistema_adminissao_demissao', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Sistema de adminissão e demissão'),
                Field('avaliacao_desempenho', requires=IS_NULL_OR(IS_IN_SET(notas)), label='Avaliação de desempenho')
                )

db.define_table('diagnostico_beta',
                Field('data', 'date', default=request.now, label='Data'), #cabeçalho
                Field('contato_responsavel', db.auth_user, requires=IS_NULL_OR(IS_IN_DB(db, 'auth_user.id', '%(first_name)s'))),
                Field('produtos_servicos', 'list:string', label='Produtos e/ou serviços comercializados'), # caracterização
                Field('produtos_servicos_mais_vendidos', 'list:string', label='Produtos e/ou serviços mais vendidos'),
                Field('produtos_servicos_menos_vendidos', 'list:string', label='Produtos ou serviços menos vendidos'),
                Field('publico_alvo', 'list:string', label='Público alvo'),
                Field('tipo_sede', requires=IS_NULL_OR(IS_IN_SET(['propria', 'alugada', 'outro'])), label='A sede da empresa é'),
                Field('total_empregados_vinculo', 'integer', label='Total de empregados com vínculo'), # RH
                Field('empregados_sem_vinculo', 'integer', label='Total de empregados sem vínculo'),
                Field('total_funcionarios', 'integer', label='Total geral de funcionários'),
                Field('setorizada_formalmente', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa está setorizada formalmente'),
                Field('num_fun_adm_finam', 'integer', label='Número de funcionários no setor administrativo/financeiro'),
                Field('num_fun_rh', 'integer', label='Número de funcionários no setor de RH'),
                Field('num_fun_comercial', 'integer', label='Número de funcionários no setor comercial (compra/venda)'),
                Field('num_func_distrib_logistica', 'integer', label='Número de funcionários no setor de distribuição/logística'),
                Field('num_func_outros', 'integer', label='Número de funcionários em outros setores'),
                Field('num_admissoes', 'integer', label='Número de admissões no último ano'),
                Field('num_demissoes', 'integer', label='Número de demissões no útlimo ano'),
                Field('num_promocoes', 'integer', label='Número de promoções no último ano'),
                Field('num_aposentadorias', 'integer', label='Número de aposentadorias no último ano'),
                Field('num_afastamentos', 'integer', label='Número de afastamentos no último ano'),
                Field('num_acidentes_trabalho', 'integer', label='Número de acidentes de trabalho no último ano'),
                Field('nao_possui_num_ocorrencias', 'boolean', label='Não possui dados sobre números de ocorrências'),
                Field('num_prop_esino_superior_compl', 'integer', label='Número de proprietários com ensino superior completo'),
                Field('num_prop_esino_medio_compl', 'integer', label='Número de proprietários com ensino médio completo'),
                Field('num_prop_ensino_fundamental_compl', 'integer', label='Número de proprietários com ensino fundamental completo'),
                Field('num_prop_ensino_superior_imcompl', 'integer', label='Número de proprietários com ensino superior incompleto'),
                Field('num_prop_ensino_medio_incompl', 'integer', label='Número de proprietários com ensino médi incompleto'),
                Field('num_prop_ensino_fundamental_imcompl', 'integer', label='Número de proprietários com ensino fundamental incompleto'),
                Field('num_func_ensino_superior_compl', 'integer', label='Número de funcionários com ensino superior completo'),
                Field('num_func_ensino_medio_compl', 'integer', label='Número de funcionários com ensino médio completo'),
                Field('num_func_ensino_fundamental_compl', 'integer', label='Número de funcionários com ensino fundamental completo'),
                Field('num_func_ensino_superior_imcompl', 'integer', label='Número de funcionários com ensino superior incompleto'),
                Field('num_func_ensino_medio_incompl', 'integer', label='Número de funcionários com ensino médio incompleto'),
                Field('num_func_ensino_fundamental_imcompl', 'integer', label='Número de funcionários com ensino fundamental inconpleto'),
                Field('programas_formais_empreendedorismo', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Existem programas formais para promover o empreendedorismo/crescimento dos empregados na empresa'),
                Field('investe_cursos_capacitacao', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa investe em cursos de capacitação profissional para os funcionários'),
                Field('cursos_capacitacao_todos_setores', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Em todos os setores'),
                Field('beneficios', 'list:string', label='A Empresa oferece aos seus funcionários acesso aos quais benefícios'),
                Field('possui_cipa', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui CIPA (Comissão Interna de Prevenção de Acidentes)'),
                Field('programa_formal_recrutamento_interno', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa mantém um programa formal de recrutamento interno'),
                Field('programa_formal_recrutamento_externo', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='E externo'),
                Field('tomada_decisoes_promocoes', 'text', label='Como as decisões sobre promoção são tomadas'),
                Field('distribui_resultados_lucros', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa pratica distribuição de resultados e/ou lucros entre os funcionários'),
                Field('programa_formal_preventivo_saude', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa tem programas formais para garantir a saúde dos empregados de modo preventivo'),
                Field('programa_formal_qualidade_vida', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa adota programas formais para garantir a qualidade de vida dos empregados'),
                Field('diretrizes_estrategicas_formalmente_definidas', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui diretrizes estratégicas formalmente definidas'), # estratégia e gestão
                Field('comunicacao_formal_estrategia_empregados', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Há comunicação formal das estratégias da empresa aos empregados'),
                Field('organograma_definido', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui um organograma definido'),
                Field('plano_cargos_salarios', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui PLANO DE CARGOS E SALÁRIOS'),
                Field('fluxograma', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui fluxograma'),
                Field('procedimento_operacional_padronizado', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui POP (Procedimento Operacional Padronizado)'),
                Field('informatizada', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa é informatizada'),
                Field('software_adotado', 'list:string', label='Qual software adotado'),
                Field('software_atende_necessidades', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='O Software atende as necessidades da empresa'),
                Field('software_emite_relatorios', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Emite relatórios'),
                Field('utiliza_informacoes_software', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Utiliza essas informações'),
                Field('responsavel_suporte_software', label='Quem é o responsável pelo suporte ao software'),
                Field('todos_funcionarios_operam_software', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Todos os funcionários operam o software'),
                Field('projeto_social_ambiental', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui algum Projeto Social ou Ambiental'),
                Field('descricao_projeto_social_ambiental', 'text', label='Se SIM, explique como é realizado'),
                Field('protecao_meio_ambiente', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa pratica alguma forma de proteção ao meio ambiente'),
                Field('descricao_protecao_meio_ambiente', 'text', label='Se SIM, qual'),
                Field('total_faturamento_anterior', 'decimal(10,2)', label='Total de faturamento no ano anterior (em reais)'), # financeiro
                Field('total_custos_fixos_ano_anterior', 'decimal(10,2)', label='Total de custos fixos no ano anterior (em reais)'),
                Field('reducao_custos', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Existe alguma prática de redução de custos'),
                Field('descricao_reducao_custos', 'text', label='Se SIM, explique como é realizada'),
                Field('ativo_empresa_ano_atual', 'decimal(10,2)', label='ATIVO DA EMPRESA EM NO ANO ATUAL'),
                Field('passivo_empresa_ano_atual', 'decimal(10,2)', label='PASSIVO DA EMPRESA NO ANO ATUAL'),
                Field('cadastro_clientes_completo', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui Cadastro de Clientes completo e eficiente'), # comercial
                Field('criterios_para_vendas', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui critérios para vendas'),
                Field('informacao_profunda_clientes', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Você tem informações mais profundas sobre seus clientes, como por exemplo, número de filhos, preferências, renda'),
                Field('pesquisa_mercado_satisfacao', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Sua empresa já realizou alguma pesquisa de mercado para avaliar a SATISFAÇÃO de seus clientes em relação a seus produtos e serviços'),
                Field('resultado_pesquisa_satisfacao', 'text', label='Se SIM, qual foi o resultado'),
                Field('estrategia_marketing', requires=IS_NULL_OR(IS_IN_SET(estrategia_marketing)), label='Em relação à Estratégia de Marketing e desenvolvimento de produtos, sua empresa possui'), #marketing
                Field('pesquisa_mercado', requires=IS_NULL_OR(IS_IN_SET(pesquisa_mercado)), label='Em relação a Estudos e Previsões de Mercado – PESQUISA DE MERCADO'),
                Field('estrategia_marca', requires=IS_NULL_OR(IS_IN_SET(estrategia_marca)), label='Estratégia de marca'),
                Field('rede_comunicacao', requires=IS_NULL_OR(IS_IN_SET(comunicacao)), label='Como você avalia a rede de comunicação na empresa tanto formal quanto informal'),
                Field('lideres_monitoram_clima_organizacional', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Os líderes monitoram o clima organizacional em suas equipes de trabalho'), # liderança
                Field('praticas_formais_perfis_competencias', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa adota práticas formais para definir, disseminar e avaliar um perfil de competências para suas lideranças'),
                Field('investimentos_formais_liderancas', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='Há investimentos formais para formação de lideranças'),
                Field('processo_regular_periodico_monitoramento_clima_organizacional', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa adota um processo regular e periódico de monitoramento e gestão do Clima Organizacional'),
                Field('obs_gerais_lideranca', 'text', label='Observações Gerais (pela empresa ou respondente)'),
                Field('interna_externa', requires=IS_NULL_OR(IS_IN_SET('Interna', 'Externa')), label='A contabilidade da empresa é'), # contabilidae
                Field('conhece_direitos_obrigacoes_tributos', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa conhece todos os seus direitos/obrigações em relação aos tributos'),
                Field('planejamento_tributario', requires=IS_NULL_OR(IS_IN_SET(sim_nao)), label='A empresa possui planejamento tributário'),
                Field('frequencia_balancos', requires=IS_NULL_OR(IS_IN_SET(periodo_mes)), label='Os balanços são realizados com que frequência'),
                Field('controle_estoques', requires=IS_NULL_OR(IS_IN_SET(periodo_mes)), label='O controle de estoque é realizado com que frequência'),
                Field('emissao_notas_fiscais', requires=IS_NULL_OR(IS_IN_SET(periodo_mes)), label='As notas fiscais são emitidas de que forma'),
                Field('obs_gerais_contabilidade', 'text', label='Observações Gerais (pelo consultor)')
                )

db.define_table('diagnostico_gama',
                Field('lideranca_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="As atividades, responsabilidades e funções do dirigente e de seus líderes (pessoas-chaves) estão definidas. Existem divisões de funções, autoridades e de responsabilidades."),
                Field('lideranca_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="Os empresários e seus líderes (pessoas-chaves) são periodicamente desenvolvidos em relação a competências de liderança, através de treinamentos, cursos ou palestras."),
                Field('lideranca_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="Os empresários interagem e demonstram interesse em satisfazer as necessidades de todas as partes interessadas (proprietários, colaboradores, fornecedores, sociedade e etc)."),
                Field('lideranca_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="A organização estabeleceu um manual de qualidade, relacionando todos os seus processos e documentos relativos à qualidade. O manual está acessível à todos os colaboradores envolvidos."),
                Field('lideranca_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="O empresário participa/conduz, regularmente (semanalmente, quinzenalmente, mensalmente etc.), o processo de análise crítica do desempenho da organização. São comparados os planejados e o resultado real obtido. Existem evidências objetivas (atas de reuniões, planos de ações corretivas etc.) que confirmam a realização dessas análises."),
                Field('lideranca_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="O empresário e os líderes disseminam, adequadamente, os resultados e as conclusões da análise crítica do desempenho e o plano de ação para a correção/melhorias também, é divulgado para todos os colaboradores."),
                Field('lideranca_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget, label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Liderança. Existem evidencias de melhorias."),
                Field('lideranca_pontos', 'double', compute=lambda r: pontos([r['lideranca_1'],
                                                                                             r['lideranca_2'],
                                                                                             r['lideranca_3'],
                                                                                             r['lideranca_4'],
                                                                                             r['lideranca_5'],
                                                                                             r['lideranca_6'],
                                                                                             r['lideranca_7']]), readable=True, writable=False, label='Pontos em liderança', default=0),
                Field('estrategias_planos_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui planejamento estratégico que leva em consideração cenário de curto, médio e longo prazo. O planejamento considera as oportunidades e ameaças do ambiente externo e as forças e fraquezas do ambiente interno."),
                Field('estrategias_planos_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="O planejamento estratégico é elaborado considerando às necessidades das partes interessadas (clientes - novos produtos, novos serviços etc.), (fornecedores - garantia de fornecimento, investimento em qualidade etc.), (comunidade - geração de empregos, preservação do meio ambiente etc.) e (colaboradores - reconhecimento, salário, capacitação, desenvolvimento pessoal, melhores condições de trabalho etc.)."),
                Field('estrategias_planos_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="O empresário considera, no processo de planejamento estratégico, a participação dos colaboradores, com adequada contribuição e colaboração."),
                Field('estrategias_planos_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="Os valores da organização (missão, visão, política da qualidade) foram definidos e disseminados. Os valores são entendidos e praticados por todos na empresa."),
                Field('estrategias_planos_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="O empresário disponibiliza os recursos necessários (recursos materiais, financeiros, disponibilidade de tempo etc.) para a execução dos planos de ação."),
                Field('estrategias_planos_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="O empresário se envolve direta e pessoalmente no acompanhamento da implementação dos planos de ações e das metas a serem cumpridas decorrentes do planejamento estratégico."),
                Field('estrategias_planos_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Estratégias e Planos Existem evidencias de melhorias."),
                Field('estrategia_planos_pontos', 'double', compute=lambda r: pontos([r['estrategias_planos_1'],
                                                                                                     r['estrategias_planos_2'],
                                                                                                     r['estrategias_planos_3'],
                                                                                                     r['estrategias_planos_4'],
                                                                                                     r['estrategias_planos_5'],
                                                                                                     r['estrategias_planos_6'],
                                                                                                     r['estrategias_planos_7'], ]), readable=True, writable=False, default=0, label='Pontos em Estratégias e Planos'),
                Field('clientes_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa identifica, analisa e compreende as necessidades e expectativas dos seus clientes atuais e potenciais."),
                Field('clientes_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa identifica o nível de satisfação de seus clientes. São realizadas pesquisas para avaliar o grau de satisfação e insatisfação com relação aos produtos e serviços."),
                Field('clientes_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa utiliza as informações obtidas nas pesquisas para promover melhoria em seus produtos e serviços."),
                Field('clientes_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa trata e responde as reclamações e sugestões realizadas pelos clientes."),
                Field('clientes_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa divulga seus produtos, serviços ou suas ações de melhorias através de propaganda escrita, filmada, televisionada, via Internet, etc."),
                Field('clientes_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa avalia a fidelidade dos clientes, e as informações obtidas são usadas para assegurar a fidelização."),
                Field('clientes_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Clientes Existem evidencias de melhorias."),
                Field('clientes_pontos', 'double', compute=lambda r: pontos([r['clientes_1'],
                                                                                            r['clientes_2'],
                                                                                            r['clientes_3'],
                                                                                            r['clientes_4'],
                                                                                            r['clientes_5'],
                                                                                            r['clientes_6'],
                                                                                            r['clientes_7']]), readable=True, writable=False, default=0, label='Pontos em Clientes'),
                Field('resp_social_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa identifica e gerencia impactos sociais e ambientais provocados pelas suas operações."),
                Field('resp_social_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa está associada a entidade ou associações de classes (Ex:Associação Comercial) para apoiar as suas atividades."),
                Field('resp_social_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização mobiliza os seus colaboradores para participarem de ações sociais promovidos ou não pela própria empresa."),
                Field('resp_social_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização mobiliza seus fornecedores e parceiros para participarem de ações sociais promovidos ou não pela própria empresa."),
                Field('resp_social_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa identifica e atende, quando possível, as reclamações e necessidades da comunidade."),
                Field('resp_social_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa zela e respeita, em suas ações, as igualdades étnicas, sexuais e sociais de todos os seus colaboradores."),
                Field('resp_social_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Sociedade. Existem evidencias de melhorias."),
                Field('resp_social_pontos', 'double', compute=lambda r: pontos([r['resp_social_1'],
                                                                                               r['resp_social_2'],
                                                                                               r['resp_social_3'],
                                                                                               r['resp_social_4'],
                                                                                               r['resp_social_5'],
                                                                                               r['resp_social_6'],
                                                                                               r['resp_social_7']]), readable=True, writable=False, default=0, label='Pontos em Responsabilidade Social'),
                Field('info_conhecimento_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa utiliza informações íntegras e atualizadas na tomada de decisões."),
                Field('info_conhecimento_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa acompanha o desempenho de seus processos através de indicadores."),
                Field('info_conhecimento_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa realiza, periodicamente, a análise e o acompanhamento dos indicadores. Os mesmos são perfeitamente compreendidos pelos colaboradores envolvidos nos processos."),
                Field('info_conhecimento_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa compara o resultado dos indicadores com dados acumulados historicamente, para determinar como está o desempenho atual em relação a períodos anteriores."),
                Field('info_conhecimento_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa incentiva e protege o capital intelectual (novas idéias, melhorias, novas tecnologias), incentivando o pensamento criativo e inovador e cuidando da proteção dos direitos autorais e das patentes desenvolvidas."),
                Field('info_conhecimento_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="Todo o conhecimento adquirido é compartilhado entre os setores e colaboradores."),
                Field('info_conhecimento_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Informações e Conhecimento. Existem evidências de melhorias para obtenção de um melhor resultado."),
                Field('info_conhecimento_pontos', 'double', compute=lambda r: pontos([r['info_conhecimento_1'],
                                                                                                     r['info_conhecimento_2'],
                                                                                                     r['info_conhecimento_3'],
                                                                                                     r['info_conhecimento_4'],
                                                                                                     r['info_conhecimento_5'],
                                                                                                     r['info_conhecimento_6'],
                                                                                                     r['info_conhecimento_7']]), readable=True, writable=False, default=0, label='Pontos em Informações e Conhecimento'),
                Field('pessoas_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa estabeleceu, formalmente, cargos e funções. As funções estão claramente descritas. "),
                Field('pessoas_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização possui processos de seleção, interno e externo. Esses processos levam em consideração os requisitos necessários para o desempenho da função."),
                Field('pessoas_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui formas definidas para remunerar, bonificar e incentivar a busca de melhorias no desempenho das pessoas."),
                Field('pessoas_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui um plano para capacitação e desenvolvimento das pessoas."),
                Field('pessoas_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="É medido o grau de satisfação e bem-estar das pessoas que compõem a força de trabalho. "),
                Field('pessoas_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="São identificados e controlados os perigos e riscos que afetam a saúde, a segurança das pessoas. "),
                Field('pessoas_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação a eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Pessoas. Existem evidências de melhorias para obtenção de um melhor resultado."),
                Field('pessoas_pontos', 'double', compute=lambda r: pontos([r['pessoas_1'],
                                                                                           r['pessoas_2'],
                                                                                           r['pessoas_3'],
                                                                                           r['pessoas_4'],
                                                                                           r['pessoas_5'],
                                                                                           r['pessoas_6'],
                                                                                           r['pessoas_7']]), readable=True, writable=False, default=0, label='Pontos em Pessoas'),
                Field('processo_1', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="As necessidades dos clientes (para o produto/serviço) e da sociedade como um todo (segurança no uso, proteção ambiental etc.) influenciam nos processos de fabricação e ou administrativos."),
                Field('processo_2', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="Os processos estão claramente definidos, e são sistematicamente acompanhados. "),
                Field('processo_3', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="As operações da empresa estão padronizadas e formalmente descritas. Os padrões são revisados regularmente para manter-se atualizados."),
                Field('processo_4', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa seleciona, qualifica, avalia e desenvolve seus fornecedores através de critérios ou requisitos."),
                Field('processo_5', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa faz uso das ferramentas de gestão/planejamento financeiro para desenvolver as estratégias e seus planos de ação."),
                Field('processo_6', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa utiliza ferramentas administrativas e fatores financeiros tais como: (fluxo de caixa, rentabilidade, custos, margem, capital de giro) para garantir o desempenho financeiro do negócio."),
                Field('processo_7', 'string', requires=IS_IN_SET(grau_atendimento, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A organização avalia, em relação à eficácia, as práticas acima descritas (itens 1 – 6), utilizadas para o gerenciar o critério Pessoas. Existem evidencias de melhorias para obtenção de um melhor resultado."),
                Field('processo_pontos', 'double', compute=lambda r: pontos([r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'],
                                                                                            r['processo_1'], ]), readable=True, writable=False, default=0, label='Pontos em Processo'),
                Field('resultados_1', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores de desempenho (resultados) relativos aos clientes."),
                Field('resultados_2', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores de desempenho relativos (resultados) as pessoas / força de trabalho."),
                Field('resultados_3', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores de desempenho (resultados) relativos aos processos / produtos / serviços."),
                Field('resultados_4', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores de desempenho (resultados) relativos a Responsabilidade Social."),
                Field('resultados_5', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores (resultados) relativos ao desempenho Econômico Financeiro."),
                Field('resultados_6', 'string', requires=IS_IN_SET(grau_resultado, error_message='Escolha uma opção.'), widget=SQLFORM.widgets.radio.widget,
                      label="A empresa possui indicadores de desempenho (resultados) relativos a avaliação e desenvolvimento de fornecedores."),
                Field('resultados_pontos', 'double', compute=lambda r: pontos_resultado([r['resultados_1'],
                                                                                       r['resultados_2'],
                                                                                       r['resultados_3'],
                                                                                       r['resultados_4'],
                                                                                       r['resultados_5'],
                                                                                       r['resultados_6'], ]), readable=True, writable=False, default=0, label='Pontos em Resultados'),
                )

db.define_table('projeto_consultoria',
                Field('cliente', db.parceiro),
                Field('diagnostico_alfa', db.diagnostico_alfa),
                Field('diagnostico_beta', db.diagnostico_beta),
                Field('diagnostico_gama', db.diagnostico_gama),
                Field('encerrado','boolean',default=False,represent=rep_sim_nao)
                )
db.projeto_consultoria.cliente.requires = IS_IN_DB(db, 'parceiro.id', '%(nome)s')
db.projeto_consultoria.cliente.represent = lambda id: db.parceiro[id].nome
db.projeto_consultoria.id.represent = lambda id: edicao(id, '/default/editar_projeto/','Editar')

db.define_table('modelo_proposta',
                Field('descricao', 'string',),
                Field('modelo', 'text')
          )
db.modelo_proposta.id.represent = lambda id: edicao(id,'/default/editar_modelo_proposta/','Editar')

db.define_table('proposta',
                Field('modelo', db.modelo_proposta),
                Field('projeto', db.projeto_consultoria),
                Field('data_criacao', 'date'),
                Field('contato_responsavel',db.auth_user,requires=IS_IN_DB(db,'auth_user.id','%(first_name)s')),
                Field('prazo', 'string'),
                Field('ch_horaria_sujerida'),
                Field('frequencia_visitas',requires=IS_IN_SET(['diárias','mensais','quinzenais','outras']),default='diárias'),
                Field('investimento', 'decimal(10,2)',represent=lambda v: 'R$ %f' % v),
                Field('forma_pagamento', 'string'),
                Field('prazo_pagamento', 'text'),
                Field('validade', 'date'),
                Field('aprovada', 'boolean', default=False,represent=rep_sim_nao),
                Field('data_aprovacao', 'date'))
db.proposta.modelo.requires = IS_IN_DB(db, 'modelo_proposta.id', '%(descricao)s')
db.proposta.id.represent = lambda id: edicao(id,'/default/editar_proposta/','Editar')

db.define_table('categoria_cenario',
               Field('descricao', 'string'))
db.categoria_cenario.id.represent = lambda id: edicao(id,'/default/editar_categoria_cenario/','Editar')

db.define_table('item_cenario',
                Field('descricao', 'string'),
                Field('categoria', db.categoria_cenario))
db.item_cenario.categoria.requires = IS_IN_DB(db, 'categoria_cenario.id', '%(descricao)s')
db.item_cenario.id.represent = lambda id: edicao(id,'/default/item_cenario/','Editar')

db.define_table('cenario',
                Field('proposta', db.proposta),
                Field('item_cenario', db.item_cenario))
db.cenario.proposta.requires = IS_IN_DB(db, 'proposta.id', '%(proposta.id)s')
db.cenario.item_cenario.requires = IS_IN_DB(db, 'item_cenario.id', '%(descricao)s')
db.cenario.item_cenario.represent = lambda id: db.item_cenario[id].descricao

db.define_table('modelo_contrato',
                Field('descricao', 'string'),
                Field('modelo', 'text'))
db.modelo_contrato.id.represent = lambda id: SPAN(A('editar', _href=URL(r=request, c="default", f="editar_modelo_contrato", args=id)))

db.define_table('contrato',
                Field('modelo', db.modelo_contrato,
                      IS_IN_DB(db, 'modelo_contrato.id', '%(descricao)s')),
                Field('proposta', db.proposta,
                      requires = IS_IN_DB(db, 'proposta.id')),
                Field('projeto', db.projeto_consultoria,
                      represent=lambda id: edicao(id,'/default/editar_projeto/','Editar')),
                Field('periodo_visitacao', 'string'),
                Field('encerramento', 'date'))
db.contrato.id.represent = lambda id: edicao(id,'/default/editar_contrato/','Editar')

db.define_table('plano_acao',
                Field('projeto',
                      db.projeto_consultoria, 
                      requires=IS_IN_DB(db,'projeto_consultoria.id','%(cliente)s-%(id)s'),
                      represent=lambda id: edicao(id,'/default/editar_projeto/','Editar'),
                      label='Projeto'),
                Field('o_que','string',label='O quê?'),
                Field('quando','date',label='Quando?'),
                Field('quanto','string',label='Quanto?'),
                Field('quem',db.auth_user,label='Quem?',
                      requires=IS_NULL_OR(IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s'))),
                Field('onde','string',label='Onde?'),
                Field('por_que','string',label='Por quê?'),
                Field('como','string',label='Como?'))
db.plano_acao.id.represent = lambda id: edicao(id,'/default/editar_plano_acao/','Editar')

db.define_table('atividade',
                Field('plano_acao',
                      db.plano_acao,
                      requires=IS_IN_DB(db,'plano_acao.id','%(projeto)s-%(id)s'),
                      represent=lambda v: edicao(v,'/default/editar_plano_acao/','Editar')),
                Field('descricao','text',label='Descrição'),
                Field('data_limite','date',label='Data limite',requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                Field('concluido','integer',label='Concluído (%)', default=0,
                      represent=lambda value:'%i%%' % value,
                      requires=IS_INT_IN_RANGE(0,100)),
            )

db.define_table('registro_info',
                Field('projeto',db.projeto_consultoria),
                Field('data','date',
                      requires=IS_DATE(format='%d/%m/%Y',error_message='use o formato 31/12/1981')),
                Field('tipo','string',
                      requires=IS_IN_SET(tipo_info)),
                Field('outro_tipo',label='Outro tipo'),
                Field('descricao','text',label='Descrição sintética da reuinão'),
                Field('atividades','text',label='Atividades que serão realizadas'),
                Field('plano_acao',db.plano_acao,
                      requires=IS_NULL_OR(IS_IN_DB(db,'plano_acao.id','%(o_que)s')),
                      represent=lambda v: (v,'Não')[v==None],
                      label='Plano de ação já apresentado'),
                Field('situacoes_definidas','text',label='Situações definidas'),
                Field('consideracoes_finais','text',label='Considerações Finais'))
db.registro_info.id.represent=lambda id: edicao(id,'/default/editar_registro_info/','Editar')

db.define_table('planejamento_estrategico',
                Field('projeto',db.projeto_consultoria),
                Field('data','date'),
                Field('participantes','list:string'),
                Field('negocio','text',label='Negócio'),
                Field('missao','text',label='Missão'),
                Field('visao','text',label='Visão'),
                Field('principios_valores','text',label='Princípios e Valores'),
                Field('objetivos','text'),
                Field('produtos_servicos','text',label='Produtos e Serviços'),
                Field('setores','text'),
                Field('funcionamento_seg_sex','string',label='Funcionamento de seg. a sex.'),
                Field('funcionamento_sab','string',label='Funcionamento aos Sábados'),
                Field('levantamento_custos_fixos','text',label='Levantamento dos custos fixos'),
                Field('levantamento_investimento','text',label='Levantamento dos investimentos'),
                Field('planejamento_marketing','text',label='Planejamento de Marketing'),
                Field('consideracoes_finais','text',label='Considerações finais'))
db.planejamento_estrategico.id.represent = lambda id: edicao(id,'/default/editar_planejamento_estrategico/','Editar')

db.define_table('setor',
                Field('descricao','string',label='Descrição'),
                Field('planejamento_estrategico',db.planejamento_estrategico),
                Field('atividades','list:string'))
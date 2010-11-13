# -*- coding: utf-8 -*- 

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    [T('Home'), False, 
     URL(request.application,'default','index'), []],
    ]
  
if auth.is_logged_in():
    response.menu = [
            ['Login',False,None,
             [
                    [T('Sair'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Editar Perfil'), False, 
                     URL(request.application,'default','user/profile')],
                    [T('Senha'), False,
                     URL(request.application,'default','user/change_password')]]
             ],
            ]

    # O primeiro usuário cadastrado é tido como o usuário master
    if is_master():
        response.menu.append(['Admin',False,None,
                              [
                               ['Log',False,URL(r=request,c='default',f='log'),[]],
                               ['Usuários',False,URL(r=request,c='default',f='usuario'),[]],
                               ['Papéis',False,URL(r=request,c='default',f='auth_group'),[]],
                               ['Atribuição de Papéis',False,URL(r=request,c='default',f='auth_membership'),[]],
                               ]
                              ])
    if auth.has_membership(auth.id_group('usuario')) or is_master():
        response.menu.append(['Consultoria',False,None,
                             [
                              ['Projetos',False,URL(r=request,c='default',f='projeto'),[]],
                              ['Modelos de Proposta',False,URL(r=request,c='default',f='modelo_proposta'),[]],
                              ['Modelos de Contrato',False,URL(r=request,c='default',f='modelo_contrato'),[]],
                              ['Cenários',False,URL(r=request,c='default',f='categoria_cenario'),[]],
                             ]
                            ])
        response.menu.append(['Relacionamentos',False,None,
                             [
                              ['Parceiros de Negócio',False,URL(r=request,c='default',f='parceiro'),[]],
                              ['Contatos',False,URL(r=request,c='default',f='contato'),[]],
                              ['Grupos',False,URL(r=request,c='default',f='grupo'),[]],
                              ['Agrupamento',False,URL(r=request,c='default',f='participacao'),[]]
                             ]
                            ])
        response.menu.append(['Caixa',False,None,
                             [
                              ['Entradas/Saídas',False,URL(r=request,c='default',f='movimento_caixa'),[]],
                              ['Transferência',False,URL(r=request,c='default',f='transferencia'),[]],
                              ['Cadastros',False,None,[
                                ['Contas',False,URL(r=request,c='default',f='conta'),[]],
                                ['Bancos',False,URL(r=request,c='default',f='banco'),[]],
                                                                                  ]],
                              ['Relatórios',False,None,[
                                                        ['Saldos',False,URL(r=request,c='default',f='saldo'),[]],
                                                        ['Fluxo de Caixa',False,URL(r=request,c='default',f='rel_fluxo_caixa'),[]],
                                                        ['Fluxo de Caixa por Conta',False,URL(r=request,c='default',f='rel_fluxo_caixa_conta'),[]],
                                                        ]
                              ],
                                                                                  
                             ]
                            ])
        response.menu.append(['Contas',False,None,
                             [
                              ['A Receber',False,URL(r=request,c='default',f='conta_a_receber'),[]],
                              ['A Pagar',False,URL(r=request,c='default',f='conta_a_pagar'),[]],
                              ['Pagar Conta',False,URL(r=request,c='default',f='pagar_conta'),[]],
                              ['Receber Conta',False,URL(r=request,c='default',f='receber_conta'),[]],
                              ['Categorias',False,URL(r=request,c='default',f='categoria_entrada_saida'),[]],
                              ['Tipos de Documentos',False,URL(r=request,c='default',f='tipo_documento'),[]],
                              ['Relatórios',False,None,[
                                                        ['Contas a Pagar',False,URL(r=request,c='default',f='rel_contas_pagar'),[]],
                                                        ['Contas a Receber',False,URL(r=request,c='default',f='rel_contas_receber'),[]],
                                                        ]
                              ],
                             ]
                            ])
        response.menu.append(['Almoxarifado',False,None,
                             [
                              ['Itens',False,URL(r=request,c='default',f='item_almoxarifado'),[]],
                              ['Movimento',False,URL(r=request,c='default',f='movimento_almoxarifado'),[]],
                              ['Relatórios',False,None,[
                                                        ['Status do Almoxarifado',False,URL(r=request,c='default',f='rel_status_almoxarifado')]
                                                        ]]
                             ]
                            ])
        response.menu.append(['Estoque',False,None,
                             [
                              ['Produtos',False,URL(r=request,c='default',f='produto'),[]],
                              ['Movimento',False,URL(r=request,c='default',f='movimento_estoque'),[]],
                              ['Unidades',False,URL(r=request,c='default',f='unidade'),[]],
                              ['Relatórios',False,None,[
                                                        ['Status do Estoque',False,URL(r=request,c='default',f='rel_status_estoque')],
                                                        ['Extrato do Estoque',False,URL(r=request,c='default',f='rel_extrato_estoque')]
                                                        ]]
                             ]])
        response.menu.append(['Pessoal',False,None,
                             [
                              ['Funcionários',False,URL(r=request,c='default',f='funcionario'),[]],
                             ]
                            ])
    elif auth.has_membership(auth.id_group('cliente')) or is_master():
        response.menu.append(['Painel',False,URL(r=request,c='cliente',f='index'),[]],
                             )
else:
    response.menu = [
           ['Login', False, None,  
            [
                   [T('Entrar'), False,
                    auth.settings.login_url],
                   [T('Perdi minha senha'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
           ]
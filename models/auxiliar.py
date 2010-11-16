# -*- coding: utf-8 -*-

data_br = IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')

def advanced_editor(field, value):
    return TEXTAREA(_id = str(field).replace('.','_'), _name=field.name, _class='text ckeditor', value=value, _cols=80, _rows=10)

def rep_sim_nao(value):
    if value:
        return 'Sim'
    else:
        return 'Não'
    
def moeda(valor):
    return 'R$ %0.2f' % valor

# para uso nos diagnosticos
notas = ['Péssimo', 'Ruim', 'Regular', 'Bom', 'Excelente']
grau_atendimento = ['Não atende a nenhum dos requisitos.',
                    'Atende apenas alguns requisitos.',
                    'Atende a todos os requisitos, mas faltam documentos (evidências objetivas) que comprovem o total atendimento.',
                    'Atende a todos os requisitos, e existem evidencias objetivas para comprovação de todo o atendimento.',
                    ]
grau_resultado = ['Não existem resultados.',
                  'Existem alguns resultados e destes a maioria possui tendéncias históricas desfaráveis e Não existem metas estabelecidas.',
                  'Existem alguns resultados e destes a maioria possui tendéncias históricas favoráveis, mas Não existem metas estabelecidas.',
                  'Existem muitos resultados e destes a maioria possui tendéncias históricas favoráveis, e existem metas estabelecidas.'
                  ]
# registro de informações
tipo_info = ['Planejamento estratégico', 
                 'Definições e tomada de decisão',
                 'Apresentação e/ou mobilização da equipe de trabalho',
                 'Diagnóstico e/ou levantamento de necessidades',
                 'Visita técnica',
                 'Setorização / Estruturação da empresa ou setor específico']


def pontos(valores):
    soma = 0
    for v in valores:
        soma+=grau_atendimento.index(v)+1
    return soma/2.

def pontos_resultado(valores):
    soma = 0
    for v in valores:
        soma+=grau_resultado.index(v)+1
    return soma*2.17

#def lideranca_pontos(r):
#    soma = grau_atendimento.index(r['lideranca_1'])+1
#    soma+= grau_atendimento.index(r['lideranca_2'])+1
#    soma+= grau_atendimento.index(r['lideranca_3'])+1
#    soma+= grau_atendimento.index(r['lideranca_4'])+1
#    soma+= grau_atendimento.index(r['lideranca_5'])+1
#    soma+= grau_atendimento.index(r['lideranca_6'])+1
#    soma+= grau_atendimento.index(r['lideranca_7'])+1
#    return soma/2.
#
#def estrategia_planos_pontos(r):
#    soma = grau_atendimento.index(r['estrategias_planos_1'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_2'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_3'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_4'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_5'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_6'])+1
#    soma+= grau_atendimento.index(r['estrategias_planos_7'])+1
#    return soma/2.
#
#def clientes_pontos(r):
#    soma = grau_atendimento.index(r['clientes_1'])+1
#    soma+= grau_atendimento.index(r['clientes_2'])+1
#    soma+= grau_atendimento.index(r['clientes_3'])+1
#    soma+= grau_atendimento.index(r['clientes_4'])+1
#    soma+= grau_atendimento.index(r['clientes_5'])+1
#    soma+= grau_atendimento.index(r['clientes_6'])+1
#    soma+= grau_atendimento.index(r['clientes_7'])+1
#    return soma/2.

    
sim_nao = ['Não', 'Sim']
estrategia_marketing = ['Nenhum planejamento estratégico formal',
                        'Algum reconhecimento da importéncia do planejamento estratégico.',
                        'Planejamento com alguma contribuição dos Diretores.',
                        'Procedimentos estabelecidos. A maioria dos Diretores participa no planejamento anual.',
                        'Um processo de planejamento estratégico claramente definido e sistematicamente aplicado']
pesquisa_mercado = ['Não é efetuado qualquer estudo de mercado. As publicaçães sobre o mercado apenas séo adquiridas mediante o interesse.',
                    'Existe um oréamento préprio para a pesquisa de mercado. Séo utilizadas outras fontes com freqçãncia. Todos os funcionérios séo encorajados a prestarem informaçães sobre os mercados.',
                    'As fontes principais e secundérias fornecem dados sobre previsées de mercado e perfis de clientes.']
estrategia_marca = ['Não  existem  ou  quase  Não  existem  referéncias  é  imagem  da  empresa,  a  marcas  ou  ao estabelecimento de marcas em documentos relacionados com o planejamento comercial.',
                    'Tem havido  algumas  tentativas  para  definir uma  estratégia de gestéo  e desenvolvimento da marca da empresa (ou para a criação de uma nova marca).',
                    'Existe  uma  estratégia  bem  definida  para  a  gestéo  e  desenvolvimento  da  marca.  O marketing é encarado como uma deciséo de investimento.',
                    'O lema da empresa foi completamente traduzido numa declaração de posição que guia os esforéos e a estratégia global do negécio.']
comunicacao = ['A comunicação  na  empresa  apresenta  fraca  fluidez  ou  dinâmica,  utilizando  canais  e instrumentos pouco ajustados.',
               'A  empresa  possui  uma  comunicação  pouco  explorada,  sem  estratégia  ou  plano explicitados anualmente, apoiando ações pontuais ou projetos internos ocasionais.',
               'A comunicação no interior da empresa e com o exterior  segue  um plano anual com objetivos bem definidos.',
               'A  empresa  possui uma estratégia  e  um  plano  de  comunicação  formalmente  aprovado  e divulgado.'
               ]
periodo_mes = ['quinzenal', 'mensal', 'bimestral', 'trimestral', 'semestral', 'anual']

#customização do jqgrid
def edicao(id,url,caption):
    url='/'+request.application+url+str(id)
    return A(TAG.button(caption,_class='ui-button ui-widget ui-state-default ui-corner-all'),_href=url)

def visualizacao(id,url):
    url='/'+request.application+url+str(id)
    return SPAN(id,' ',A('Ver',_href=url))

def fpdf_sanitize(s):
    import sanitizer
    reutrn = sanitizer.sanitize(s,permitted_tags=['h1',
                                                  'h2',
                                                  'h3',
                                                  'h4',
                                                  'h5',
                                                  'h6',
                                                  'h7',
                                                  'h7',
                                                  'h8',
                                                  'p',
                                                  'b',
                                                  'i',
                                                  'u',
                                                  'font',
                                                  'center',
                                                  'a',
                                                  'img',
                                                  'ol',
                                                  'ul',
                                                  'li',
                                                  'table',
                                                  'thead',
                                                  'tfoot',
                                                  'tbody',
                                                  'tr',
                                                  'th',
                                                  'td',
                                                  'span'],
                                            allowed_attributes={'h1':['align'],
                                                                'h2':['align'],
                                                                'h3':['align'],
                                                                'h4':['align'],
                                                                'h5':['align'],
                                                                'h6':['align'],
                                                                'h7':['align'],
                                                                'h8':['align'],
                                                                'p':['align'],
                                                                'font':['face','size','color'],
                                                                'a':['href'],
                                                                'img':['src','width','height'],
                                                                'table':['border','width'],
                                                                'tr':['bgcolor'],
                                                                'th':['algin','bgcolor','width'],
                                                                'td':['align','bgcolor','width']
                                                                }
                                                              ,escape=True)
    
def decssify(s):
    import re
    align = re.compile('text-align:(.*);')
    dom = TAG(s)
    tags = ['p','h1','h2','h3','h4','h5','h6','h7','h8']
    for p in dom.elements('p, h1, h2 ,h3 ,h4, h5, h6, h7 ,h8, th, td'):
        style = p['_style']
        if style:
            res=re.search(align,p['_style'])
            if res:
                p['_align']=res.groups()[0]
                p['_style']=None
    return str(dom)



# Autor: Fabiano Weimar dos Santos (xiru)
# Correcao em 20080407: Gustavo Henrique Cervi (100:"cento") => (1:"cento')
# Correção em 20100311: Luiz Fernando B. Vital adicionado {0:""} ao ext[0], pois dava KeyError: 0 em números como 200, 1200, 300, etc.

import sys

ext = [{0:"", 1:"um", 2:"dois", 3:"três", 4:"quatro", 5:"cinco", 6:"seis",
7:"sete", 8:"oito", 9:"nove", 10:"dez", 11:"onze", 12:"doze",
13:"treze", 14:"quatorze", 15:"quinze", 16:"dezesseis", 
17:"dezessete", 18:"dezoito", 19:"dezenove"}, {2:"vinte", 3:"trinta",
4:"quarenta", 5:"cinquenta", 6:"sessenta", 7:"setenta", 8:"oitenta",
9:"noventa"}, {1:"cento", 2:"duzentos", 3:"trezentos",
4:"quatrocentos", 5:"quinhentos", 6:"seissentos", 7:"setessentos",
8:"oitocentos", 9:"novecentos"}]

und = ['', ' mil', (' milhão', ' milhões'), (' bilhão', ' bilhões'),
(' trilhão', ' trilhões')]

def cent(s, grand):
    s = '0' * (3 - len(s)) + s
    if s == '000':
        return ''
    if s == '100': 
        return 'cem'
    ret = ''
    dez = s[1] + s[2]
    if s[0] != '0':
        ret += ext[2][int(s[0])]
        if dez != '00':
            ret += ' e '
    if int(dez) < 20:
        ret += ext[0][int(dez)]
    else:
        if s[1] != '0':
            ret += ext[1][int(s[1])]
            if s[2] != '0':
                ret += ' e ' + ext[0][int(s[2])]
    
    return ret + (type(und[grand]) == type(()) and (int(s) > 1 and und[grand][1] or und[grand][0]) or und[grand])

def extenso(n):
    sn = str(int(n))
    ret = []
    grand = 0
    while sn:
        s = sn[-3:]
        sn = sn[:-3]
        ret.append(cent(s, grand))
        grand += 1
    ret.reverse()
    return ' e '.join([r for r in ret if r])

if __name__ == '__main__':
    n = sys.argv[1]
    print n
    print extenso(n)
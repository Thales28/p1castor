import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso à agenda. Um compromisso tem no mínimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False  
  novaAtividade = ''
  if dataValida(extras[0]):
    novaAtividade = novaAtividade + extras[0]+' '
  if horaValida(extras[1]):
    novaAtividade = novaAtividade + extras[1]+' '
  if prioridadeValida(extras[2]):
    novaAtividade = novaAtividade + extras[2]+' '
  novaAtividade = novaAtividade + descricao+' '
  if contextoValido(extras[3]):
    novaAtividade = novaAtividade + extras[3]+' '
  if projetoValido(extras[4]):
    novaAtividade = novaAtividade + extras[4]+' '
  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  alfabeto = 'abcdefghijklmnopqrstuvwxyz'
  if len(pri) != 3 or pri[0] != '(' or pri[2] != ')':
    return False
  for x in alfabeto:
    if pri[1] == x:
      return True
  for x in alfabeto.upper():
    if pri[1] == x:
      return True
  return False

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  elif horaMin[0] > '2' or (horaMin[0] == '2' and horaMin[1] > '3') or horaMin[2] > '5':
    return False
  return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  elif data[0] > '3' or (data[0] == '3' and data[1] > '1') or data[2] > '1' or (data[2] == '1' and data[3] > '2'):
    return False
  elif (data[0] == '3' and data[1] == '1' and data[2] == '0' and (data[3] == '4' or data[3] == '6' or data[3] == '9')):
    return False
  elif (data[0] == '3' and data[1] == '1' and data[2] == '1' and data[3] == '1') or (data[0] > '2' and data[2] == '0' and data[3] == '2'):
    return False
  return True
  
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) < 2 or proj[0] != '+':
    return False
  return True

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) < 2 or cont[0] != '@':
    return False
  return True

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, (data, hora, prioridade,  contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    desc = ''
    data = '' 
    hora = ''
    pri = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    for x in tokens:
      if (data == '') and dataValida(x):
        data = x
      elif (hora == '') and horaValida(x):
        hora = x
      elif (pri == '') and prioridadeValida(x):
        pri = x
      elif (contexto == '') and contextoValido(x):
        contexto = x
      elif (projeto == '') and projetoValido(x):
        projeto = x
      else:
        desc = desc + x + ' '

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  fp = open(TODO_FILE, 'r')
  linhas = fp.readlines()
  fp.close()
  return organizar(linhas)

def ordenarPorDataHora(itens):
  i = 0
  while i < len(itens):
    j = 0
    while j < (len(itens)-1):
      #Casos em que eu automaticamente quero que percam prioridade: Sem data e hora OU se houver data, porém se o próximo ítem tiver apenas hora:
      if ((itens[j][1][0] == '') and (itens[j][1][1] == '')) or ((itens[j][1][0] != '') and ((itens[j+1][1][0] == '') and (itens[j+1][1][1] != ''))):
        temporaria = itens[j]
        itens[j] = itens[j+1]
        itens[j+1] = temporaria
      elif (itens[j][1][0] != '') and (itens[j+1][1][0] != ''):
        #Se o ítem sendo visto e o próximo tiverem datas, nós vamos compará-las para saber qual a maior para perder prioridade:
        if (itens[j][1][0][4:] > itens[j+1][1][0][4:]): # ([j]:ítem conforme o contador)([1]:posição na tupla em que tão os extras)([0]:posição das datas na tupla)([4:]:pegando apenas o ano da data)
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
        elif (itens[j][1][0][4:] == itens[j+1][1][0][4:]) and (itens[j][1][0][2:4] > itens[j+1][1][0][2:4]):
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
        elif (itens[j][1][0][2:] == itens[j+1][1][0][2:]) and (itens[j][1][0][:2] > itens[j+1][1][0][:2]):
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
        elif (itens[j][1][0] == itens[j+1][1][0]) and (itens[j][1][1] == ''):#se as datas forem iguais, mas o ítem do contador não tiver hora ele perde prioridade.
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
        elif (itens[j][1][0] == itens[j+1][1][0]) and (itens[j][1][1] != '') and (itens[j+1][1][1] != ''):
          #Caso as datas sejam iguais, mas os ítens possuam hora, nós iremos compará-las:
          if (itens[j][1][1][:2] > itens[j+1][1][1][:2]):
            temporaria = itens[j]
            itens[j] = itens[j+1]
            itens[j+1] = temporaria
          elif (itens[j][1][1][:2] == itens[j+1][1][1][:2]) and (itens[j][1][1][2:] > itens[j+1][1][1][2:]):
            temporaria = itens[j]
            itens[j] = itens[j+1]
            itens[j+1] = temporaria
      elif (itens[j][1][0] == '') and (itens[j][1][1] != '') and (itens[j+1][1][0] == '') and (itens[j+1][1][1] != ''):
        #Caso os ítens possuam apenas horas:
        if itens[j][1][1][:2] > itens[j+1][1][1][:2]:
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
        elif (itens[j][1][0][2:] == itens[j+1][1][0][2:]) and (itens[j][1][0][:2] > itens[j+1][1][0][:2]):
          temporaria = itens[j]
          itens[j] = itens[j+1]
          itens[j+1] = temporaria
      j = j+1
    i = i+1
  return itens
   
def ordenarPorPrioridade(itens):

  ################ COMPLETAR

  return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (data, hora, prioridade, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'listar'
    itemParaListar = organizar([' '.join(comandos)])[0]
    # itemParaListar = (descricao, (data, hora, prioridade, contexto, projeto))
    listar(itemParaListar[0], itemParaListar[1]) # novos itens não têm prioridade
  elif comandos[1] == REMOVER:
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
#processarComandos(sys.argv)

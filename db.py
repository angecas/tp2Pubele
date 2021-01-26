import shelve
import os

def find_all():
    with shelve.open('relatorios.db') as s:
        return list(s.keys())


def find_one(relatorio):
    with shelve.open('relatorios.db') as s:
        return s[relatorio]


def insert(relatorio):
    with shelve.open('relatorios.db', writeback=True) as s:
        s[relatorio['relatorio']] = relatorio
        return list(s.keys())


#elimina pelo titulo (tit é o titulo)
   
def deletebytitle(tit):
    with shelve.open('relatorios.db', writeback=True) as s:
        for it in s:
            if tit in list(s[it].values()):
                del(s[it])


#elimina todos os relatorios

def  apagatodos():
    with shelve.open('relatorios.db') as s:
        for it in s:
            del( s[it] )

def ordenaalfa():
    L=[]
    with shelve.open('relatorios.db') as s:
        for it in s:
            L.append(str(it))
    return sorted(L)
            
            
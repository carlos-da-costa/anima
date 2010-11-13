#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IS_CPF:
    def __init__(self,error_message='CPF inválido.'):
        self.e = error_message
        
    def __call__(self, value):
        cpfcnpj = local_import('cpfcnpj')
        ret = cpfcnpj.validar_cpf(value)
        if ret:
            return (ret, None)
        else:
            return (value, self.e)
        
class IS_CNPJ:
    def __init__(self,error_message='CNPJ inválido'):
        self.e = error_message
    
    def __call__(self,value):
        cpfcnpj = local_import('cpfcnpj')
        ret = cpfcnpj.validar_cnpj(value)
        if ret:
            return (ret, None)
        else:
            return (value, self.e)
        
class IS_CPF_OR_CNPJ():
    def __init__(self,error_message='CPF ou CNPJ inválido'):
        self.e = error_message
    
    def __call__(self,value):
        cpfcnpj = local_import('cpfcnpj')
        ret_cpf = cpfcnpj.validar_cpf(value)
        ret_cnpj = cpfcnpj.validar_cnpj(value)
        if ret_cpf:
            return (ret_cpf, None)
        elif ret_cnpj:
            return (ret_cnpj, None)
        else:
            return (value, self.e)
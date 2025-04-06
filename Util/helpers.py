def gerar_id(lista):
    return len(lista) + 1 if lista else 1

def validar_campos(dados, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            return False, f"O campo '{campo}' é obrigatório."
    return True, None

def validar_numeros(dados, campos_numericos):
    for campo in campos_numericos:
        if dados.get(campo) is not None and not isinstance(dados[campo], (int, float)):
            return False, f"O campo '{campo}' deve ser um número."
        if dados.get(campo, 0) < 0:
            return False, f"O campo '{campo}' deve ser um número positivo."
    return True, None

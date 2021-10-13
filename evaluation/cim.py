# Function: CIM
def cim_method(standards, data, weights):
    return sum(data/standards*weights)*100
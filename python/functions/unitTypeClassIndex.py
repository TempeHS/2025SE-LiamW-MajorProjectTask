
def unitTypeClassIndex(unitType,unitClass):
    translatedType = None
    translatedClass = None
    if unitType == 0:
        translatedType = "light"
    if unitClass == 0:
        translatedClass = "biological"
    
    return translatedType, translatedClass
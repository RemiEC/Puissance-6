import Fonctions_de_base

pourcentage_amplitude = 0.6
''' 
Renvoie le meilleur play à faire suivant le state donné en considérant que l'adversaire va faire les plays optimum
mais ici on va élaguer des options afin de gagner en rapidité d'exécution (remplacerai fonction MiniMax)

@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ return    Une action optimale à faire par le joueur
'''
def Alpha_Beta(state,joueur):
    if(joueur == 'X') : opposant = 'O'
    if(joueur == 'O') : opposant = 'X'
    max_Depth = 4 #Profondeur maximale
    resultat = Max_Value_Alpha_Beta(state,joueur,opposant, -10000000000, 10000000000, 0, max_Depth)
    return resultat


"""
Reflexion pour le tour de l'opposant, qui va prendre l'action qui a le gain minimum pour le joueur avec la méthode alpha beta (plus opti)

@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ opposant  Le symbole correspondant à l'adversaire (X/O)
@ alpha     La valeur max déjà obtenue avec les autres options à cet étage, permet de déterminer quand faire une coupure alpha
@ beta      La valeur min déjà obtenue avec les autres options à cet étage, permet de déterminer quand faire une coupure beta
@ prof_max  La profondeur max a laquelle on descend   
@ prof_act  La profondeur actuelle
@ return    La valeur de l'utility d'un état
"""

def Min_Value_Alpha_Beta(state,joueur,opposant,alpha,beta,prof_act,prof_max):
    if(Fonctions_de_base.Terminal_Test(state) or prof_act==prof_max) : return Fonctions_de_base.Utility_Vincent_Remi(state,joueur,opposant)
    prof_act+=1
    #valeur infiniment haute
    v = 10000000000
    #Ici ce sont les actions de l'opposant qu'on prend car c'est son tour

    #! Diminution de l'amplitude de l'arbre

    liste_value=[]
    liste_action = []
    for a in Fonctions_de_base.Action(state):
        value = Fonctions_de_base.Utility_Vincent_Remi(Fonctions_de_base.Result(state,a,opposant), joueur, opposant)
        liste_value.append(value)
        liste_action.append(a)

    # * ON PEUT MODIFIER LE POURCENTAGE
    # * ON PREND LES % PIRES PLAYS CAR C'EST L'ADVERSAIRE QUI JOUE
    # * ON GAGNE AINSI DU TEMPS ET ON NE REGARDE PAS LES PLAYS ININTERESSANTS

    liste_action_conservees = []
    for i in range(int(len(liste_value)*pourcentage_amplitude)):
        index_value_min = liste_value.index(min(liste_value))
        liste_action_conservees.append(liste_action[index_value_min])
        del liste_value[index_value_min]
        del liste_action[index_value_min]

    #! FIN Diminution de l'amplitude de l'arbre

    for a in liste_action_conservees:
        v = min(v,Max_Value_Alpha_Beta(Fonctions_de_base.Result(state,a,opposant),joueur,opposant,alpha,beta,prof_act,prof_max))
        if (v <= alpha) : return v
        beta = min(beta,v)
    return v


'''
Reflexion pour le tour du joueur, qui va prendre l'action qui a le gain maximum pour lui avec la méthode alpha beta (plus opti)

@ state             Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur            Le symbole correspondant au joueur (X/O)
@ opposant          Le symbole correspondant à l'adversaire (X/O)
@ alpha             La valeur max déjà obtenue avec les autres options à cet étage, permet de déterminer quand faire une coupure alpha
@ beta              La valeur min déjà obtenue avec les autres options à cet étage, permet de déterminer quand faire une coupure beta
@ renvoyer_action   Détermine s'il faut uniquement renvoyer la value ou aussi l'action associée
@ return            La valeur de l'utility d'un état (+ l'action associée)
'''


def Max_Value_Alpha_Beta(state,joueur,opposant,alpha,beta, prof_act,prof_max):
    if(Fonctions_de_base.Terminal_Test(state) or prof_act==prof_max ) : return Fonctions_de_base.Utility_Vincent_Remi(state,joueur,opposant)
    prof_act+=1
    #valeur infiniment basse
    v = -1000000000000
    if(prof_act==1):
        sauvegarde_action = []
        #Ici ce sont les actions du joueur qu'on prend car c'est son tour

        #! Diminution de l'amplitude de l'arbre

        liste_value=[]
        liste_action = []
        for a in Fonctions_de_base.Action(state):
            value = Fonctions_de_base.Utility_Vincent_Remi(Fonctions_de_base.Result(state,a,joueur), joueur, opposant)
            liste_value.append(value)
            liste_action.append(a)

        # * ON PEUT MODIFIER LE POURCENTAGE
        # * ON PREND LES % MEILLEURS PLAYS CAR C'EST L'IA QUI JOUE
        # * ON GAGNE AINSI DU TEMPS ET ON NE REGARDE PAS LES PLAYS ININTERESSANTS
        liste_action_conservees = []
        for i in range(int(len(liste_value)* pourcentage_amplitude )):
            index_value_min = liste_value.index(max(liste_value))
            liste_action_conservees.append(liste_action[index_value_min])
            del liste_value[index_value_min]
            del liste_action[index_value_min]

        #! FIN Diminution de l'amplitude de l'arbre

        for a in liste_action_conservees:
            ancien_v = v
            v = max(v,Min_Value_Alpha_Beta(Fonctions_de_base.Result(state,a,joueur),joueur,opposant,alpha,beta,prof_act,prof_max))
            if(ancien_v < v): sauvegarde_action=a
            if (v >= beta) : return [v,sauvegarde_action]
            alpha = max(alpha,v)
        return [v,sauvegarde_action]
    #Ici ce sont les actions de l'opposant qu'on prend car c'est son tour

    #! Diminution de l'amplitude de l'arbre

    liste_value=[]
    liste_action = []
    for a in Fonctions_de_base.Action(state):
        value = Fonctions_de_base.Utility_Vincent_Remi(Fonctions_de_base.Result(state,a,joueur), joueur, opposant)
        liste_value.append(value)
        liste_action.append(a)

    # * ON PEUT MODIFIER LE POURCENTAGE
    # * ON PREND LES % MEILLEURS PLAYS CAR C'EST L'IA QUI JOUE
    # * ON GAGNE AINSI DU TEMPS ET ON NE REGARDE PAS LES PLAYS ININTERESSANTS

    liste_action_conservees = []
    for i in range(int(len(liste_value)*pourcentage_amplitude)):
        index_value_min = liste_value.index(max(liste_value))
        liste_action_conservees.append(liste_action[index_value_min])
        del liste_value[index_value_min]
        del liste_action[index_value_min]
    
    #! FIN Diminution de l'amplitude de l'arbre

    for a in liste_action_conservees:
        v = max(v,Min_Value_Alpha_Beta(Fonctions_de_base.Result(state,a,joueur),joueur,opposant,alpha,beta,prof_act,prof_max))
        if (v >= beta) : return v
        alpha = max(alpha,v)
    return v

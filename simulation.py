import numpy as np
import matplotlib.pyplot as plt


def sum(tab, s, e):
    t = 0
    for i in range(s, e):
        t += tab[i]
    return t


def zerotab(le, la):
    tab = []
    for i in range(le):
        tab.append([])
        for j in range(la):
            tab[i].append(0)
    return tab


def avaible(tab):
    for i in range(len(tab)):
        if tab[i] == -1:
            return i
    return -1


def endCycle(progression,num_etapes):
    for i in range(len(progression)):
        if progression[i][1] != num_etapes:
            return False
    return True


def simulation(duree, start):
    time = start * 60

    num_equipments = len(duree)
    num_etapes = len(duree[0])

    start_times = zerotab(num_equipments, num_etapes)
    end_times = zerotab(num_equipments, num_etapes)
    etapes = []
    for i in range(num_etapes):
        etapes.append([-1,-1])

    progression = []
    for i in range(num_equipments):
        progression.append([sum(duree[i], 0, num_etapes), 0,
                            0])  # On stock le temps total, l'étape actuel pour l'équipement (on commence a 0)
        # et la durée executé de l'étape
    while endCycle(progression, num_etapes) == False:
        print(time // 60, "h", time % 60, ":\t")
        waiting = []
        for i in range(num_etapes):
            waiting.append([])
        for i in range(num_equipments):
            if progression[i][1] != num_etapes:
                if progression[i][2] == duree[i][progression[i][1]]:  # si un equipement a fini une etape
                    for j in range(2):
                        if etapes[progression[i][1]][j] == i:  # libere de l'espace pour l'etape occupé
                            etapes[progression[i][1]][j] = -1
                    end_times[i][progression[i][1]] = time  # note le moment ou se termine la tache
                    print("L'équipement ", i + 1, " termine l'étape : ", progression[i][1] + 1, ". \t")
                    progression[i][1] += 1  # actualise la progression
                    progression[i][2] = 0

        for i in range(num_equipments):
            if progression[i][1] != num_etapes:
                if progression[i][2] == 0:  # si un equipement a pas commencer la progression de son etape
                    av = avaible(etapes[i])
                    if av != -1:  # si il y a de la place libre
                        waiting[progression[i][1]].append(i)  # on ajoute dans la file d'attente

        for i in range(num_etapes):
            if len(waiting[i]) != 0:  # Si il y a un/des equipements en attente
                for j in range(2):  # Boucle taille 2 car on verifie si il y a pas 2 place libres pour l'etape
                    av = avaible(etapes[i])  # On verifie donc une 2-eme fois pour rajouter une 2-eme etape si possible
                    if len(waiting[i]) != 0:
                        if av != -1:
                            DM = 0
                            best = 0
                            for j in range(len(waiting[i])):  # Ordonnancer "DM"
                                if sum(duree[waiting[i][j]], progression[waiting[i][j]][1], num_etapes) > best:
                                    DM = waiting[i][j]
                            etapes[i][av] = DM
                            start_times[DM][progression[DM][1]] = time
                            print("L'équipement ", DM + 1, " commence l'étape : ", progression[DM][1] + 1, ". \t")
                            waiting[i].pop(j)

            for j in range(2):

                if etapes[i][j] != (-1):
                    progression[etapes[i][j]][2] = progression[etapes[i][j]][2] + 1
                    print("L'équipement ", etapes[i][j] + 1, "est en cours de progression sur l'étape :", i+1)



        print("")
        time += 1
    print("Le cyle aura durée : ", (time - start*60)//60,"h",((time - start*60)%60)-1)


    start_times = np.array(start_times)
    end_times = np.array(end_times)
    durations = np.array(duree)


    equipments = [f"Equipement {i + 1}" for i in range(num_equipments)]
    steps = [f"Etape {i + 1}" for i in range(num_etapes)]


    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['blue', 'green', 'orange']

    for equip_idx, equip in enumerate(equipments):
        for step_idx, step in enumerate(steps):
            start = start_times[equip_idx][step_idx]
            duration = durations[equip_idx][step_idx]
            ax.barh(equip, duration, left=start, color=colors[step_idx], edgecolor='black')



    max_end = end_times.max()
    ax.set_xlim(0, max_end + 5)


    ax.set_xlabel("Time (minutes from 10:00 AM)")
    ax.set_title("Production Cycle of Equipments")
    ax.set_yticks(range(num_equipments))
    ax.set_yticklabels(equipments)
    ax.grid(True, linestyle='--', linewidth=0.7)


    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    duree = [[5, 7, 4], [5, 7, 6], [10, 11, 2]]
    '''start = int(input("Choisissez l'heure de début de la production "))
    '''
    simulation(duree,10)



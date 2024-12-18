import numpy as np
import matplotlib.pyplot as plt

def distance(p1,p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def dansLeCercleCirconscrit(point, triangle):
    x_bary = (triangle[0][0] + triangle[1][0] + triangle[2][0])/3
    y_bary= (triangle[0][1] + triangle[1][1] + triangle[2][1])/3
    barycentre = [x_bary,y_bary]
    rayon = distance(barycentre,triangle[0])
    dist_bary = distance(barycentre,point)
    if rayon> dist_bary:
        return True
    else:
        return False

#Méthode intuitive est naive avec une complexité en o(n3), triple boucle for (ouch) --> pistes d'amélioration: se renseigner sur une méthode plus optimale ou passer par des array pour faire les manips (?)
def delaunay(liste_points):
    triangles = []
    # Initialisation de la triangulation avec les trois premiers points
    triangles.append([liste_points[0], liste_points[1], liste_points[2],"valide"])

    for i in range(3, len(liste_points)):  # Commence avec le 4ème point
        point = liste_points[i]
        for triangle in triangles[:]: 
            if triangle[3]=="valide":  #On crée des triangles avec tous les points d'un triangle pré-existant
                triangle1 = [point, triangle[0], triangle[1],"valide"]
                triangle2 = [point, triangle[1], triangle[2],"valide"]
                triangle3 = [point, triangle[2], triangle[0],"valide"]
                for i in range(3):  # On regarde pour tous les points du triangle qu'on relie s'il est dans le cercle inscrit d'un triangle qu'on a créé
                    if dansLeCercleCirconscrit(triangle[i], triangle1):
                        triangle1[3]= "invalide"
                    if dansLeCercleCirconscrit(triangle[i], triangle2):
                        triangle2[3]="invalide"
                    if not dansLeCercleCirconscrit(triangle[i], triangle3):
                        triangle3[3]="invalide"
                if dansLeCercleCirconscrit(point,triangle): # On regarde si le point que l'on vient de rajouter est dans le triangle avec lequel on compare
                    triangle[3]="invalide" 
    triangulation =[]
    for triangle in triangles:
        if triangle[3] == "valide": #On récupère dans la triangulation seulement les triangles qui sont valides
            triangulation.append(triangle)
    return triangulation

# Fonction pour tracer la triangulation
def afficher_triangulation():
    plt.clf()  # Efface la triangulation déjà affichée
    triangulation = delaunay(points)

    triangles_indices = []
    for triangle in triangulation:
        indices = [
            np.where((points == triangle[0]).all(axis=1))[0][0],
            np.where((points == triangle[1]).all(axis=1))[0][0],
            np.where((points == triangle[2]).all(axis=1))[0][0],
        ]
        triangles_indices.append(indices)

    plt.triplot(points[:, 0], points[:, 1], triangles_indices, color='blue', alpha=0.6, lw=1.2) #Ligne qui gère l'affichage des triangles
    plt.scatter(points[:, 0], points[:, 1], color='red', s=20) #Ligne qui gère l'affichage des points

    for i, [x, y] in enumerate(points):  #possible car la liste des points est un array
        plt.text(x + 0.002, y + 0.0002, str(i), color='black', fontsize=10)

    plt.title("Triangulation de Delaunay Interactive (cliquez pour y ajouter des points)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.draw()

def click_souris(event): #Fonction qui gère le click de souris 
    if event.xdata is not None and event.ydata is not None:  # On ne prend en compte que les clicks qui se font à l'intérieur des axes
        global points
        new_point = np.array([[event.xdata, event.ydata]])
        points = np.vstack([points, new_point]) # = points.append(...) pour une liste, sauf que là on a un array
        afficher_triangulation()




if __name__ == "__main__":

    # Points initiaux
    points = np.random.rand(3, 2)

    plt.figure(figsize=(8, 8))

    afficher_triangulation()

    plt.connect('button_press_event', click_souris) #Trouvée dans la doc de matplotlib

    plt.show()

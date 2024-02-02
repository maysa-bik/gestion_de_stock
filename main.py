import pygame
#from add_product import add_product
#from delete_product import delete_product
#from update_product import update_product
import mysql.connector

pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Store:
    def __init__(self, window, font, mycursor) -> None:
        self.window = window
        self.font = font 
        self.mycursor = mycursor

    def afficher_produits(self):
        self.window.fill(WHITE)

        # Exécuter une requête pour récupérer la liste des produits depuis la base de données
        self.mycursor.execute("SELECT * FROM product")
        produits = self.mycursor.fetchall()

        # Afficher les produits sur l'écran
        for i, produit in enumerate(produits):
            produit_text = f"{produit[1]} - Prix: {produit[3]} - Quantité: {produit[4]}"
            text_surface = self.font.render(produit_text, True, (0,0,0))
            self.window.blit(text_surface,(50, 50 + i * 50))


def main():

    # Configuration de la fenêtre
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Gestion de stock") 


    font = pygame.font.SysFont(None, 36)
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='maysa1995',
        database='store'
    )
    mycursor = mydb.cursor()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
                # Créer une instance de la classe ProductManager
        store = Store(window, font, mycursor)
        store.afficher_produits()    
        pygame.display.update()

    pygame.quit()            

if __name__ == "__main__":
    main()


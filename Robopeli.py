import pygame
import random
 
class Robopeli:
 
    def __init__(self):
        pygame.init()
        self.naytto = pygame.display.set_mode((640, 480))
 
        # Fontit
        pygame.display.set_caption("Vie mörköjen joulurahat")
        self.pelifontti = pygame.font.SysFont("trebuchetmsbolditalic", 15)
        self.alkufontti = pygame.font.SysFont("trebuchetmsbolditalic", 25)
        
        # Kuvat
        self.morko = pygame.image.load("hirvio.png")
        self.robo = pygame.image.load("robo.png")
        self.kolikko = pygame.image.load("kolikko.png")
 
        self.nollaa_arvot()
 
        # Pelissä on 3 tilaa; alkunäyttö, peli, ja loppunäyttö. Näillä kontrolloidaan mikä kulloinkin.
        self.alku = True
        self.loppu = False
 
        self.kello = pygame.time.Clock()
 
        self.silmukka()
 
    # Nollataan hahmojen arvot ja laskuri uutta peliä varten
    def nollaa_arvot(self):
        self.robo_x = 0
        self.robo_y = 480-self.robo.get_height()
 
        self.robo_oikealle = False
        self.robo_vasemmalle = False
        self.robo_ylos = False
        self.robo_alas = False
 
        self.kolikko_x = random.randint(0, 640-self.kolikko.get_width())
        self.kolikko_y = random.randint(0, 480-self.kolikko.get_height())
 
        self.seuraava_morko_x = 0
        self.seuraava_morko_y = 0
 
        self.morko_x = 0
        self.morko_y = 0
        self.morko_nopeus_x = 2
        self.morko_nopeus_y = 2
        
 
        self.laskuri = 0
 
    # Robotin liikkuminen 4 suuntaan
    def robo_liikuta(self, tapahtuma):
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_LEFT:
                self.robo_vasemmalle = True
            if tapahtuma.key == pygame.K_RIGHT:
                self.robo_oikealle = True
            if tapahtuma.key == pygame.K_UP:
                self.robo_ylos = True
            if tapahtuma.key == pygame.K_DOWN:
                self.robo_alas = True
 
        if tapahtuma.type == pygame.KEYUP:
            if tapahtuma.key == pygame.K_LEFT:
                self.robo_vasemmalle = False
            if tapahtuma.key == pygame.K_RIGHT:
                self.robo_oikealle = False
            if tapahtuma.key == pygame.K_UP:
                self.robo_ylos = False
            if tapahtuma.key == pygame.K_DOWN:
                self.robo_alas = False
 
    # Mörkö joka seuraa robottia
    def liikuta_seuraavaa_morkoa(self):
        if self.seuraava_morko_x > self.robo_x:
            self.seuraava_morko_x -= 1
        if self.seuraava_morko_x < self.robo_x:
            self.seuraava_morko_x += 1
        if self.seuraava_morko_y > self.robo_y:
            self.seuraava_morko_y -= 1
        if self.seuraava_morko_y < self.robo_y:
            self.seuraava_morko_y += 1
 
    # Funktio jolla pidetään robo rajojen sisällä
    def tsekkaa_rajat(self):
        if self.robo_oikealle and self.robo_x+self.robo.get_width() <= 640:
            self.robo_x += 2
        if self.robo_vasemmalle and self.robo_x >= 0:
            self.robo_x -= 2
        if self.robo_ylos and self.robo_y >= 0:
            self.robo_y -= 2
        if self.robo_alas and self.robo_y+self.robo.get_height() <= 480:
            self.robo_y += 2
 
    # Tsekataan onko jomman kumman mörön keskipiste robotin sisällä. Jos on niin kuolema koittaa.
    def tsekkaa_kuolitko(self):
        eka_morko = (self.morko_x+self.morko.get_height()/2, self.morko_y+self.morko.get_width()/2)
        toka_morko = (self.seuraava_morko_x+self.morko.get_height()/2, self.seuraava_morko_y+self.morko.get_width()/2)
 
        if self.robo_x <= eka_morko[0] <= (self.robo_x+self.robo.get_width()) and self.robo_y <= eka_morko[1] <= (self.robo_y+self.robo.get_height()):
            self.loppu = True
        if self.robo_x <= toka_morko[0] <= (self.robo_x+self.robo.get_width()) and self.robo_y <= toka_morko[1] <= (self.robo_y+self.robo.get_height()):
            self.loppu = True
 
    # Arvotaan kolikolle uusi satunnainen paikka, jos kolikon keskipiste on robon rajojen sisällä.
    def tsekkaa_saitko_kolikon(self):
        kolikon_x = self.kolikko_x+self.kolikko.get_width()/2
        kolikon_y = self.kolikko_y+self.kolikko.get_height()/2
        if self.robo_x <= kolikon_x <= (self.robo_x+self.robo.get_width()) and self.robo_y <= kolikon_y <= (self.robo_y+self.robo.get_height()):
            self.uusi_kolikko()
            self.laskuri += 1
    
    # Kolikon paikan arvonta.
    def uusi_kolikko(self):
        self.kolikko_x = random.randint(0, 640-self.kolikko.get_width())
        self.kolikko_y = random.randint(0, 480-self.kolikko.get_height())
 
    # Tsekataan toiminnot.
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            self.robo_liikuta(tapahtuma)
 
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_p:
                    self.alku = False
                    self.loppu = False
                    self.nollaa_arvot()
                if tapahtuma.key == pygame.K_ESCAPE:
                    self.loppu = True
            if tapahtuma.type == pygame.QUIT:
                exit()
 
    def piirra_alkunaytto(self):
        alkuteksti = self.alkufontti.render("Vie möröiltä joulurahat!", True, (0, 100, 0))
        alkuteksti2 = self.alkufontti.render("Varasta mahdollisimman monta kolikkoa", True, (0, 100, 0))
        alkuteksti3 = self.alkufontti.render("ennen kuin mörkö saa sinut kiinni!", True, (0, 100, 0))
        alkuteksti4 = self.pelifontti.render("Pelaa painamalla P. Lopeta painamalla ESC", True, (0, 0, 200))
 
        self.naytto.fill((255, 0, 0))
        self.naytto.blit(alkuteksti, (150, 150))
        self.naytto.blit(alkuteksti2, (80, 200))
        self.naytto.blit(alkuteksti3, (90, 250))
        self.naytto.blit(alkuteksti4, (100, 400))
 
        pygame.display.flip()
 
 
    def piirra_pelinaytto(self):
        pisteteksti = self.pelifontti.render("Kolikoita:" + str(self.laskuri), True, (255, 0, 0))
        self.naytto.fill((0, 100, 0))
        self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
        self.naytto.blit(self.morko, (self.morko_x, self.morko_y))
        self.naytto.blit(self.morko, (self.seuraava_morko_x, self.seuraava_morko_y))
        self.naytto.blit(self.kolikko, (self.kolikko_x, self.kolikko_y))
        self.naytto.blit(pisteteksti, (540, 20))
        pygame.display.flip()
 
    def piirra_loppunaytto(self):
        lopputeksti = self.alkufontti.render("Voi voi, jäit kiinni varas!", True, (255, 0, 0))
        if self.laskuri == 0:
            lopputeksti2 = self.alkufontti.render("Et saanut yhtään kolikkoa!", True, (255, 0, 0))
            lopputeksti3 = self.alkufontti.render("Se on hyvä, ei jouluna sovikaan varastaa", True, (255, 0, 0))
        elif self.laskuri < 10:
            lopputeksti2 = self.alkufontti.render("Ehdit saada " + str(self.laskuri) + " kolikkoa.", True, (255, 0, 0))
            lopputeksti3 = self.alkufontti.render("Ihan hyvä, jäi möröillekin vähän pesämunaa.", True, (255, 0, 0))
        else:
            lopputeksti2 = self.alkufontti.render("Ehdit saada " + str(self.laskuri) + " kolikkoa!", True, (255, 0, 0))
            lopputeksti3 = self.alkufontti.render("Taitaa möröille tulla laiha joulu!", True, (255, 0, 0))
 
        lopputeksti4 = self.pelifontti.render("Paina P jos haluat pelata uudestaan", True, (0, 0, 200))
 
        self.naytto.fill((0, 0, 0))
        self.naytto.blit(lopputeksti, (80, 150))
        self.naytto.blit(lopputeksti2, (80, 200))
        self.naytto.blit(lopputeksti3, (80, 250))
        self.naytto.blit(lopputeksti4, (100, 400))
        pygame.display.flip()
 
    # Pomppivan mörön liikkuminen.
    def liikuta_morko(self):
        self.morko_y += self.morko_nopeus_y
        self.morko_x += self.morko_nopeus_x
 
        if self.morko_nopeus_x > 0 and self.morko_x+self.morko.get_width() >= 640:
            self.morko_nopeus_x = -self.morko_nopeus_x
        if self.morko_nopeus_x < 0 and self.morko_x <= 0:
            self.morko_nopeus_x = -self.morko_nopeus_x
        if self.morko_nopeus_y > 0 and self.morko_y+self.morko.get_height() >= 480:
            self.morko_nopeus_y = -self.morko_nopeus_y
        if self.morko_nopeus_y < 0 and self.morko_y <= 0:
            self.morko_nopeus_y = -self.morko_nopeus_y
 
    # Pelilooppi. alun alku- ja loppumuuttujien avulla kontrolloidaan piirretäänkö alku-, loppu- vai pelinäyttö.
    def silmukka(self):
        while True:
 
            if self.alku == True:
                self.tutki_tapahtumat()
                self.piirra_alkunaytto()
                
                
            elif self.loppu == True:
                self.tutki_tapahtumat()
                self.piirra_loppunaytto()
                
            else:
 
                self.tutki_tapahtumat()
                self.tsekkaa_rajat()
                self.piirra_pelinaytto()
                self.liikuta_morko()
                self.liikuta_seuraavaa_morkoa()
                self.tsekkaa_kuolitko()
                self.tsekkaa_saitko_kolikon()
                self.kello.tick(60)
 
 
if __name__ == "__main__":
    Robopeli()


Robopeli()
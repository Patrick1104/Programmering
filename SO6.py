import tkinter as tk
import tkinter.ttk as ttk
import time
import random
n = 25



class Ung(object):
    # Constructor: laver en ny "ung" person
    def __init__(self, canvas, x, y, fill):
        # Bestemmer cirklernes parametre og størrelser
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')

        self.x = x
        self.y = y
        self.infected = False
        self.immunity = False
        self.healthy = True
        self.isolate = False
        self.immunitytimer = 0
        self.countdowntimer = 0 

    def isolate(self):
        self.immune()

    # Bestemmer hvordan, og hvor hurtigt agenterne "går"
    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        a = 2
        if self.isolate:
            a = 0
        dx = random.choice([-a, a])
        dy = random.choice([-a, a])

    # Definere isolation og dens atributter
    

        #self.canvas.move(self.id, dx, dy)
        self.x = self.x + dx
        self.y = self.y + dy

        # Laver en border
        if self.x < 10:
            self.x = 10

        if self.x > 740:
            self.x = 740

        if self.y < 10:
            self.y = 10

        if self.y > 740:
            self.y = 740

        r = 4
        self.canvas.coords(self.id, self.x-r, self.y-r, self.x+r, self.y+r)

    # Checker om en ung er inficieret
    def check_infected(self, persons):
        if self.immunitytimer > 0:
            self.immunitytimer -=1
            if self.immunitytimer == 0:
                self.immunity = False
                self.canvas.itemconfig(self.id, fill='black')

        if self.countdowntimer > 0:
            self.countdowntimer -=1
            if self.countdowntimer == 0:
                self.countdowntimer +=2
                if random.random()>0.1:
                    #self.immune()
                    self.infect()

        for ung in persons:
            d = ((self.x - ung.x)**2 + (self.y - ung.y)**2)**(1/2)

            # Bestemmer den rækkevidde for, hvor tæt på de skal være på en inficeeret for at blive inficeret
            if d < 200 and ung.infected == True and not self.immune and not self.healthy:
                if random.random()>0.5:
                    self.infect()
                    self.healthy = False
                else: 
                    self.immune(50)

    # Giver farven til en inficeret
    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.id, fill='lime green')
    
    # Definere imunitet og dens atributter
    def immune(self, t):
        self.immunity = True
        self.immunitytimer = t
        self.infected = False
        self.canvas.itemconfig(self.id, fill='red')
    
    




class Voksen(object):

    def __init__(self, canvas, x, y, fill):
        
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')

        self.x = x
        self.y = y
        self.infected = False

    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        dx = random.choice([-2, 2])
        dy = random.choice([-2, 2])

        if self.x < 10:
            self.x = 10

        if self.x > 740:
            self.x = 740

        if self.y < 10:
            self.y = 10

        if self.y > 740:
            self.y = 740

        self.x = self.x + dx
        self.y = self.y + dy

        r = 4
        self.canvas.coords(self.id, self.x-r, self.y-r, self.x+r, self.y+r)    

        

    def check_infected(self, persons):
        for voksen in persons:
            d = ((self.x - voksen.x)**2 + (self.y - voksen.y)**2)**(1/2)

            if d < 20 and voksen.infected == True:
                self.infect()

    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.id, fill='green')

class Ældre(object):
    
    def __init__(self, canvas, x, y, fill):
        
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')

        self.x = x
        self.y = y
        self.infected = False

    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        dx = random.choice([-2, 2])
        dy = random.choice([-2, 2])


        self.x = self.x + dx
        self.y = self.y + dy

        if self.x < 10:
            self.x = 10

        if self.x > 740:
            self.x = 740

        if self.y < 10:
            self.y = 10

        if self.y > 740:
            self.y = 740

        r = 4
        self.canvas.coords(self.id, self.x-r, self.y-r, self.x+r, self.y+r)

    def check_infected(self, persons):
        for ældre in persons:
            d = ((self.x - ældre.x)**2 + (self.y - ældre.y)**2)**(1/2)

            if d < 20 and ældre.infected == True:
                self.infect()

    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.id, fill='yellow')





class App(object):
    def __init__(self, master, **kwargs):

        # Bestemmer "spillefladen" som kan ses
        self.master = master
        self.canvas = tk.Canvas(self.master, width=750, height=750,background='white')
        self.canvas.pack()

        # Laver en "reset" knap
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)

        # Start / init simulationen
        self.init_sim()

        self.master.after(0, self.update)
        self.frame=0

    def update(self):

        SU = 0

        for u in self.persons:
            if isinstance(u, Ung) and not u.infected:
                SU += 1

        print(SU)


        # Køre / genstarter "move" ligningen
        for u in self.persons:
            u.move()
            u.check_infected(self.persons)



        self.master.after(100, self.update)
        self.frame += 1

    # Når simulationen starter, bestemmer den hvor agenterne generere
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        for i in range(n):
            x = random.randint(0,750)
            y = random.randint(0,750)
            u = Ung(self.canvas, x, y, 'Black')
            x = random.randint(0,750)
            y = random.randint(0,750)
            v = Voksen(self.canvas, x, y, 'blue')
            x = random.randint(0,750)
            y = random.randint(0,750)
            æ = Ældre(self.canvas, x, y, 'brown')
            # Bestemmer "risikoen" for en agent generere inficeret
            if random.uniform(0,1) < 0.05:
                u.infect()
                v.infect()
                æ.infect()

            self.persons.append(u)
            self.persons.append(v)
            self.persons.append(æ)
    

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))
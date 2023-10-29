#Librerie
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

#File
file_inventario = "./magazzino/inventario.csv"
file_transazioni = "./magazzino/transazioni.csv"

#Magazzino
class Magazzino():
    def __init__(self):
        self.inventario = self.leggi_inventario()

    def leggi_inventario(self):
        try:
            inventario = {}
            with open(file_inventario, "r") as file:
                testo = csv.reader(file)
                for riga in testo:
                    oggetto, quantità = riga
                    inventario[oggetto] = int(quantità)
            return inventario
        except:
            self.genera_errore("Errore nella lettura dell'inventario")

    def genera_errore(self, messaggio):
        messagebox.showwarning("Errore", messaggio)

    def aggiungi_oggetto(self, oggetto, quantità):
        if oggetto in self.inventario.keys():
            self.inventario[oggetto] += quantità
        else:
            self.inventario[oggetto] = quantità
        self.aggiorna_inventario()
        data = datetime.now().strftime("%d:%m:%Y")
        self.scrivi_transazione(data, "Entrata", oggetto, quantità, None)

    def rimuovi_oggetto(self, oggetto, quantità, destinatario):
        self.inventario[oggetto] -= quantità
        if self.inventario[oggetto] == 0:
            self.inventario.pop(oggetto)
        self.aggiorna_inventario()
        data = datetime.now().strftime("%d:%m:%Y")
        self.scrivi_transazione(data, "Uscita", oggetto, quantità, destinatario)
        
    def aggiorna_inventario(self):
        try:
            testo = []
            with open(file_inventario, "w") as file:
                scrittore = csv.writer(file)
                for chiave in self.inventario:
                    testo.append([chiave, self.inventario[chiave]])
                scrittore.writerows(testo)
        except:
            self.genera_errore("Errore nella scrittura dell'inventario")

    def scrivi_transazione(self, data, tipo, oggetto, quantità, destinatario):
        try:
            riga = [data, tipo, oggetto, quantità]
            if(tipo == "Uscita"):
                riga.append(destinatario)
            with open(file_transazioni, "a") as file:
                scrittore = csv.writer(file)
                scrittore.writerow(riga)
        except:
            self.genera_errore("Errore nella scrittura della transazione")

#App
class App:
    def __init__(self, root, magazzino):
        self.root = root
        self.magazzino = magazzino

        root.title("Inventario")

        self.label_oggetto = tk.Label(root, text = "Oggetto:")
        self.label_oggetto.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.entry_oggetto = tk.Entry(root)
        self.entry_oggetto.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.label_quantità = tk.Label(root, text = "Quantità:")
        self.label_quantità.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.entry_quantità = tk.Entry(root)
        self.entry_quantità.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.label_destinatario = tk.Label(root, text = "Destinatario:")
        self.label_destinatario.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.entry_destinatario = tk.Entry(root)
        self.entry_destinatario.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.add_button = tk.Button(root, text = "Aggiungi", command = self.aggiungi_oggetto)
        self.add_button.grid(row = 3, column = 0, padx = 5, pady = 5)

        self.remove_button = tk.Button(root, text = "Rimuovi", command = self.rimuovi_oggetto)
        self.remove_button.grid(row = 4, column = 0, padx = 5, pady = 5)

    def aggiungi_oggetto(self):
        try:
            quantità = int(self.entry_quantità.get())
        except ValueError:
            messagebox.showwarning("Attenzione", "Inserire una quantità valida")
            return
        try:
            oggetto = self.entry_oggetto.get()
            
            if not oggetto.strip():
                messagebox.showwarning("Attenzione", "Inserire un oggetto")
                return
        
            if quantità <= 0:
                messagebox.showwarning("Attenzione", "Inserire una quantità positiva")
            else:
                self.magazzino.aggiungi_oggetto(oggetto, quantità)
                self.entry_oggetto.delete(0, tk.END)
                self.entry_quantità.delete(0, tk.END)
                messagebox.showinfo("Info", "Oggetto aggiunto correttamente")
        except:
            messagebox.showinfo("Attenzione", "Inserire oggetto e quantità")
    
    def rimuovi_oggetto(self):
        try:
            quantità = int(self.entry_quantità.get())
        except ValueError:
            messagebox.showwarning("Attenzione", "Inserire una quantità valida")
            return
        try:
            oggetto = self.entry_oggetto.get()

            if not oggetto.strip():
                messagebox.showwarning("Attenzione", "Inserire un oggetto")
                return
            
            if oggetto not in self.magazzino.inventario:
                messagebox.showwarning("Attenzione", "Oggetto non presente nell'inventario")
                return
            
            destinatario = self.entry_destinatario.get()

            if not destinatario.strip():
                messagebox.showwarning("Attenzione", "Inserire un destinatario")
                return

            if quantità <= 0:
                messagebox.showwarning("Attenzione", "Inserire una quantità positiva")
                return
            
            if quantità > self.magazzino.inventario[oggetto]:
                messagebox.showwarning("Attenzione", "Quantità non disponibile")
                return

            self.magazzino.rimuovi_oggetto(oggetto, quantità, destinatario)
            self.entry_oggetto.delete(0, tk.END)
            self.entry_quantità.delete(0, tk.END)
            self.entry_destinatario.delete(0, tk.END)
            messagebox.showinfo("Info", "Oggetto rimosso correttamente")

        except:    
            messagebox.showinfo("Attenzione", "Inserire oggetto, quantità e destinatario validi")
    
#Main
def main():
    magazzino = Magazzino()
    root = tk.Tk()
    app = App(root, magazzino)
    root.mainloop()

#Esecuzione
if __name__ == "__main__":
    main()
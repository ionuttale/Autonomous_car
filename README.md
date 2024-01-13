Executarea programului:
	
	Pentru a putea rula proiectul trebuie să se urmărească următorii pași:
1.	se clonează branch-ul server pe dispozitivul ce urmează a fi folosit ca server:

	git clone –branch server https://github.com/ionuttale/autonomous_car.git

2.	se clonează branch-ul self_driving_car pe raspberry:

	git clone –branch self_driving car https://github.com/ionuttale/autonomous_car.git
    
3.	se importă modulele necesare folosind comanda pip install -r requirements.txt atât în terminalul de pe server, cât și în terminalul de pe raspberry
4.	se modifică adresa IP a server-ului și a raspberry-ului din fișierele server.py și main.py
5.	se rulează comanda python3 server.py în terminalul server-ului. 
	
	*Dacă nu funcționează comanda precizată, se recomandă folosirea unui IDE (ex. VSCODE) și rularea sa folosind butonul RUN*

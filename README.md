# kmboxNet per Python
La libreria kmboxNet offre un'interfaccia per programmare controlli di input fisici per tastiera e mouse via rete, utilizzabile in ambienti Python. Questa guida fornisce una panoramica su come configurare e utilizzare kmboxNet per i tuoi progetti.

## Introduzione
kmboxNet è progettata per consentire ai programmatori Python di simulare azioni fisiche di tastiera e mouse in maniera programmatica. Che tu stia sviluppando automazioni per test o creando interazioni complesse per applicazioni, kmboxNet offre gli strumenti necessari per integrare controlli fisici nel tuo software.

## Installazione Fisica e Configurazione Iniziale
Per utilizzare kmboxNet, è necessario seguire alcuni passaggi iniziali per configurare correttamente il dispositivo con il tuo PC. Questi passaggi garantiscono che il dispositivo sia pronto per comunicare con i tuoi script Python.

## Collegamento Hardware

-Collegamento Cavi: Collega i due cavi blu forniti dal dispositivo al tuo PC. Questi cavi sono essenziali per stabilire la connessione tra il dispositivo kmboxNet e il PC.
-Connessione Dispositivi di Input: Collega il mouse, la tastiera, o entrambi, al dispositivo kmboxNet secondo le tue necessità operative.

## Configurazione Software
La prima volta che il dispositivo viene connesso al PC, verrà riconosciuto come un dispositivo di memoria. Segui questi passi per configurare il software necessario:

-Installazione Software: Apri il dispositivo di memoria nel tuo esploratore file e trova l'eseguibile fornito (ad esempio, setup.exe o un nome simile). Esegui questo file per installare il software necessario per kmboxNet sul tuo PC.

-Configurazione Automatica: Dopo aver completato l'installazione, avvia kmNet auto config per configurare automaticamente il dispositivo. Questo passaggio è cruciale per assicurare che il dispositivo sia pronto per essere utilizzato con i tuoi script Python.

## Verifica Installazione
Una volta completata la configurazione software, il dispositivo kmboxNet è pronto all'uso. Puoi iniziare a integrare le funzioni della libreria nei tuoi progetti Python per automatizzare e controllare dispositivi di input fisici.puoi verificare nel cmd usando il comando “ping 192.168.2.188”


## Configurazione
Prima di iniziare, assicurati di copiare il file kmNet_xxxxx.pyd nella directory del codice sorgente del tuo progetto, dove xxxxx indica la versione e la piattaforma specifica di Python che stai utilizzando.

## Requisiti
Python 3.x
Windows OS (64 bit)
Installazione
Rinomina il file kmNet.cp311-win_amd64.pyd in kmNet.pyd per uniformarlo al tuo ambiente Python.
Assicurati che tutti i cavi siano correttamente collegati prima di procedere.

## Funzioni Dettagliate

Di seguito, troverai una panoramica dettagliata delle funzioni disponibili in kmboxNet e come utilizzarle nel tuo progetto Python.

## Inizializzazione

init(ip, port, UUID): Inizializza la connessione al dispositivo. Deve essere chiamata una volta all'inizio.
ip: Indirizzo IP del dispositivo.
port: Numero di porta.
UUID: Identificativo unico del dispositivo.

## Controllo Mouse

move(x, y): Sposta il mouse in modo relativo alle coordinate specificate.

move_auto(x, y, duration): Sposta il mouse verso le coordinate specificate con un movimento che simula l'azione umana, entro il tempo (in millisecondi) definito da duration.

move_beizer(x, y, duration, cx1, cy1, [cx2, cy2]): Sposta il mouse lungo una curva di Bézier specificata dai punti di controllo.

left(state): Controlla lo stato del pulsante sinistro del mouse (state può essere 0 per rilascio o 1 per pressione).

right(state): Controlla lo stato del pulsante destro del mouse.

middle(state): Controlla lo stato del pulsante centrale del mouse.

wheel(direction): Simula il movimento della rotellina del mouse. Valori positivi per scroll verso l'alto, negativi verso il basso.

## Controllo Tastiera
keydown(key): Simula la pressione di un tasto della tastiera.
keyup(key): Simula il rilascio di un tasto della tastiera.

## Monitoraggio e Blocco
monitor(enable): Abilita o disabilita il monitoraggio dello stato fisico di tasti e mouse (enable può essere 0 o 1).
isdown_left(), isdown_right(), isdown_middle(), isdown_side1(), isdown_side2(): Verificano se il rispettivo pulsante del mouse è premuto al momento della chiamata.



esempi su come utilizzare le funzioni principali:


""# Inizializzazione
kmNet.init('192.168.1.100', '8080', 'UUID-UNICO-DEL-DISPOSITIVO')

# Movimento mouse
kmNet.move(100, 100)  # Movimento immediato
kmNet.move_auto(1920, 1080, 200)  # Movimento simula azione umana

# Pressione e rilascio tasti mouse
kmNet.left(1)  # Premi
kmNet.left(0)  # Rilascia

# Pressione e rilascio tasti tastiera
kmNet.keydown(0x04)  # Tasto 'A'
kmNet.keyup(0x04)

# Monitoraggio e blocco
kmNet.monitor(1)  # Abilita monitoraggio
print(kmNet.isdown_left())  # Controlla stato pulsante sinistro""


Assicurati di sostituire i valori come l'indirizzo IP, il numero di porta e l'UUID con quelli specifici del tuo dispositivo.

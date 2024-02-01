'''
Test della velocità di chiamata al movimento del mouse ok
'''
import kmNet # importa il modulo kmNet
import time
kmNet.init('192.168.2.188','8320','24875054') # connessione al dispositivo
# seguente è il tempo impiegato da python per chiamare 10000 volte la funzione di movimento del mouse
t1 = time.time()
cnt = 10000
while cnt > 0:
    kmNet.move(0, 10)
    cnt = cnt - 1
    kmNet.move(0, -10)
    cnt = cnt - 1

t2 = time.time()
print('10000 chiamate impiegano %s ms' % ((t2 - t1) * 1000))


'''
Monitoraggio fisico del mouse ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connessione al dispositivo
kmNet.monitor(10000) # abilita la funzione di monitoraggio della tastiera e del mouse
while 1:
    if kmNet.isdown_left():
        print('il tasto sinistro è premuto')
    if kmNet.isdown_right():
        print("il tasto destro è premuto")
    if kmNet.isdown_middle():
        print("il tasto centrale è premuto")
    if kmNet.isdown_side1():
        print('il tasto laterale 1 è premuto')
    if kmNet.isdown_side2():
        print("il tasto laterale 2 è premuto")
    time.sleep(0.5)


'''
Monitoraggio fisico della tastiera ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connessione al dispositivo
kmNet.monitor(10000) # abilita la funzione di monitoraggio della tastiera e del mouse
while 1:
    if kmNet.isdown_keyboard(4) == 1: # 4 è il codice del tasto A della tastiera
        print('il tasto A è premuto') # il tasto A è premuto
    time.sleep(0.5)


'''
Test di blocco ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connessione al dispositivo
kmNet.monitor(10000) # abilita la funzione di monitoraggio della tastiera e del mouse
kmNet.mask_keyboard(4) # blocca il tasto A della tastiera, premendo A non succederà nulla, ma sarà possibile rilevarne la pressione
while 1:
    if kmNet.isdown_keyboard(4) == 1: # 4 è il codice del tasto A della tastiera
        print('il tasto A è premuto') # il tasto A è premuto
    time.sleep(0.5)


'''
Test di visualizzazione immagine fallito --- c'è qualche problema.
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connessione al dispositivo
pic = bytearray(gImage_128x80) # ci sono problemi
kmNet.lcd_picture(pic)

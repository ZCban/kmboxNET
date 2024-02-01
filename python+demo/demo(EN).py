'''
Mouse movement call speed test ok
'''
import kmNet # import kmNet module
import time
kmNet.init('192.168.2.188','8320','24875054') # connect to the box
# Below is the time it takes for python to call the mouse movement function 10000 times
t1 = time.time()
cnt = 10000
while cnt > 0:
    kmNet.move(0, 10)
    cnt = cnt - 1
    kmNet.move(0, -10)
    cnt = cnt - 1

t2 = time.time()
print('Time for 10000 calls %s ms' % ((t2 - t1) * 1000))


'''
Mouse physical monitoring ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connect to the box
kmNet.monitor(10000) # enable keyboard and mouse monitoring function
while 1:
    if kmNet.isdown_left():
        print('left button is down')
    if kmNet.isdown_right():
        print("right button is down")
    if kmNet.isdown_middle():
        print("middle button is down")
    if kmNet.isdown_side1():
        print('side1 button is down')
    if kmNet.isdown_side2():
        print("side2 button is down")
    time.sleep(0.5)


'''
Keyboard physical monitoring ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connect to the box
kmNet.monitor(10000) # enable keyboard and mouse monitoring function
while 1:
    if kmNet.isdown_keyboard(4) == 1: # 4 is the keycode for the 'A' key
        print('A key is down') # A key is pressed
    time.sleep(0.5)


'''
Blocking test ok
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connect to the box
kmNet.monitor(10000) # enable keyboard and mouse monitoring function
kmNet.mask_keyboard(4) # block the 'A' key, pressing A will have no effect but it can be detected as pressed
while 1:
    if kmNet.isdown_keyboard(4) == 1: # 4 is the keycode for the 'A' key
        print('A key is down') # A key is pressed
    time.sleep(0.5)


'''
Image display test failed --- there's some problem.
'''
import kmNet
import time
kmNet.init('192.168.2.188','12545','F101383B') # connect to the box
pic = bytearray(gImage_128x80) # there are problems
kmNet.lcd_picture(pic)

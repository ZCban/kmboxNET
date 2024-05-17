// kmNetLib.cpp : This file contains the "main" function. Program execution begins and ends there.
//

#include <iostream>
#include <stdio.h>
#include <Winsock2.h>
#include "math.h"
#include "NetConfig/kmboxNet.h"
#include "NetConfig/HidTable.h"
#include "picture.h"

#pragma warning(disable : 4996)

int main() {
    int ret;

    // Initial connection test - Must connect successfully before using other APIs
    printf("---------------- This program is a demo for kmboxNet version call test --------------\r\n");
    ret = kmNet_init((char*)"192.168.2.188", (char*)"8338", (char*)"24ba5054"); // Connect to the box
    // If this function does not return, it means IP or UUID is incorrect. Please check if it matches the display on the box screen

    kmNet_monitor(10000); // Use port 10000 to monitor physical keyboard and mouse messages, ensure the port does not conflict with other programs
    Sleep(1000);

    while (true) {
        if (kmNet_monitor_mouse_left() == 1) { // If the left mouse button is pressed
            printf("Left mouse button pressed\r\n");
            while (kmNet_monitor_mouse_left() == 1) Sleep(1); // Wait for the left button to be released
            kmNet_monitor(0); // Disable monitoring
        }
        Sleep(1); // Sleep to avoid high CPU usage
    }

    printf("Call speed test, please wait about 10 seconds...\r\n");
    int cnt = 10000;
    long startime = GetTickCount();
    while (cnt > 0) {
        ret = kmNet_mouse_move(0, -100); cnt--;
        if (ret)
            printf("tx error %d  ret0=%d\r\n", cnt, ret);
        ret = kmNet_mouse_move(0, 100);  cnt--;
        if (ret)
            printf("tx error %d  ret1=%d\r\n", cnt, ret);
    }
    printf("\t10000 calls took = %ld ms\r\n", GetTickCount() - startime);

    printf("Display test:\r\n");
    while (1) {
        startime = GetTickCount();
        kmNet_lcd_color(0);
        printf("\tFull screen solid color fill took = %ld ms\r\n", GetTickCount() - startime);
        startime = GetTickCount();
        kmNet_lcd_picture_bottom(gImage_128x80); // Display 128x80 image on the bottom half
        printf("\tHalf screen picture refresh took = %ld ms\r\n", GetTickCount() - startime);
        startime = GetTickCount();
        kmNet_lcd_picture(gImage_128x160); // Display 128x160 image on the full screen
        printf("\tFull screen picture refresh took = %ld ms\r\n", GetTickCount() - startime);
        break;
    }

#if 0
    kmNet_init((char*)"192.168.2.166", (char*)"1234", (char*)"F101383B"); // Connect to the box
    printf("Change box IP address\r\n");
    kmNet_setconfig((char*)"192.168.2.166", 1234);
    printf("Reboot is required to take effect\r\n");
    kmNet_reboot();
#endif

    // Physical keyboard and mouse monitoring function test
    printf("Physical keyboard and mouse monitoring function, press left, middle, and right buttons to exit the test\r\n");
    printf("Note: If you cannot monitor the key information, please turn off the Windows firewall\r\n");
    kmNet_monitor(1000); // Enable keyboard and mouse monitoring function, listening port is 1000
    int exit = 0;
    while ((exit & 0x07) != 0x07) {
        // Mouse button detection
        if (kmNet_monitor_mouse_left() == 1) { // Left mouse button pressed
            printf("Left mouse button pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_mouse_left() == 1); // Wait for the left button to be released
            printf("Left mouse button released\r\n");
            exit |= 0x01;
        }

        if (kmNet_monitor_mouse_middle() == 1) { // Middle mouse button pressed
            printf("Middle mouse button pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_mouse_middle() == 1); // Wait for the middle button to be released
            printf("Middle mouse button released\r\n");
            exit |= 0x02;
        }

        if (kmNet_monitor_mouse_right() == 1) { // Right mouse button pressed
            printf("Right mouse button pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_mouse_right() == 1); // Wait for the right button to be released
            printf("Right mouse button released\r\n");
            exit |= 0x04;
        }

        if (kmNet_monitor_mouse_side1() == 1) { // Side mouse button 1 pressed
            printf("Side mouse button 1 pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_mouse_side1() == 1); // Wait for side button 1 to be released
            printf("Side mouse button 1 released\r\n");
            exit |= 0x08;
        }

        if (kmNet_monitor_mouse_side2() == 1) { // Side mouse button 2 pressed
            printf("Side mouse button 2 pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_mouse_side2() == 1); // Wait for side button 2 to be released
            printf("Side mouse button 2 released\r\n");
            exit |= 0x10;
        }

        if (kmNet_monitor_keyboard(KEY_A) == 1) { // Keyboard A key pressed
            printf("Keyboard A key pressed\r\n");
            do { Sleep(1); } while (kmNet_monitor_keyboard(KEY_A) == 1); // Wait for the A key to be released
            printf("Keyboard A key released\r\n");
            exit |= 0x20;
        }
        Sleep(1);
    }

    // Simulate artificial trajectory test
    while (true) {
        // Open the drawing tool and press the left mouse button to see the movement trajectory
        if (kmNet_monitor_mouse_left()) { // If the left mouse button is pressed
            startime = GetTickCount();
            ret = kmNet_mouse_move_auto(400, 300, 200); // Expected to complete within 200ms
            printf("\tTime taken = %ld ms ret = %d\r\n", GetTickCount() - startime, ret); // Actual time taken
            while (kmNet_monitor_mouse_left()) Sleep(1); // Wait for the left button to be released
        }
        Sleep(1); // Sleep to avoid high CPU usage
    }

    // Additional examples of key presses and mouse movements
    printf("Simulate mouse click and key press examples:\r\n");

    // Simulate left mouse click
    printf("Simulating left mouse click...\r\n");
    kmNet_mouse_left(1); // Press left mouse button
    Sleep(100); // Hold for 100ms
    kmNet_mouse_left(0); // Release left mouse button
    Sleep(100);

    // Simulate right mouse click
    printf("Simulating right mouse click...\r\n");
    kmNet_mouse_right(1); // Press right mouse button
    Sleep(100); // Hold for 100ms
    kmNet_mouse_right(0); // Release right mouse button
    Sleep(100);

    // Simulate middle mouse click
    printf("Simulating middle mouse click...\r\n");
    kmNet_mouse_middle(1); // Press middle mouse button
    Sleep(100); // Hold for 100ms
    kmNet_mouse_middle(0); // Release middle mouse button
    Sleep(100);


    // Simulate mouse movement
    printf("Simulating mouse movement...\r\n");
    kmNet_move(100, 0); // Move mouse right
    Sleep(100);
    kmNet_move(-100, 0); // Move mouse left
    Sleep(100);
    kmNet_move_auto((100, 0),200)//simulate human mouse movement

    // Re-enable physical mouse monitoring
    kmNet_monitor(1); // Enable keyboard and mouse monitoring function

#if 0 // Mask mouse test
    printf("Physical keyboard and mouse masking test:\r\n");
    kmNet_monitor(1); // Enable keyboard and mouse monitoring function
    kmNet_mask_mouse_left(1); // Mask left mouse button
    kmNet_mask_mouse_middle(1); // Mask middle mouse button
    kmNet_mask_mouse_right(1); // Mask right mouse button
    kmNet_mask_mouse_side1(1); // Mask side mouse button 1
    kmNet_mask_mouse_side2(1); // Mask side mouse button 2
    kmNet_mask_mouse_x(1); // Mask mouse x direction
    kmNet_mask_mouse_y(1); // Mask mouse y direction -- with the above code enabled, the mouse is basically useless
    kmNet_mask_keyboard(KEY_A); // Mask keyboard A key
    int timeout = 1000;
    while (true) { // Exit after 10 seconds
        if (kmNet_monitor_mouse_left()) { // If the physical left mouse button is pressed
            printf("Physical left mouse button pressed\r\n");
            while (kmNet_monitor_mouse_left()) Sleep(1); // Wait for the left button to be released
        }
        if (kmNet_monitor_mouse_middle()) { // If the physical middle mouse button is pressed
            printf("Physical middle mouse button pressed\r\n");
            while (kmNet_monitor_mouse_middle()) Sleep(1); // Wait for the middle button to be released
        }
        if (kmNet_monitor_mouse_right()) { // If the physical right mouse button is pressed
            printf("Physical right mouse button pressed\r\n");
            while (kmNet_monitor_mouse_right()) Sleep(1); // Wait for the right button to be released
        }
        if (kmNet_monitor_mouse_side1()) { // If the physical side mouse button 1 is pressed
            printf("Physical side mouse button 1 pressed\r\n");
            while (kmNet_monitor_mouse_side1()) Sleep(1); // Wait for side button 1 to be released
        }

        if (kmNet_monitor_mouse_side2()) { // If the physical side mouse button 2 is pressed
            printf("Physical side mouse button 2 pressed\r\n");
            while (kmNet_monitor_mouse_side2()) Sleep(1); // Wait for side button 2 to be released
        }

        if (kmNet_monitor_keyboard(KEY_A)) {
            printf("Keyboard A key pressed\r\n");
            while (kmNet_monitor_keyboard(KEY_A)) Sleep(1); // Wait for the A key to be released
            printf("Keyboard A key released\r\n");
        }
        Sleep(1); // Sleep to avoid high CPU usage
        if (timeout == 0) break;
        timeout--;
    }
    printf("Unmask all\r\n");
    kmNet_unmask_all(); // Unmask all. Now the keyboard and mouse can be used normally
#endif

#if 0
    kmNet_mouse_left(0); // Release
    kmNet_mouse_all(1, 0, 0, 0); // Press
    kmNet_mouse_all(0, 0, 0, 0); // Release
    kmNet_mouse_right(1); // Press
    // Keyboard key test
    kmNet_keydown(4); // a key press
    kmNet_reboot(); // Reboot the box
    kmNet_mouse_right(0); // Release
    kmNet_mouse_all(2, 0, 0, 0); // Press
    kmNet_mouse_all(0, 0, 0, 0); // Release
    // Middle mouse button test
    kmNet_mouse_middle(1); // Press
    kmNet_mouse_middle(0); // Release
    kmNet_mouse_all(4, 0, 0, 0); // Press
    kmNet_mouse_all(0, 0, 0, 0); // Release
#endif
}

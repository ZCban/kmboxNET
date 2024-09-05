#include <stdio.h>
#include <Winsock2.h>
#include "math.h"
#pragma warning(disable : 4996)

#define 	cmd_connect			0xaf3c2828 
#define     cmd_mouse_move		0xaede7345 
#define		cmd_mouse_left		0x9823AE8D 
#define		cmd_mouse_middle	0x97a3AE8D 
#define		cmd_mouse_right		0x238d8212 
#define		cmd_mouse_wheel		0xffeead38 
#define     cmd_mouse_automove	0xaede7346 
#define     cmd_keyboard_all    0x123c2c2f 
#define		cmd_reboot			0xaa8855aa 
#define     cmd_bazerMove       0xa238455a 
#define     cmd_monitor         0x27388020 
#define     cmd_debug           0x27382021 
#define     cmd_mask_mouse      0x23234343 
#define     cmd_unmask_all      0x23344343 
#define     cmd_setconfig       0x1d3d3323 
#define     cmd_showpic         0x12334883 
#define     cmd_setvidpid       0xffed3232 

extern SOCKET sockClientfd; 
typedef struct
{	
	unsigned int  mac;			
	unsigned int  rand;			
	unsigned int  indexpts;		
	unsigned int  cmd;			
}cmd_head_t;

typedef struct
{
	unsigned char buff[1024];	//
}cmd_data_t;
typedef struct
{
	unsigned short buff[512];	//
}cmd_u16_t;


typedef struct
{
	int button;
	int x;
	int y;
	int wheel;
	int point[10];
}soft_mouse_t;


typedef struct
{
	char ctrl;
	char resvel;
	char button[10];
}soft_keyboard_t;


typedef struct
{
	cmd_head_t head;
	union {
		cmd_data_t      u8buff;		 
		cmd_u16_t       u16buff;	  
		soft_mouse_t    cmd_mouse;    
		soft_keyboard_t cmd_keyboard; 
	};
}client_tx;

enum
{
	err_creat_socket = -9000,	
	err_net_version,		
	err_net_tx,		
	err_net_rx_timeout,		
	err_net_cmd,			
	err_net_pts,			
	success = 0,				
	usb_dev_tx_timeout,		
};




int kmNet_init(char* ip, char* port, char* mac);//ok
int kmNet_reboot(void);
int kmNet_setconfig(char* ip, unsigned short port);		  
int kmNet_setvidpid(unsigned short vid, unsigned short pid);




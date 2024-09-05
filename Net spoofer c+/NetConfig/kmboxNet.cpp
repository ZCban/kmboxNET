#include "kmboxNet.h"

#include <time.h>
#define monitor_ok    2
#define monitor_exit  0
SOCKET sockClientfd  = 0;				
SOCKET sockMonitorfd = 0;				
client_tx tx;							
client_tx rx;							
SOCKADDR_IN addrSrv;
soft_mouse_t    softmouse;				
soft_keyboard_t softkeyboard;			
static int monitor_run = 0;				
static int mask_keyboard_mouse_flag = 0;
static short monitor_port = 0;


#pragma pack(1)
typedef struct {
	unsigned char report_id;
	unsigned char buttons;		
	short x;					
	short y;					
	short wheel;				
}standard_mouse_report_t;

typedef struct {
	unsigned char report_id;
	unsigned char buttons;      
	unsigned char data[10];     
}standard_keyboard_report_t;
#pragma pack()

standard_mouse_report_t		hw_mouse;   
standard_keyboard_report_t	hw_keyboard;


int myrand(int a, int b)
{
	int min = a < b ? a : b;
	int max = a > b ? a : b;
	return ((rand() % (max - min)) + min);
}

unsigned int StrToHex(char* pbSrc, int nLen)
{
	char h1, h2;
	unsigned char s1, s2;
	int i;
	unsigned int pbDest[16] = { 0 };
	for (i = 0; i < nLen; i++) {
		h1 = pbSrc[2 * i];
		h2 = pbSrc[2 * i + 1];
		s1 = toupper(h1) - 0x30;
		if (s1 > 9)
			s1 -= 7;
		s2 = toupper(h2) - 0x30;
		if (s2 > 9)
			s2 -= 7;
		pbDest[i] = s1 * 16 + s2;
	}
	return pbDest[0] << 24 | pbDest[1] << 16 | pbDest[2] << 8 | pbDest[3];
}

int NetRxReturnHandle(client_tx* rx, client_tx* tx)		 
{
	if (rx->head.cmd != tx->head.cmd)
		return  err_net_cmd;
	if (rx->head.indexpts != tx->head.indexpts)
		return  err_net_pts;
	return 0;				


}



int kmNet_init(char* ip, char* port, char* mac)
{
	WORD wVersionRequested;WSADATA wsaData;	int err;
	wVersionRequested = MAKEWORD(1, 1);
	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) 		return err_creat_socket;
	if (LOBYTE(wsaData.wVersion) != 1 || HIBYTE(wsaData.wVersion) != 1) {
		WSACleanup(); sockClientfd = -1;
		return err_net_version;
	}
	srand((unsigned)time(NULL));
	sockClientfd = socket(AF_INET, SOCK_DGRAM, 0);
	addrSrv.sin_addr.S_un.S_addr = inet_addr(ip);
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(atoi(port));
	tx.head.mac = StrToHex(mac, 4);		
	tx.head.rand = rand();				 
	tx.head.indexpts = 0;				 
	tx.head.cmd = cmd_connect;			 
	memset(&softmouse, 0, sizeof(softmouse));	
	memset(&softkeyboard, 0, sizeof(softkeyboard));
	err = sendto(sockClientfd, (const char*)&tx, sizeof(cmd_head_t), 0, (struct sockaddr*)&addrSrv, sizeof(addrSrv));
	Sleep(20);
	int clen = sizeof(addrSrv);
	err = recvfrom(sockClientfd, (char*)&rx, 1024, 0, (struct sockaddr*)&addrSrv, &clen);
	if (err < 0)
		return err_net_rx_timeout;
	return NetRxReturnHandle(&rx, &tx);
}




int kmNet_reboot(void)
{
	int err;
	if (sockClientfd <= 0)		return err_creat_socket;
	tx.head.indexpts++;				
	tx.head.cmd = cmd_reboot;		
	tx.head.rand = rand();			
	int length = sizeof(cmd_head_t);
	sendto(sockClientfd, (const char*)&tx, length, 0, (struct sockaddr*)&addrSrv, sizeof(addrSrv));
	SOCKADDR_IN sclient;
	int clen = sizeof(sclient);
	err = recvfrom(sockClientfd, (char*)&rx, 1024, 0, (struct sockaddr*)&sclient, &clen);
	WSACleanup();
	sockClientfd = -1;
	if (err < 0)
		return err_net_rx_timeout;
	return NetRxReturnHandle(&rx, &tx);

}



int kmNet_setconfig(char* ip, unsigned short port)
{
	int err;
	if (sockClientfd <= 0)		return err_creat_socket;
	tx.head.indexpts++;					
	tx.head.cmd = cmd_setconfig;		
	tx.head.rand = inet_addr(ip); ;
	tx.u8buff.buff[0] = port >> 8;
	tx.u8buff.buff[1] = port >> 0;
	int length = sizeof(cmd_head_t) + 2;
	sendto(sockClientfd, (const char*)&tx, length, 0, (struct sockaddr*)&addrSrv, sizeof(addrSrv));
	SOCKADDR_IN sclient;
	int clen = sizeof(sclient);
	err = recvfrom(sockClientfd, (char*)&rx, 1024, 0, (struct sockaddr*)&sclient, &clen);
	if (err < 0)
		return err_net_rx_timeout;
	return NetRxReturnHandle(&rx, &tx);
}

int kmNet_setvidpid(unsigned short vid, unsigned short pid)
{
	int err;
	if (sockClientfd <= 0)		return err_creat_socket;
	
	tx.head.indexpts++;					
	tx.head.cmd = cmd_setvidpid;		
	tx.head.rand = vid | pid << 16;
	int length = sizeof(cmd_head_t);
	sendto(sockClientfd, (const char*)&tx, length, 0, (struct sockaddr*)&addrSrv, sizeof(addrSrv));
	SOCKADDR_IN sclient;
	int clen = sizeof(sclient);
	err = recvfrom(sockClientfd, (char*)&rx, 1024, 0, (struct sockaddr*)&sclient, &clen);
	return NetRxReturnHandle(&rx, &tx);
}

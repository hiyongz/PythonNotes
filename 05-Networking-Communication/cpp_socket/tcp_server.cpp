#include <stdio.h>  
#include <winsock2.h>  //��ʼ�������̺���

#pragma comment(lib,"ws2_32.lib")  

int main(int argc, char* argv[])
{
	//��ʼ��WSA  
	WORD sockVersion = MAKEWORD(2, 2);
	WSADATA wsaData;//WSADATA��һ�����ݽṹ������ṹ�������洢��WSAStartup�������ú󷵻ص�Windows Sockets���ݡ�������Winsock.dllִ�е����ݡ�
	
    //����winsock�⣬��ʼ��ϵͳ�������Ա��Ժ��������ĺ�������
	if (WSAStartup(sockVersion, &wsaData) != 0)
	{
		return 0;
	}

	//�����׽���(�����Ķ˿�)
	SOCKET slisten = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (slisten == INVALID_SOCKET)
	{
		printf("socket error !");
		return 0;
	}

	//��IP�Ͷ˿�,��sockaddr_in�ṹ��װ���ַ��Ϣ  
	sockaddr_in sin;
	sin.sin_family = AF_INET;
	sin.sin_port = htons(8887); //htons:�������޷��Ŷ�������ת���������ֽ�˳��
	sin.sin_addr.S_un.S_addr = INADDR_ANY;//ָ����ַΪ0.0.0.0�ĵ�ַ
	//�׽��ֺͱ��ص�ַ��
	if (bind(slisten, (LPSOCKADDR)&sin, sizeof(sin)) == SOCKET_ERROR)
	{
		printf("bind error !");
	}

	//��ʼ����  
	if (listen(slisten, 5) == SOCKET_ERROR) //sockfd�����ڱ�ʶһ��������δ�����׽ӿڵ������֡�
											//backlog���ȴ����Ӷ��е���󳤶ȡ�
	{
		printf("listen error !");
		return 0;
	}

	//ѭ����������  
	SOCKET sClient;
	sockaddr_in remoteAddr;
	int nAddrlen = sizeof(remoteAddr);
	char revData[255];
	while (true)
	{
		//printf("�ȴ�����...\n");
		sClient = accept(slisten, (SOCKADDR *)&remoteAddr, &nAddrlen);
		if (sClient == INVALID_SOCKET)
		{
			printf("accept error !");
			continue;
		}
		//printf("���ܵ�һ�����ӣ�%s \r\n", inet_ntoa(remoteAddr.sin_addr));//��ӡ�������ߵ�ip

		//��������  
		int ret = recv(sClient, revData, 255, 0);
		if (ret > 0)
		{
			// Ϊ��ֹ��ӡ����,���ַ�����β��Ϊ0x00
			revData[ret] = 0x00;
			//printf(revData);
		}
		int nums = atoi(revData);
		//printf("%d\n", nums);

		if (nums == 6)
		{
			printf(revData);
		}
		else
		{
			printf("%d", 1);
		}
		//��������  
		//const char * sendData = "��ã�TCP�ͻ��ˣ�\n";
		const char * sendData = "1\n";
		send(sClient, sendData, strlen(sendData), 0);
		closesocket(sClient);
	}

	closesocket(slisten);
	WSACleanup();
	return 0;
}
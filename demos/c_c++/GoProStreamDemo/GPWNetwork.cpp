/* GPWNetwork.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:53 UTC 2022 */


#include "GPWNetwork.h"

WSASession::WSASession()
{
    int ret = WSAStartup(MAKEWORD(2, 2), &data);
    if (ret != 0)
        throw std::system_error(WSAGetLastError(), std::system_category(), "WSAStartup Failed");
}
WSASession::~WSASession()
{
    WSACleanup();
}

UDPSocket::UDPSocket()
{
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET)
    {
        int blah = WSAGetLastError();
        printf("error opening socket %d", blah);
        throw std::system_error(WSAGetLastError(), std::system_category(), "Error opening socket");
    }
}
UDPSocket::~UDPSocket()
{
    closesocket(sock);
}

void UDPSocket::SendTo(const std::string& address, unsigned short port, const char* buffer, int len, int flags)
{
    sockaddr_in add;
    add.sin_family = AF_INET;
    InetPtonA(AF_INET, (PCSTR)(address.c_str()), &add.sin_addr.s_addr);
    
    add.sin_port = htons(port);
    int ret = sendto(sock, buffer, len, flags, reinterpret_cast<SOCKADDR *>(&add), sizeof(add));
    if (ret < 0)
        throw std::system_error(WSAGetLastError(), std::system_category(), "sendto failed");
}

sockaddr_in UDPSocket::RecvFrom(char* buffer, int len, int& received, int flags)
{
    sockaddr_in from;
    int size = sizeof(from);
    int ret = recvfrom(sock, buffer, len, flags, reinterpret_cast<SOCKADDR *>(&from), &size);
    if (ret < 0)
        throw std::system_error(WSAGetLastError(), std::system_category(), "recvfrom failed");
    received = ret;

    return from;
}
void UDPSocket::Bind(unsigned short port)
{
    sockaddr_in add;
    add.sin_family = AF_INET;
    add.sin_addr.s_addr = htonl(INADDR_ANY);
    add.sin_port = htons(port);

    int ret = bind(sock, reinterpret_cast<SOCKADDR *>(&add), sizeof(add));
    if (ret < 0)
        throw std::system_error(WSAGetLastError(), std::system_category(), "Bind failed");
}


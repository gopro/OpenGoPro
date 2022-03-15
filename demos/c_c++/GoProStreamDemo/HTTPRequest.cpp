/* HTTPRequest.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:53 UTC 2022 */

#include "HTTPRequest.h"

HTTPRequest::HTTPRequest(const std::string& host, const short port)
    : Host(host), Port(port)
{
    InitWinsock();
    if ((Sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET)
    {
        int err = WSAGetLastError();
        throw std::exception("Couldn't create socket " + err);
    }
}

HTTPRequest::~HTTPRequest()
{
    WSACleanup();
    closesocket(Sock);
}


std::string HTTPRequest::get_response()
{
    return Response;
}

bool HTTPRequest::InitWinsock()
{
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(1, 1), &wsaData) != 0)
    {
        return false;
    }

    return true;
}

bool HTTPRequest::loop_recieve()
{
    while (true)
    {
        char recvBuf[256];

        auto nret = recv(Sock, recvBuf, sizeof(recvBuf), 0);
        if (nret == -1)
        {
            return false;
        }
        else if (nret == 0)
        {
            break;
        }

        Response.append(recvBuf, nret);
    }

    return true;
}

bool HTTPRequest::resolve_and_connect()
{
    bool retbool = true;
    if (connected)
        return retbool;
    sockaddr_in add;
    add.sin_family = AF_INET;
    InetPtonA(AF_INET, Host.c_str(), &add.sin_addr.s_addr);
    add.sin_port = htons(Port);
    int ret = -1;

    // Set non-blocking 
    unsigned long modeB = 1;
    ret = ioctlsocket(Sock, FIONBIO, &modeB);
    if (ret != NO_ERROR)
        OutputDebugStringA("ioctlsocket failed\n");

    try
    {
        ret = connect(Sock, reinterpret_cast<SOCKADDR*>(&add), sizeof(add));

        if (ret < 0)
        {
            int boo = WSAGetLastError();
            if (boo == WSAEWOULDBLOCK)
            {
                OutputDebugStringA("connect in progress - selecting\n");
                fd_set setW, setE;

                FD_ZERO(&setW);
                FD_SET(Sock, &setW);
                FD_ZERO(&setE);
                FD_SET(Sock, &setE);

                timeval time_out = { 0 };
                time_out.tv_sec = 2;
                time_out.tv_usec = 0;

                ret = select(0, NULL, &setW, &setE, &time_out);
                if (ret <= 0)
                {
                    // select() failed or connection timed out
                    closesocket(Sock);
                    if (ret == 0)
                    {
                        TimedOut = true;
                        WSASetLastError(WSAETIMEDOUT);
                    }
                    ret = -1;
                }
                if (FD_ISSET(Sock, &setE))
                {
                    // connection failed
                    closesocket(Sock);
                    ret = -1;
                }
                // put socked in blocking mode...
                modeB = 0;
                if (ioctlsocket(Sock, FIONBIO, &modeB) == SOCKET_ERROR)
                {
                    closesocket(Sock);
                    ret = -1;
                }
            }
            else
            {
                ret = -1;
            }
        }
    }
    catch(...)
    {

    }
    if (ret < 0)
    {
        int err = WSAGetLastError();
        char buf[128] = { 0 };
        sprintf(buf, "error opening socket %d", err);
        OutputDebugStringA(buf);
    }
    else
    {
        connected = true;
    }

    return retbool;
}

bool HTTPRequest::get_request(const std::string& path)
{
    if (!resolve_and_connect())
        return false;

    std::string request = "GET " + path + " HTTP/1.1" + "\r\n";
    request += "Host: " + Host + "\r\n";
    request += "Connection: close\r\n";
    request += "\r\n";

    if (send(Sock, request.c_str(), request.length(), 0) == SOCKET_ERROR)
    {
        return false;
    }

    return loop_recieve();
}
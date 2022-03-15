/* UDPSocketCapture.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:53 UTC 2022 */

#include "UDPSocketCapture.h"
#include "HTTPRequest.h"
#include "GoProStreamDemo.h"

#ifndef snprintf
#define snprintf(buf,len, format,...) _snprintf_s(buf, len,len, format, __VA_ARGS__)
#endif

#define READ_BUFFER_SIZE 16384

extern "C"
{
#include "demuxing_decoding.h"
}
#include "BufferNegotiator.h"

UDPSocketCapture::UDPSocketCapture()
{

}

UDPSocketCapture::~UDPSocketCapture()
{
    Stop();
}

LONG GetStringRegKey(HKEY hKey, const std::string& strValueName, std::string& strValue)
{
    CHAR szBuffer[512] = { 0 };
    DWORD dwBufferSize = sizeof(szBuffer);
    ULONG nError;
    nError = RegQueryValueExA(hKey, strValueName.c_str(), 0, NULL, (LPBYTE)szBuffer, &dwBufferSize);
    if (ERROR_SUCCESS == nError)
    {
        strValue = szBuffer;
    }
    return nError;
}
int UDPSocketCapture::FindCamera(std::string& address)
{
    int ret = -1;
    address = "";
    WSAData wsaData;
    if (WSAStartup(MAKEWORD(1, 1), &wsaData) != 0)
    {
        return 255;
    }

    std::string myaddr = "";
    address = "";

    char logbuf[100] = { 0 };
    char ac[80];
    if (gethostname(ac, sizeof(ac)) == SOCKET_ERROR)
    {
        
        snprintf(logbuf, 100, "Error %d when getting local host name.\n", WSAGetLastError());
        OutputDebugStringA(logbuf);
        WSACleanup();
        return -1;
    }
    snprintf(logbuf, 100, "Host name is %s\n", ac);
    OutputDebugStringA(logbuf);

    struct hostent* phe = gethostbyname(ac);
    struct addrinfo* result = NULL;
    struct addrinfo* res = NULL;
    getaddrinfo(ac, NULL, NULL, &result);
    if (phe == 0)
    {
        OutputDebugStringA("Bad host lookup.\n");
        WSACleanup();
        return -1;
    }

    for (int i = 0; phe->h_addr_list[i] != 0; ++i)
    {
        struct in_addr addr;
        memcpy(&addr, phe->h_addr_list[i], sizeof(struct in_addr));
        snprintf(logbuf, 100, "Address %d: %s\n ", i , inet_ntoa(addr));
        OutputDebugStringA(logbuf);
        if ((int)addr.S_un.S_un_b.s_b1 == 172 && ((int)addr.S_un.S_un_b.s_b2 >= 20 && (int)addr.S_un.S_un_b.s_b2 <= 29) &&
            ((int)addr.S_un.S_un_b.s_b4 >= 50 && (int)addr.S_un.S_un_b.s_b4 <= 70))
        {
            address = inet_ntoa(addr);
            address.replace(address.length() - 1, 1, "1");
            ret = 0;
        }
    }

    WSACleanup();

    return ret;
}


void UDPSocketCapture::Start(int height)
{
    if (!mStarted)
    {
        mHeight = height;
        this->mCaptureThread = std::thread(CaptureThread, this);
        this->mOutputThread = std::thread(OutputThread, this);
        mStarted = true;
    }
}

void UDPSocketCapture::Stop()
{
    if (mStarted)
    {
        StopDecoding();
        StopCapture();
        mQuitNow = true;
        if (mCaptureThread.joinable())
            mCaptureThread.join();
        if(mOutputThread.joinable())
            mOutputThread.join();
        mStarted = false;
    }
}

void UDPSocketCapture::GetBuffer(uint8_t* buf, long bufsize, long& bytesReturned)
{
    mBufMutex.lock();
    static size_t actualbytes = 0;
    if (buf == NULL || bufsize == 0)
    {
        mBufMutex.unlock();
        return;
    }
    bytesReturned = ::GetBuffer(buf, bufsize);

    if (bytesReturned == 0)
    {
        if (mBigBuf == NULL)
        {
            char path[MAX_PATH];
            std::string spath = "";
            HMODULE hm = NULL;

            if (GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                (LPCSTR)&GetStringRegKey, &hm) == 0)
            {
                int err = GetLastError();
                fprintf(stderr, "GetModuleHandle failed, error = %d\n", err);
            }
            if (GetModuleFileNameA(hm, path, sizeof(path)) == 0)
            {
                int err = GetLastError();
                fprintf(stderr, "GetModuleFileName failed, error = %d\n", err);
            }
            spath = path;
            size_t slashpos = spath.find_last_of("\\", spath.length()) + 1;
#ifdef USE_PREVIEW_STREAM
            spath.replace(slashpos, spath.length() - slashpos, "raw720.img");
#else
            spath.replace(slashpos, spath.length() - slashpos, "raw.img");
#endif

            mBigBuf = (uint8_t*)malloc(BIG_BUF_SIZE);
            if (mBigBuf != NULL)
            {
                FILE* ou = fopen(spath.c_str(), "rb");
                if (ou)
                {
                    actualbytes = fread(mBigBuf, 1, BIG_BUF_SIZE, ou);
                    fclose(ou);
                    bytesReturned = actualbytes;
                }
                else
                {
                    free(mBigBuf);
                    mBigBuf = NULL;
                }
            }
        }
        if (mBigBuf != NULL)
        {
            if (bufsize!=0 && bufsize >= actualbytes)
            {
                memcpy(buf, mBigBuf, actualbytes);
                bytesReturned = actualbytes;
            }
        }
        
    }

    mBufMutex.unlock();
}

void UDPSocketCapture::WriteBuffer(uint8_t* buf, int bufsize)
{
    mBufMutex.lock();
    mBufMutex.unlock();
}

/*
This function is responsible for calling decode on the captured buffer
*/
void UDPSocketCapture::OutputThread(UDPSocketCapture* me)
{
    std::string addr = "";
    
    while (FindCamera(addr) != 0 && !me->mQuitNow)
    {
        Sleep(500);
    }

    if (!me->mQuitNow)
    {
        bool alreadyStarted = false;

        {
            HTTPRequest req(addr, 8080);
            if (req.get_request("/gopro/webcam/status"))
            {
                std::string stat = req.get_response();
                std::string findme = "\"status\": 2";
                if (stat.find(findme, 0) != std::string::npos)
                    alreadyStarted = true;
            }
            if (alreadyStarted)
            {
                HTTPRequest req(addr, 8080);
                if (req.get_request("/gopro/webcam/stop"))
                {
                    std::string stat = req.get_response();
                }
                Sleep(200);
            }
        }
        {
            HTTPRequest req(addr, 8080);
#ifdef USE_PREVIEW_STREAM
            std::string startaddr = "/gopro/camera/stream/start";
#else
            std::string startaddr = "/gopro/webcam/start?res=%d&fov=0";
#endif
            
            char bufff[256] = { 0 };
            int parm = 12;
            if(me->mHeight == 720)
            {
                parm = 7;
            }
            snprintf(bufff, 256, startaddr.c_str(), parm);
            std::string buf = bufff;
            if (req.get_request(buf))
            {
                std::string stat = req.get_response();
            }
        }

        const char* url = "udp://@0.0.0.0:8554";

        while (!me->mQuitNow)
        {
            try
            {
                DecodeStream();
            }
            catch (...)
            {
                OutputDebugStringA("Decode crashed, quitting everything\n");
            }
        }

        {

            HTTPRequest req(addr, 8080);
#ifdef USE_PREVIEW_STREAM
            req.get_request("/gopro/camera/stream/stop");
#else
            req.get_request("/gopro/webcam/stop");
            if (!req.TimedOut)
            {
                HTTPRequest req2(addr, 8080);
                req2.get_request("/gopro/webcam/exit");
            }
#endif

        }
    }
    
    OutputDebugStringA("LEAVING THREAD\n");
}


/*
This is the main function that captures TS data from the camera and saves it to a buffer
*/
void UDPSocketCapture::CaptureThread(UDPSocketCapture* me)
{
    WSASession session;
    char buf[READ_BUFFER_SIZE] = { 0 };
    OutputDebugStringA("Starting receive thread\n");
    UDPSocket* mysock = new UDPSocket();
    mysock->Bind(8554);

    while (true)
    {
        if (mysock == NULL)
        {
            mysock = new UDPSocket();
            mysock->Bind(8554);
        }
        int received = 0;
        sockaddr_in blop = mysock->RecvFrom(buf, READ_BUFFER_SIZE, received);
        //LOGF::Instance()->LOG("Received %d bytes\n", received);

        if (received == READ_BUFFER_SIZE)
            OutputDebugStringA("Maxed out the buffer\n");
        if (received == 1 || me->mQuitNow)
        {
            //fclose(myfile);
            break;
        }

        WriteInputBuffer((uint8_t*)buf, received);
        
        memset(buf, 0, READ_BUFFER_SIZE);
    }
}

void UDPSocketCapture::StopCapture()
{
    UDPSocket soc;
    char buf = 'q';
    soc.SendTo("127.0.0.1", 8554, &buf, 1);
    StopInput();
}

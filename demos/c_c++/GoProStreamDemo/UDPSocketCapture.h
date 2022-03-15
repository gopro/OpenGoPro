/* UDPSocketCapture.h/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:53 UTC 2022 */

#pragma once

#include "GPWNetwork.h"
#include <thread>
#include <mutex>

#define BIG_BUF_SIZE 3110400

class UDPSocketCapture
{
public:
    UDPSocketCapture();
    virtual ~UDPSocketCapture();

    void Start(int height = 1080);
    void Stop();

    void GetBuffer(uint8_t* buf, long bufsize, long&bytesReturned);
    void WriteBuffer(uint8_t* buf, int bufsize);
    
protected:
    static void CaptureThread(UDPSocketCapture* me);
    static void OutputThread(UDPSocketCapture* me);
    static int FindCamera(std::string& address);
    void StopCapture();
    std::thread mCaptureThread;
    std::thread mOutputThread;

    bool mStarted = false;
    bool mQuitNow = false;
    uint8_t* mBigBuf = NULL;
    int mBigBufPos = 0;
    std::mutex mBufMutex;
    int mHeight = 1080;

};


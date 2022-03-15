/* BufferNegotiator.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:52 UTC 2022 */


#include "BufferNegotiator.h"
#include "GoProStreamDemo.h"
#include <mutex>
#include <condition_variable>
#include <algorithm>
#include "stdafx.h"

std::mutex locker;

std::mutex inputlock;
std::condition_variable sleepy;

extern "C" uint8_t* video_dst_data[4];
extern "C" long video_dst_bufsize;
#define MAX_INPUT_BUF_SIZE 232768
uint8_t inputbuffer[MAX_INPUT_BUF_SIZE] = { 0 };
int inputbuffersize = 0;
static int quit_now = 0;

long GetBuffer(uint8_t* dest, long buflen)
{
    long ret = 0;
    int blackbuf = 0;
    locker.lock();

#ifndef USE_PREVIEW_STREAM
    //for 1080
    if (video_dst_bufsize == 0 || 
        (video_dst_data[0][0] == 0 //upper left
            && video_dst_data[0][1035840] == 0 //center
            && video_dst_data[0][1919] == 0     //upper right
            && video_dst_data[0][2071680] == 0     //lower left
            && video_dst_data[0][2073599] == 0)) //lower right
        blackbuf = 1;
#else
    //for 720
    if (video_dst_bufsize == 0 ||
        (video_dst_data[0][0] == 0 //upper left
            && video_dst_data[0][460800] == 0 //center
            && video_dst_data[0][1279] == 0     //upper right
            && video_dst_data[0][920320] == 0     //lower left
            && video_dst_data[0][921599] == 0)) //lower right
        blackbuf = 1;
#endif


    if (video_dst_bufsize>0 && buflen >= video_dst_bufsize && !blackbuf)
    {
        memcpy(dest, video_dst_data[0], video_dst_bufsize);
        ret = video_dst_bufsize;
    }
    else
    {
        ret = 0;
    }

    locker.unlock();
    return ret;
}

void LockBuffer()
{
    locker.lock();
}

void UnlockBuffer()
{
    locker.unlock();
}

/*
This function stores the buffer for consumption by the decoding/demuxing thread
*/
void WriteInputBuffer(uint8_t* buf, int buf_size)
{
    inputlock.lock();
    if (buf_size <= MAX_INPUT_BUF_SIZE)
    {
        //buffer is full
        if (inputbuffersize + buf_size > MAX_INPUT_BUF_SIZE)
        {
            //clear the buffer
            inputbuffersize = 0;
            OutputDebugStringA("clearing the buffer\n");
        }
        if (buf[0] == 'G' && (buf_size % 188 == 0))
        {
            memcpy(&inputbuffer[inputbuffersize], buf, buf_size);
            inputbuffersize += buf_size;

        }

        sleepy.notify_all();
    }
    inputlock.unlock();
}

void StopInput()
{
    inputlock.lock();
    quit_now = 1;
    sleepy.notify_all();
    inputlock.unlock();
}

void StartInput()
{
    inputlock.lock();
    quit_now = 0;
    inputlock.unlock();
}

int ReadInputBuffer(uint8_t* buf, int buf_size)
{
    if (quit_now)
    {
        return -1;
    }
    std::unique_lock<std::mutex> lck(inputlock);
    while (inputbuffersize == 0 && quit_now==0)
    {
        sleepy.wait(lck);
    }
    if (quit_now)
    {
        return -1;
    }
    int new_size = min(buf_size, inputbuffersize);
    /* copy internal buffer data to buf */
    memcpy(buf, inputbuffer, new_size);
    memmove(inputbuffer, &inputbuffer[new_size], inputbuffersize - new_size);
    inputbuffersize -= new_size;

    return new_size;
}
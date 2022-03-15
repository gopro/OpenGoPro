/* BufferNegotiator.h/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:53 UTC 2022 */

#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

    long GetBuffer(uint8_t* dest, long buflen);

    void LockBuffer();

    void UnlockBuffer();

    void StartInput();

    void StopInput();

    void WriteInputBuffer(uint8_t* buf, int buf_size);

    int ReadInputBuffer(uint8_t* buf, int buf_size);

#ifdef __cplusplus
}
#endif
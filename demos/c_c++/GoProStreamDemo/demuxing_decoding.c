#pragma warning( disable : 4996)
/*
 * Copyright (c) 2012 Stefano Sabatini
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/**
 * @file
 * Demuxing and decoding example.
 *
 * Show how to use the libavformat and libavcodec API to demux and
 * decode audio and video data.
 * @example demuxing_decoding.c
 */

#ifdef BUSTED_COMPILER
#define inline __inline
#ifndef snprintf
#define snprintf(buf,len, format,...) _snprintf_s(buf, len,len, format, __VA_ARGS__)
#endif
#endif

#include <libavutil/imgutils.h>
#include <libavutil/samplefmt.h>
#include <libavutil/timestamp.h>
#include <libavformat/avformat.h>
#include <libavformat/avio.h>

#include "BufferNegotiator.h"

static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *video_dec_ctx = NULL, *audio_dec_ctx = NULL;
static AVIOContext* avio_ctx = NULL;
static uint8_t* avio_ctx_buffer = NULL;
static size_t avio_ctx_buffer_size = 48128;
static int width, height;
static enum AVPixelFormat pix_fmt;
static AVStream *video_stream = NULL, *audio_stream = NULL;
static int stopDecoding = 0;

uint8_t *video_dst_data[4] = {NULL};
static int      video_dst_linesize[4];
long video_dst_bufsize;

static int video_stream_idx = -1, audio_stream_idx = -1;
static AVFrame *frame = NULL;
static AVPacket pkt;
static int video_frame_count = 0;
static int audio_frame_count = 0;


static int read_packet(void* opaque, uint8_t* buf, int buf_size);

/* Enable or disable frame reference counting. You are not supposed to support
 * both paths in your application but pick the one most appropriate to your
 * needs. Look for the use of refcount in this example to see what are the
 * differences of API usage between them. */
static int refcount = 0;

static int decode_packet(int *got_frame, int cached)
{
    int ret = 0;
    int decoded = pkt.size;

    *got_frame = 0;

    if (pkt.stream_index == video_stream_idx) {
        /* decode video frame */
        ret = avcodec_decode_video2(video_dec_ctx, frame, got_frame, &pkt);
        if (ret < 0) {
            fprintf(stderr, "Error decoding video frame (%s)\n", av_err2str(ret));
            return ret;
        }

        if (*got_frame) {

            if (frame->width != width || frame->height != height ||
                frame->format != pix_fmt) {
                /* To handle this change, one could call av_image_alloc again and
                 * decode the following frames into another rawvideo file. */
                fprintf(stderr, "Error: Width, height and pixel format have to be "
                        "constant in a rawvideo file, but the width, height or "
                        "pixel format of the input video changed:\n"
                        "old: width = %d, height = %d, format = %s\n"
                        "new: width = %d, height = %d, format = %s\n",
                        width, height, av_get_pix_fmt_name(pix_fmt),
                        frame->width, frame->height,
                        av_get_pix_fmt_name(frame->format));
                return -1;
            }

            printf("video_frame%s n:%d coded_n:%d\n",
                   cached ? "(cached)" : "",
                   video_frame_count++, frame->coded_picture_number);

            /* copy decoded frame to destination buffer:
             * this is required since rawvideo expects non aligned data */
            LockBuffer();
            av_image_copy(video_dst_data, video_dst_linesize,
                          (const uint8_t **)(frame->data), frame->linesize,
                          pix_fmt, width, height);
            UnlockBuffer();
            /* write to rawvideo file */
            //fwrite(video_dst_data[0], 1, video_dst_bufsize, video_dst_file);
        }
    } else if (pkt.stream_index == audio_stream_idx) {
        /* decode audio frame */
        ret = avcodec_decode_audio4(audio_dec_ctx, frame, got_frame, &pkt);
        if (ret < 0) {
            fprintf(stderr, "Error decoding audio frame (%s)\n", av_err2str(ret));
            return ret;
        }
        /* Some audio decoders decode only part of the packet, and have to be
         * called again with the remainder of the packet data.
         * Sample: fate-suite/lossless-audio/luckynight-partial.shn
         * Also, some decoders might over-read the packet. */
        decoded = FFMIN(ret, pkt.size);

        if (*got_frame) {
            size_t unpadded_linesize = frame->nb_samples * av_get_bytes_per_sample(frame->format);
            //printf("audio_frame%s n:%d nb_samples:%d pts:%s\n",
            //       cached ? "(cached)" : "",
            //       audio_frame_count++, frame->nb_samples,
            //       av_ts2timestr(frame->pts, &audio_dec_ctx->time_base));

            /* Write the raw audio data samples of the first plane. This works
             * fine for packed formats (e.g. AV_SAMPLE_FMT_S16). However,
             * most audio decoders output planar audio, which uses a separate
             * plane of audio samples for each channel (e.g. AV_SAMPLE_FMT_S16P).
             * In other words, this code will write only the first audio channel
             * in these cases.
             * You should use libswresample or libavfilter to convert the frame
             * to packed data. */
            //fwrite(frame->extended_data[0], 1, unpadded_linesize, audio_dst_file);
        }
    }

    /* If we use frame reference counting, we own the data and need
     * to de-reference it when we don't use it anymore */
    if (*got_frame && refcount)
        av_frame_unref(frame);

    return decoded;
}

static int open_codec_context(int *stream_idx,
                              AVCodecContext **dec_ctx, AVFormatContext *fmt_ctx, enum AVMediaType type)
{
    int ret, stream_index;
    AVStream *st;
    AVCodec *dec = NULL;
    AVDictionary *opts = NULL;

    ret = av_find_best_stream(fmt_ctx, type, -1, -1, NULL, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not find %s stream in input\n",
                av_get_media_type_string(type));
        return ret;
    } else {
        stream_index = ret;
        st = fmt_ctx->streams[stream_index];

        /* find decoder for the stream */
        dec = avcodec_find_decoder(st->codecpar->codec_id);
        if (!dec) {
            fprintf(stderr, "Failed to find %s codec\n",
                    av_get_media_type_string(type));
            return AVERROR(EINVAL);
        }

        /* Allocate a codec context for the decoder */
        *dec_ctx = avcodec_alloc_context3(dec);
        if (!*dec_ctx) {
            fprintf(stderr, "Failed to allocate the %s codec context\n",
                    av_get_media_type_string(type));
            return AVERROR(ENOMEM);
        }

        /* Copy codec parameters from input stream to output codec context */
        if ((ret = avcodec_parameters_to_context(*dec_ctx, st->codecpar)) < 0) {
            fprintf(stderr, "Failed to copy %s codec parameters to decoder context\n",
                    av_get_media_type_string(type));
            return ret;
        }

        /* Init the decoders, with or without reference counting */
        av_dict_set(&opts, "refcounted_frames", refcount ? "1" : "0", 0);
        if ((ret = avcodec_open2(*dec_ctx, dec, &opts)) < 0) {
            fprintf(stderr, "Failed to open %s codec\n",
                    av_get_media_type_string(type));
            return ret;
        }
        *stream_idx = stream_index;
    }

    return 0;
}

static int get_format_from_sample_fmt(const char **fmt,
                                      enum AVSampleFormat sample_fmt)
{
    int i;
    struct sample_fmt_entry {
        enum AVSampleFormat sample_fmt; const char *fmt_be, *fmt_le;
    } sample_fmt_entries[] = {
        { AV_SAMPLE_FMT_U8,  "u8",    "u8"    },
        { AV_SAMPLE_FMT_S16, "s16be", "s16le" },
        { AV_SAMPLE_FMT_S32, "s32be", "s32le" },
        { AV_SAMPLE_FMT_FLT, "f32be", "f32le" },
        { AV_SAMPLE_FMT_DBL, "f64be", "f64le" },
    };
    *fmt = NULL;

    for (i = 0; i < FF_ARRAY_ELEMS(sample_fmt_entries); i++) {
        struct sample_fmt_entry *entry = &sample_fmt_entries[i];
        if (sample_fmt == entry->sample_fmt) {
            *fmt = AV_NE(entry->fmt_be, entry->fmt_le);
            return 0;
        }
    }

    fprintf(stderr,
            "sample format %s is not supported as output format\n",
            av_get_sample_fmt_name(sample_fmt));
    return -1;
}

int StopDecoding()
{
    stopDecoding = 1;

    return 0;
}

static int shouldInterrupt(void * junk)
{
    return stopDecoding;
}

int DecodeStream()
{
    int ret = 0, got_frame = 0;
    stopDecoding = 0;
    char* format = "mpegts";
    
    if (stopDecoding)
    {
        return -1;
    }
    
    do
    {
        AVInputFormat* fmt = NULL;

        if (stopDecoding == 1)
            return -1;
        fmt = av_find_input_format(format);
        fmt_ctx = avformat_alloc_context();
        fmt_ctx->interrupt_callback.callback = shouldInterrupt;
        fmt_ctx->interrupt_callback.opaque = NULL;
        AVDictionary* format_opts = NULL;
        av_dict_set(&format_opts, "probesize", "4194304", 0);

        avio_ctx_buffer = av_malloc(avio_ctx_buffer_size);
        if (!avio_ctx_buffer)
        {
            ret = AVERROR(ENOMEM);
            goto end;
        }
        avio_ctx = avio_alloc_context(avio_ctx_buffer, avio_ctx_buffer_size,
            0, NULL, &read_packet, NULL, NULL);
        if (!avio_ctx)
        {
            ret = AVERROR(ENOMEM);
            goto end;
        }
        fmt_ctx->pb = avio_ctx;

        int averr = 0;
        /* open input file, and allocate format context */
        while ((averr = avformat_open_input(&fmt_ctx, NULL, fmt, &format_opts)) < 0)
        {
            if (stopDecoding == 1)
            {
                return -1;
            }
            _sleep(200);
        }

        int tries = 0;
        /* retrieve stream information */
        while (tries < 3)
        {
            if (avformat_find_stream_info(fmt_ctx, NULL) < 0)
            {
                fprintf(stderr, "Could not find stream information\n");
                tries++;
            }
            else
            {
                break;
            }
        }

        if (open_codec_context(&video_stream_idx, &video_dec_ctx, fmt_ctx, AVMEDIA_TYPE_VIDEO) >= 0)
        {
            video_stream = fmt_ctx->streams[video_stream_idx];

            /* allocate image where the decoded image will be put */
            width = video_dec_ctx->width;
            height = video_dec_ctx->height;
            pix_fmt = video_dec_ctx->pix_fmt;
            LockBuffer();
            ret = av_image_alloc(video_dst_data, video_dst_linesize, width, height, pix_fmt, 1);
            UnlockBuffer();
            if (ret < 0)
            {
                fprintf(stderr, "Could not allocate raw video buffer\n");
                goto end;
            }
            LockBuffer();
            video_dst_bufsize = ret;
            UnlockBuffer();
        }

        if (!video_stream)
        {
            fprintf(stderr, "Could not find video stream in the input, aborting\n");
            ret = 1;
            goto end;
        }

        frame = av_frame_alloc();
        if (!frame)
        {
            fprintf(stderr, "Could not allocate frame\n");
            ret = AVERROR(ENOMEM);
            goto end;
        }

        /* initialize packet, set data to NULL, let the demuxer fill it */
        av_init_packet(&pkt);
        pkt.data = NULL;
        pkt.size = 0;
        avio_flush(fmt_ctx->pb);
        avformat_flush(fmt_ctx);
        /* read frames from the file */
        while (av_read_frame(fmt_ctx, &pkt) >= 0 && !stopDecoding)
        {
            AVPacket orig_pkt = pkt;
            do
            {
                ret = decode_packet(&got_frame, 0);
                if (ret < 0)
                    break;
                pkt.data += ret;
                pkt.size -= ret;
            } while (pkt.size > 0);
            av_packet_unref(&orig_pkt);
        }

        /* flush cached frames */
        pkt.data = NULL;
        pkt.size = 0;
        do
        {
            decode_packet(&got_frame, 1);
        } while (got_frame);
end:
        LockBuffer();
        video_dst_bufsize = 0;

        avcodec_free_context(&video_dec_ctx);
        avcodec_free_context(&audio_dec_ctx);
        avformat_close_input(&fmt_ctx);
        av_freep(&avio_ctx->buffer);
        av_freep(&avio_ctx);
        avio_ctx = NULL;
        video_dec_ctx = NULL;
        audio_dec_ctx = NULL;
        fmt_ctx = NULL;

        av_frame_free(&frame);
        frame = NULL;
        av_free(video_dst_data[0]);
        video_dst_data[0] = NULL;
        UnlockBuffer();

        
    } while (1);

    return ret < 0;
}

static int read_packet(void* opaque, uint8_t* buf, int buf_size)
{
    int ret = ReadInputBuffer(buf, buf_size);

    return ret;
}



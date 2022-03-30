/* stream.c/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:05:40 PM */

#include <curl/curl.h>
#include <string.h>
#include <stdint.h>
#include <chrono>
#include <thread>

/**
 * PREVIEW STREAM COMMANDS DEMO:
 * Commands used in this demo can be found in the WiFi documentation here: https://github.com/gopro/OpenGoPro/tree/main/docs/wifi
 * List of HTTP Error codes and their meanings can be found here: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
 */

#define HTTP_ERR_CODE_OK 200
#define ERR_FAILURE -1
#define ERR_SUCCESS 0

enum PreviewStreamRequest
{
    eUnknown = -1,
    eStartStreamRequest,
    eEndStreamRequest,
    eDemo
};

/**
 * Function to get response code of curl request
 * @param curlReq - curl request
 * @return - return http error code
 */
long get_response_code(CURL *curlReq)
{
    long resp_code;
    curl_easy_getinfo(curlReq, CURLINFO_RESPONSE_CODE, &resp_code);
    return resp_code;
}

/**
 * Function to send curl request and check response code
 * @param curl - curl request
 * @return - 0, if successful. -1 if any step failed
 */
long perform_request(CURL *curlReq)
{
    CURLcode curlCode = curl_easy_perform(curlReq);
    // Check if curl request succeeded
    if(curlCode != CURLE_OK)
    {
        curl_easy_cleanup(curlReq);
        printf("\nFailed to perform curl request - received CURLcode error:%d\n", curlCode);
        return ERR_FAILURE;
    }

    // Check HTTP response code
    long resp_code = get_response_code(curlReq);
    if(resp_code != HTTP_ERR_CODE_OK)
    {
        curl_easy_cleanup(curlReq);
        printf("\nRequest returned HTTP error code:%ld\n", resp_code);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}

enum PreviewStreamRequest check_user_request(int num_inputs, char *input)
{
    if(num_inputs == 2)
    {
        if((strcmp(input, "-s") == 0) || (strcmp(input, "--start") == 0))
        {
            return eStartStreamRequest;
        }
        if((strcmp(input, "-e") == 0) || (strcmp(input, "--end") == 0))
        {
            return eEndStreamRequest;
        }
        if((strcmp(input, "-d") == 0) || (strcmp(input, "--demo") == 0))
        {
            return eDemo;
        }
    }
    return eUnknown;
}

void help()
{
    printf("\nUsage");
    printf("\n\t./stream_commands -s, --start");
    printf("\n\t./stream_commands -e, --end");
    printf("\n\t./stream_commands -d, --demo");
}

int start_stream(CURL *curl)
{
    printf("\nStarting preview stream");
    curl_easy_setopt(curl, CURLOPT_URL, "http://10.5.5.9:8080/gopro/camera/stream/start");
    if (perform_request(curl) == ERR_FAILURE)
    {
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}

int stop_stream(CURL *curl)
{
    printf("\nStopping preview stream");
    curl_easy_setopt(curl, CURLOPT_URL, "http://10.5.5.9:8080/gopro/camera/stream/stop");
    if (perform_request(curl) == ERR_FAILURE)
    {
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}

int main(int argc, char *argv[])
{
    /**
     * To test this demo, a media player that supports UDP is necessary.
     * VLC is a good option, which can be found here https://www.videolan.org/
     * The UDP address:port is udp://0.0.0.0:8554
     */

    enum PreviewStreamRequest user_request = check_user_request(argc, argv[1]);
    if(user_request == eUnknown)
    {
        printf("\nCouldn't run command");
        help();
        return ERR_FAILURE;
    }

    CURL *curl = curl_easy_init();
    if(curl != NULL)
    {
        switch(user_request)
        {
            case eStartStreamRequest:
            {
                if(start_stream(curl) == ERR_FAILURE)
                {
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }
                break;
            }
            case eEndStreamRequest:
            {
                if(stop_stream(curl) == ERR_FAILURE)
                {
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }
                break;
            }
            case eDemo:
            {
                uint32_t duration = 0;
                // Prompt to see how long the user wants the preview stream to run
                printf("\nEnter stream duration(seconds): ");
                int result = scanf("%u", &duration);

                if (result != 1)
                {
                    printf("\nStream duration was invalid, exiting demo");
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }
                // stop preview stream in case it was previously running
                if(stop_stream(curl) == ERR_FAILURE)
                {
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }

                if(start_stream(curl) == ERR_FAILURE)
                {
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }

                printf("\nStream will run for %u seconds\n", duration);
                std::this_thread::sleep_for(std::chrono::seconds(duration));

                if(stop_stream(curl) == ERR_FAILURE)
                {
                    curl_easy_cleanup(curl);
                    return ERR_FAILURE;
                }
                printf("\nSuccessfully exited demo");
                break;
            }
            default:
            {
                curl_easy_cleanup(curl);
                printf("\nUnknown request type used:%d", user_request);
                return ERR_FAILURE;
            }
        }
    }
    else
    {
        printf("\nFailed to init curl object") ;
        return ERR_FAILURE;
    }

    curl_easy_cleanup(curl);
    return ERR_SUCCESS;
}
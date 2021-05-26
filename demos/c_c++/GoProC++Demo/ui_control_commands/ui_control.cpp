/* ui_control.cpp/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu, May 20, 2021  8:24:32 PM */

#include <iostream>
#include <curl/curl.h>
#include "cJSON.h"
/**
 * UI CONTROL COMMANDS DEMO:
 * List of HTTP Error codes and their meanings can be found here: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
 */

#define HTTP_ERR_CODE_OK 200
#define ERR_FAILURE -1
#define ERR_SUCCESS 0

using namespace std;

enum SettingsRequest
{
    eUnknown = -1,
    eListFiles,
    eListFilesPretty,
    eMediaInfo,
    eMediaInfoPretty,
    eDownloadMedia,
    eDemo
};


//@TODO: Move get_response_code and perform_request to a helper file
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
        printf("\nFailed to perform curl request - received error code:%d", curlCode);
        return ERR_FAILURE;
    }

    // Check response code
    long resp_code = get_response_code(curlReq);
    if(resp_code != HTTP_ERR_CODE_OK)
    {
        printf("\nRequest returned http error code:%ld", resp_code);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}
size_t json_response_callback(char *contents, size_t size, size_t mem, void *data)
{
    size_t json_size = size * mem;
    char *json_data  = (char*)data;
    strcat(json_data, contents);
    return json_size;
}


int send_write_request(CURL *curl, const char *path, const char* curl_response)
{
    if(curl_response == NULL)
    {
        printf("\nResponse is NULL");
        return ERR_FAILURE;
    }

    CURLcode code = curl_easy_setopt(curl, CURLOPT_URL, path);
    if(code != CURLE_OK)
    {
        printf("\nFailed to get media list - received error code:%d", code);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }

    code = curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, json_response_callback);
    if(code != CURLE_OK)
    {
        printf("\nFailed to setup callback function - received error code:%d", code);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    code = curl_easy_setopt(curl, CURLOPT_WRITEDATA, curl_response);
    if (code != CURLE_OK)
    {
        printf("\nFailed to write json data");
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }

    if(perform_request(curl) == ERR_FAILURE)
    {
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}

SettingsRequest check_user_request(int num_inputs, char *input)
{
    if(num_inputs == 2)
    {
        if((strcmp(input, "--list_files") == 0) || (strcmp(input, "-l") == 0))
        {
            return eListFiles;
        }
        if((strcmp(input, "--list_files_pretty") == 0) || (strcmp(input, "-f") == 0))
        {
            return eListFilesPretty;
        }
        return eUnknown;
    }

    if(num_inputs == 3)
    {
        if((strcmp(input, "--info") == 0) || (strcmp(input, "-i") == 0))
        {
            return eMediaInfo;
        }
        if((strcmp(input, "--info_pretty") == 0) || (strcmp(input, "-p") == 0))
        {
            return eMediaInfoPretty;
        }
        if((strcmp(input, "--demo") == 0) || (strcmp(input, "-d") == 0))
        {
            return eDemo;
        }
    }
    if(num_inputs == 4)
    {
        if((strcmp(input, "--download") == 0) || (strcmp(input, "-g") == 0))
        {
            return eDownloadMedia;
        }
    }
    return eUnknown;
}

void help()
{
    /**
     * @TODO: Add support for these commands and maybe add keep-alive
     */
    printf("\nUsage");
    printf("\n\t./ui_control_commands -s, --set_settings <setting_id, option_value>");
    printf("\n\t./ui_control_commands -c, --camera_state");
    printf("\n\t./ui_control_commands -m, --set_mode <mode_group_id>");
    printf("\n\t./ui_control_commands -g, --get_presets");
    printf("\n\t./ui_control_commands -p, --set_preset_group <preset_group_id>");
    printf("\n\t./ui_control_commands -l, --load_preset <preset_id>");
    printf("\n\t./ui_control_commands -d, --demo");
}

int main()
{
    CURL *curl = curl_easy_init();
    if(curl != NULL)
    {
        curl_easy_setopt(curl, CURLOPT_URL, "http://10.5.5.9:8080/gopro/camera/setting?setting_id=2&opt_value=0");

        if(perform_request(curl) == ERR_FAILURE)
        {
            curl_easy_cleanup(curl);
            return ERR_FAILURE;
        }
    }
    return 0;
}
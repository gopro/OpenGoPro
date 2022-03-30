/* media.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:05:39 PM */

#include <iostream>
#include <curl/curl.h>
#include <cjson/cJSON.h>
#include <cstring>
#include <stdio.h>
/**
 * MEDIA COMMANDS DEMO:
 * Commands used in this demo can be found in the WiFi documentation here: https://github.com/gopro/OpenGoPro/tree/main/docs/wifi
 * List of HTTP Error codes and their meanings can be found here: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
 */

#define HTTP_ERR_CODE_OK 200
#define ERR_FAILURE -1
#define ERR_SUCCESS 0

using namespace std;

enum MediaRequest
{
    eUnknown = -1,
    eListFiles,
    eListFilesPretty,
    eMediaInfo,
    eMediaInfoPretty,
    eDownloadMedia,
    eHilightFile,
    eHilightMoment,
    eHilightRemove,
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
        printf("\nFailed to perform curl request - received error code:%d\n", curlCode);
        return ERR_FAILURE;
    }

    // Check response code
    long resp_code = get_response_code(curlReq);
    if(resp_code != HTTP_ERR_CODE_OK)
    {
        printf("\nRequest returned http error code:%ld\n", resp_code);
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

size_t file_response_callback(char *contents, size_t size, size_t mem, void *data)
{
    FILE *file  = (FILE*)data;
    size_t file_size = fwrite(contents, size, mem, file);
    return file_size;
}

MediaRequest check_user_request(int num_inputs, char *input_array[])
{
    char* input = input_array[1];
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
        if(strcmp(input, "--tag-moment") == 0)
        {
            return eHilightMoment;
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
        if(strcmp(input, "--tag-photo") == 0)
        {
            return eHilightFile;
        }
        if(strcmp(input, "--tag-photo-remove") == 0)
        {
            return eHilightRemove;
        }
    }

    if(num_inputs >= 4)
    {
        if((strcmp(input, "--download") == 0) || (strcmp(input, "-g") == 0))
        {
            return eDownloadMedia;
        }

        if(strcmp(input, "--tag-video") == 0)
        {
            return eHilightFile;
        }
        if(strcmp(input, "--tag-video-remove") == 0)
        {
            return eHilightRemove;
        }
    }
    return eUnknown;
}

int send_write_request(CURL *curl, const char *path, const char* curl_response, FILE *file)
{
    if(curl_response == NULL && file == NULL)
    {
        printf("\nBoth inputs to write data are NULL");
        return ERR_FAILURE;
    }

    CURLcode code = curl_easy_setopt(curl, CURLOPT_URL, path);
    if(code != CURLE_OK)
    {
        printf("\nFailed to perform curl operation - received error code:%d", code);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }

    // check if we should write the data to a const char* or FILE*
    if(file == NULL)
    {
        code = curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, json_response_callback);
        if(code != CURLE_OK)
        {
            printf("\nFailed to setup callback function - received error code:%d", code);
            curl_easy_cleanup(curl);
            return ERR_FAILURE;
        }

        code = curl_easy_setopt(curl, CURLOPT_WRITEDATA, curl_response);
        if (code != CURLE_OK) {
            printf("\nFailed to write json data");
            curl_easy_cleanup(curl);
            return ERR_FAILURE;
        }
    }
    else
    {
        code = curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, file_response_callback);
        if(code != CURLE_OK)
        {
            printf("\nFailed to setup callback function - received error code:%d", code);
            curl_easy_cleanup(curl);
            return ERR_FAILURE;
        }
        code = curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);
        if (code != CURLE_OK)
        {
            printf("\nFailed to write json data");
            curl_easy_cleanup(curl);
            return ERR_FAILURE;
        }
    }

    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 15L);

    if(perform_request(curl) == ERR_FAILURE)
    {
        printf("\nFailed to perform request:%s", path);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    return ERR_SUCCESS;
}

int download_media_file(CURL *curl, const char *media_file, const char *out_file)
{
    if(curl == NULL || media_file == NULL || out_file == NULL)
    {
        printf("\ncurl:%p, media_file:%s or out_file:%s is NULL", curl, media_file, out_file);
        return ERR_FAILURE;
    }

    FILE *file = fopen(out_file, "w");
    if(file == NULL)
    {
        printf("\nCouldn't open %s\n", out_file);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    string path = "http://10.5.5.9:8080/videos/DCIM/" + string(media_file);
    printf("\nDownloading %s to %s\n", media_file, out_file);
    if(send_write_request(curl, path.c_str(), NULL, file) != ERR_SUCCESS)
    {
        fclose(file);
        curl_easy_cleanup(curl);
        return ERR_FAILURE;
    }
    fclose(file);
    return ERR_SUCCESS;
}

void help()
{
    printf("\nUsage");
    printf("\n\t./media_commands <-l, --list_files>");
    printf("\n\t./media_commands <-f, --list_files_pretty>");
    printf("\n\t./media_commands <-i, --info> <camera_file_path>(i.e: 100GOPRO/GH010433.MP4");
    printf("\n\t./media_commands <-p, --info_pretty> <camera_file_path>(i.e: 100GOPRO/GH010433.MP4");
    printf("\n\t./media_commands <-g, --download> <camera_file_path> <output_path/output_file_name>");
    printf("\n\t./media_commands --tag-moment");
    printf("\n\t./media_commands --tag-video <video_file_path> <offset_ms>");
    printf("\n\t./media_commands --tag-photo <photo_file_path>");
    printf("\n\t./media_commands --tag-video-remove <video_file_path> <offset_ms>");
    printf("\n\t./media_commands --tag-photo-remove <photo_file_path>");
    printf("\n\t./media_commands <-d, --demo> <output_path>\n");
}

int download_first_file(CURL *curl, cJSON *fs_array, const char* directory, const char* output_path)
{
    cJSON *media_item = fs_array->child;
    if(cJSON_GetArraySize(fs_array) <= 0)
    {
        printf("\nNo media files found on camera");
        return ERR_SUCCESS;
    }

    // loop through the first media item
    while(media_item != NULL)
    {
        if((media_item->type == cJSON_String) && (strcmp(media_item->string, "n") == 0))
        {
            string dir(directory);
            string file(media_item->valuestring);
            string src_path = dir + "/" + file;
            string dst_path = string(output_path) + file;
            return download_media_file(curl, src_path.c_str(), dst_path.c_str());
        }
        media_item = media_item->next;
    }
    printf("\nFailed to parse media file in file system array");
    return ERR_FAILURE;
}

int main(int argc, char* argv[])
{
    if(argc < 2 || argc > 5)
    {
        help();
        return ERR_FAILURE;
    }

    MediaRequest request = check_user_request(argc, argv);
    if(request == eUnknown)
    {
        help();
        return ERR_FAILURE;
    }

    CURL *curl = curl_easy_init();
    int ret = ERR_SUCCESS;

    if(curl != NULL)
    {
        char curl_response[CURL_MAX_WRITE_SIZE];
        memset(&curl_response,'\0', CURL_MAX_WRITE_SIZE);
        switch(request)
        {
            case eListFiles:
            {
                const string& path = "http://10.5.5.9:8080/gopro/media/list";
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    ret =  ERR_FAILURE;
                    break;
                }
                printf("\n%s\n", curl_response);
                break;
            }
            case eListFilesPretty:
            {
                const string& path = "http://10.5.5.9:8080/gopro/media/list";
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                cJSON *json = cJSON_Parse(curl_response);
                const char *json_pretty = cJSON_Print(json);
                printf("\n%s\n", json_pretty);
                break;
            }
            case eMediaInfo:
            {
                string file(argv[2]);
                string path = "http://10.5.5.9:8080/gopro/media/info?path=" + file;
                printf("\n%s info:", file.c_str());
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                printf("\n%s\n", curl_response);
                break;
            }
            case eMediaInfoPretty:
            {
                string file(argv[2]);
                string path = "http://10.5.5.9:8080/gopro/media/info?path=" + file;
                printf("\n%s info:", file.c_str());
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                cJSON *json = cJSON_Parse(curl_response);
                if(json == NULL)
                {
                    printf("\nCouldn't parse json response");
                    ret = ERR_FAILURE;
                    break;
                }
                const char *json_pretty = cJSON_Print(json);
                printf("\n%s\n", json_pretty);
                break;
            }
            case eDownloadMedia:
            {
                string media_file(argv[2]);
                string out_file(argv[3]);
                ret = download_media_file(curl, media_file.c_str(), out_file.c_str());
                break;
            }
            case eHilightFile:
            {
                string file(argv[2]);
                // Get the offset for the tag. Value should be in ms.
                // Note: if file is a photo, no offset should be given
                string offset_ms = "";
                if(argc >= 4)
                    offset_ms = "&ms=" + string(argv[3]);
                const string& path = "http://10.5.5.9:8080/gopro/media/hilight/file?path=" + file + offset_ms;
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                printf("\n%s\n", curl_response);
                break;                break;
            }
            case eHilightRemove:
            {
                string file(argv[2]);
                // Get the offset for the tag. Value should be in ms
                // Note: if file is a photo, no offset should be given
                string offset_ms = "";
                if(argc >= 4)
                    offset_ms = "&ms=" + string(argv[3]);
                const string& path = "http://10.5.5.9:8080/gopro/media/hilight/remove?path=" + file + offset_ms;
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                printf("\n%s\n", curl_response);
                break;                break;
            }
            case eHilightMoment:
            {
                const string& path = "http://10.5.5.9:8080/gopro/media/hilight/moment";
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                printf("\n%s\n", curl_response);
                break;                break;
            }
            case eDemo:
            {
                /*
                 * Demo will gather media list and download first file
                 */
                const string& path = "http://10.5.5.9:8080/gopro/media/list";
                if(send_write_request(curl, path.c_str(), curl_response, NULL) != ERR_SUCCESS)
                {
                    return ERR_FAILURE;
                }
                cJSON *json = cJSON_Parse(curl_response);
                if(json == NULL)
                {
                    printf("\nCouldn't parse json response");
                    ret =  ERR_FAILURE;
                    break;
                }
                cJSON *media_list = NULL;
                char* directory = NULL;
                // Find file system array in media list json response
                for(media_list = json->child; media_list != NULL;)
                {
                    if((media_list->type == cJSON_String) && (strcmp(media_list->string, "d") == 0))
                    {
                        directory = media_list->valuestring;
                        media_list = media_list->next;
                        continue;
                    }
                    if((media_list->type == cJSON_Array) && (strcmp(media_list->string, "fs") == 0))
                    {
                        media_list = media_list->child;
                        break;
                    }
                    if((media_list->type == cJSON_Array) || (media_list->type == cJSON_Object))
                    {
                        media_list = media_list->child;
                        continue;
                    }
                    media_list = media_list->next;
                }

                cJSON *fs_array = media_list;
                if(fs_array == NULL)
                {
                    printf("\nfs_array is null");
                    ret =  ERR_FAILURE;
                    break;
                }
                ret = download_first_file(curl, fs_array, directory, argv[2]);
                break;
            }
            default:
            {
                printf("\nUnknown media request:%d\n", request);
                ret =  ERR_FAILURE;
                break;
            }
        }
    }
    curl_easy_cleanup(curl);
    return ret;
}
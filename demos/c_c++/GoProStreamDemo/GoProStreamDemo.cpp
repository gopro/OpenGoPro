/* GoProStreamDemo.cpp/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Sat Mar  5 01:05:52 UTC 2022 */

// GoProStreamDemo.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "GoProStreamDemo.h"
#include <thread>
#include "UDPSocketCapture.h"
#include <d2d1.h>
extern "C"
{
#include "libavcodec\avcodec.h"
}

#define BUF_SIZE_1080 3110400 // 1920 * 1080 + (1920 *1080)/2
#define BUF_SIZE_720  1382400 // 1280 * 720 + (1280 *720)/2

int BUF_SIZE = BUF_SIZE_1080;
int HEIGHT = 1080;
int WIDTH = 1920;

#ifndef max
#define max(a,b)            (((a) > (b)) ? (a) : (b))
#endif

#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif

int quitNow = 0;
HWND myWin = 0;
std::thread myThread;
std::thread capThread;

HBITMAP myBitmap;
COLORREF* imgBuf = (COLORREF*)calloc(2073600, sizeof(COLORREF));
void yuv2rgb(uint8_t yValue, uint8_t uValue, uint8_t vValue,
    uint8_t* r, uint8_t* g, uint8_t* b);

void CaptureFrames();

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE hInst;                                // current instance
WCHAR szTitle[MAX_LOADSTRING];                  // The title bar text
WCHAR szWindowClass[MAX_LOADSTRING];            // the main window class name

// Forward declarations of functions included in this code module:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

UDPSocketCapture capper;

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);


    // Initialize global strings
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_GOPROSTREAMDEMO, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // Perform application initialization:
    if (!InitInstance (hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_GOPROSTREAMDEMO));
#ifdef USE_PREVIEW_STREAM
    HEIGHT = 720;
    WIDTH = 1280;
    BUF_SIZE = BUF_SIZE_720;
#endif
    MSG msg;
    capper.Start();

    capThread = std::thread(CaptureFrames);
    capThread.detach();

    // Main message loop:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }
    capper.Stop();
    return (int) msg.wParam;
}

//
//  FUNCTION: MyRegisterClass()
//
//  PURPOSE: Registers the window class.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style          = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = WndProc;
    wcex.cbClsExtra     = 0;
    wcex.cbWndExtra     = 0;
    wcex.hInstance      = hInstance;
    wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_GOPROSTREAMDEMO));
    wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName   = MAKEINTRESOURCEW(IDC_GOPROSTREAMDEMO);
    wcex.lpszClassName  = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   FUNCTION: InitInstance(HINSTANCE, int)
//
//   PURPOSE: Saves instance handle and creates main window
//
//   COMMENTS:
//
//        In this function, we save the instance handle in a global variable and
//        create and display the main program window.
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // Store instance handle in our global variable

   HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, nullptr, nullptr, hInstance, nullptr);

   if (!hWnd)
   {
      return FALSE;
   }
   myWin = hWnd;
   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE: Processes messages for the main window.
//
//  WM_COMMAND  - process the application menu
//  WM_PAINT    - Paint the main window
//  WM_DESTROY  - post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_COMMAND:
        {
            int wmId = LOWORD(wParam);
            // Parse the menu selections:
            switch (wmId)
            {
            case IDM_ABOUT:
                DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
                break;
            case IDM_EXIT:
                DestroyWindow(hWnd);
                break;
            default:
                return DefWindowProc(hWnd, message, wParam, lParam);
            }
        }
        break;
    case WM_PAINT:
        {
            RECT rect;
            int width;
            int height;
            
            if (GetWindowRect(hWnd, &rect))
            {
                width = rect.right - rect.left;
                height = rect.bottom - rect.top;
            }
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            // TODO: Add any drawing code that uses hdc here...

            /////////////////
#ifdef SHOW_CAM_OUTPUT
            // Creating temp bitmap
            HBITMAP map = CreateBitmap(WIDTH, 
                HEIGHT, 
                1, 
                32, 
                (void*)imgBuf); 

            HDC src = CreateCompatibleDC(hdc); 
            SelectObject(src, map); 

            BitBlt(hdc, 
                10,  
                10,  
                WIDTH, 
                HEIGHT, 
                src, 
                0,   
                0,   
                SRCCOPY); 
            DeleteObject(map);
            DeleteDC(src);
#endif
            
            EndPaint(hWnd, &ps);
        }
        break;
    case WM_DESTROY:
        quitNow = 1;
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}

void CaptureFrames()
{
    uint8_t* buf = (uint8_t*)malloc(BUF_SIZE_1080);
    static int countstart = 0;
    long bytesReturned = 0;
    //std::this_thread::sleep_for(std::chrono::seconds(6));
    while (!quitNow)
    {
        capper.GetBuffer(buf, BUF_SIZE, bytesReturned);
        
        if (bytesReturned > 100)
        {
            //for 1080 frames
            //0-2073599 = Y
            //2073600 - 2591999 = U
            //2592000 - 3110399 = V
            uint8_t r, g, b;
            int uindex = HEIGHT*WIDTH, vindex = HEIGHT*WIDTH + ((HEIGHT*WIDTH)/4);
            int strider = 0;
#ifdef SHOW_CAM_OUTPUT
#ifndef SHOW_CAM_OUTPUT_ORIGINAL
            for (int i = 0; i < HEIGHT * WIDTH; i++)
            {
                int lineNumber = i / WIDTH;
                int place = i % WIDTH;
                int oddline = ((lineNumber) % 2);
                strider = ((place) / 2) + (((lineNumber / 2) + (lineNumber%2)) * (WIDTH/2));
                if (oddline)
                    strider -= (WIDTH/2);
                if (place == WIDTH-1)
                    strider += 0;
                yuv2rgb(buf[i], buf[uindex + strider], buf[vindex+strider], &r, &g, &b);
                imgBuf[i] = RGB(b, g, r);
                //imgBuf[i] = RGB(buf[i], buf[i], buf[i]);
            }
#endif
#endif
#ifdef SHOW_CAM_OUTPUT
#ifdef SHOW_CAM_OUTPUT_ORIGINAL
            //this is the Y channel
            for (int j = 0, i = 0; i < HEIGHT*WIDTH; j++, i++)
            {
                imgBuf[j] = RGB(buf[i], buf[i], buf[i]);
            }
            //uncomment this to see UV channels
            /*
            for (int j = 0, i = HEIGHT*WIDTH; i < BUF_SIZE; j++, i++)
            {
                imgBuf[j] = RGB(buf[i], buf[i], buf[i]);
            }
            */
#endif
#endif
        
#ifdef SHOW_CAM_OUTPUT
            InvalidateRect(myWin, NULL, false);
            UpdateWindow(myWin);
#endif

        }
        else
        {
            bytesReturned = 0;
        }
        
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    free(buf);
}

void yuv2rgb(uint8_t yValue, uint8_t uValue, uint8_t vValue,
                        uint8_t* r, uint8_t* g, uint8_t* b) 
{
    /*int rTmp = yValue + (1.403 * vValue);
    int gTmp = yValue - (0.344 * uValue) - (0.714 * vValue);
    int bTmp = yValue + (1.770 * uValue);*/
        
    /*int rTmp = yValue + (1.402 * (vValue - 128));
    int gTmp = yValue - (0.34414 * (uValue - 128)) - (0.71414 * (vValue - 128));
    int bTmp = yValue + (1.772 * (uValue - 128));*/

    int rTmp = yValue + (1.370705 * (vValue - 128));
    int gTmp = yValue - (0.698001 * (vValue - 128)) - (0.337633 * (uValue - 128));
    int bTmp = yValue + (1.732446 * (uValue - 128));

    *r = min(max(rTmp, 0), 255);
    *g = min(max(gTmp, 0), 255);
    *b = min(max(bTmp, 0), 255);
}



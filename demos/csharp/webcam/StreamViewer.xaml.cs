/* StreamViewer.xaml.cs/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Oct 20 21:41:18 UTC 2021 */

﻿using Microsoft.Win32;
using System;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Controls;

namespace GoProWebcamViewer
{
    enum Status
    {
        SUCCESS,
        FAILURE
    }

    /// <summary>
    /// Interaction logic for StreamViewer.xaml
    /// </summary>
    public partial class StreamViewer : Window, INotifyPropertyChanged
    {
        bool bQuit = false;
        bool zoomMan = false;

        private string playerEnabledText, webcamEnabledText, previewEnabledText;
        private bool playerEnabled
        {
            get { return playerEnabledText == "enabled" ? true : false; }
            set
            {
                playerEnabledText = value == true ? "enabled" : "disabled";
                UpdateStatusBar();
            }
        }
        private bool webcamEnabled
        {
            get { return webcamEnabledText == "enabled" ? true : false; }
            set
            {
                webcamEnabledText = value == true ? "enabled" : "disabled";
                UpdateStatusBar();
            }
        }
        private bool previewEnabled
        {
            get { return previewEnabledText == "enabled" ? true : false; }
            set
            {
                previewEnabledText = value == true ? "enabled" : "disabled";
                UpdateStatusBar();
            }
        }

        private string ipaddr = "unknown";

        public event PropertyChangedEventHandler PropertyChanged;

        public string IPAddr
        {
            get { return ipaddr; }
            set
            {
                ipaddr = value;
                OnPropertyChanged("IPAddr");
            }
        }

        public StreamViewer()
        {
            InitializeComponent();
            this.Top = Properties.Settings.Default.FTop;
            this.Left = Properties.Settings.Default.FLeft;
            this.Height = Properties.Settings.Default.FHeight;
            this.Width = Properties.Settings.Default.FWidth;

            if (this.Height == 0)
            {
                this.Height = 600;
                this.Width = 800;
            }
            ipaddr = Properties.Settings.Default.IPAddress;

            this.txtIPAddr.Text = ipaddr;
            DataContext = this;

            var vlcLibDirectory = new DirectoryInfo(System.IO.Path.Combine("./", "libvlc", IntPtr.Size == 4 ? "win-x86" : "win-x64"));

            var options = new string[]
            {
                // VLC options can be given here. Please refer to the VLC command line documentation.
            };

            mPlayer.SourceProvider.CreatePlayer(vlcLibDirectory, options);

            new Timer(IPAddrCheck, this, 50, 10000);

            playerEnabled = false;
            webcamEnabled = false;
            previewEnabled = false;
        }

        private void Log(string text)
        {
            Dispatcher.Invoke((Action)delegate ()
            { /* update UI */
                this.txtGeneral.Text += text;
            });
        }

        private void UpdateStatusBar()
        {
            Dispatcher.Invoke((Action)delegate ()
            { /* update UI */
                this.txtStatusBar.Text = $"Player: {playerEnabledText,-20}Webcam: {webcamEnabledText,-20}Preview: {previewEnabledText,-20}";
            });
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            bQuit = true;
            ThreadPool.QueueUserWorkItem(_ => mPlayer.SourceProvider.MediaPlayer.Stop());

            if (WindowState == WindowState.Maximized)
            {
                // Use the RestoreBounds as the current values will be 0, 0 and the size of the screen
                Properties.Settings.Default.FTop = RestoreBounds.Top;
                Properties.Settings.Default.FLeft = RestoreBounds.Left;
                Properties.Settings.Default.FHeight = RestoreBounds.Height;
                Properties.Settings.Default.FWidth = RestoreBounds.Width;
            }
            else
            {
                Properties.Settings.Default.FTop = this.Top;
                Properties.Settings.Default.FLeft = this.Left;
                Properties.Settings.Default.FHeight = this.Height;
                Properties.Settings.Default.FWidth = this.Width;
            }
            Properties.Settings.Default.IPAddress = ipaddr;
            Properties.Settings.Default.Save();
        }

        private Status SendHTTPRequest(string endpoint)
        {
            Status status = Status.FAILURE;
            if (ipaddr == "not found")
                return status;
            string responseString;
            string requestString = "http://" + ipaddr + ":8080/gopro/" + endpoint;
            HttpWebResponse resp;
            HttpWebRequest req = HttpWebRequest.CreateHttp(requestString);
            req.Method = "GET";
            req.KeepAlive = false;
            try
            {
                Log(requestString + " ==> \n");
                resp = (HttpWebResponse)req.GetResponse();
                responseString = new StreamReader(resp.GetResponseStream()).ReadToEnd();
                resp.Close();
                status = Status.SUCCESS;
            }
            catch (WebException ep)
            {
                responseString = "Failed url " + endpoint + ": " + ep.Message;
                HttpWebResponse respy = (HttpWebResponse)ep.Response;
                if (respy != null)
                {
                    responseString = new StreamReader(respy.GetResponseStream()).ReadToEnd();
                }
            }
            if (!bQuit)
            {
                Log(responseString);
            }

            return status;
        }

        private Status SetSetting(int id, int value)
        {
            return SendHTTPRequest("camera/setting?setting=" + id.ToString() + "&option=" + value.ToString());
        }

        private void btnStatusStream_Click(object sender, RoutedEventArgs e)
        {
            SendHTTPRequest("webcam/status");
        }

        private void btnClearText_Click(object sender, RoutedEventArgs e)
        {
            txtGeneral.Clear();
            txtStatusBar.Text = "";
        }

        private void HideStream()
        {
            ThreadPool.QueueUserWorkItem(_ => mPlayer.SourceProvider.MediaPlayer.Stop());
            playerEnabled = false;
        }

        private void sldZoom_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (!zoomMan)
            {
                SendHTTPRequest("camera/digital_zoom?percent=" + Convert.ToInt32(sldZoom.Value));
            }
        }

        private void Thumb_DragStarted(object sender, System.Windows.Controls.Primitives.DragStartedEventArgs e)
        {
            zoomMan = true;
        }

        private void Thumb_DragCompleted(object sender, System.Windows.Controls.Primitives.DragCompletedEventArgs e)
        {
            zoomMan = false;
            SendHTTPRequest("camera/digital_zoom?percent=" + Convert.ToInt32(sldZoom.Value));
        }

        private void btnFOV_Click(object sender, RoutedEventArgs e)
        {
            int value = Convert.ToInt32(((ComboBoxItem)cmbFOV.SelectedItem).Content.ToString());
            SetSetting(43, value);
        }

        private void txtIPAddr_TextChanged(object sender, TextChangedEventArgs e)
        {
            ipaddr = txtIPAddr.Text;
        }

        private void IPAddrCheck(object state)
        {
            String strHostName = Dns.GetHostName();
            bool found = false;
            // Find host by name
            IPHostEntry iphostentry = Dns.GetHostEntry(strHostName);

            // Enumerate IP addresses
            foreach (IPAddress ipaddress in iphostentry.AddressList)
            {
                if (ipaddress.AddressFamily == AddressFamily.InterNetwork)
                {
                    byte[] abytes = ipaddress.GetAddressBytes();
                    if (abytes[0] == 172 && abytes[1] >= 20 && abytes[1] <= 29 && abytes[3] >= 50 && abytes[3] <= 70)
                    {
                        ipaddr = ipaddress.ToString();
                        StringBuilder sb = new StringBuilder(ipaddress.ToString());
                        sb[ipaddress.ToString().Length - 1] = '1';
                        IPAddr = sb.ToString();
                        found = true;
                        break;
                    }
                }
            }
            if (!found)
                IPAddr = "not found";

        }
        protected void OnPropertyChanged(string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        private void btnPreview_Click(object sender, RoutedEventArgs e)
        {
            if (SendHTTPRequest("webcam/preview") == Status.SUCCESS)
            {
                btnFOV.IsEnabled = true;
                sldZoom.IsEnabled = true;
                previewEnabled = true;
                webcamEnabled = false;
            }
        }

        private void btnStart_Click(object sender, RoutedEventArgs e)
        {
            if (SendHTTPRequest("webcam/start") == Status.SUCCESS)
            {
                btnFOV.IsEnabled = false;
                sldZoom.IsEnabled = false;
                webcamEnabled = true;
                previewEnabled = false;
            }
        }

        private void btnStop_Click(object sender, RoutedEventArgs e)
        {
            if (SendHTTPRequest("webcam/stop") == Status.SUCCESS)
            {
                HideStream();
                btnFOV.IsEnabled = false;
                sldZoom.IsEnabled = false;
                webcamEnabled = false;
            }
        }

        private void btnExit_Click(object sender, RoutedEventArgs e)
        {
            if (SendHTTPRequest("webcam/exit") == Status.SUCCESS)
            {
                HideStream();
                btnFOV.IsEnabled = false;
                sldZoom.IsEnabled = false;
                webcamEnabled = false;
                previewEnabled = false;
            }
        }

        private void btnStartPlayer_Click(object sender, RoutedEventArgs e)
        {
            Log("Starting video player...\n");
            ThreadPool.QueueUserWorkItem(_ =>
            {
                mPlayer.SourceProvider.MediaPlayer.Play(new Uri("udp://@0.0.0.0:8554", UriKind.Absolute), new string[] { "--network-caching=10", "--no-audio" });
            });
            playerEnabled = true;
        }

        private void btnStopPlayer_Click(object sender, RoutedEventArgs e)
        {
            Log("Stopping video player...\n");
            HideStream();
        }

        private void btnMute_Click(object sender, RoutedEventArgs e)
        {
            Log("Toggling mute...\n");
            ThreadPool.QueueUserWorkItem(_ => mPlayer.SourceProvider.MediaPlayer.Audio.ToggleMute());
        }
    }
}

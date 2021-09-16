/* MainWindow.xaml.cs/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:05:38 PM */

﻿using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Devices.Enumeration;
using Windows.Media.MediaProperties;
using Windows.Storage.Streams;

namespace GoProCSharpSample
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {

        public class GDeviceInformation
        {
            public GDeviceInformation(DeviceInformation inDeviceInformation, bool inPresent, bool inConnected)
            {
                DeviceInfo = inDeviceInformation;
                IsPresent = inPresent;
                IsConnected = inConnected;
            } 
            public DeviceInformation DeviceInfo { get; set; } = null;
            public bool IsPresent { get; set; } = false;
            public bool IsConnected { get; set; } = false;
            public bool IsVisible { get { return IsPresent || IsConnected; } }

            private GDeviceInformation() { }
        }

        #region Binded Properties
        public ObservableCollection<GDeviceInformation> Devices
        {
            get; set;
        } = new ObservableCollection<GDeviceInformation>();

        private bool mEncoding = false;
        public bool Encoding
        {
            get
            {
                return mEncoding;
            }
            set
            {
                mEncoding = value;
                if (this.PropertyChanged != null)
                {
                    PropertyChanged(this, new PropertyChangedEventArgs("Encoding"));
                }
            }
        }

        private int mBatterylevel = 0;
        public int BatteryLevel
        {
            get
            {
                return mBatterylevel;
            }
            set
            {
                mBatterylevel = value;
                if (this.PropertyChanged != null)
                {
                    PropertyChanged(this, new PropertyChangedEventArgs("BatteryLevel"));
                }
            }
        }

        private bool mWifiOn = false;
        public bool WifiOn
        {
            get
            {
                return mWifiOn;
            }
            set
            {
                mWifiOn = value;
                if (this.PropertyChanged != null)
                {
                    PropertyChanged(this, new PropertyChangedEventArgs("WifiOn"));
                }
            }
        }

        #endregion

        #region Bluetooth Device Members
        private BluetoothLEDevice mBLED = null;
        public GattCharacteristic mNotifyCmds = null;
        public GattCharacteristic mSendCmds = null;
        public GattCharacteristic mSetSettings = null;
        public GattCharacteristic mNotifySettings = null;
        public GattCharacteristic mSendQueries = null;
        public GattCharacteristic mNotifyQueryResp = null;
        public GattCharacteristic mReadAPName = null;
        public GattCharacteristic mReadAPPass = null;
        #endregion

        public event PropertyChangedEventHandler PropertyChanged;

        DeviceWatcher mDeviceWatcher = null;
        private readonly Dictionary<string, DeviceInformation> mAllDevices = new Dictionary<string, DeviceInformation>();

        public MainWindow()
        {
            InitializeComponent();
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
        }

        #region Button Click Handlers

        private void BtnScanBLE_Click(object sender, RoutedEventArgs e)
        {
            string BLESelector = "System.Devices.Aep.ProtocolId:=\"{bb7bb05e-5972-42b5-94fc-76eaa7084d49}\"";
            DeviceInformationKind deviceInformationKind = DeviceInformationKind.AssociationEndpoint;
            string[] requiredProperties = { "System.Devices.Aep.Bluetooth.Le.IsConnectable", "System.Devices.Aep.IsConnected" };

            mDeviceWatcher = DeviceInformation.CreateWatcher(BLESelector, requiredProperties, deviceInformationKind);
            mDeviceWatcher.Added += MDeviceWatcher_Added; ;
            mDeviceWatcher.Updated += MDeviceWatcher_Updated; ;
            mDeviceWatcher.Removed += MDeviceWatcher_Removed; ;
            mDeviceWatcher.EnumerationCompleted += MDeviceWatcher_EnumerationCompleted; ;
            mDeviceWatcher.Stopped += MDeviceWatcher_Stopped; ;

            this.txtStatusBar.Text = "Scanning for devices...";
            mDeviceWatcher.Start();
        }
        private async void BtnPair_Click(object sender, RoutedEventArgs e)
        {
            GDeviceInformation lDevice = (GDeviceInformation)lbDevices.SelectedItem;
            if (lDevice != null)
            {
                StatusOutput("Pairing started");

                mBLED = await BluetoothLEDevice.FromIdAsync(lDevice.DeviceInfo.Id);
                mBLED.DeviceInformation.Pairing.Custom.PairingRequested += Custom_PairingRequested;
                if (mBLED.DeviceInformation.Pairing.CanPair)
                {
                    DevicePairingProtectionLevel dppl = mBLED.DeviceInformation.Pairing.ProtectionLevel;
                    DevicePairingResult dpr = await mBLED.DeviceInformation.Pairing.Custom.PairAsync(DevicePairingKinds.ConfirmOnly, dppl);

                    StatusOutput("Pairing result = " + dpr.Status.ToString());
                }
                else
                {
                    StatusOutput("Pairing failed");
                }
            }
            else
            {
                StatusOutput("Select a device");
            }
        }
        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            StatusOutput("Connecting...");
            GDeviceInformation mDI = (GDeviceInformation)lbDevices.SelectedItem;
            if (mDI == null)
            {
                StatusOutput("No device selected");
                return;
            }
            mBLED = await BluetoothLEDevice.FromIdAsync(mDI.DeviceInfo.Id);
            if(!mBLED.DeviceInformation.Pairing.IsPaired)
            {
                StatusOutput("Device not paired");
                return;
            }
            GattDeviceServicesResult result = await mBLED.GetGattServicesAsync();
            mBLED.ConnectionStatusChanged += MBLED_ConnectionStatusChanged;

            if (result.Status == GattCommunicationStatus.Success)
            {
                IReadOnlyList<GattDeviceService> services = result.Services;
                foreach (GattDeviceService gatt in services)
                {
                    GattCharacteristicsResult res = await gatt.GetCharacteristicsAsync();
                    if (res.Status == GattCommunicationStatus.Success)
                    {
                        IReadOnlyList<GattCharacteristic> characteristics = res.Characteristics;
                        foreach (GattCharacteristic characteristic in characteristics)
                        {
                            GattCharacteristicProperties properties = characteristic.CharacteristicProperties;
                            if (properties.HasFlag(GattCharacteristicProperties.Read))
                            {
                                // This characteristic supports reading from it.
                            }
                            if (properties.HasFlag(GattCharacteristicProperties.Write))
                            {
                                // This characteristic supports writing to it.
                            }
                            if (properties.HasFlag(GattCharacteristicProperties.Notify))
                            {
                                // This characteristic supports subscribing to notifications.
                            }
                            if (characteristic.Uuid.ToString() == "b5f90002-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mReadAPName = characteristic;
                            }
                            if (characteristic.Uuid.ToString() == "b5f90003-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mReadAPPass = characteristic;
                            }
                            if (characteristic.Uuid.ToString() == "b5f90072-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mSendCmds = characteristic;
                            }
                            if (characteristic.Uuid.ToString() == "b5f90073-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mNotifyCmds = characteristic;
                                GattCommunicationStatus status = await mNotifyCmds.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
                                if (status == GattCommunicationStatus.Success)
                                {
                                    mNotifyCmds.ValueChanged += MNotifyCmds_ValueChanged;
                                }
                                else
                                {
                                    //failure
                                    StatusOutput("Failed to attach notify cmd " + status);
                                }
                            }
                            if (characteristic.Uuid.ToString() == "b5f90074-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mSetSettings = characteristic;
                            }
                            if (characteristic.Uuid.ToString() == "b5f90075-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mNotifySettings = characteristic;
                                GattCommunicationStatus status = await mNotifySettings.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
                                if (status == GattCommunicationStatus.Success)
                                {
                                    mNotifySettings.ValueChanged += MNotifySettings_ValueChanged;
                                }
                                else
                                {
                                    //failure
                                    StatusOutput("Failed to attach notify settings " + status);
                                }
                            }
                            if (characteristic.Uuid.ToString() == "b5f90076-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mSendQueries = characteristic;
                            }
                            if (characteristic.Uuid.ToString() == "b5f90077-aa8d-11e3-9046-0002a5d5c51b")
                            {
                                mNotifyQueryResp = characteristic;
                                GattCommunicationStatus status = await mNotifyQueryResp.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
                                if (status == GattCommunicationStatus.Success)
                                {
                                    mNotifyQueryResp.ValueChanged += MNotifyQueryResp_ValueChanged;
                                    if (mSendQueries != null)
                                    {
                                        //Register for settings and status updates
                                        DataWriter mm = new DataWriter();
                                        mm.WriteBytes(new byte[] { 1, 0x52 });
                                        GattCommunicationStatus gat = await mSendQueries.WriteValueAsync(mm.DetachBuffer());
                                        mm = new DataWriter();
                                        mm.WriteBytes(new byte[] { 1, 0x53 });
                                        gat = await mSendQueries.WriteValueAsync(mm.DetachBuffer());
                                    }
                                    else
                                    {
                                        StatusOutput("send queries was null!");
                                    }
                                }
                                else
                                {
                                    //failure
                                    StatusOutput("Failed to attach notify query " + status);
                                }
                            }
                        }
                    }
                }
                SetThirdPartySource();
            }
            else if (result.Status == GattCommunicationStatus.Unreachable)
            {
                //couldn't find camera
                StatusOutput("Connection failed");
            }
        }
        private async void BtnReadAPName_Click(object sender, RoutedEventArgs e)
        {
            if (mReadAPName != null)
            {
                GattReadResult res = await mReadAPName.ReadValueAsync();
                if (res.Status == GattCommunicationStatus.Success)
                {
                    DataReader dataReader = Windows.Storage.Streams.DataReader.FromBuffer(res.Value);
                    string output = dataReader.ReadString(res.Value.Length);
                    txtAPName.Text = output;
                }
                else
                {
                    StatusOutput("Failed to read ap name");
                }
            }
            else
            {
                StatusOutput("Not connected");
            }
        }
        private async void BtnReadAPPass_Click(object sender, RoutedEventArgs e)
        {
            if (mReadAPPass != null)
            {
                GattReadResult res = await mReadAPPass.ReadValueAsync();
                if (res.Status == GattCommunicationStatus.Success)
                {
                    DataReader dataReader = Windows.Storage.Streams.DataReader.FromBuffer(res.Value);
                    string output = dataReader.ReadString(res.Value.Length);
                    txtAPPassword.Text = output;
                }
                else
                {
                    StatusOutput("Failed to read password");
                }
            }
            else
            {
                StatusOutput("Not connected");
            }
        }
        private void BtnTurnWifiOn_Click(object sender, RoutedEventArgs e)
        {
            TogglefWifiAP(1);
        }
        private void BtnTurnWifiOff_Click(object sender, RoutedEventArgs e)
        {
            TogglefWifiAP(0);
        }
        private void BtnShutterOn_Click(object sender, RoutedEventArgs e)
        {
            ToggleShutter(1);
        }
        private void BtnShutterOff_Click(object sender, RoutedEventArgs e)
        {
            ToggleShutter(0);
        }

        #endregion

        #region Device Watcher Event Handlers
        private void MDeviceWatcher_Stopped(DeviceWatcher sender, object args)
        {
            Application.Current.Dispatcher.BeginInvoke(new Action(() =>
            {
                this.txtStatusBar.Text = "Scan Stopped!";
            }));
        }

        private void MDeviceWatcher_EnumerationCompleted(DeviceWatcher sender, object args)
        {
            Application.Current.Dispatcher.BeginInvoke(new Action(() =>
            {
                this.txtStatusBar.Text = "Scan Complete";
            }));
        }

        private void MDeviceWatcher_Removed(DeviceWatcher sender, DeviceInformationUpdate args)
        {
            for (int i = 0; i < Devices.Count; i++)
            {
                if (Devices[i].DeviceInfo.Id == args.Id)
                {
                    Application.Current.Dispatcher.BeginInvoke(new Action(() =>
                    {
                        Devices.RemoveAt(i);
                    }));
                    break;
                }
            }
        }

        private void MDeviceWatcher_Updated(DeviceWatcher sender, DeviceInformationUpdate args)
        {
            bool isPresent = false, isConnected = false, found = false;

            if (args.Properties.ContainsKey("System.Devices.Aep.Bluetooth.Le.IsConnectable"))
            {
                isPresent = (bool)args.Properties["System.Devices.Aep.Bluetooth.Le.IsConnectable"];
            }
            if (args.Properties.ContainsKey("System.Devices.Aep.IsConnected"))
            {
                isConnected = (bool)args.Properties["System.Devices.Aep.IsConnected"];
            }

            for (int i = 0; i < Devices.Count; i++)
            {
                if (Devices[i].DeviceInfo.Id == args.Id)
                {
                    found = true;
                    Application.Current.Dispatcher.BeginInvoke(new Action(() =>
                    {
                        Devices[i].DeviceInfo.Update(args);
                        Devices[i].IsPresent = isPresent;
                        Devices[i].IsConnected = isConnected;
                    }));
                    break;
                }
            }
            if(!found && (isPresent || isConnected))
            {
                if (mAllDevices.ContainsKey(args.Id))
                {
                    mAllDevices[args.Id].Update(args);
                    Application.Current.Dispatcher.BeginInvoke(new Action(() =>
                    {
                        Devices.Add(new GDeviceInformation(mAllDevices[args.Id], isPresent, isConnected));
                    }));
                }
            }
        }

        private void MDeviceWatcher_Added(DeviceWatcher sender, DeviceInformation args)
        {
            bool isPresent = false;
            bool isConnected = false;

            if (args.Properties.ContainsKey("System.Devices.Aep.Bluetooth.Le.IsConnectable"))
            {
                isPresent = (bool)args.Properties["System.Devices.Aep.Bluetooth.Le.IsConnectable"];
            }
            if (args.Properties.ContainsKey("System.Devices.Aep.IsConnected"))
            {
                isConnected = (bool)args.Properties["System.Devices.Aep.IsConnected"];
            }

            if (args.Name != "" && args.Name.Contains("GoPro"))
            {
                bool found = false;
                if (!mAllDevices.ContainsKey(args.Id))
                {
                    mAllDevices.Add(args.Id, args);
                }
                for (int i = 0; i < Devices.Count; i++)
                {
                    if (Devices[i].DeviceInfo.Id == args.Id)
                    {
                        found = true;
                        Application.Current.Dispatcher.BeginInvoke(new Action(() =>
                        {
                            Devices[i].DeviceInfo = args;
                            Devices[i].IsPresent = isPresent;
                            Devices[i].IsConnected = isConnected;
                        }));
                        break;
                    }
                }
                if (!found && (isPresent || isConnected))
                {
                    Application.Current.Dispatcher.BeginInvoke(new Action(() =>
                    {
                        Devices.Add(new GDeviceInformation(args, isPresent, isConnected));
                    }));
                }
            }
        }

        #endregion

        #region BLE Device Handlers

        private void MBLED_ConnectionStatusChanged(BluetoothLEDevice sender, object args)
        {
            if (sender.ConnectionStatus == BluetoothConnectionStatus.Connected)
                StatusOutput("CONNECTED");
            else
                StatusOutput("DISCONNECTED");
        }
        private void Custom_PairingRequested(DeviceInformationCustomPairing sender, DevicePairingRequestedEventArgs args)
        {
            StatusOutput("Pairing request...");
            args.Accept();
        }

        #endregion

        #region Gatt Characteristic Notification Handlers

        private readonly List<byte> mBufQ = new List<byte>();
        private int mExpectedLengthQ = 0;
        private void MNotifyQueryResp_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            var reader = DataReader.FromBuffer(args.CharacteristicValue);
            byte[] myBytes = new byte[reader.UnconsumedBufferLength];
            reader.ReadBytes(myBytes);
            int newLength = ReadBytesIntoBuffer(myBytes, mBufQ);
            if (newLength > 0)
                mExpectedLengthQ = newLength;

            if (mExpectedLengthQ == mBufQ.Count)
            {
                if ((mBufQ[0] == 0x53 || mBufQ[0] == 0x93) && mBufQ[1] == 0)
                {
                    //status messages
                    for (int k = 0; k < mBufQ.Count;)
                    {
                        if (mBufQ[k] == 10)
                        {
                            Encoding = mBufQ[k + 2] > 0;
                        }
                        if (mBufQ[k] == 70)
                        {
                            BatteryLevel = mBufQ[k + 2];
                        }
                        if(mBufQ[k] == 69)
                        {
                            WifiOn = mBufQ[k + 2] == 1;
                        }
                        k += 2 + mBufQ[k + 1];
                    }
                }
                else
                {
                    //Unhandled Query Message
                }
                mBufQ.Clear();
                mExpectedLengthQ = 0;
            }
        }

        private readonly List<byte> mBufSet = new List<byte>();
        private int mExpectedLengthSet = 0;
        private void MNotifySettings_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            var reader = DataReader.FromBuffer(args.CharacteristicValue);
            byte[] myBytes = new byte[reader.UnconsumedBufferLength];
            reader.ReadBytes(myBytes);
            int newLength = ReadBytesIntoBuffer(myBytes, mBufSet);
            if (newLength > 0)
                mExpectedLengthSet = newLength;

            if (mExpectedLengthSet == mBufSet.Count)
            {
                /*
                if (mBufSet[0] == 0xXX)
                {

                }
                */
                mBufSet.Clear();
            }
        }

        private readonly List<byte> mBufCmd = new List<byte>();
        private int mExpectedLengthCmd = 0;
        private void MNotifyCmds_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            var reader = DataReader.FromBuffer(args.CharacteristicValue);
            byte[] myBytes = new byte[reader.UnconsumedBufferLength];
            reader.ReadBytes(myBytes);
            int newLength = ReadBytesIntoBuffer(myBytes, mBufCmd);
            if (newLength > 0)
                mExpectedLengthCmd = newLength;

            if (mExpectedLengthCmd == mBufCmd.Count)
            {
                /*
                if (mBufCmd[0] == 0xXX)
                {

                }
                */
                mBufCmd.Clear();
            }
        }

        #endregion

        #region Private Helper Functions

        private async void SetThirdPartySource()
        {
            DataWriter mm = new DataWriter();
            mm.WriteBytes(new byte[] { 0x01, 0x50 });
            GattCommunicationStatus res = GattCommunicationStatus.Unreachable;

            if (mSendCmds != null)
            {
                res = await mSendCmds.WriteValueAsync(mm.DetachBuffer());
            }
            if (res != GattCommunicationStatus.Success && mSendCmds != null)
            {
                StatusOutput("Failed to set command source: " + res.ToString());
            }
        }

        private void StatusOutput(string status)
        {
            Application.Current.Dispatcher.BeginInvoke(new Action(() =>
            {
                this.txtStatusBar.Text = status;
            }));
        }
        private int ReadBytesIntoBuffer(byte[] bytes, List<byte> mBuf)
        {
            int returnLength = -1;
            int startbyte = 1;
            int theseBytes = bytes.Length;
            if ((bytes[0] & 32) > 0)
            {
                //extended 13 bit header
                startbyte = 2;
                int len = ((bytes[0] & 0xF) << 8) | bytes[1];
                returnLength = len;
            }
            else if ((bytes[0] & 64) > 0)
            {
                //extended 16 bit header
                startbyte = 3;
                int len = (bytes[1] << 8) | bytes[2];
                returnLength = len;
            }
            else if ((bytes[0] & 128) > 0)
            {
                //its a continuation packet
            }
            else
            {
                //8 bit header
                returnLength = bytes[0];
            }
            for (int k = startbyte; k < theseBytes; k++)
                mBuf.Add(bytes[k]);

            return returnLength;
        }
        private async void TogglefWifiAP(int onOff)
        {
            DataWriter mm = new DataWriter();
            mm.WriteBytes(new byte[] { 0x03, 0x17, 0x01, (byte)onOff });
            GattCommunicationStatus res = GattCommunicationStatus.Unreachable;

            if (onOff != 1 && onOff != 0)
            {
                res = GattCommunicationStatus.AccessDenied;
            }
            else if (mSendCmds != null)
            {
                res = await mSendCmds.WriteValueAsync(mm.DetachBuffer());
            }
            if (res != GattCommunicationStatus.Success)
            {
                StatusOutput("Failed to turn on wifi: " + res.ToString());
            }
        }
        private async void ToggleShutter(int onOff)
        {
            DataWriter mm = new DataWriter();
            mm.WriteBytes(new byte[] { 3, 1, 1, (byte)onOff });
            GattCommunicationStatus res = GattCommunicationStatus.Unreachable;

            if (onOff != 1 && onOff != 0)
            {
                res = GattCommunicationStatus.AccessDenied;
            }
            else if (mSendCmds != null)
            {
                res = await mSendCmds.WriteValueAsync(mm.DetachBuffer());
            }
            if (res != GattCommunicationStatus.Success)
            {
                StatusOutput("Failed to send shutter: " + res.ToString());
            }
        }

        #endregion

    }

    public class BrushBoolColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (!(bool)value)
            {
                return new SolidColorBrush(Color.FromRgb(100, 100, 100));
            }
            return new SolidColorBrush(Color.FromRgb(255, 100, 100));
        }
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}

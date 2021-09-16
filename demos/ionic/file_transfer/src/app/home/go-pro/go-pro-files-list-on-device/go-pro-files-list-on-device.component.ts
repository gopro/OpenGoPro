/* go-pro-files-list-on-device.component.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoadingController, ToastController } from '@ionic/angular';
import { GoProService } from '../go-pro.service';
export interface GoProFileOnDevice {
  fileName: string;
  filePath: string;
  fileType: 'image' | 'video';
  fileSize: number;
}
@Component({
  selector: 'app-go-pro-files-list-on-device',
  templateUrl: './go-pro-files-list-on-device.component.html',
  styleUrls: ['./go-pro-files-list-on-device.component.scss'],
})
export class GoProFilesListOnDeviceComponent implements OnInit {
  filesOnDevice: GoProFileOnDevice[] = [];

  constructor(
    public goProService: GoProService,
    public router: Router,
    public loadingController: LoadingController,
    public toastController: ToastController
  ) {}

  async ngOnInit() {
    this.filesOnDevice = await this.goProService.loadFilesFromStorage();
    await this.goProService.loadDocuments();
  }

  previewFileFromDevice(goProFileOnDevice: GoProFileOnDevice) {
    this.router.navigate(['/home/go-pro/file-detail-on-device'], {
      state: { goProFileOnDevice },
    });
  }

  async deleteFileFromDevice(goProFileOnDevice: GoProFileOnDevice) {
    const loading = await this.loadingController.create({
      message: `Deleting file ${goProFileOnDevice.fileName}`,
    });

    try {
      await loading.present();

      await this.goProService.deleteFileFromDevice(goProFileOnDevice);

      this.filesOnDevice = await this.goProService.loadFilesFromStorage();

      await loading.dismiss();
      this.presentToast(`${goProFileOnDevice.fileName} deleted ✅`);
    } catch (error) {
      await loading.dismiss();
      console.log(error);
      this.presentToast(JSON.stringify(error, null, 2));
    }
  }

  async presentToast(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 1700,
    });
    toast.present();
  }
}

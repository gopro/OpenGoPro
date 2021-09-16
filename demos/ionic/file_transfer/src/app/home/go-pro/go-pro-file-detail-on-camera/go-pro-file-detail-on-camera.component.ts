/* go-pro-file-detail-on-camera.component.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { Route } from '@angular/compiler/src/core';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Http } from '@capacitor-community/http';
import { Directory, Filesystem } from '@capacitor/filesystem';
import { LoadingController, ToastController } from '@ionic/angular';
import { GoProFileOnCamera } from '../go-pro-files-list-on-camera/go-pro-files-list-on-camera.component';
import { GoProFileOnDevice } from '../go-pro-files-list-on-device/go-pro-files-list-on-device.component';
import { Storage } from '@capacitor/storage';
import { GoProService } from '../go-pro.service';
@Component({
  selector: 'app-go-pro-file-detail-on-camera',
  templateUrl: './go-pro-file-detail-on-camera.component.html',
  styleUrls: ['./go-pro-file-detail-on-camera.component.scss'],
})
export class GoProFileDetailOnCameraComponent implements OnInit {
  goProFileOnCamera: GoProFileOnCamera;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public loadingController: LoadingController,
    public toastController: ToastController,
    public goProService: GoProService
  ) {
    this.route.queryParams.subscribe((params) => {
      const state = this.router.getCurrentNavigation().extras.state;
      if (state) {
        this.goProFileOnCamera = state.goProFileOnCamera;
      }
    });
  }

  ngOnInit() {}

  async downloadFileFromGoProCamera() {
    const loading = await this.loadingController.create({
      message: 'Please wait... Download in progress',
    });

    try {
      await loading.present();

      const filePath = this.goProFileOnCamera.fileName;
      const fileDirectory = this.goProService.goProFilesDirectory;

      await Http.downloadFile({
        url: this.goProFileOnCamera.fileUrl,
        filePath: filePath,
        fileDirectory: fileDirectory,
      });

      const savedFile = await Filesystem.getUri({
        path: filePath,
        directory: fileDirectory,
      });

      const newFileOnDevice: GoProFileOnDevice = {
        fileName: this.goProFileOnCamera.fileName,
        fileSize: this.goProFileOnCamera.fileSize,
        fileType: this.goProFileOnCamera.fileType,
        filePath: savedFile.uri,
      };

      this.goProService.addFileToStorage(newFileOnDevice);

      await loading.dismiss();

      this.presentToast(`${this.goProFileOnCamera.fileName} downloaded ✅`);
    } catch (error) {
      await loading.dismiss();
      console.log(error);
      this.presentToast(JSON.stringify(error, null, 2));
    }

    // TODO: download this.goProFileOnCamera()
  }

  async presentToast(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 1700,
    });
    toast.present();
  }
}

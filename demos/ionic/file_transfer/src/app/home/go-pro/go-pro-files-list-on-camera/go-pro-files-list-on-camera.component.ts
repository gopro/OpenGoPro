/* go-pro-files-list-on-camera.component.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Http } from '@capacitor-community/http';
import { ToastController } from '@ionic/angular';

export interface GoProFileOnCamera {
  fileName: string;
  fileUrl: string;
  fileType: 'image' | 'video';
  fileSize: number;
}

@Component({
  selector: 'app-go-pro-files-list-on-camera',
  templateUrl: './go-pro-files-list-on-camera.component.html',
  styleUrls: ['./go-pro-files-list-on-camera.component.scss'],
})
export class GoProFilesListOnCameraComponent implements OnInit {
  readonly goproBaseUrl = 'http://10.5.5.9:8080';

  filesOnGoPro: GoProFileOnCamera[] = [];

  constructor(public toastController: ToastController, public router: Router) {}

  ngOnInit() {
    this.fetchFilesFromGoProCamera();
  }

  async fetchFilesFromGoProCamera() {
    const mediaListUrl = `${this.goproBaseUrl}/gopro/media/list`;
    const mediaListItemUrl = `${this.goproBaseUrl}/videos/DCIM/100GOPRO`;

    try {
      const response = await Http.get({ url: mediaListUrl });

      const files = response.data.media[0].fs as any[];

      // const fileNames: string[] = files.map((e) => e.n);

      this.filesOnGoPro = files.map<GoProFileOnCamera>((file) => ({
        fileName: file.n,
        fileUrl: `${mediaListItemUrl}/${file.n}`,
        fileType: file.n.includes('.MP4') ? 'video' : 'image',
        fileSize: Math.round(parseInt(file.s) / 1048576),
      }));

      this.presentToast('Successfully fetched go pro media');
    } catch (error) {
      console.error(error);
      this.presentToast('Failed to fetch go pro media');
    }
  }

  previewFileFromGoProCamera(goProFileOnCamera: GoProFileOnCamera) {
    this.router.navigate(['/home/go-pro/file-detail-on-camera'], {
      state: { goProFileOnCamera },
    });
  }

  async presentToast(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 1700,
    });
    toast.present();
  }
}

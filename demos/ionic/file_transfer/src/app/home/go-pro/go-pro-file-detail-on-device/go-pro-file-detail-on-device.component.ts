/* go-pro-file-detail-on-device.component.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { Capacitor } from '@capacitor/core';
import { Directory, Filesystem } from '@capacitor/filesystem';
import { isPlatform } from '@ionic/core';
import { GoProFileOnDevice } from '../go-pro-files-list-on-device/go-pro-files-list-on-device.component';
import { GoProService } from '../go-pro.service';

@Component({
  selector: 'app-go-pro-file-detail-on-device',
  templateUrl: './go-pro-file-detail-on-device.component.html',
  styleUrls: ['./go-pro-file-detail-on-device.component.scss'],
})
export class GoProFileDetailOnDeviceComponent implements OnInit {
  goProFileOnDevice: GoProFileOnDevice;
  fileSrc: string | SafeUrl;

  customFileUri?: string;
  customFileBlob?: string;
  customFileUriSrc?: string;
  customFileUriTrusted?: any;
  customFileUriSrcTrusted?: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public goProService: GoProService,
    private sanitizer: DomSanitizer
  ) {
    this.route.queryParams.subscribe((params) => {
      const state = this.router.getCurrentNavigation().extras.state;
      if (state) {
        this.goProFileOnDevice = state.goProFileOnDevice;
      }
    });
  }

  async ngOnInit() {
    this.initFileSrc();
  }

  async initFileSrc() {
    // Capacitor and Cordova apps are hosted on a local HTTP server
    // and are served with the http:// protocol. Some plugins, however,
    // attempt to access device files via the file:// protocol.
    // To avoid difficulties between http:// and file://,
    // paths to device files must be rewritten to use the local HTTP server.
    // For example, file:///path/to/device/file must be rewritten as
    // http://<host>:<port>/<prefix>/path/to/device/file before being rendered in the app.
    // you can read more at https://ionicframework.com/docs/core-concepts/webview#file-protocol

    // perfect code will be something like
    // *.component.ts ----> this.fileSrc = Capacitor.convertFileSrc(this.goProFileOnDevice.filePath)
    // *.component.html --> <img [src]="fileSrc"/> or <video [src]="fileSrc"
    // but it only works on android for ios we need to do extra things

    const fileUri = await this.getFileUri();
    const fileSrc = await this.getFileSrc(fileUri);
    this.fileSrc = fileSrc;
  }

  private async getFileUri(): Promise<string> {
    // I do this because on ios after ionic restart
    // it can not find file that I downloaded before 😳
    // but for android it's working fine so we need extra check for ios only
    if (isPlatform('ios')) {
      const getUriResult = await Filesystem.getUri({
        path: this.goProFileOnDevice.fileName,
        directory: this.goProService.goProFilesDirectory,
      });
      return getUriResult.uri;
    }

    return this.goProFileOnDevice.filePath;
  }

  private getFileSrc(fileUri: string): string | SafeUrl {
    // I do this because on for videos on ios it says unsafe url 😳
    // but for android it's working fine so we need extra check for ios only

    if (isPlatform('ios')) {
      const fileSrcForImage = Capacitor.convertFileSrc(fileUri);
      // you can read more about sanitizer here https://angular.io/guide/security#trusting-safe-values
      const fileSrcForVideo = this.sanitizer.bypassSecurityTrustUrl(
        Capacitor.convertFileSrc(fileUri)
      );

      return this.goProFileOnDevice.fileType == 'video'
        ? fileSrcForVideo
        : fileSrcForImage;
    }

    return Capacitor.convertFileSrc(fileUri);
  }
}

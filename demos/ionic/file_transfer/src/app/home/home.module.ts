/* home.module.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { HomePage } from './home.page';

import { HomePageRoutingModule } from './home-routing.module';
import { GoProFileDetailOnCameraComponent } from './go-pro/go-pro-file-detail-on-camera/go-pro-file-detail-on-camera.component';
import { GoProFilesListOnCameraComponent } from './go-pro/go-pro-files-list-on-camera/go-pro-files-list-on-camera.component';
import { GoProFilesListOnDeviceComponent } from './go-pro/go-pro-files-list-on-device/go-pro-files-list-on-device.component';
import { GoProService } from './go-pro/go-pro.service';
import { GoProFileDetailOnDeviceComponent } from './go-pro/go-pro-file-detail-on-device/go-pro-file-detail-on-device.component';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, HomePageRoutingModule],
  providers: [GoProService],
  declarations: [
    HomePage,
    GoProFilesListOnCameraComponent,
    GoProFilesListOnDeviceComponent,
    GoProFileDetailOnCameraComponent,
    GoProFileDetailOnDeviceComponent,
  ],
})
export class HomePageModule {}

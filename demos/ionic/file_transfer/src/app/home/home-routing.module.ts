/* home-routing.module.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GoProFileDetailOnCameraComponent } from './go-pro/go-pro-file-detail-on-camera/go-pro-file-detail-on-camera.component';
import { GoProFileDetailOnDeviceComponent } from './go-pro/go-pro-file-detail-on-device/go-pro-file-detail-on-device.component';
import { GoProFilesListOnCameraComponent } from './go-pro/go-pro-files-list-on-camera/go-pro-files-list-on-camera.component';
import { GoProFilesListOnDeviceComponent } from './go-pro/go-pro-files-list-on-device/go-pro-files-list-on-device.component';
import { HomePage } from './home.page';

const routes: Routes = [
  {
    path: '',
    component: HomePage,
  },
  {
    path: 'go-pro/files-on-camera',
    component: GoProFilesListOnCameraComponent,
  },
  {
    path: 'go-pro/file-detail-on-camera',
    component: GoProFileDetailOnCameraComponent,
  },
  {
    path: 'go-pro/files-on-device',
    component: GoProFilesListOnDeviceComponent,
  },
  {
    path: 'go-pro/file-detail-on-device',
    component: GoProFileDetailOnDeviceComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HomePageRoutingModule {}

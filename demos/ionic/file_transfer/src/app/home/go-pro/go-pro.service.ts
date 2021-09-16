/* go-pro.service.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { Injectable } from '@angular/core';
import { Directory, Filesystem } from '@capacitor/filesystem';
import { Storage } from '@capacitor/storage';
import { isPlatform } from '@ionic/core';
import { GoProFileOnDevice } from './go-pro-files-list-on-device/go-pro-files-list-on-device.component';

@Injectable({
  providedIn: 'root',
})
export class GoProService {
  private GO_PRO_FILES_ON_DEVICE_STORAGE_KEY =
    'GO_PRO_FILES_ON_DEVICE_STORAGE_KEY';

  readonly goProFilesDirectory = Directory.Data;

  constructor() {}

  async loadFilesFromStorage() {
    const result = await Storage.get({
      key: this.GO_PRO_FILES_ON_DEVICE_STORAGE_KEY,
    });
    const filesOnDevice: GoProFileOnDevice[] = JSON.parse(result.value) || [];
    console.log('filesOnDeviceStorage', filesOnDevice);
    return filesOnDevice;
  }

  private async saveFilesToStorage(files: GoProFileOnDevice[]) {
    await Storage.set({
      key: this.GO_PRO_FILES_ON_DEVICE_STORAGE_KEY,
      value: JSON.stringify(files),
    });
  }

  async addFileToStorage(fileToAdd: GoProFileOnDevice) {
    const filesOnDevice = await this.loadFilesFromStorage();
    filesOnDevice.unshift(fileToAdd);
    await this.saveFilesToStorage(filesOnDevice);
  }

  private async deleteFileFromStorage(fileToDelete: GoProFileOnDevice) {
    const filesOnDevice = await this.loadFilesFromStorage();
    const updatedFilesOnDevice = filesOnDevice.filter(
      (f) => f.filePath !== fileToDelete.filePath
    );
    this.saveFilesToStorage(updatedFilesOnDevice);
  }

  async deleteFileFromDevice(goProFileOnDevice: GoProFileOnDevice) {
    await Filesystem.deleteFile({
      path: goProFileOnDevice.fileName,
      directory: this.goProFilesDirectory,
    });

    await this.deleteFileFromStorage(goProFileOnDevice);
  }

  async loadDocuments() {
    console.log(`loadDocuments`);

    const folderContent = await Filesystem.readdir({
      directory: this.goProFilesDirectory,
      path: '',
    });
    console.log('folderContent', folderContent);

    const files = await Promise.all(
      folderContent.files.map(async (file) => {
        const stat = await Filesystem.stat({
          directory: this.goProFilesDirectory,
          path: file,
        });

        // stat.type can be 'directory', 'file' etc

        return {
          name: file,
          isFile: stat.type === 'file',
        };
      })
    );
    console.log('files', files);
  }
}

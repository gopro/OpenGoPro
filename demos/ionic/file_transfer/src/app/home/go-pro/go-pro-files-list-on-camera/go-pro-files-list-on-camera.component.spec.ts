/* go-pro-files-list-on-camera.component.spec.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { GoProFilesListOnCameraComponent } from './go-pro-files-list-on-camera.component';

describe('GoProFilesListOnCameraComponent', () => {
  let component: GoProFilesListOnCameraComponent;
  let fixture: ComponentFixture<GoProFilesListOnCameraComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ GoProFilesListOnCameraComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(GoProFilesListOnCameraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

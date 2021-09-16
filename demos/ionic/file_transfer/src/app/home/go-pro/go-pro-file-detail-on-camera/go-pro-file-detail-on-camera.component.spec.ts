/* go-pro-file-detail-on-camera.component.spec.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { GoProFileDetailOnCameraComponent } from './go-pro-file-detail-on-camera.component';

describe('GoProFileDetailOnCameraComponent', () => {
  let component: GoProFileDetailOnCameraComponent;
  let fixture: ComponentFixture<GoProFileDetailOnCameraComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ GoProFileDetailOnCameraComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(GoProFileDetailOnCameraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

/* go-pro-file-detail-on-device.component.spec.ts/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  8, 2021 11:42:11 AM */

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { GoProFileDetailOnDeviceComponent } from './go-pro-file-detail-on-device.component';

describe('GoProFileDetailOnDeviceComponent', () => {
  let component: GoProFileDetailOnDeviceComponent;
  let fixture: ComponentFixture<GoProFileDetailOnDeviceComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ GoProFileDetailOnDeviceComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(GoProFileDetailOnDeviceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

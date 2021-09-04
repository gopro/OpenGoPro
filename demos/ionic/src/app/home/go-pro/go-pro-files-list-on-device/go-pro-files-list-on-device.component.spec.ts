import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { GoProFilesListOnDeviceComponent } from './go-pro-files-list-on-device.component';

describe('GoProFilesListOnDeviceComponent', () => {
  let component: GoProFilesListOnDeviceComponent;
  let fixture: ComponentFixture<GoProFilesListOnDeviceComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ GoProFilesListOnDeviceComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(GoProFilesListOnDeviceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

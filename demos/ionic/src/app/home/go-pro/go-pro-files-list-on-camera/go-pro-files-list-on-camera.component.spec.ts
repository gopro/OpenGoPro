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

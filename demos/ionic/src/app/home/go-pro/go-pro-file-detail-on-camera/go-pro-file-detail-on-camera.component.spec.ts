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

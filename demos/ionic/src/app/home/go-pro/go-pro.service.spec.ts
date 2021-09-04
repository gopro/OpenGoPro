import { TestBed } from '@angular/core/testing';

import { GoProService } from './go-pro.service';

describe('GoProService', () => {
  let service: GoProService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GoProService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

/* go-pro.service.spec.ts/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  8, 2021 11:42:13 AM */

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

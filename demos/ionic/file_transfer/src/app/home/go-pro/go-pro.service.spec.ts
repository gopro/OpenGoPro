/* go-pro.service.spec.ts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep  8 21:37:27 UTC 2021 */

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

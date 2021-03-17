import { TestBed } from '@angular/core/testing';

import { KgmlFilesService } from './kgml-files.service';

describe('KgmlFilesService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: KgmlFilesService = TestBed.get(KgmlFilesService);
    expect(service).toBeTruthy();
  });
});

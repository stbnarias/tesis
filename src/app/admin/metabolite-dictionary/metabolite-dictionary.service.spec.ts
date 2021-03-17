import { TestBed } from '@angular/core/testing';

import { MetaboliteDictionaryService } from './metabolite-dictionary.service';

describe('MetaboliteDictionaryService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MetaboliteDictionaryService = TestBed.get(MetaboliteDictionaryService);
    expect(service).toBeTruthy();
  });
});

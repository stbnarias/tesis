import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MetaboliteDictionaryComponent } from './metabolite-dictionary.component';

describe('MetaboliteDictionaryComponent', () => {
  let component: MetaboliteDictionaryComponent;
  let fixture: ComponentFixture<MetaboliteDictionaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MetaboliteDictionaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MetaboliteDictionaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlgorithmSelectorComponent } from './algorithm-selector.component';

describe('AlgorithmSelectorComponent', () => {
  let component: AlgorithmSelectorComponent;
  let fixture: ComponentFixture<AlgorithmSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlgorithmSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlgorithmSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

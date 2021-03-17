import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlgorithmExecutionResultComponent } from './algorithm-execution-result.component';

describe('AlgorithmExecutionResultComponent', () => {
  let component: AlgorithmExecutionResultComponent;
  let fixture: ComponentFixture<AlgorithmExecutionResultComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlgorithmExecutionResultComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlgorithmExecutionResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

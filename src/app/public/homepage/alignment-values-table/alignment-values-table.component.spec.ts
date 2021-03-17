import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlignmentValuesTableComponent } from './alignment-values-table.component';

describe('AlignmentValuesTableComponent', () => {
  let component: AlignmentValuesTableComponent;
  let fixture: ComponentFixture<AlignmentValuesTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlignmentValuesTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlignmentValuesTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

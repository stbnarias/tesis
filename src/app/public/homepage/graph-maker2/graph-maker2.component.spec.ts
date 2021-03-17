import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphMaker2Component } from './graph-maker2.component';

describe('GraphMaker2Component', () => {
  let component: GraphMaker2Component;
  let fixture: ComponentFixture<GraphMaker2Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GraphMaker2Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GraphMaker2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

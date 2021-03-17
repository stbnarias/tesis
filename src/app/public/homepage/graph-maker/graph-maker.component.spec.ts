import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphMakerComponent } from './graph-maker.component';

describe('GraphMakerComponent', () => {
  let component: GraphMakerComponent;
  let fixture: ComponentFixture<GraphMakerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GraphMakerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GraphMakerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

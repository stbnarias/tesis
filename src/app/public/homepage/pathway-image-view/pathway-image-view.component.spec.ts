import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PathwayImageViewComponent } from './pathway-image-view.component';

describe('PathwayImageViewComponent', () => {
  let component: PathwayImageViewComponent;
  let fixture: ComponentFixture<PathwayImageViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PathwayImageViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PathwayImageViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

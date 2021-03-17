import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KgmlFilesListComponent } from './kgml-files-list.component';

describe('KgmlFilesListComponent', () => {
  let component: KgmlFilesListComponent;
  let fixture: ComponentFixture<KgmlFilesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KgmlFilesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KgmlFilesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

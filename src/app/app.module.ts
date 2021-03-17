import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomepageComponent } from './public/homepage/homepage.component';
import { LandingpageComponent } from './public/landingpage/landingpage.component';
import { AdminbaseComponent } from './admin/adminbase/adminbase.component';
import { KgmlDataTableComponent } from './admin/kgml-data-table/kgml-data-table.component';
import { KgmlFilesListComponent } from './admin/kgml-files-list/kgml-files-list.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from "@angular/forms";
import { AlgorithmSelectorComponent } from './public/homepage/algorithm-selector/algorithm-selector.component';
import { AlignmentValuesTableComponent } from './public/homepage/alignment-values-table/alignment-values-table.component';
import {
  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatIconModule,
  MatButtonModule,
  MatFormFieldModule,
  MatInputModule
} from '@angular/material';
import { HomepageService } from './public/homepage/homepage.service';
import { PathwayImageViewComponent } from './public/homepage/pathway-image-view/pathway-image-view.component';
import { AlgorithmExecutionResultComponent } from './public/homepage/algorithm-execution-result/algorithm-execution-result.component';
import { MetaboliteDictionaryComponent } from './admin/metabolite-dictionary/metabolite-dictionary.component';
import { GraphMakerComponent } from './public/homepage/graph-maker/graph-maker.component';
import { GraphMaker2Component } from './public/homepage/graph-maker2/graph-maker2.component';


@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    LandingpageComponent,
    AdminbaseComponent,
    KgmlDataTableComponent,
    KgmlFilesListComponent,
    AlgorithmSelectorComponent,
    PathwayImageViewComponent,
    AlignmentValuesTableComponent,
    AlgorithmExecutionResultComponent,
    MetaboliteDictionaryComponent,
    GraphMakerComponent,
    GraphMaker2Component
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatIconModule,
    MatButtonModule,
    MatSortModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ],
  providers: [HomepageService],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomepageComponent } from './public/homepage/homepage.component';
import { LandingpageComponent } from './public/landingpage/landingpage.component';
import { AdminbaseComponent } from './admin/adminbase/adminbase.component';
import { KgmlDataTableComponent } from './admin/kgml-data-table/kgml-data-table.component';
import { KgmlFilesListComponent} from './admin/kgml-files-list/kgml-files-list.component';

const routes: Routes = [
  {path: '', component: LandingpageComponent},
  {path: 'homepage', component: HomepageComponent},
  {path: 'adminbase', component: AdminbaseComponent},
  {path: 'login', component: LandingpageComponent},
  {path: 'signup', component: LandingpageComponent},
  {path: 'admin', component: KgmlDataTableComponent},
  {path: 'admin2', component: KgmlFilesListComponent},
  {path: '**', pathMatch: 'full', redirectTo: ''}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

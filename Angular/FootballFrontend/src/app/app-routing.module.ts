import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';



const routes: Routes = [
  {
    path: '',
    redirectTo: 'index',
    pathMatch: 'full'    
  },
  { 
    path: 'viewtournament', 
    component: AppComponent, 
  },
  // { 
  //   path: '',
  //   component: DashboardComponent,
  //   canActivate: [AuthGuard]    
  // } 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { TournamentsService } from './app.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { FormBuilder } from '@angular/forms';
// var $ = require( 'jquery' );
// require( 'datatables.net' )( window, $ );
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  tour = []
  register = false; 
  tourdetails = true;
  formenable=false;
  status = false;
  induvi = false;
  title = 'FootballFrontend';
  message = '';
  id= '';
  matchstatusvalues =[];
  @ViewChild(DataTableDirective, {static: false})
  
  dtElement: DataTableDirective;

  dtOptions: DataTables.Settings = {};
  checkoutForm;
  dtTrigger: Subject<any> = new Subject();
  constructor(private _tourService:TournamentsService,
    private _route:Router,
    private formBuilder: FormBuilder,
      
    ) {
      this.checkoutForm = this.formBuilder.group({
        TournamentName: '',
        TeamName: '',
        CoachName: '',
        ManagerName: '',
      });
    }
    induvaltour = []
    someClickHandler(info: any): void {
      this.message = info.TournamentName
      this.id = info.Tourid
      this.tourdetails = false
      this.induvi = true
      
      this._tourService.getTournament(info.Tourid).subscribe(
        res => {
          console.log(res)
          
          this.induvaltour=res.message
          if(res.registerstatus == true){
            this.register = true

          }
          

        },
        err => console.log(err)
      )
      console.log(this.message = info.Tourid + ' - ' + info.Tourid);
    }

    ngOnInit() {
      
      this._tourService.getTour().subscribe(
        res => {
          console.log(res)
          this.tour=res.message
          this.rerender()

        },
        err => console.log(err)
      )
      this.loadData()
    }

    public loadData() {
      const that = this;
      this.dtOptions = {
        order: [[0, 'desc']],
        responsive: true,
        paging: true,
        pageLength: 15,
        search: true,
        searching:true,
        pagingType: "full_numbers",
      data: this.tour,
      // scrollCollapse:true,
        columns: [{
          title: 'Tourid',
          data: 'Tourid'
        }, {
          title: 'TournamentName',
          data: 'TournamentName'
        }, {
          title: 'RegStartDate',
          data: 'RegStartDate'
        },
        {
          title: 'RegEndDate',
          data: 'RegEndDate'
        },
        {
          title: 'TournamentStartDate',
          data: 'TournamentStartDate'
        },
        {
          title: 'TournamentEndDate',
          data: 'TournamentEndDate'
        },
        {
          title: 'AllowedTeams',
          data: 'AllowedTeams'
        },
        {
          title: 'Venue',
          data: 'Venue'
        }
      ],
      rowCallback: (row: Node, data: any[] | Object, index: number) => {
        const self = this;
        // Unbind first in order to avoid any duplicate handler
        // (see https://github.com/l-lin/angular-datatables/issues/87)
        $('td', row).unbind('click');
        $('td', row).bind('click', () => {
          self.someClickHandler(data);
        });
        return row;
      }
    
      };
    }
    
  
    ngAfterViewInit(): void {
      this.dtTrigger.next();
    }
  
    ngOnDestroy(): void {
      // Do not forget to unsubscribe the event
      this.dtTrigger.unsubscribe();
    }
  
    rerender(): void {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        // dtInstance.destroy();
        dtInstance.clear()
        dtInstance.rows.add(this.tour).draw();
        // this.dtTrigger.next();
        // var ctrlobj = {};
        // for (let i = 0; i <= this.controllarr.length; i++) {
        //   // console.log(this.controllarr[i])
        //   // let vdata;
        //   // vdata= this.controllarr[i]
  
        //   var data;
        //   data = this.controllarr[i];
        //   ctrlobj[data] = ['', Validators.];
        // }
        // this.tableform = this.fb.group(ctrlobj);
        // this.tracesModalObj.close('table loaded');
        // Call the dtTrigger to rerender again
  
      });
    }
    rerender2(): void {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        // dtInstance.destroy();
        dtInstance.clear()
        dtInstance.rows.add(this.tour).draw();
        // this.dtTrigger.next();
        // var ctrlobj = {};
        // for (let i = 0; i <= this.controllarr.length; i++) {
        //   // console.log(this.controllarr[i])
        //   // let vdata;
        //   // vdata= this.controllarr[i]
  
        //   var data;
        //   data = this.controllarr[i];
        //   ctrlobj[data] = ['', Validators.];
        // }
        // this.tableform = this.fb.group(ctrlobj);
        // this.tracesModalObj.close('table loaded');
        // Call the dtTrigger to rerender again
  
      });
    }
    RegisterForm(){
      this.formenable = true
      this.induvi =false
    }
    induvailclose(){
      this.induvi =false
      this.tourdetails = true
      this.loadData()
      this. rerender()
    }

    onSubmit(checkoutForm){
      
      debugger
      this._tourService.register(checkoutForm).subscribe(
        res => {
          console.log(res)
          
          this.induvaltour=res.message
          if(res.status == 'pass'){
            
            this.formenable = false
            this.tourdetails =true
            this.loadData()
            this. rerender()
            alert("Successfully Registered")
          }
          

        },
        err => console.log(err)
      )
    }
    
    matchstatus(){
      this.status = true
      this.tourdetails =false
      this._tourService.getstatus().subscribe(
        res => {
          console.log(res)
          
          this.matchstatusvalues=res.data

        },
        err => console.log(err)
      )
    }
    tourdetailsshow(){
      this.status = false
      this.tourdetails =true
      this.loadData()
      this. rerender()
    }

    }
  